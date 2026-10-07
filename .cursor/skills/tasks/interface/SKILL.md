---
name: interface
description: Define views and user flows in INTERFACE.md, or create a sitemap, prompts, and a coherent series of UX images using an image-generation skill discovered in the project. Generation is optional and requires a user request; not application implementation.
---

# Define and visualize the interface

Support two outcomes: interface documentation, or a requested series of images showing how someone uses the product. A document request does not authorize image generation. A request for UX images includes the sitemap and prompt preparation needed to produce them; do not stop at a list of prompts when generation was requested.

Read the relevant pitch, existing interface decisions, and supplied references. Use the existing canonical interface document, otherwise `.project/documents/INTERFACE.md` in the team repository. If the project uses DESIGN.md, preserve it unless a rename is authorized. Adapt [the template](templates/INTERFACE.md) only where needed; do not rewrite finished specifications or create implementation plans as a side effect.

## Discover generation capability first

For an image request, identify a suitable installed image-generation skill before creating or modifying artifacts. Inspect the project's skill names and descriptions, starting with model skills and widening to other project skill locations only if needed. Read the selected skill and its required usage instructions. Discover by capability; do not assume a particular provider, model, or script path.

If no suitable image-generation skill exists, stop and report that missing capability. Do not create a sitemap, prompts, substitute code mockups, or a new API integration. If a skill exists but cannot run because credentials, tools, reference support, or required authorization are missing, report that specific blocker before starting generation work. Do not expose credentials or make paid calls merely to test setup.

## Map the experience

Use the requested scope and existing product decisions to identify the smallest series that explains the central user journey. Distinguish pages from dialogs, panels, and important states. Include recovery or empty states when they change what the user can do; do not generate every conceivable state.

Keep a concise sitemap in INTERFACE.md: a small linked list or flow showing where the user starts, which action opens each view, and where it leads. Reuse an existing sufficient map. Give each planned view a short, stable, purpose-based name and explain its purpose in one or two sentences. Use that same name for its document heading, prompt filename, and generated view folder; sequence numbers may order prompt filenames but hashes must not be user-facing names. Use natural prose and lists, not tables or inventories of labeled fields. Do not invent product features to make a more impressive gallery.

## Prepare prompts and references

Bootstrap or approved images are optional inputs, not prerequisites. Check supplied paths and the project’s documented image locations; do not search unrelated repositories for a base. If a suitable image exists, inspect it and preserve its established visual choices. If none exists, use the pitch and interface to prepare and generate the first overview without a reference image, then inspect and reuse that output for dependent views. This first image is part of the requested series, not a separate bootstrap task requiring permission. Make routine visual choices as proposals; do not claim human approval. Pause for selection only when the user explicitly requested it, or ask if they explicitly require a particular missing reference rather than an original base.

Create one saved prompt per planned image in the format required by the discovered model skill. Specify the view's purpose, visible UI, interaction state, sample content, and what must stay consistent with the base. Use fictional sample data. Choose supported dimensions and aspect ratio for the actual layout. Image quality must always be high; never use medium, low, or an unspecified provider default. If the discovered generator cannot supply high quality, report that limitation rather than downgrade.

Keep prompts, images, and generation records under the project's existing artifact convention. Otherwise use `.project/visuals/<provider>/<model>/<view-id>/` in the team repository. In INTERFACE.md, link each view's prompt and, once available, its image and native run record. Briefly state the base dependency and the action connecting it to the next view; do not duplicate entire prompts there.

## Generate the series

Follow the discovered image skill's execution, settings, cost, and recovery instructions. Use the smallest planned request count, one image per selected view unless the user requested variants, within existing authorization and spending limits. Do not add a separate approval gate merely because prompts were prepared by an agent; honor any user-requested review and model-skill requirements.

Generate and inspect the base before dependent views. Supply its actual saved image path to each dependent request; independent calls do not share context. Generate the remaining views sequentially, carrying suitable references explicitly. Inspect each image for layout, legibility, state, and consistency. Record a material defect instead of silently accepting it or entering an open-ended regeneration loop.

On resume, preserve completed outputs and unresolved request records. Follow the model skill's reconciliation procedure rather than resubmitting a timed-out job blindly. If execution becomes blocked, retain the completed artifacts and report which views remain unfinished.

## Revise an existing view

Resolve the user’s view name through INTERFACE.md and its linked prompt and image. Ask only if the reference is genuinely ambiguous. Inspect the current image, modify its source prompt for the requested change, and use the discovered generator’s revision procedure to save a new version under the same view name. Preserve previous images and run records. A prompt-only request stops before generation; a request to change the image includes regeneration within the established limits.

Update that view’s current artifact links after generation and inspection. Do not regenerate unrelated views. If the edited image is a base, identify affected dependents and leave their regeneration outside scope unless requested. Keep view entries in short prose sections, not a table, so the user can refer to the same names in later requests.

## Finish

Return the sitemap/document and image paths, the order to view them, and concrete limitations. Distinguish generated, visually inspected, and human-approved; images do not verify application behavior. Return evidence for the coordinator's consolidated audit, not a separate worker log. Stop without changing the pitch, implementing the app, or generating unrequested variants.
