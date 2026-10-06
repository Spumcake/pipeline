---
name: readme
description: Write or revisit a project's public README.md so it matches the current codebase — badges, description, features, demo, stack, quick start, install, documentation, contributing, and license. Use before each commit to reconcile the README with what changed; not for specifications, changelogs, or marketing copy.
---

# Write and maintain the README

The README is the front page of the repository and the only document an outside tester or new contributor is guaranteed to read. It describes the app as it is at this commit, not as planned. Use [the template](templates/README.md). Honor an existing README's structure and wording where it is still accurate; do not rewrite for style.

## Sources

Read only what the README needs:

- PITCH for the one-paragraph description and who the app is for;
- the code, manifests, and SYSTEMS for the stack and the source layout;
- TASK and TESTING for run, install, and check commands;
- PLAN and audits only to tell completed features from planned ones;
- existing LICENSE, CONTRIBUTING.md, SECURITY.md, and `docs/` files for links;
- `git remote get-url origin` for the GitHub owner and repository name.

Treat the code as the authority when documents disagree, and report the disagreement. Use only commands recorded in TASK or TESTING or present in the project's manifests and scripts; never invent one. Release testing installs from this README on a fresh clone, so a wrong command will be found there.

## Sections

Follow this order and omit any section with nothing true to say:

1. **Title and badges.** Badges only for a public GitHub repository. Use shields.io: a stars badge linked to the stargazers page, and a Discord badge only when the user has supplied an invite link. Copy the badge pattern from the template.
2. **Hero image**, if the project has an approved one, such as an INTERFACE overview image.
3. **Description.** Two or three sentences: what it is, who it is for, where it runs. Add one line of status, such as beta or pre-release, from TASK's version convention.
4. **Features.** Short bullets of what works today. Planned work is not a feature.
5. **Demo**, only when the user has supplied a GitHub-hosted video URL (`https://github.com/user-attachments/assets/...`). Put the bare URL on its own line; GitHub renders it as a player. These URLs are created by dropping a video into GitHub's web editor; you cannot create one. Preserve an existing demo URL.
6. **Stack.** Languages, frameworks, storage, and notable services, as bullets.
7. **Quick start.** The fastest working path from nothing to the running app: prerequisites in one sentence, one command block, what to open, and what you should see.
8. **Install**, when setting up for real use differs from the quick start: configuration, data location, running as a service. Add other project-specific sections, such as running on a server, only when the project has them.
9. **Development.** A short source-layout block and the common check commands from TESTING.
10. **Documentation.** Links to existing user-facing documents. Do not link the agent working documents under `.project/` unless the project makes them public.
11. **Contributing and license.** Link CONTRIBUTING.md and SECURITY.md when they exist. Name the license from the LICENSE file. If there is no license, do not choose one; omit the license line and report the missing decision.

## Size and voice

Model the length on a mature open-source README: usually 300–1,300 words, scaled to how much the project actually offers. A small local app needs a few hundred words. Plain sentences, short paragraphs, commands in fenced blocks, no tables, no emoji, no hype. Address the reader directly. Never claim a check, platform, or integration that the codebase does not have.

## Revisit before each commit

When work is about to be committed, reconcile the README with what changed:

1. Find what changed since the README was last updated: `git log -1 --format=%h -- README.md` for the baseline, then `git diff --stat <baseline>` plus uncommitted changes.
2. Check only the sections those changes could affect: a new or removed feature, a dependency or stack change, a changed command, port, path, or configuration, a new document, license, or contributing file.
3. Edit only those sections. If nothing in the README is affected, leave it untouched and say so.

Do not commit. Return the README path, the sections changed or "no change needed", and any missing input: a license decision, a demo URL, a Discord invite, or a command that has never been run.
