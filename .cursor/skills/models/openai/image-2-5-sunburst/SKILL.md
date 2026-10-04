---
name: openrouter-image-2-5-sunburst
description: Generate images sequentially from reviewed prompt files through OpenRouter, with optional reference images and resumable local records. Use when the user requests OpenRouter image generation or a batch of image prompts; not for creating application UI code.
---

# OpenRouter GPT Image 2.5 Sunburst

Always generate at `quality: high`. Never lower quality to medium, low, or a provider default, including for previews or retries. The script enforces this before sending a request. If the selected model cannot support high quality, report the incompatibility rather than downgrade.

Read [usage and recovery instructions](README.md) before execution. The bundled script requires Python 3.10+ and no third-party packages. This is a portable skill: explicitly load this file or install it using the chosen agent runner's supported mechanism; its location alone does not activate it.

1. Identify the named view, selected prompt files, output directory, model, reference images, and authorized request count. Use short purpose-based prompt filenames; the script derives readable view folders from them. Use `--name` only to select a stable view name for a single prompt. Follow the guide’s named-view revision procedure when the user requests changes; edit the source prompt and generate a new version without overwriting earlier records. Read only the selected prompts. Use config defaults, per-prompt flat frontmatter, and CLI overrides in that precedence order (see the guide). Choose settings within the requested presentation and spending constraints; inspect resolved settings in the dry run. Preserve user-approved text; do not silently rewrite it or transmit unrelated project files.
2. Check current model availability, reference support, parameter support, and pricing using the official Image API documentation/catalogue linked in the guide. The example model is a documented example, not a promise of account availability. Keep secrets in the environment.
3. For related UI views, generate the overview first. Inspect it and obtain a selection if user review was requested before generating dependent views with that saved image as `--reference`. Do not assume sequential requests share conversation or image context.
4. Run the script without `--execute` to validate inputs offline. Execute only within the user's generation authorization, using `--max-requests` to bound calls. A request-count limit is not a dollar budget; use account spending controls for a hard monetary limit.
5. Inspect generated images for the requested content, legibility, layout, and consistency. Report failures honestly; a saved response is not visual approval. Regeneration incurs another request and must remain within authorized scope.
6. Resume by repeating the same command. Completed matching requests are skipped; unresolved requests block automatic resubmission. Follow the guide's reconciliation procedure instead of deleting tracking files to make the script run.

Deliver paths to images with prompt identities, actual usage/cost if returned, and visual-review limitations. Never label unknown cost as zero. No automatic publishing, committing generated assets, or live generation merely to test setup.
