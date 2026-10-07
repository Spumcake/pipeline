# Changelog

## Version convention

Pipeline uses `MAJOR.MINOR.PATCH`. Earlier proof-of-concept releases used `MAJOR.MINOR.PATCH-poc.N`.

- `0.x` is experimental: workflows and generated-document conventions may change. No compatibility guarantee is implied; migration-impacting changes are called out here.
- During the proof of concept, increment `poc.N` for the next published iteration of the same intended release.
- Increment MINOR for a new capability set or a material workflow/template contract change; PATCH for compatible corrections after a base release.
- After 1.0, increment MAJOR for incompatible public resource/workflow contracts, MINOR for compatible additions, and PATCH for compatible fixes.
- Git release tags, when created, use `v` followed by the version. A changelog entry or tag does not establish operational verification.

Version applies to the Pipeline bundle, not the applications it prepares. Project readiness is reported separately as **specified**, **configured**, or **verified**, tied to evidence. Release versions reflect the maintained bundle; verification claims remain limited to recorded evidence.

## Unreleased

- Rename the project from Resources to Pipeline.
- Define four test levels: preview after a change, scripted tests for that change, deterministic every-commit GitHub Actions checks, and release testing of tagged candidates. The tests skill places each check at one level.
- Add a Verification-owned TESTING.md template with every-commit commands, a release-test brief for an outside tester, and a coverage record keyed by version and commit. Verification records the commit it checked and recommends release candidates.
- Require audits to record the version and commit; the Coordinator may read the current commit and dirty state for that purpose only.
- Add the candidate skill and workflow: `<version>-candidate.<n>` tags on `dev` pin the commit to `candidate/<tag>` and open a test-request issue. The user tags and merges.
- Add a Documentation subagent and README skill modelled on mature open-source READMEs (badges, description, features, demo, stack, quick start, install, development, documentation, contributing, license). The Coordinator has it revisit the README before coordinated work is committed.
- Add the Coordinator-owned **team** skill and template. The Coordinator advises on the outside team a project needs (people, agent teams such as Grok Bot, automated services, or a mix) and writes the project's root TEAM.md. TEAM.md covers branches and tags, the owner, version control and release-testing roles plus project-specific ones, labels, and access limits, and stays neutral about who fills each role. The Coordinator treats that team's `blocked` and `ci-failure` issues as findings. Usage step 1 in the README can ask what team the project needs.
- Add the worktrees layout: Cursor opens a project's `worktrees/` folder, which holds Pipeline, the workspace AGENTS.md, a separate project documents repository at `.project/`, and one folder per app branch. Pipeline files and project documents never go into the app's branches; INTERFACE.md moves to `.project/documents/` and TEAM.md to `.project/TEAM.md`.
- Add a Branch Manager subagent and worktrees skill. It creates one worktree per concurrent assignment from `dev`, commits finished work, merges it into `dev`, commits the project documents, and removes merged worktrees. Agents commit locally; the owner pushes. The candidate workflow names the documents repository through `PROJECT_DOCS_REPO`.
- Validation: YAML parsed and the issue script dry-run with a stubbed `gh`. No Cursor, GitHub Actions, or Grok trial has been run.

## 1.0.0 — 2026-10-04

First 1.0 release, designated by the project owner following successful user-run preparation, UX generation, and incremental implementation trials. Recent image naming/high-quality enforcement and concurrency instruction changes have not been independently retested.

- Make concurrent implementation a normal coordinator consideration, with bounded workers, exclusive ownership, and a designated integration worker.

- Fold systems-document authoring into Technical Planner and move SYSTEMS.md.template alongside agent templates. Remove the standalone systems skill and synchronize the role/template to example. Existing project SYSTEMS.md is unchanged.

- Require exact timestamped archives before replacing PLAN/TODO for another slice or clearing completed work. Keep routine progress edits in place and preserve unfinished work; synchronize instructions to example without modifying its active project documents.

- Require high image quality in generation instructions and enforce it in the client; reject lower or unset quality before sending requests. Update example configuration and clear its previous prompts/generated outputs at user request. No generation or tests run.

- Use purpose-named image folders with preserved numbered revisions and internal request hashes. Add named-view prompt editing/regeneration guidance; relocate existing example outputs and repair links without generating images. Changes untested at user request.

- Clarify that UX image series need no existing bootstrap artwork: generate an initial overview from the product documents, then reuse it as the visual base. Synced to example; no generation or tests run.

- Extend interface visualization into a discover-first workflow: sitemap, saved prompts, and a sequential UX image series with explicit base references. Abort before artifacts if no suitable image skill exists. Remove tables from the interface template. Synced to example; no workflow or generation tests run.

- Rewrite the project AGENTS template as concise shared session instructions, remove the role catalog, and reference skills by name. Align coordinator authorship guidance; existing example project documents are not regenerated.

- Add plan and todo creation skills with short prose/checklist templates. Coordinator guidance describes their purpose and upkeep without automatically generating project documents. Preserve event-based audit records; no hourly logging.

- Convert the distributable payload from `.github/` to `.cursor/` for Cursor IDE. Keep Coordinator as a manually attached main-chat rule; migrate five workers to native Cursor subagents with inherited models.
- Replace VS Code invocation/tool metadata with Cursor configuration. Code Review is read-only; other role limits remain instructions over inherited tools.
- Update active skill/model paths and import instructions. Coordinator templates use `.md.template` suffixes to avoid agent discovery. Historical audit records are untouched; no model trial performed.

