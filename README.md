# Pipeline

Pipeline is a set of Cursor agents, rules, and skills that take a software idea from a short brief through specification, design, and incremental implementation. A coordinator splits the work into small tasks, each with limited context, a clear owner, and checks.

## Quick start

Pipeline works in a `worktrees/` folder that holds one folder per branch of your app. Create it and copy in the `.cursor/` folder:

```sh
mkdir -p <project>/worktrees && cd <project>/worktrees
pipeline_checkout="$(mktemp -d)"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Spumcake/Pipeline.git "$pipeline_checkout"
git -C "$pipeline_checkout" sparse-checkout set .cursor
mkdir -p .cursor
cp -Ri "$pipeline_checkout/.cursor/." .cursor/
```

If your app already has a repository, clone it into `worktrees/main`. Otherwise the agent creates one. Pipeline keeps its files and your project documents outside the app's branches, with the documents in their own repository at `worktrees/.project`.

## Usage

Open the `worktrees/` folder in Cursor and start an Agent chat. Send each brief and wait for it to finish before sending the next.

### Preparation

1. **Ask the agent how it would approach your idea.** Describe the app in your own words: who it is for, what they need to do, where it runs, and what it should not do.

   ```text
   @coordinator I want <your app: who uses it, what they need to do, where it runs, and anything it must not include>. How would you approach building this?
   ```

   Optionally add the question below. The team handles and tests commits, and can be people, a team of agents, automated services, or a mix.

   ```text
   What team would be necessary to build this?
   ```

2. **Ask the agent to prepare for implementation.**

   ```text
   @coordinator Go ahead and complete the preparation needed to make this ready for implementation, using the available roles. Reuse existing work, resolve what you can, and ask me only about decisions that genuinely need my input. Stop before writing application code, and summarize what's ready and anything still blocking implementation.
   ```

3. **Ask the agent for images of the user journey (optional).**

   ```text
   @coordinator Generate a series of images showing the app's main user journey, using our existing project documents and bootstrap images. I want to see how the screens and important interaction states connect, with a consistent visual design. Don't implement the app.
   ```

---

### Working with an agent team

These steps set up an agent team, such as Grok Bot, to handle and test your commits from GitHub. Skip them if you test on your own. If there is no code to check yet, come back here after the first slice.

1. **Ask the agent to set up the team's side of the project.**

   ```text
   @coordinator Set up version control and integration for an outside team that handles and tests our commits. Agree the version with me, have the roles prepare TESTING.md and the every-commit and candidate workflows, and write TEAM.md. Tell me what I need to set up in GitHub.
   ```

2. **Push both repositories to GitHub:** the app repository, with `main` and `dev`, and the project documents repository in `worktrees/.project`. Then make the GitHub settings the agent listed.

3. **Create a GitHub token** for the team: a fine-grained token limited to the app and project documents repositories, with the permissions listed in TEAM.md.

4. **Give the token to the bots as an environment variable.** In Grok Bot, say "I need an environment variable" and enter `GH_TOKEN` in the masked input it returns. Never paste the token into a chat.

5. **Ask a bot to build the team.**

   ```text
   Clone <app repository URL> and <project documents repository URL>, read TEAM.md in the project documents repository, and create the bots, skills, and routines needed to fill the roles it describes. Use GH_TOKEN for GitHub. Tell me what else you need from me, then show me how each role will work before it acts on its own.
   ```

---

### Implementation

1. **Discuss the scope with the agent.** Talk through what you want built and what the finished app looks like. The agent uses this conversation as context for the next briefs.

2. **Ask the agent to recommend a vertical slice.**

   ```text
   @coordinator Based on our existing specifications, recommend the next vertical slice that I can try myself. Explain what that slice would let me do, what it depends on, and how we would know it works. Explain what subagents and skills you'd use. Keep this conversational. Don't create or edit files or begin implementation yet.
   ```

3. **Ask the agent for a plan and todo list.**

   ```text
   @coordinator Review the decisions recorded in the devlogs (if available) and our existing specifications to create an implementation plan and a short, prioritized todo list. Start with the agreed vertical slice, make its completion criteria clear, and keep later work broad. Don't implement anything yet; flag any consequential gaps rather than inventing decisions.
   ```

4. **Ask the agent to implement the slice.**

   ```text
   @coordinator Implement the agreed vertical slice from our plan, using the available agents and working rules. Verify its completion criteria and leave it runnable with clear instructions so I can try it. Use concurrent implementation workers where the slice has independent parts, with clear ownership and an integration step. Update the todos, plan status, and audit with what actually happened, then stop before starting the next slice.
   ```

5. **Try the slice, then push `dev` and the project documents.** The agents commit locally; you push. If you have a team, it checks every commit and opens a `ci-failure` issue when checks fail.

6. **Tag a release candidate when the agent recommends one.** Run the tag commands it gives you. The team tests that commit and opens a pull request to `main` for you to review and merge, or labels the request `blocked` with its report. Ask the agent to record the result.

Repeat steps 2 to 6 for each slice that follows.
