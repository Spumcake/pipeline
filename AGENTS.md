# Working principles

These instructions govern development of Pipeline. Import only `.cursor/` into consuming projects; do not copy this root file, README.md, or CHANGELOG.md. Coordinator templates generate project-specific instructions.

Pipeline provides reusable agent definitions and capabilities for focused development. Its purpose is to keep one agent from having to understand and solve an entire project at once. Judge pipeline decisions by whether they reduce unnecessary context, coordination, and work while delivering the requested outcome.

## Agents and skills

- `.cursor/agents/` contains agent definitions and their supporting resources, including templates. Reusable skills belong under `.cursor/skills/`. A role defines responsibility, allowed actions, relevant context, expected output, and when to stop.
- `.cursor/skills/` contains reusable capabilities that different agents can consult. A skill explains how to perform an operation; it does not create a worker or isolate context. Do not disguise a role as a skill.
- `.cursor/rules/coordinator.mdc` is a manual rule for the main conversation, attached with `@coordinator`. It is not a subagent or a role selected from a VS Code dropdown.
- The coordinator is the main conversation's role. It partitions work, invokes predefined workers, resolves dependencies, and combines results. It should not repeat every worker's investigation or implementation.
- Before starting a project's multi-agent implementation, have the required roles defined, discoverable, and callable in the chosen environment. Confirm real delegation with a small bounded task. Role descriptions alone are not evidence that delegation works.
- Before executing a coordinated request, match its required capabilities to suitable callable roles. If one is missing, stop and tell the user what role should be added; if a definition exists but cannot run, report that activation blocker. Do not perform partial work, write substitute documents/audits, or use a generic role to bypass the gap. Coordinator-owned TASK/PLAN/TODO/AGENTS authorship remains direct work, but does not permit inventing missing specialist decisions.

## Pipeline preparation

Preparation remains a distinct phase. The coordinator discovers roles and their prerequisites rather than enforcing a fixed team or document sequence. Document-creation skills are reusable capabilities; roles own their use and review. Before dependent work, check only the documents needed for that assignment. Each selected role checks its own prerequisites. If a specialist document is missing or materially incomplete, its owning role uses the relevant skill within the authorized preparation scope rather than guessing or generating the entire kit automatically:

- [Product Designer](.cursor/agents/product-designer.md) owns PITCH via the [pitch skill](.cursor/skills/pipeline/pitch/SKILL.md): user intent and constraints; default `.project/documents/PITCH.md`.
- [Product Designer](.cursor/agents/product-designer.md) also owns root `INTERFACE.md` via the [interface skill](.cursor/skills/tasks/interface/SKILL.md), and discovers model skills to generate requested mockups. The Coordinator delegates this work rather than generating images itself.
- [Technical Planner](.cursor/agents/technical-planner.md) owns technical boundaries and `.project/documents/SYSTEMS.md` directly, using its own [template](.cursor/agents/templates/technical-planner/SYSTEMS.md.template).
- [Coordinator](.cursor/rules/coordinator.mdc) directly creates and maintains TASK.md (scope, acceptance, preview and delivery), PLAN.md (milestones and dependencies), TODO.md (prioritized assignments and status), project AGENTS.md (working rules), and root TEAM.md (version control and integration, addressed to the outside team that handles and tests commits, via the [team skill](.cursor/skills/pipeline/team/SKILL.md)). The Coordinator updates TODO on dispatch/results/blockers, PLAN on milestone or dependency changes, and consolidates evidence in timestamped audits at project task or milestone boundaries. These files link to each other instead of duplicating state. TASK and AGENTS authorship remain role responsibilities. PLAN and TODO use the plan and todo skills when implementation planning is authorized; missing files alone do not trigger creation. Templates live under `.cursor/agents/templates/coordinator/` with `.md.template` suffixes so they are not discovered as agent definitions.

Honor existing canonical locations and explicit user paths. Do not maintain duplicate authorities. Writing a specification does not authorize implementation. Missing material intent requires a focused question or an explicit unknown, not an invented requirement.

