---
name: fresh-install
description: Install and start an app from a fresh clone using only its README and testing documents, recording every step, guess, and gap.
---

# Fresh install

Act as a newcomer with a clean machine and only the repository. The question is whether the documents alone get someone from clone to a running app.

1. Read the README's quick start and install sections, and the install and test-data notes in TESTING.md. Do not read source code to work out how to install; that is the gap you are testing for.
2. Check the stated prerequisites. Install missing system tools only if the README tells the reader to; record each one.
3. Follow the steps exactly as written, in order. Record every command and its outcome.
4. When a step fails or is unclear, record it, then make the smallest reasonable attempt to continue and mark that step as a guess. A guess means the documents were not enough.
5. Load the test data TESTING.md names, into isolated storage only.
6. Confirm the app is running the way the README says: the address or command and what you should see. Take a screenshot.

Result:

- **Pass:** started using the documents alone, with no guesses.
- **Pass with notes:** started, but needed guesses or found inaccuracies. List each one as advisory, unless TESTING.md says otherwise.
- **Blocking failure:** could not start the app even with reasonable guesses. Include the step, the error, and what the documents said.

Return the steps, commands, guesses, screenshots, and the address or command the journeys should use. Leave the app running for the next skill.
