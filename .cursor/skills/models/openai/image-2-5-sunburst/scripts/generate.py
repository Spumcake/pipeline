#!/usr/bin/env python3
"""Sequential OpenRouter Image API client. Standard library only; dry-run by default."""
import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
from pathlib import Path
import sys
import urllib.request
import urllib.error

API = 'https://openrouter.ai/api/v1/images'
PARAMETERS = {'size', 'resolution', 'aspect_ratio', 'quality', 'output_format', 'background', 'output_compression', 'seed'}


def load_env(path):
    """Read only the API key; never execute shell code or override an existing key."""
    if os.environ.get('OPENROUTER_API_KEY'):
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith('export '):
            line = line[7:].strip()
        name, separator, value = line.partition('=')
        if separator and name.strip() == 'OPENROUTER_API_KEY':
            value = value.strip()
            if value[:1] in {'"', "'"}:
                quote = value[0]
                end = value.find(quote, 1)
                if end < 0 or (value[end+1:].strip() and not value[end+1:].strip().startswith('#')):
                    raise ValueError('Invalid quoted API key in env file')
                value = value[1:end]
            else:
                value = value.split(' #', 1)[0].strip()
            if not value:
                raise ValueError('Empty API key in env file')
            os.environ['OPENROUTER_API_KEY'] = value
            return
    raise ValueError('Env file must define OPENROUTER_API_KEY')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)


def validate_settings(settings):
    if not isinstance(settings, dict) or set(settings) - (PARAMETERS | {'model'}):
        raise ValueError('Unknown generation setting')
    if 'quality' in settings and settings['quality'] != 'high':
        raise ValueError('Image quality must be high; lowering or unsetting quality is not allowed')
    for key, value in settings.items():
        if value is None and key != 'model':
            continue  # Explicit null removes an inherited setting.
        if key in {'seed', 'output_compression'}:
            if type(value) is not int:
                raise ValueError(f'{key} must be an integer')
            if key == 'output_compression' and not 0 <= value <= 100:
                raise ValueError('output_compression must be between 0 and 100')
        elif not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} must be a non-empty string')


def read_prompt(path):
    text = path.read_text(encoding='utf-8-sig').strip()
    settings = {}
    lines = text.splitlines()
    if lines and lines[0] == '---':
        try:
            end = lines.index('---', 1)
        except ValueError:
            raise ValueError(f'Unclosed prompt metadata: {path}') from None
        for line in lines[1:end]:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, separator, raw = line.partition(':')
            key, raw = key.strip(), raw.strip()
            if not separator or key in settings:
                raise ValueError(f'Invalid or duplicate metadata key: {key}')
            # Deliberately limited flat YAML subset; no nested structures or execution.
            if raw.startswith('"'):
                try:
                    value = json.loads(raw)
                except ValueError:
                    raise ValueError(f'Invalid quoted metadata value: {key}') from None
            elif raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
                value = raw[1:-1].replace("''", "'")
            elif raw in {'null', '~'}:
                value = None
            elif re.fullmatch(r'-?\d+', raw):
                value = int(raw)
            elif re.fullmatch(r'[A-Za-z0-9_./:-]+', raw):
                value = raw
            else:
                raise ValueError(f'Unsupported metadata value: {key}')
            settings[key] = value
        text = '\n'.join(lines[end+1:]).strip()
    validate_settings(settings)
    lines = text.splitlines()
    if '## Prompt' in lines:
        text = '\n'.join(lines[lines.index('## Prompt')+1:]).strip()
    if not text:
        raise ValueError(f'Empty prompt: {path}')
    return text, settings