Automatic effort audits apply to the shipped Coordinator's work in a consuming project, not to maintenance of Pipeline itself. Do not create an audit for routine work on this repository unless explicitly requested. Existing local notes are under `../../documents/audits/` relative to this checkout (the outer Pipeline folder); do not recreate `.project/documents/` here or move those notes back. In target projects, the Coordinator consolidates worker evidence into `.project/documents/audits/` unless the project specifies another location. Workers and document skills do not independently generate automatic effort logs.

## Execution roles

- [Task Operations](.cursor/agents/task-operations.md) implements bounded changes in an established stack; it is not an all-purpose fallback.
- [Code Review](.cursor/agents/code-review.md) reviews assigned code or document consistency and returns actionable findings without fixing them.
- [Verification](.cursor/agents/verification.md) runs proportionate acceptance checks, tests, builds, and available preview interactions without changing product code. It owns TESTING.md and recommends release candidates.
- [Documentation](.cursor/agents/documentation.md) owns the public README.md and revisits it before each commit.

Version control and release testing in app repositories are handled by an outside team, such as Grok Bots, which reads the project's TEAM.md. TEAM.md must stand on its own: that team reads only the app repository, never the `.cursor/` payload. The tester works from an app repository alone and never depends on the `.cursor/` payload, so keep TESTING.md, README, and the project documents sufficient for it.

Each role establishes its prerequisites. If a document it does not own is needed, it returns that need to the Coordinator for the owner. Do not demand every document for every small task. Workers report missing capabilities; they do not take over another role. Cursor subagents inherit the parent session's tools. Code Review uses Cursor's `readonly: true`; other roles need writes for their assigned artifacts or executed checks. Role prose is not a per-tool permission system.

## Strict role scope

Role definitions are hard capability boundaries, including advice and how-to requests. The Coordinator must route specialist requests before inspecting project contents or Git. Skills cannot expand role authority. Unsupported requests stop with a missing-role explanation. A single-document request is not permission to build the whole pipeline.

## Assignments and concurrency

Give each worker a self-contained assignment: concrete outcome, relevant files and shared contracts, ownership and exclusions, observable acceptance criteria, required verification, and a stopping point. Use the smallest assignment that produces a useful result.

Run independent assignments concurrently when supported. Establish shared contracts first and avoid concurrent edits to the same files. Dependent work waits for its prerequisite; reviewing a change requires that change to exist. Distinguish requested parallelism from observed overlapping execution.

Workers return a concise result: changes or findings, verification actually performed, and any material blocker. The coordinator integrates these results without copying entire working histories into its context. Do not delegate trivial work just to keep every role busy.

## Context and focus

Read the assigned files and relevant instructions first. Search for specific unknowns and read targeted sections; do not load the entire repository, archive, roadmap, or every skill by default. Retrieve additional context only to answer a concrete question needed for the task.

Keep product intent and the current acceptance criteria visible. Use existing patterns where appropriate. Do not invent requirements, frameworks, abstractions, documents, or review stages to make the task more comprehensive. Ask about a material ambiguity; resolve routine implementation choices within scope.

An implementation request should produce a working increment, not an expanding plan. Investigate enough to make the next safe change. If progress stalls, identify the specific obstacle and narrow the assignment rather than repeating broad analysis.

## Verification and stopping

Roles whose responsibility includes writing, changing, or reviewing tests must consult [the testing skill](.cursor/skills/tasks/tests/SKILL.md). Future role definitions with those responsibilities must explicitly reference it. Load it when applicable, not into every conversation automatically.

Specify verification proportional to the behavior and risk. Test count and coverage percentage are not goals by themselves. Preserve required checks; do not create new gates without a concrete need.

Stop when the assigned outcome and agreed checks are satisfied. Repeat or broaden verification only for a relevant change, failure, or unresolved risk. Report actual execution separately from source inspection and human preview. Never invent a pass, an approval, or evidence of delegation.
