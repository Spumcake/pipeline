# Pipeline

Pipeline is a set of Cursor agents, rules, and skills that take a software idea from a short brief through specification, design, and incremental implementation. A coordinator splits the work into small tasks, each with limited context, a clear owner, and checks.

## Quick start

From your project's root, copy in the `.cursor/` folder:

```sh
pipeline_checkout="$(mktemp -d)"
git clone --depth 1 --filter=blob:none --sparse https://github.com/Spumcake/Pipeline.git "$pipeline_checkout"
git -C "$pipeline_checkout" sparse-checkout set .cursor
mkdir -p .cursor
cp -Ri "$pipeline_checkout/.cursor/." .cursor/
```

## Usage

Open the project in Cursor and start an Agent chat. Then send these briefs in order. Wait for each to finish before sending the next.

1. **Ask the agent how it would approach your idea.** Describe the app in your own words: who it is for, what they need to do, where it runs, and what it should not do. Optionally, also ask what team you would need to handle and test its commits. That team can be people, a team of agents, automated services, or a mix.

   ```text
   @coordinator I want <your app: who uses it, what they need to do, where it runs, and anything it must not include>. How would you approach building this?
   ```

   Optionally add:

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

4. **Discuss the scope with the agent.** Talk through what you want built and what the finished app looks like. The agent uses this conversation as context for the next briefs.

5. **Ask the agent to recommend a vertical slice.**

   ```text
   @coordinator Based on our existing specifications, recommend the next vertical slice that I can try myself. Explain what that slice would let me do, what it depends on, and how we would know it works. Explain what subagents and skills you'd use. Keep this conversational. Don't create or edit files or begin implementation yet.
   ```

6. **Ask the agent for a plan and todo list.**

   ```text
   @coordinator Review the decisions recorded in the devlogs (if available) and our existing specifications to create an implementation plan and a short, prioritized todo list. Start with the agreed vertical slice, make its completion criteria clear, and keep later work broad. Don't implement anything yet; flag any consequential gaps rather than inventing decisions.
   ```

7. **Ask the agent to implement the slice.**

   ```text
   @coordinator Implement the agreed vertical slice from our plan, using the available agents and working rules. Verify its completion criteria and leave it runnable with clear instructions so I can try it. Use concurrent implementation workers where the slice has independent parts, with clear ownership and an integration step. Update the todos, plan status, and audit with what actually happened, then stop before starting the next slice.
   ```

Try the slice, then repeat the last three briefs for each slice that follows.
