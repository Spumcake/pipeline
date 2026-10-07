---
name: team
description: Advise on the team a project needs to handle and test its commits, and create or update its TEAM.md — branches and tags, owner, roles fitted to the project, labels, and access limits. Coordinator-owned. TEAM.md stays neutral about whether roles are filled by people, agents, or services.
---

# Plan the integration team and write TEAM.md

TEAM.md tells an outside team how to handle and test new commits in the app repository: what lands where, which roles exist, how release candidates are tested, and the limits of the team's access. The team reads only the app and team repositories, so TEAM.md must stand on its own. It is not for the development agents, who follow AGENTS.md.

## Who can fill a team

A team can be any mix of the following. Know the options, so you can advise on them and so the roles in TEAM.md suit all of them.

- **People:** maintainers, testers, or reviewers working through GitHub.
- **Agent teams:** persistent AI agents that each take a role and work together.
  - xAI's Grok Bot, in beta since August 2026, is one example. Each bot has a role and its own conversations, memory, and history. All bots on an account share one cloud computer with a browser, a terminal, and files.
  - Grok Bots learn reusable skills from chat or from a recorded demonstration. They run routines on a schedule or on Slack and GitHub events, and can coordinate in group chats.
  - Grok Bots ask before sending, publishing, or deleting, unless the user's auto-review rules allow it. A user can set one up by having it read TEAM.md and build its own approximation of the roles described.
  - Other providers offer similar persistent-agent products, and open-source platforms such as Rakazo can be self-hosted. Capabilities and access change quickly, so check current details before relying on any one product.
- **Automated services:** GitHub Actions, bots, and other services that react to events deterministically.

## Advise on the team

When the user asks what team a project needs, answer in conversation. Do not write TEAM.md unless that is authorized. Derive the roles from the project's actual needs, using PITCH, SYSTEMS, TASK, and TESTING where they exist. For each role, say:

- what it is responsible for;
- how often it acts;
- what judgment it needs;
- what access it needs.

Then describe the options for filling each role, with their trade-offs: people, an agent team, automation, or a mix. Here you may recommend. Respect the user's constraints on cost, privacy, and trust.

## Fit the roles to the project

The template's **Version control** and **Release testing** roles cover the standard flow, in which development lands on `dev`, candidates are tagged, and released code reaches `main` through a pull request. Keep them unless the user has agreed a different flow.

Add a role only when the project has a recurring responsibility in handling or testing commits that those roles do not cover. Examples:

- deployment and rollback for a hosted service;
- device or platform testing for mobile or desktop builds;
- data migration oversight for apps with important stored data;
- security review for authentication, payments, or personal data;
- accessibility or localization review for a public interface.

Do not add roles for development work, which belongs to the development agents, or for hypothetical needs.

## Keep TEAM.md neutral

TEAM.md describes roles, not who fills them. Never:

- say or imply whether a role is held by a person, an agent, or a service;
- name a product, provider, or model;
- prescribe tools beyond GitHub itself.

Describe each role by its responsibility, when it acts, what it reads, what it produces, and its limits, so that a person, an agent team, or an automated service can each take it on. Your advice on who should fill the roles belongs in conversation, not in the file.

## Write it

Create TEAM.md when authorized work sets up the project's integration flow, for example installing the candidate workflow or defining every-commit checks, or when the user asks for it. Do not create it just because Pipeline is installed or the file is missing.

It depends on facts owned elsewhere. Before writing, confirm they exist, or return the gap to the owner:

- the version convention in TASK;
- TESTING.md with every-commit commands and a release-test section, from Verification;
- the every-commit and candidate workflow files, from an implementation role;
- the app repository URL (`git -C worktrees/dev remote get-url origin`), the team repository URL (`git remote get-url origin`), and the owner the user names.

Adapt [the template](templates/TEAM.md) and save it as `TEAM.md` at the root of the team repository, unless the project already has a canonical location. It never goes into the app repository.

- Fill in the project facts: name, both repository URLs, one-sentence description, owner, workflow files, document paths, and whether the app stores data.
- Add project-specific roles where the template marks the place.
- Keep the rest of the template's wording unless the project's flow actually differs.
- Use only established facts. Leave a placeholder out rather than guessing a workflow name, path, or owner.
- Reference TESTING.md and the project documents instead of copying them. TEAM.md says how the team works; TESTING.md says what to test.
- Plain sentences and short lists, no tables.
- No tokens, secrets, or personal contact details beyond the owner's name or GitHub login.

## Keep it current

Update TEAM.md in place when any of these change:

- the branch model;
- workflow files;
- labels;
- document locations;
- the owner;
- the roles the project needs;
- required access permissions.

Do not regenerate it for routine development.

Return the path and any missing fact, then stop. Writing TEAM.md does not set up accounts, tokens, or repository settings, or recruit anyone; list those for the user.
