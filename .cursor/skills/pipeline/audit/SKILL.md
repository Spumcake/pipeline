---
name: audit
description: Record a Coordinator's substantial target-project effort, or an explicitly requested audit, in a brief timestamped file. Record intent, actual participants, attempts, outcome, evidence, and remaining work; replaces a rolling CHECKING.md without triggering a broad audit automatically.
---

# Record a substantial effort

Write a factual checkpoint for the Coordinator's target-project workflow or an explicit user request. Do not automatically audit maintenance of Pipeline, direct skill use, or individual worker assignments. Use at a milestone boundary or after an authorized coordinated project task changes files and completes, stops blocked, or is abandoned. Include consequential failures and their recovery in that record. An explicitly requested investigation or review audit is also in scope. Do not create a file for each read, tool call, trivial edit, or worker message. One coordinated effort should normally produce one record using the workers' concise results; a task and milestone completed together need only one. No hourly cadence, automatic commits, or progress screenshots.

## Gather only what is needed

Use the request, actual actions, changed artifacts, returned worker results, and checks already performed. Do not reread the entire project or launch tests simply to complete this record. Summarize observable actions and decisions, not private reasoning or a transcript.

If asked to review document consistency, inspect the relevant sources and relationships: preserved intent, ownership/contracts, dependencies, and whether the next task's acceptance fits its scope. Cite concrete contradictions and their consequences. Separate blockers from optional suggestions. Do not expand the review into redesign or runtime verification. Disclose self-review rather than claiming independence.

## Write the record

Adapt [the template](templates/AUDIT.md). Honor a target project's existing audit location or explicit destination; otherwise use the default below. The outer Pipeline development-notes folder is not a default for consuming projects. Obtain the actual current UTC time from the environment and create:

`.project/documents/audits/YYYY-MM-DDTHH-mm-ssZ-short-topic.md`, relative to the workspace root, in the project documents repository

Create the folder when needed. Use a numeric suffix on collision; never overwrite an earlier audit. Do not create or update CHECKING.md. Preserve existing historical reports and link them if relevant. On a follow-up, create a new record linking the previous one and describe what changed.

Include the intended outcome, actual roles involved and their assignments, concise attempts/changes, achieved outcome or blocker, and evidence/limits. Distinguish requested roles from actually invoked workers, independent review from self-review, and planned concurrency from observed overlap. If one agent did the work, say so.

For checks, report what ran and its result; distinguish inspection, automated execution, human review, and unverified claims. Link relevant files or existing output instead of copying logs. Record the version from TASK's version convention and the app commit the evidence applies to (for example `git -C dev rev-parse --short HEAD`), noting uncommitted changes; TESTING.md's coverage record and later release testing depend on it. Do not require hashes for every document. Exclude secrets and unnecessary personal data.

Aim for a brief record, usually 150–300 words; add only detail needed to explain material findings. Record failed or abandoned approaches that explain the outcome without narrating every step. Do not fabricate approvals, costs, or measurements.

## Finish

When PLAN or TODO exists, the Coordinator updates affected milestones or checklist items from the same evidence and links this record where useful. Do not create either document just to complete an audit. Do not mark a milestone verified merely because implementation ended, or reopen specialist documents for cosmetic edits. The audit is history, not a second roadmap or queue.

Check that the outcome and evidence agree, references resolve or are explicitly unavailable, and the next action is clear. Saving an audit does not approve the work or authorize another phase. Return its path and stop; do not audit the act of writing an audit.
