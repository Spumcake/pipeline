---
name: team
description: Create or update a project's root TEAM.md, addressed to the outside team that handles and tests new commits — branches and tags, owner, version control and release-testing roles, labels, and access limits. Coordinator-owned; not instructions for development agents.
---

# Write the integration team document

TEAM.md tells an outside team how to handle and test new commits in this repository: what lands where, who may do what, how release candidates are tested, and the limits of the team's access. The team may be people or bots. They read only the repository, so TEAM.md must stand on its own. It is not for the development agents, who follow AGENTS.md.

## When to create it

Create TEAM.md when authorized work sets up the project's integration flow, for example installing the candidate workflow or defining every-commit checks, or when the user asks for it. Do not create it just because Pipeline is installed or the file is missing.

It depends on facts owned elsewhere. Before writing, confirm they exist, or return the gap to the owner:

- the version convention in TASK;
- TESTING.md with every-commit commands and a release-test section, from Verification;
- the every-commit and candidate workflow files, from an implementation role;
- the repository URL from `git remote get-url origin`, and the owner the user names.

Use only established facts. Leave a placeholder out rather than guessing a workflow name, path, or owner.

## Write it

Adapt [the template](templates/TEAM.md) and save it at the repository root as `TEAM.md`, unless the project already has a canonical location. Keep the template's branch model, roles, labels, report contents, and limits unless the project's integration flow actually differs. If it does, change only the affected lines. Fill in the project facts: name, repository, one-sentence description, owner, workflow files, document paths, and whether the app stores data.

Reference TESTING.md and the project documents instead of copying their content. TEAM.md says how the team works; TESTING.md says what to test. Write plain sentences and short lists, with no tables. Never include tokens, secrets, or personal contact details beyond the owner's name or GitHub login.

## Keep it current

Update TEAM.md in place when the branch model, workflow files, labels, document locations, owner, or required token permissions change. Do not regenerate it for routine development.

Return the path and any missing fact, then stop. Writing TEAM.md does not set up accounts, tokens, or repository settings; list those for the user.
