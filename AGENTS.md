# spum-pipeline — working principles

These instructions govern development of spum-pipeline. Import only `.cursor/`, into a consuming project's team repository (`<app>-team`); do not copy this root file, README.md, or `.project/CHANGELOG.md`. Coordinator templates generate project-specific instructions. New development records default to `.project/documents/development/` with lowercase filenames; preserve existing canonical paths. PITCH defaults to `.project/documents/PITCH.md` and INTERFACE to root `INTERFACE.md`.

Pipeline provides reusable agent definitions and capabilities for focused development. Its purpose is to keep one agent from having to understand and solve an entire project at once. Judge pipeline decisions by whether they reduce unnecessary context, coordination, and work while delivering the requested outcome.

## Agents and skills

- `.cursor/agents/` contains agent definitions and their supporting resources, including templates. Reusable skills belong under `.cursor/skills/`. A role defines responsibility, allowed actions, relevant context, expected output, and when to stop.
- `.cursor/skills/` contains reusable capabilities that different agents can consult. A skill explains how to perform an operation; it does not create a worker or isolate context. Do not disguise a role as a skill.
- `.cursor/rules/development.mdc` is a manual rule for the main conversation, attached with `@development`. It is not a subagent or a role selected from a VS Code dropdown.
- The coordinator is the main conversation's role. It partitions work, invokes predefined workers, resolves dependencies, and combines results. It should not repeat every worker's investigation or implementation.
- Before starting a project's multi-agent implementation, have the required roles defined, discoverable, and callable in the chosen environment. Confirm real delegation with a small bounded task. Role descriptions alone are not evidence that delegation works.
- Before executing a coordinated request, match its required capabilities to suitable callable roles. If one is missing, stop and tell the user what role should be added; if a definition exists but cannot run, report that activation blocker. Do not perform partial work, write substitute documents/audits, or use a generic role to bypass the gap. Coordinator-owned TASK/PLAN/TODO/AGENTS authorship remains direct work, but does not permit inventing missing specialist decisions.

## Pipeline preparation

Preparation remains a distinct phase. The coordinator discovers roles and their prerequisites rather than enforcing a fixed team or document sequence. Document-creation skills are reusable capabilities; roles own their use and review. Before dependent work, check only the documents needed for that assignment. Each selected role checks its own prerequisites. If a specialist document is missing or materially incomplete, its owning role uses the relevant skill within the authorized preparation scope rather than guessing or generating the entire kit automatically:

- [Product Designer](.cursor/agents/product-designer.md) owns PITCH via the [pitch skill](.cursor/skills/pipeline/pitch/SKILL.md): user intent and constraints; default `.project/documents/PITCH.md`.
- [Product Designer](.cursor/agents/product-designer.md) also owns root `INTERFACE.md` via the [interface skill](.cursor/skills/tasks/interface/SKILL.md), and discovers model skills to generate requested mockups. The Coordinator delegates this work rather than generating images itself.
- [Technical Planner](.cursor/agents/technical-planner.md) owns technical boundaries and `.project/documents/development/systems.md` directly, using its own [template](.cursor/agents/templates/technical-planner/SYSTEMS.md.template).
- [Coordinator](.cursor/rules/development.mdc) directly creates and maintains TASK.md (scope, acceptance, preview and delivery), PLAN.md (milestones and dependencies), TODO.md (prioritized assignments and status), project AGENTS.md (working rules), and TEAM.md at the team repository's root (version control and integration, addressed to the outside team that handles and tests commits, via the [team skill](.cursor/skills/pipeline/team/SKILL.md)). The Coordinator updates TODO on dispatch/results/blockers, PLAN on milestone or dependency changes, and consolidates evidence in timestamped audits at milestone boundaries or when coordinated work stops blocked or abandoned. These files link to each other instead of duplicating state. TASK and AGENTS authorship remain role responsibilities. PLAN and TODO use the plan and todo skills when implementation planning is authorized; missing files alone do not trigger creation. Templates live under `.cursor/agents/templates/coordinator/` with `.md.template` suffixes so they are not discovered as agent definitions.

Honor existing canonical locations and explicit user paths. Do not maintain duplicate authorities. Writing a specification does not authorize implementation. Missing material intent requires a focused question or an explicit unknown, not an invented requirement.

Automatic effort audits apply to the shipped Coordinator's work in a consuming project, not to maintenance of Pipeline itself. Do not create an audit for routine work on this repository unless explicitly requested. Preserve existing local notes and historical records at their current paths; do not invent an outer checkout or relocate records during maintenance. In target projects, the Coordinator consolidates worker evidence into `.project/documents/development/audits/` unless the project specifies another location. Workers and document skills do not independently generate automatic effort logs.

## Execution roles

- [Task Operations](.cursor/agents/task-operations.md) implements bounded changes in an established stack; it is not an all-purpose fallback.
- [Code Review](.cursor/agents/code-review.md) reviews assigned code or document consistency and returns actionable findings without fixing them.
- [Verification](.cursor/agents/verification.md) runs proportionate acceptance checks, tests, builds, and available preview interactions without changing product code. It owns the testing record and recommends candidates only after a version is agreed and appropriate acceptance evidence exists. It does not routinely repeat the implementer’s passing unit suite.
- Task Operations owns the app README and deterministic automation when assigned; revisit the README when a command or setup step changes.
- [Branch Manager](.cursor/agents/branch-manager.md) runs every state-changing Git operation: worktree setup and cleanup, commits, merges into `dev`, and team repository commits. It never pushes or tags.

Consuming projects use the layout from the [worktrees skill](.cursor/skills/tasks/worktrees/SKILL.md). Cursor opens the project's team repository, `<app>-team`, which holds `.cursor/`, AGENTS.md, TEAM.md, and `.project/documents/`. Each app repository is a bare clone under ignored `src/<repo>/worktrees/.bare/`, with `src/<repo>/worktrees/dev/` as its permanent worktree. Existing inline apps remain in place until migration is authorized. Pipeline files and project documents never go into the app repository. Implementers check affected behavior before reporting completion. Commits happen only when requested, through Branch Manager; installed hooks check staged contents and CI repeats deterministic checks. Verification handles requested or milestone acceptance journeys. Milestone audits identify actual app revisions and dirty state. App-related team commits identify matching app revisions in `App-Commit:` trailers; pipeline-only maintenance needs no app trailer.

Version control and release testing in app repositories are handled by an outside team, which reads the project's TEAM.md. That team reads only the app and team repositories, never the `.cursor/` payload, so TEAM.md, TESTING.md, README, and the project documents must be sufficient for it.

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

Pipeline and document maintenance closes after edits and relevant consistency checks, without an app Verification run or automatic audit. Do not commit, push, tag, install application automation, or migrate a consuming project merely because pipeline maintenance was requested.