def payload_for(config, path, references, overrides=None):
    parameters = config.get('parameters', {})
    if not isinstance(parameters, dict) or set(parameters) - PARAMETERS:
        raise ValueError('Unsupported configuration parameter')
    settings = dict(parameters, model=config.get('model'))
    validate_settings(settings)
    text, metadata = read_prompt(path)
    validate_settings(overrides or {})
    settings.update(metadata)
    settings.update(overrides or {})
    settings = {key: value for key, value in settings.items() if value is not None}
    model = settings.get('model')
    if not model or 'PLACEHOLDER' in model:
        raise ValueError('Set a verified OpenRouter image model ID')
    if 'size' in settings and ({'aspect_ratio', 'resolution'} & settings.keys()):
        raise ValueError('Use size alone, or aspect_ratio/resolution; clear inherited settings with null or --unset')
    settings['quality'] = 'high'  # Mandatory, including when callers omit it.
    payload = dict(settings, prompt=text, n=1)
    if references:
        payload['input_references'] = []
        for ref in references:
            mime = mimetypes.guess_type(ref.name)[0]
            if mime not in {'image/png', 'image/jpeg', 'image/webp'}:
                raise ValueError('References must be PNG, JPEG, or WebP')
            encoded = base64.b64encode(ref.read_bytes()).decode()
            payload['input_references'].append({'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{encoded}'}})
    return payload


def request_image(payload, key, timeout):
    request = urllib.request.Request(API, data=json.dumps(payload).encode(), headers={
        'Authorization': f'Bearer {key}', 'Content-Type': 'application/json',
    })
    # Never automatically retry a paid request.
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def decode_image(response):
    items = response.get('data', [])
    if len(items) != 1:
        raise ValueError('Expected one output image')
    data = base64.b64decode(items[0]['b64_json'], validate=True)
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return data, '.png'
    if data.startswith(b'\xff\xd8\xff'):
        return data, '.jpg'
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return data, '.webp'
    raise ValueError('Unsupported or unrecognized image bytes; response retained')


def view_name(path, name=None):
    """Use the prompt's purpose as its stable folder name, never the request hash."""
    value = name if name is not None else re.sub(r'^\d+[-_ ]*', '', path.stem)
    value = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')[:64].rstrip('-')
    if not value:
        raise ValueError('Use a descriptive prompt filename or --name')
    return value


def find_request(output, identity):
    # Read legacy hash folders and named versions without losing resume protection.
    for state_path in sorted(set(output.glob('*/status.json')) | set(output.glob('*/v*/status.json'))):
        state = json.loads(state_path.read_text())
        if state.get('identity') == identity:
            return state_path.parent
    legacy = output / identity
    if legacy.exists():
        raise ValueError(f'Legacy request has no matching status: {legacy}; reconcile it first')
    return None


def next_version(output, name):
    folder = output / name
    if folder.exists():
        for state_path in folder.glob('v*/status.json'):
            state = json.loads(state_path.read_text())
            if state.get('status') != 'complete':
                raise ValueError(f'Unresolved prior request in {state_path.parent}; reconcile before a new version')
    numbers = [int(p.name[1:]) for p in folder.glob('v*') if re.fullmatch(r'v\d+', p.name)]
    return folder / f'v{max(numbers, default=0) + 1:03d}'


