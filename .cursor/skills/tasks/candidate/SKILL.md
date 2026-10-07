---
name: candidate
description: Decide when a dev commit should become a release candidate, prepare it for outside release testing, install the candidate workflow, and record the tester's result in TESTING.md. Not for every commit, merging, or running the release tests yourself.
---

# Prepare and record a release candidate

A release candidate is one `dev` commit that an outside tester installs from a fresh clone and tests before it is proposed for `main`. The tester works only from the repository: README, TESTING.md, and the project documents. Testing costs real time and usage, so it happens only when a candidate is recommended and the user tags it.

## When to recommend one

Recommend a candidate when at least one of these is true:

- a PLAN milestone is complete;
- the change touches installation, setup, dependencies, stored data, or data migrations;
- several features have been completed since the last candidate in TESTING.md;
- the user is about to publish a version.

Do not recommend one for wording, styling, refactoring, or a single feature that the after-change, scripted, and every-commit levels already cover. Say why in one sentence either way when asked.

## Prerequisites

Before recommending, confirm or report as missing:

- TASK's version convention names the version this candidate represents;
- the work is committed and pushed to `dev`, and its every-commit checks passed at that commit;
- TESTING.md's release-test section covers the changed journeys and lists blocking failures;
- the README's install and quick-start instructions match the current code;
- the candidate workflow is installed.

Return a missing prerequisite to the coordinator for its owner. Do not tag around it.

## Tag the candidate

Candidate tags are `<version>-candidate.<n>`, for example `1.2.0-candidate.1`. Increase `n` when the same version is tested again after a fix. The user tags; agents give the commands and do not run them unless the user explicitly asks:

```bash
git tag -a 1.2.0-candidate.1 <commit> -m "Release candidate 1.2.0-candidate.1"
git push origin 1.2.0-candidate.1
```

Add the candidate to TESTING.md as requested, with its commit and one sentence on what changed since the previous candidate.

## What happens next

The candidate workflow checks that the tagged commit is on `dev`, creates the branch `candidate/<tag>` at that commit, and opens a "Release test" issue labelled `release-test`, naming the version, tag, and commit for the tester. The tester clones that commit, follows the release-test section, and either opens a pull request from `candidate/<tag>` to `main` with its report, or posts the report on the issue and labels it `blocked`. The user reviews and merges. The pinned branch keeps later `dev` work out of the tested pull request.

## Record the result

When assigned, Verification reads the tester's report from the pull request or issue and updates TESTING.md: the candidate entry's result and link, and the coverage record for each criterion the report verified or failed. Blocking failures go to the coordinator as findings for the next work; advisory notes are recorded but do not block. A fix that follows is a new candidate with a new tag, not a re-run of the old one. Do not re-request testing for an unchanged commit unless the user asks.

## Install the workflow

This is one-time setup per project, done by an implementation role when assigned. Copy [the workflow](templates/candidate.yml) into the app repository at `dev/.github/workflows/candidate.yml` without project-specific changes. Then report what only the user can set up:

- the outside team's access to this repository: a fine-grained token for the GitHub CLI, with the permissions listed in the project's TEAM.md. The Coordinator writes TEAM.md with the **team** skill;
- the repository variable `PROJECT_DOCS_REPO`, set to the project documents repository's URL, so request issues tell the tester where TESTING.md and TEAM.md are;
- the optional repository variable `RELEASE_TESTER`, only when the tester has its own GitHub account to mention and assign.

Do not create accounts, tokens, or repository settings. Whether the tester picks up requests reliably is unconfirmed until a first trial; report the trial's outcome honestly.

Return the recommendation, missing prerequisites, or recorded result, then stop.
