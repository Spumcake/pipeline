---
name: upgrade-test
description: Check that data stored by the previous tested version of an app survives an upgrade to the candidate commit.
---

# Upgrade test

Run only when TESTING.md says the app keeps stored data. Otherwise report "not applicable".

1. From TESTING.md's Candidates, find the previous passed candidate or released version. If there is none, report "first candidate; no upgrade path" and stop.
2. In a separate folder under `/workspace/runs/<tag>/upgrade/`, check out that previous commit and install it following its own README.
3. Load the test data TESTING.md names, then use the app to create a few representative records through the interface, such as one of each main kind and one in a non-default state. Note them and take a screenshot.
4. Stop the old version. Check out the candidate commit in the same folder, keeping the stored data where the README says it lives. Follow the candidate README's upgrade or migration steps, if any.
5. Start the candidate and confirm every noted record is present and correct, and that a new action on old data works.

Data missing, changed, or unreadable after the upgrade is a blocking failure. Steps that the README did not mention but were needed are advisory, or blocking when the upgrade cannot be completed without guessing.

Return the previous version tested, the records checked, the result, and evidence.
