---
name: plan
description: Create or update a concise prose implementation roadmap when planning that work is authorized.
---

# Write a readable implementation plan

Use this skill when authorized work requires creating or revising an implementation roadmap. Installing pipeline resources, discussing an approach, or finding that PLAN.md is absent does not by itself call for creating it. Preserve an existing canonical location; the default is `.project/documents/development/plan.md`.

## Preserve earlier work

Routine progress updates stay in place. Before replacing the document for a new slice, substantially rewriting it, or clearing completed work, archive its exact existing contents under the project's documents directory: `archive/YYYY-MM-DDTHH-mm-ssZ-short-purpose/`, keeping the original filename. Use the actual UTC time and a short descriptive purpose; when replacing PLAN and TODO together, use the same archive folder for both. Never overwrite an earlier archive; add a numeric suffix if needed.

Save and confirm the unchanged archive copy before replacing the active file. If archiving fails, leave the active document intact and report the blocker. Retain outstanding decisions and unfinished work in the replacement unless explicitly deferred or dropped; do not silently lose them. Add one short relative link to the previous version in the new document. An audit or Git history does not replace this archive. Do not archive or reset documents merely because a new slice starts if a small update is sufficient.

Read only the agreed scope and the technical decisions needed to order the work. Use [the template](templates/PLAN.md). Describe each milestone in a short paragraph: what becomes usable, what must come first, and what observable result means it is complete. State which work can proceed together when that matters. Link existing acceptance criteria rather than copying them. Preserve agreed version names; do not invent dates, estimates, decisions, or progress.

Write for a person reading the plan. Use descriptive headings and natural sentences, not tables, metadata fields, or semicolon-separated records. Keep the first plan around 200–400 words and later milestones brief; length is a ceiling to aim below, not a quota. Omit irrelevant sections. Detailed assignments belong in the coordinator's handoffs, current actions in TODO, and execution evidence in audits.

Update only affected milestones when dependencies, decisions, or verified progress change. Distinguish intended outcomes from completed work. Return the path and any consequential unresolved decision, then stop. Do not create TODO, run implementation, or launch a trial as a side effect.
