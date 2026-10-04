import base64
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import generate


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.prompt = self.root / 'one.md'
        self.prompt.write_text('# Notes\nIgnore this\n## Prompt\nDraw a tool.')
        self.output = self.root / 'output'
        self.config = {'model': 'test/model'}
        self.response = {'data': [{'b64_json': base64.b64encode(b'\x89PNG\r\n\x1a\nfixture').decode()}], 'usage': {'cost': 0.1}}

    def run_job(self, **kwargs):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-only'}):
            generate.run_jobs(self.config, [self.prompt], [], self.output, **kwargs)

    def test_env_key_loading_without_shell_execution(self):
        env = self.root / '.env'
        env.write_text("export OPENROUTER_API_KEY='literal-$(not-executed)' # comment\n")
        with patch.dict(os.environ, {}, clear=True):
            generate.load_env(env)
            self.assertEqual(os.environ['OPENROUTER_API_KEY'], 'literal-$(not-executed)')
            env.write_text('OPENROUTER_API_KEY=replacement')
            generate.load_env(env)
            self.assertEqual(os.environ['OPENROUTER_API_KEY'], 'literal-$(not-executed)')

    def test_dry_run_never_calls_api_or_creates_output(self):
        with patch.object(generate, 'request_image') as call:
            self.run_job()
        call.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_completed_request_is_skipped_and_tampering_blocks(self):
        with patch.object(generate, 'request_image', return_value=self.response) as call:
            self.run_job(execute=True)
            self.run_job(execute=True)
            self.assertEqual(call.call_count, 1)
            self.assertEqual(call.call_args.args[0]['prompt'], 'Draw a tool.')
            next(self.output.glob('*/image.png')).write_bytes(b'changed')
            with self.assertRaises(ValueError):
                self.run_job(execute=True)
            self.assertEqual(call.call_count, 1)

    def test_uncertain_failure_blocks_resubmission(self):
        with patch.object(generate, 'request_image', side_effect=TimeoutError) as call:
            with self.assertRaises(RuntimeError):
                self.run_job(execute=True)
            with self.assertRaises(ValueError):
                self.run_job(execute=True)
            self.assertEqual(call.call_count, 1)
        state = json.loads(next(self.output.glob('*/status.json')).read_text())
        self.assertEqual(state['status'], 'unresolved')

    def test_request_limit_and_resume(self):
        other = self.root / 'two.txt'
        other.write_text('Another tool')
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-only'}), patch.object(generate, 'request_image', return_value=self.response) as call:
            for _ in range(2):
                generate.run_jobs(self.config, [self.prompt, other], [], self.output, True, 1)
            self.assertEqual(call.call_count, 2)

    def test_reference_bytes_affect_identity(self):
        ref = self.root / 'reference.png'
        ref.write_bytes(b'first')
        first = generate.payload_for(self.config, self.prompt, [ref])
        ref.write_bytes(b'second')
        second = generate.payload_for(self.config, self.prompt, [ref])
        self.assertNotEqual(first, second)

    def test_metadata_and_override_precedence(self):
        self.prompt.write_text('---\nmodel: test/prompt\naspect_ratio: "3:2"\nquality: high\nseed: 42\n---\n## Prompt\nDraw a tool.')
        config = {'model': 'test/default', 'parameters': {'quality': 'low', 'aspect_ratio': '1:1'}}
        payload = generate.payload_for(config, self.prompt, [], {'quality': 'medium'})
        self.assertEqual(payload['quality'], 'medium')
        self.assertEqual(payload['aspect_ratio'], '3:2')
        self.assertEqual(payload['model'], 'test/prompt')
        self.assertEqual(payload['seed'], 42)
        self.assertEqual(payload['prompt'], 'Draw a tool.')

    def test_invalid_metadata_blocks_entire_batch(self):
        other = self.root / 'bad.md'
        other.write_text('---\nqualty: high\n---\nA tool')
        with patch.object(generate, 'request_image') as call:
            with self.assertRaises(ValueError):
                generate.run_jobs(self.config, [self.prompt, other], [], self.output, True)
            call.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_metadata_validation(self):
        for header in ['quality: high\nquality: low', 'seed: nope', 'quality: [high]', 'output_compression: 101']:
            with self.subTest(header=header):
                self.prompt.write_text('---\n' + header + '\n---\nDraw')
                with self.assertRaises(ValueError):
                    generate.payload_for(self.config, self.prompt, [])

    def test_clear_inherited_dimension_setting(self):
        config = {'model': 'test/model', 'parameters': {'aspect_ratio': '3:2'}}
        self.prompt.write_text('---\nsize: "1024x1024"\naspect_ratio: null\n---\nDraw')
        payload = generate.payload_for(config, self.prompt, [])
        self.assertNotIn('aspect_ratio', payload)
        self.assertEqual(payload['size'], '1024x1024')

    def test_setting_changes_create_new_request_identity(self):
        with patch.object(generate, 'request_image', return_value=self.response) as call:
            self.run_job(execute=True, overrides={'quality': 'low'})
            self.run_job(execute=True, overrides={'quality': 'high'})
            self.run_job(execute=True, overrides={'quality': 'high'})
            self.assertEqual(call.call_count, 2)

    def test_existing_lock_prevents_request(self):
        self.output.mkdir()
        (self.output / '.generation.lock').write_text('other process')
        with patch.object(generate, 'request_image') as call:
            with self.assertRaises(FileExistsError):
                self.run_job(execute=True)
            call.assert_not_called()


if __name__ == '__main__':
    unittest.main()
