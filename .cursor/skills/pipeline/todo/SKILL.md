---
name: todo
description: Create or update a short prioritized checklist of near-term work when task planning is authorized.
---

# Write a short, human-readable todo list

Use this skill when authorized work needs a prioritized task list or an update to one. Do not create TODO.md just because the pipeline is installed, specifications exist, or the file is missing. Preserve an existing canonical location; the default is `.project/documents/development/todo.md`.

## Preserve earlier work

Routine progress updates stay in place. Before replacing the document for a new slice, substantially rewriting it, or clearing completed work, archive its exact existing contents under the project's documents directory: `archive/YYYY-MM-DDTHH-mm-ssZ-short-purpose/`, keeping the original filename. Use the actual UTC time and a short descriptive purpose; when replacing PLAN and TODO together, use the same archive folder for both. Never overwrite an earlier archive; add a numeric suffix if needed.

Save and confirm the unchanged archive copy before replacing the active file. If archiving fails, leave the active document intact and report the blocker. Retain outstanding decisions and unfinished work in the replacement unless explicitly deferred or dropped; do not silently lose them. Add one short relative link to the previous version in the new document. An audit or Git history does not replace this archive. Do not archive or reset documents merely because a new slice starts if a small update is sufficient.

Read the current goal and relevant plan or assignment, not the whole project. Use [the template](templates/TODO.md). List only the next useful actions in priority order. Each checkbox should be a natural sentence explaining what to do and the result it should produce. Usually one sentence is enough; add a short second sentence only for a real blocker or dependency. Name an owner only when that helps the reader.

Keep it small: normally three to seven current actions, well under 200 words. Do not invent tasks to fill that range. No tables, field lists, status banners, nested specifications, or repeated contracts. File permissions, full test procedures, and delegation instructions belong in the coordinator's handoff, not in each todo. Link existing detail only when useful. Later milestones stay in PLAN.

Check an item only when the agreed outcome is actually achieved. Describe a blocked item in ordinary language; do not mark it complete. Keep completed items brief, link relevant audit evidence, and archive the existing list before removing stale completed items. The coordinator maintains the shared list from worker results to avoid concurrent edits.

Return the path and any blocker, then stop. Writing a list does not authorize executing it, creating other documents, or running tests.
