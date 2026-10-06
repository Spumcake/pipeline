---
name: journey-test
description: Work through an app's selected user journeys in a browser as a first-time user, comparing behavior with its acceptance criteria and interface design and capturing evidence.
---

# Journey test

Use the running app from the fresh install. Work through each selected journey from TESTING.md as a first-time user with the goal it describes.

For each journey:

1. Read its goal, the TASK acceptance criteria it links, and the INTERFACE flow or views it names. Note what must be observable.
2. Pursue the goal through the interface the way a newcomer would. Do not read source code or use routes the interface does not offer. Note where you hesitated, backtracked, or could not find the next step.
3. Try the failure cases the criteria describe, such as a refused double booking or an invalid date. Confirm the app refuses and keeps the earlier state.
4. Compare what you see with INTERFACE's description of those views and states, and with its journey images when present.
5. Take a screenshot at each meaningful state, and capture console errors.

Classify each result:

- **Pass:** the goal was achieved and every observable outcome in the criteria held.
- **Fail (blocking):** the goal could not be achieved, a criterion's outcome did not hold, data was lost or wrong, or the app broke with an error the user can see.
- **Advisory:** the goal was achieved, but with confusion, unclear wording, or visible differences from INTERFACE.
- **Not tested:** say why.

Keep each journey's data separate where TESTING.md says to, and do not repeat a journey that already passed. Return the result for each journey with criterion IDs, evidence paths, and advisory notes.