- Enforce strict role scope and route-before-inspection; prohibit Coordinator Git investigation and specialist fallback.
- Cap pitches at 700 words with no tables or administrative preamble; bound reference research to one query and three pages with no manuals/PDFs.

- Refocus pitch creation on solution criteria, concrete usage strategies, verified reference-product adaptations, and presentation criteria from short human input.
- Replace the table-heavy pitch template with a prose-led product brief; move architecture and delivery-process detail out of its remit.
- Align Product Designer instructions and the README trial example with this input-to-pitch workflow.

## 0.3.0-poc.1 — 2026-10-03

**Status: proof of concept; revised example-project trial pending.** Material workflow and installation change.

- Replace role-like automation skills with six native VS Code agent definitions: Coordinator, Product Designer, Technical Planner, Task Operations, Code Review, and Verification.
- Coordinator owns TASK.md and project AGENTS.md, discovers specialist roles, and stops unsupported requests instead of doing specialist work itself.
- Retain focused PITCH, INTERFACE (formerly DESIGN), SYSTEMS (formerly ARCHITECTURE), and audit skills; add purposeful testing guidance. Templates accompany their roles or skills.
- Move model utilities to `.github/skills/models/`; image mockup requests belong to Product Designer.
- Import only `.github/`. Root AGENTS.md, README.md, and CHANGELOG.md are Pipeline development/usage files, not target-project instructions.
- Replace rolling CHECKING.md with brief timestamped Coordinator project audits. Workers return evidence without automatic duplicate records; Pipeline maintenance does not trigger audits.
- Migration: review obsolete `.github/agents/automation/` and `.github/models/` copies, merge the new payload, and reconcile existing DESIGN/ARCHITECTURE documents with their new names deliberately. Preserve unrelated project files and historical evidence.
- Validation: role/skill structure and local references checked. Editor activation, routing, end-to-end project execution, and concurrent execution of this revised bundle remain unverified.

## 0.2.0-poc.2 — 2026-10-02

- Move designer into automation skills, add its usage README and shared DESIGN.md template, and update discovery links.
- Place the designer view/UX map at repository-root `DESIGN.md` by default; generated image artifacts remain under `.project/models/`.

## 0.2.0-poc.1 — 2026-10-02

**Status: proof of concept; full development pipeline unverified.** New visual-design and model-resource capabilities.

- Add a designer skill for pitch-driven view/UX maps, discovered model skills, base-image dependencies, named prompt/image pairs, provenance, and visual review.
- Add OpenRouter Sunburst image-generation resources: skill, script, configuration example, local tests, and usage guide.
- Resolve image settings from config defaults, per-prompt metadata, and CLI overrides; validate before submitting and include effective settings in resume identity.
- Support explicit local environment-file loading, reference images, sequential request limits, and safe failure/resume records.
- Broaden the main usage guide to cover model utilities and document agents-only sparse checkouts.
- Validation: 12 local script tests pass; low-quality generation and resume exercised live. A supervised designer trial extended the workshop example with two medium-quality reference-based views, preserved named prompt/image pairs, and recorded provenance and visual review. Independent-agent evaluation and human approval remain pending.

## 0.1.0-poc.2 — 2026-10-02

**Status: proof of concept; full pipeline unverified.** Agent-template iteration of the initial release.

- Add five portable agent templates: coordinator, implementation specialist, user experience reviewer, acceptance verifier, and test/build runner.
- Connect the agents skill to the templates for project-specific adaptation; define bounded assignments, ownership, evidence, and handoffs without requiring every role on every task.
- Templates remain unactivated and behaviorally unverified; no runner configuration or example-project trial is included in this change.
- Validation: agents skill structural validation, local template links, and whitespace checks pass.

## 0.1.0-poc.1 — 2026-10-02

**Status: proof of concept; full pipeline unverified.** Initial publication for a subsequent example-project trial. No complete pitch-to-implementation run has been demonstrated.

### Added

- Six project-agnostic skills: pitch, pipeline, discovery, spec, agents, and checking.
- PITCH.md, TASK.md, ARCHITECTURE.md, and AGENTS.md templates with contextual placeholders.
- Pitch example and README usage instructions, including cloning resources into a target project's `.project/resources`.

### Strengthened before initial publication

- Separate specified, configured, and verified readiness; report missing setup without inventing evidence.
- Require observable acceptance conditions for every milestone and trace the roadmap to the central user journey.
- Identify operational concurrency prerequisites, runner activation, isolated resources, and integration evidence.
- Define pre-commit versus integration/release checks, blocking failures/unavailable checks, and evidence identity.
- Require reproducible preview recipes and controlled failure checks when mechanisms exist and execution is authorized.
- Preserve the boundary between kit preparation and product implementation while allowing explicitly requested local pipeline configuration.

### Validation and limitations

- Skill frontmatter and names validated; local resource references and template section references checked.
- Pitch and PITCH/ARCHITECTURE templates retain their prior content in this iteration.
- Operational preview, check effectiveness, concurrent execution, and complete example-project acceptance remain unverified.
- No default reusable subagent roster or executable dependency scheduler is included.
