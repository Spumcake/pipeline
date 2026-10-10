---
name: worktrees
description: The project workspace layout — a team repository holding Pipeline and the project documents, with each app repository's branches in named worktree folders under src — and how those worktrees are created, committed, verified, merged into dev, and cleaned up. Read before any work that touches files or Git.
---

# The team repository

Cursor opens the project's **team repository**. It holds Pipeline, the working rules, TEAM.md, and the project documents. Each app repository lives under `src/<repo>/worktrees/`, which the team repository ignores. `src/` will hold more repositories. The project records its app repository names and URLs in AGENTS.md. This is a supported layout, not permission to migrate an existing inline app or create a remote.

```text
<team>/                              team repository (Cursor opens this)
  .cursor/                           Pipeline
  AGENTS.md                          project working rules
  TEAM.md                            for the outside team that handles and tests commits
  .project/documents/development/    systems, tasks, plan, todo, testing, notes, audits, archive
  .gitignore                         includes /src/
  .cursorindexingignore              keeps duplicate checkouts out of Cursor's index
  src/<repo>/worktrees/              one app repository, ignored by the team repository
    .bare/                           bare clone of that repository
    dev/                             permanent worktree on branch dev
    work-<name>/                     temporary worktree on branch work/<name>
```

## Repositories

- **The team repository** versions everything except the apps: Pipeline, AGENTS.md, TEAM.md, and the project documents. Record its URL in AGENTS.md and TEAM.md.
- **Each app repository** holds only that app: source, tests, README, `.github/workflows/`, and its own configuration. Never put Pipeline files or project documents in it. Record each URL in AGENTS.md and TEAM.md.

Existing projects may keep application code in their current repository until migration is explicitly authorized. Name that repository and its current working directory in assignments; do not pretend a separate app checkout exists. Preserve existing canonical document paths.

Paths such as `.project/documents/` are relative to the team repository's root. App paths are relative to a named worktree, such as `src/<repo>/worktrees/dev/`. Every assignment names the repository and the worktree.

## Worktrees

- **`src/<repo>/worktrees/.bare/`** is a bare clone. It holds that app's history without checking out a copy.
- **`src/<repo>/worktrees/dev/`** is the only permanent checkout of that repository. Work is integrated there, and a single implementation worker for that repository works in it directly.
- **`src/<repo>/worktrees/work-<name>/`** folders are temporary. Each concurrent implementation assignment gets one, on branch `work/<name>` created from the current `dev` commit of that repository. `<name>` is a short slug of the assignment, such as `work/loan-rules` in `src/<repo>/worktrees/work-loan-rules/`. Folder names are branch names with `/` replaced by `-`.
- **`main`** is not checked out. It changes only when the owner merges a pull request on GitHub. Check it out only for a specific need, such as comparing with a release, and remove it afterwards.

`.cursorindexingignore` lists `src/*/worktrees/.bare/`, `src/*/worktrees/work-*/`, and `src/*/worktrees/main/`, so Cursor's search sees one copy of each app. Agents can still open files there when assigned.

## Who does what

- **The branch-manager** is the only role that changes Git state, in the team repository or any app repository. It creates and removes worktrees, commits, merges into `dev`, commits the team repository, and fast-forwards from GitHub when asked. It never pushes, tags, force-updates, rewrites history, or changes remotes.
- **The Coordinator** has the branch-manager create a worktree for each concurrent assignment before dispatch, names the repository and the folder in each assignment, and asks for commits, merges, and cleanup at the points below.
- **Workers** edit only inside the worktree their assignment names, plus project documents they own. They run builds, tests, and previews from that worktree. They may read Git state, such as `git -C src/<repo>/worktrees/dev rev-parse --short HEAD`, but never change it.
- **The owner** pushes each repository, tags candidates, and merges on GitHub.

## Lifecycle of a slice

1. **Start:** when a `work-*` worktree exists, the branch-manager checks for stale worktrees (see Cleanup). Otherwise skip this step.
2. **Assign:** one worker for a repository works in `src/<repo>/worktrees/dev/`. With several assignments in one repository, the branch-manager creates one `work-<name>/` per assignment from the same `dev` commit. The assignment names the repository and the worktree.
3. **Commit,** only when the user asks:
   - The branch-manager commits each worker's changes on its branch and merges it into `dev` with a merge commit. A single worker's changes are committed directly on `dev`.
   - When installed, the app's pre-commit hook runs the agreed deterministic suite on staged files and blocks a failing commit. Report a missing hook rather than claiming coverage. Never bypass it. A rejected commit goes back to the worker that owns the code.
   - If a merge conflicts, the branch-manager leaves the merge in progress in `src/<repo>/worktrees/dev/` and reports the files. The integration worker resolves them there, and the branch-manager completes the merge.
4. **Record:** at a milestone, the audit names the app commit's short hash and subject line, and the agreed version, if any. Verification records acceptance results in testing.md against that commit.
5. **Commit the team repository,** when the user asks: the branch-manager commits assigned pipeline and document changes. App-related documents carry `App-Commit: <short hash>` trailers identifying the relevant repositories; pipeline-only maintenance needs no app trailer.
6. **Clean up:** remove merged worktrees and branches.
7. **Push:** the owner pushes `dev` and the team repository. The branch-manager never pushes; report the commands for the owner.

## Cleanup

- **On merge:** remove the merged worktree with `git worktree remove`, and delete its branch with `git branch -d`.
- **On abandonment:** when an assignment is cancelled or fails, remove its worktree once nothing in it is needed. An unmerged branch is deleted only with the owner's approval; otherwise report it.
- **When a `work-*` worktree exists:** for each `src/*/worktrees/.bare` that exists:
  - run `git worktree list` and `git worktree prune` in that bare clone;
  - report any work worktree or branch that is merged, abandoned, or older than the current task;
  - remove the merged ones.
- **`main`:** remove any `main` checkout when its purpose is done.

## Setting up a repository

When assigned, the branch-manager sets up one repository that has no `src/<repo>/worktrees/` yet. Do not change an existing remote.

1. **Ignore files:** `.gitignore` contains `/src/`. The leading slash keeps `.cursor/skills/tasks/worktrees/` tracked. `.cursorindexingignore` contains the duplicate-checkout entries above.
2. **Clone:**

```text
git clone --bare <url> src/<repo>/worktrees/.bare
git -C src/<repo>/worktrees/.bare config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
git -C src/<repo>/worktrees/.bare fetch origin
git -C src/<repo>/worktrees/.bare worktree add ../dev dev
git -C src/<repo>/worktrees/.bare config core.hooksPath .githooks
```

   The last line enables the repository's pre-commit hook, which runs the unit suite on every commit. Skip it for a repository without `.githooks/`.

   Add `dev` from `main` when `dev` does not exist: `git -C src/<repo>/worktrees/.bare worktree add -b dev ../dev origin/main`.
3. **New app, no URL yet:** initialise `src/<repo>/worktrees/.bare` as a bare repository with `main` as the default branch. Create the first commit through a temporary worktree, add `src/<repo>/worktrees/dev` on `dev`, and remove the temporary worktree. Report the URL the owner must create.
4. **Report:** the worktree list, the `dev` commit, and anything the owner must create on GitHub.
