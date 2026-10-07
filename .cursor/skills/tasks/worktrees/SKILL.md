---
name: worktrees
description: The project workspace layout — a team repository holding Pipeline and the project documents, with the app repository's branches checked out as worktrees inside it — and how worktrees are created, committed, verified, merged into dev, and cleaned up. Read before any work that touches files or Git.
---

# Work in the team repository and its worktrees

Cursor opens the project's **team repository**, named `<app>-team`. It holds Pipeline, the working rules, TEAM.md, and the project documents. The app's own repository lives inside it under `worktrees/`, which the team repository ignores.

```text
<app>-team/                team repository (Cursor opens this)
  .cursor/                 Pipeline
  AGENTS.md                project working rules
  TEAM.md                  for the outside team that handles and tests commits
  .project/documents/      PITCH, INTERFACE, SYSTEMS, TASK, PLAN, TODO, TESTING, audits, archive, devlog
  .project/presentation/   generated images and prompts
  .gitignore               includes worktrees/
  .cursorindexingignore    keeps duplicate checkouts out of Cursor's index
  worktrees/               app repository, ignored by the team repository
    .bare/                 bare clone of the app repository
    dev/                   permanent worktree on branch dev
    work-<name>/           temporary worktree on branch work/<name>
```

## Two repositories

- **The team repository** versions everything except the app: Pipeline, AGENTS.md, TEAM.md, and the project documents. Pushed to GitHub as `<app>-team`, it gives an outside team everything it needs to read.
- **The app repository** holds only the app: source, tests, README, `.github/workflows/`, and its own configuration. Never put Pipeline files or project documents in it.

Paths such as `.project/documents/` are relative to the team repository's root. App paths are relative to a worktree, such as `worktrees/dev/src/`. Record the app repository's URL in AGENTS.md so a fresh clone of the team repository can recreate `worktrees/`.

## Worktrees

- **`worktrees/.bare/`** is a bare clone. It holds the app's history without checking out a copy.
- **`worktrees/dev/`** is the only permanent checkout. Work is integrated there, and a single implementation worker works in it directly.
- **`worktrees/work-<name>/`** folders are temporary. Each concurrent implementation assignment gets one, on branch `work/<name>` created from the current `dev` commit. `<name>` is a short slug of the assignment, such as `work/loan-rules` in `worktrees/work-loan-rules/`. Folder names are branch names with `/` replaced by `-`.
- **`main`** is not checked out. It changes only when the owner merges a pull request on GitHub. Check it out only for a specific need, such as comparing with a release, and remove it afterwards.

`.cursorindexingignore` lists `worktrees/.bare/`, `worktrees/work-*/`, and `worktrees/main/`, so Cursor's search sees one copy of the app. Agents can still open files there when assigned.

## Who does what

- **The branch-manager** is the only role that changes Git state, in either repository. It creates and removes worktrees, commits, merges into `dev`, commits the team repository, and fast-forwards from GitHub when asked. It never pushes, tags, force-updates, or rewrites history.
- **The Coordinator** has the branch-manager create a worktree for each concurrent assignment before dispatch, names the folder in each assignment, and asks for commits, merges, and cleanup at the points below.
- **Workers** edit only inside the worktree their assignment names, plus project documents they own. They run builds, tests, and previews from that worktree. They may read Git state, such as `git -C worktrees/dev rev-parse --short HEAD`, but never change it.
- **The owner** pushes both repositories, tags candidates, and merges on GitHub.

## Lifecycle of a slice

1. **Start:** the branch-manager checks for stale worktrees (see Cleanup).
2. **Assign:** one worker works in `worktrees/dev/`. With several, the branch-manager creates one `work-<name>/` per assignment from the same `dev` commit.
3. **Commit:**
   - Before any app commit, the README is revisited against the change.
   - The branch-manager commits each worker's changes on its branch and merges it into `dev` with a merge commit. A single worker's changes are committed directly on `dev`.
   - If a merge conflicts, the branch-manager leaves the merge in progress in `worktrees/dev/` and reports the files. The integration worker resolves them there, and the branch-manager completes the merge.
4. **Verify the commit:** Verification checks the resulting `dev` commit with a clean working tree, so its evidence names an exact commit. A failure is fixed in a new commit, with the README revisited first, and verified again.
5. **Record:** the audit names the verified app commit's short hash and subject line, and the version. The coverage record in TESTING.md uses the same commit.
6. **Commit the team repository:** the branch-manager commits the documents, including the audit, with an `App-Commit: <short hash>` trailer naming the verified app commit.
7. **Clean up:** remove merged worktrees and branches.
8. **Push:** the owner pushes `dev` and the team repository.

## Cleanup

- **On merge:** remove the merged worktree with `git worktree remove`, and delete its branch with `git branch -d`.
- **On abandonment:** when an assignment is cancelled or fails, remove its worktree once nothing in it is needed. An unmerged branch is deleted only with the owner's approval; otherwise report it.
- **At the start of each task:**
  - run `git worktree list` and `git worktree prune`;
  - report any work worktree or branch that is merged, abandoned, or older than the current task;
  - remove the merged ones.
- **`main`:** remove any `main` checkout when its purpose is done.

## Setting up the workspace

When assigned, the branch-manager sets up a team repository that has no `worktrees/` yet:

1. **Ignore files:** make sure `.gitignore` contains `worktrees/` and `.cursorindexingignore` contains the duplicate-checkout entries above.
2. **Existing app repository:**
   - `git clone --bare <url> worktrees/.bare`, then set `remote.origin.fetch` to `+refs/heads/*:refs/remotes/origin/*` and fetch;
   - add `worktrees/dev` on branch `dev`, creating it from `main` if it does not exist.
3. **New app:** initialise `worktrees/.bare` as a bare repository with `main` as the default branch. Create the first commit through a temporary worktree, add `worktrees/dev` on `dev`, and remove the temporary worktree.
4. **Report:** anything the owner must create on GitHub, such as the two repositories, and the app repository URL to record in AGENTS.md.
