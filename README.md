# Resources for Cursor

Resources is a reusable collection of agent definitions, skills, and templates for taking a software idea through specification, design, and incremental implementation. We built it after seeing agents become overwhelmed by large codebases and broad assignments, spending too much time analyzing instead of delivering useful changes. Its purpose is to divide work into focused tasks with limited context, clear ownership, and meaningful checks, allowing agents to work concurrently where useful while keeping progress understandable and reviewable by a person.

Version **1.0.0** includes a main-chat Coordinator rule, five focused subagents, and reusable document/model skills. Verification limits are noted below.

## Install into a project

Import **only `.cursor/`**. Resources' root AGENTS.md, README.md, and CHANGELOG.md describe this repository; do not copy them over a project's own files.

From your target project root:

```sh
resources_checkout="$(mktemp -d)"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Spumcake/Resources.git "$resources_checkout"
git -C "$resources_checkout" sparse-checkout set .cursor
mkdir -p .cursor
cp -Ri "$resources_checkout/.cursor/." .cursor/
```

Review overwrite prompts when merging with an existing installation. Preserve unrelated rules and agents. Remove the temporary checkout when finished.

Keep the folder layout intact so references resolve. When migrating, review and remove only obsolete Resources definitions from `.github/agents/` and `.github/skills/`; do not delete unrelated GitHub configuration or project files.

## Use it in Cursor

1. Open the target project folder in Cursor and start a fresh **Agent** chat.
2. Attach the manual **coordinator** rule with `@coordinator` (choose the rule in the suggestions). It applies to this conversation; it is not a Coordinator subagent.
3. Describe what you want in your own words. The rule interprets intent and existing authorization; no prescribed prompt wording is required.

The Coordinator can explain which roles it would use without dispatching them. Work is delegated when the requested outcome actually requires it. A discussion does not create files. If a suitable role is missing, the Coordinator reports the gap and stops.

For direct work, invoke a worker by its slash name, such as `/product-designer`, or mention its exact name naturally. Direct invocation bypasses coordination. Cursor documents [manual rules](https://cursor.com/docs/rules) and [native subagents](https://cursor.com/docs/subagents).

## Responsibilities

| Definition | Responsibility |
| --- | --- |
| [Coordinator rule](.cursor/rules/coordinator.mdc) | Interpret intent, explain/delegate work, own TASK.md, PLAN.md, TODO.md, and project AGENTS.md, consolidate authorized-work audits. |
| [product-designer](.cursor/agents/product-designer.md) | Product intent, PITCH.md, INTERFACE.md, and requested mockups through model skills. |
| [technical-planner](.cursor/agents/technical-planner.md) | SYSTEMS.md, technical boundaries, contracts, and prerequisites. |
| [task-operations](.cursor/agents/task-operations.md) | Bounded implementation in an established stack. |
| [code-review](.cursor/agents/code-review.md) | Read-only review of assigned code or document consistency. |
| [verification](.cursor/agents/verification.md) | Relevant tests/builds and available browser preview checks; no product fixes. |

Workers use `model: inherit`, so they default to the main chat's model. Only Code Review is configured `readonly: true`; other roles need write access for documents, outputs, or test/build artifacts. Cursor tools are inherited from the parent, so the old VS Code tool allowlists are not retained. Role scope instructions still apply. Worker instructions prohibit further delegation.

Subagents run in separate contexts. Independent assignments can run concurrently, but completed work must be confirmed from actual tool results; configuration does not prove overlap. Keep shared-file ownership clear.

## Skills and templates

Cursor discovers the [skills](.cursor/skills/) recursively. Read only the capability needed for the assignment:

- [Pitch](.cursor/skills/pipeline/pitch/SKILL.md): a short public-readable product pitch with bounded reference research.
- [Interface](.cursor/skills/tasks/interface/SKILL.md): sitemap, flows, presentation, and requested UX image series through a discovered image-generation skill. Stops if no suitable generator exists.
- [Plan](.cursor/skills/pipeline/plan/SKILL.md): a brief prose roadmap when implementation planning is authorized.
- [Todo](.cursor/skills/pipeline/todo/SKILL.md): a short checklist of current actions, without assignment specifications.
- [Testing](.cursor/skills/tasks/tests/SKILL.md): meaningful checks and stopping rules.
- [Image generation](.cursor/skills/models/openai/image-2-5-sunburst/SKILL.md): authorized model execution and recovery.
- [Audit](.cursor/skills/pipeline/audit/SKILL.md): one brief record of coordinated project work, not routine Resources maintenance.

Coordinator document templates live in [.cursor/agents/templates/coordinator/](.cursor/agents/templates/coordinator/) with `.md.template` suffixes to distinguish them from worker definitions. These templates produce TASK.md (scope and acceptance) and AGENTS.md (working rules). The plan and todo skills own their own templates. PLAN.md and TODO.md are created when the authorized work needs them, not automatically during setup or specification preparation. The Coordinator updates plans and todos as work advances, and writes brief timestamped audits at task or milestone boundaries; workers return evidence without maintaining separate logs. Technical Planner directly authors SYSTEMS.md using its [role-owned template](.cursor/agents/templates/technical-planner/SYSTEMS.md.template); there is no separate systems skill. Document skills include their own templates. See [Cursor skill discovery](https://cursor.com/docs/skills).

Target documents retain their existing defaults: root INTERFACE.md and AGENTS.md; PITCH.md, SYSTEMS.md, TASK.md, PLAN.md, TODO.md, and coordinator audits under `.project/documents/`. Honor explicit project locations. Existing Resources audit records outside this checkout are not part of the payload and are not altered by this conversion.

Generated AGENTS.md is a concise shared entry point for every agent: project purpose, language, session orientation, orchestration, records, verification, and boundaries. It references skills by name and leaves role definitions in their own files.

After specification or bootstrap work, you can ask the Coordinator to generate images of the main user journey. It delegates the interface workflow, which discovers a generator, maps the views, prepares prompts, and produces consistent images using existing references. Image generation remains optional; a documentation request does not trigger it.

## Validation and ongoing development

The user has reported successful preparation, UX image generation, and incremental implementation in the example project, primarily in Cursor. Recent image naming/high-quality enforcement and concurrency guidance changes have not been independently retested. Version 1.0.0 does not imply identical behavior across models or runners. The example has received the current payload; future Resources edits still need to be copied into consuming projects.
