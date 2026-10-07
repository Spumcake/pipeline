---
name: worktrees
description: The project workspace layout — Pipeline and project documents outside the app's branches, each branch in its own folder — and how worktrees are created, assigned, committed, merged into dev, and removed. Read before any work that touches files or Git.
---

# Work in the worktrees layout

Cursor opens the project's `worktrees/` folder. Pipeline and the project documents live there, outside the app's branches. Each branch of the app repository is checked out in its own folder beside them.

```text
worktrees/                 workspace root, not itself a repository
  .cursor/                 Pipeline
  AGENTS.md                project working rules
  .project/                project documents repository
    TEAM.md
    documents/             PITCH, INTERFACE, SYSTEMS, TASK, PLAN, TODO, TESTING, audits, archive, devlog
    presentation/, models/ generated images and prompts
  main/                    app repository, branch main
  dev/                     app repository, branch dev
  work-<name>/             app repository, branch work/<name>
```

## Two repositories

- **The app repository** holds only the app: source, tests, README, `.github/workflows/`, and the app's own configuration. Never put Pipeline files or project documents in it.
- **The project documents repository** is `worktrees/.project/`, a separate git repository with one branch, `main`. It is pushed to GitHub separately, so an outside team can read TEAM.md, TESTING.md, and the other documents.
- **`.cursor/` and AGENTS.md** belong to neither repository. They stay in the workspace.

Paths written as `.project/documents/...` are relative to the workspace root. App paths are relative to a branch folder, such as `dev/src/...`.

## Branch folders

- **`main/`** holds released code. Nobody edits it; it changes only by fast-forwarding from GitHub after the owner merges.
- **`dev/`** is where work is integrated, and where a single implementation worker works directly.
- **`work-<name>/`** folders are temporary. Each concurrent implementation assignment gets one, on branch `work/<name>` created from the current `dev`. `<name>` is a short slug of the assignment, such as `work/loan-rules`, in folder `work-loan-rules/`.

Folder names are branch names with `/` replaced by `-`.

## Who does what

- **The branch-manager** is the only role that runs Git commands that change state, in either repository. It creates and removes worktrees, commits, merges into `dev`, and fast-forwards `main` and `dev` from GitHub when asked. It never pushes, tags, force-updates, or rewrites history.
- **The Coordinator** asks the branch-manager for a worktree before dispatching each concurrent assignment, and names that folder in the assignment. It asks the branch-manager to commit and merge each finished assignment, and to commit the project documents at the end of a task.
- **Workers** edit only inside the branch folder they are assigned, plus any project documents they own. They run builds, tests, and previews from that folder. They may read Git state, for example `git -C dev rev-parse --short HEAD`, but never change it.
- **The owner** pushes both repositories, tags candidates, and merges on GitHub.

## Lifecycle of a slice

1. With one worker, it works in `dev/`. With several, the branch-manager creates one `work-<name>/` per assignment from the same `dev` commit.
2. Each worker finishes and returns. The branch-manager commits its changes on its branch.
3. The branch-manager merges each work branch into `dev` with a merge commit. If a merge conflicts, it leaves the merge in progress in `dev/` and reports the files. The integration worker resolves them in `dev/`, then the branch-manager completes the merge.
4. After verification, the README revisit, and any documentation updates, the branch-manager commits remaining changes in `dev/` and commits the project documents in `.project/`.
5. The branch-manager removes merged work folders and their local branches.
6. The owner pushes `dev` and the project documents.

## Setting up a new workspace

If `worktrees/` has no app repository yet, the branch-manager can do the following when assigned:

- clone the owner's repository into `main/`, or initialise one there with branch `main`;
- add `dev/` as a worktree on branch `dev`;
- initialise `.project/` as its own repository if it is not one.

It reports anything the owner must create on GitHub, such as the two remote repositories.