def run_jobs(config, paths, refs, output, execute=False, limit=1, overrides=None, name=None):
    if limit < 1:
        raise ValueError('Request limit must be positive')
    if name is not None and len(paths) != 1:
        raise ValueError('--name requires a single prompt file')
    jobs = []
    for path in paths:
        payload = payload_for(config, path, refs, overrides)
        identity = digest(json.dumps(payload, sort_keys=True).encode())
        jobs.append((path, payload, identity))
    if not execute:
        for path, payload, identity in jobs:
            settings = {k: v for k, v in payload.items() if k not in {'prompt', 'input_references'}}
            destination = find_request(output, identity) or next_version(output, view_name(path, name))
            print(f'Plan: {path.name} -> {destination} {json.dumps(settings, sort_keys=True)}')
        print(f'Dry run: no API calls. At most {limit} new requests per execution; no dollar cap enforced.')
        return
    key = os.environ.get('OPENROUTER_API_KEY')
    if not key:
        raise ValueError('Set OPENROUTER_API_KEY in the environment')
    output.mkdir(parents=True, exist_ok=True)
    # Exclusive creation guards concurrent writers. After a crash, reconcile before removing.
    lock = output / '.generation.lock'
    with lock.open('x') as handle:
        handle.write(str(os.getpid()))
    try:
        count = 0
        for path, payload, identity in jobs:
            cached = find_request(output, identity)
            job = cached or next_version(output, view_name(path, name))
            state_path = job / 'status.json'
            if state_path.exists():
                state = json.loads(state_path.read_text())
                if state['status'] == 'complete':
                    image = job / state['image']
                    if not image.exists() or digest(image.read_bytes()) != state['sha256']:
                        raise ValueError('Completed output missing or modified; restore it rather than resubmit')
                    print(f'Skip completed: {path.name}')
                    continue
                raise ValueError(f'Unresolved prior request in {job}; reconcile before any resubmission')
            if count >= limit:
                print('Request limit reached; remaining prompts deferred.')
                break
            job.mkdir(parents=True, exist_ok=False)
            (job / 'prompt.md').write_bytes(path.read_bytes())
            save_json(job / 'request.json', payload)
            save_json(job / 'sources.json', {'prompt': str(path.resolve()), 'references': [str(r.resolve()) for r in refs]})
            state = {'status': 'in_flight', 'identity': identity, 'view': view_name(path, name), 'version': job.name}
            save_json(state_path, state)
            count += 1
            try:
                response = request_image(payload, key, config.get('timeout_seconds', 300))
                save_json(job / 'response.json', response)
                data, extension = decode_image(response)
                image = job / ('image' + extension)
                image.write_bytes(data)
                state.update(status='complete', image=image.name, sha256=digest(data), usage=response.get('usage'), response_id=response.get('id'))
                save_json(state_path, state)
                print(f'Saved: {image}')
            except Exception as error:
                # Avoid logging response bodies, prompts, or credentials in errors.
                state.update(status='unresolved', error_type=type(error).__name__)
                if isinstance(error, urllib.error.HTTPError):
                    state['http_status'] = error.code
                save_json(state_path, state)
                detail = f'HTTP {error.code}' if isinstance(error, urllib.error.HTTPError) else type(error).__name__
                raise RuntimeError(f'Request unresolved ({detail}); inspect {job}. No retry sent.') from None
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file', type=Path, help='Explicit .env file; reads only OPENROUTER_API_KEY')
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--prompts', type=Path, required=True, help='One file or a folder of .md/.txt files')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--name', help='Readable view name for a single prompt; defaults to its filename without a leading number')
    parser.add_argument('--reference', type=Path, action='append', default=[])
    parser.add_argument('--max-requests', type=int, default=1)
    parser.add_argument('--execute', action='store_true', help='Send paid requests; default is offline dry run')
    for setting in sorted(PARAMETERS | {'model'}):
        parser.add_argument('--' + setting.replace('_', '-'), type=int if setting in {'seed', 'output_compression'} else str)
    parser.add_argument('--unset', choices=sorted(PARAMETERS), action='append', default=[], help='Omit an inherited setting; use underscore names')
    args = parser.parse_args()
    overrides = {k: getattr(args, k) for k in PARAMETERS | {'model'} if getattr(args, k) is not None}
    if set(args.unset) & overrides.keys():
        parser.error('Cannot both set and unset the same setting')
    overrides.update({k: None for k in args.unset})
    if args.execute and args.env_file:
        load_env(args.env_file)
    paths = sorted(p for p in args.prompts.iterdir() if p.suffix in {'.md', '.txt'}) if args.prompts.is_dir() else [args.prompts]
    if not paths:
        parser.error('No prompt files found')
    run_jobs(json.loads(args.config.read_text()), paths, args.reference, args.output, args.execute, args.max_requests, overrides, args.name)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'{type(error).__name__}: {error}', file=sys.stderr)
        sys.exit(1)
