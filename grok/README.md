# Grok release tester

These files set up a Grok Bot as an outside release tester for apps built with Pipeline. The bot tests the app, not Pipeline. It works from the app repository alone: the README, TESTING.md, and the project documents. It never needs the `.cursor/` payload.

The skills here are the reviewed source text. Copy them into Grok's skill library; do not edit them only in Grok. Grok Bot is in beta, and the details below come from third-party guides checked in October 2026. Confirm them in a first trial.

## How it fits

1. A `dev` commit is tagged `<version>-candidate.<n>`.
2. The project's candidate workflow pins it to `candidate/<tag>` and opens a "Release test" issue that mentions and assigns the tester's GitHub account.
3. A Grok routine on that GitHub event runs `/release-test` with the issue. A manual `/release-test <repository> <tag>` in chat does the same.
4. Passed: the bot opens a pull request from `candidate/<tag>` to `main` with its report and closes the issue. Blocked: it posts the report on the issue and adds the `blocked` label.
5. You review and merge.

## Setup

- **One bot.** Name it something like "Release Tester". All bots on an account share one VM, files, and logins, so a second bot adds interference, not isolation.
- **A separate Grok account if possible**, so the VM holds no unrelated logins.
- **A GitHub account for the bot**, added to each app repository with a fine-grained token: Contents read, Pull requests read and write, Issues read and write. No push or admin access. Enter it through Grok's secure credential input, never in chat.
- **Branch protection on `main` and `dev`**, so only you merge.
- **The repository variable `RELEASE_TESTER`** set to the bot's GitHub login.
- **Grok approval rules:** "Always allow" only for opening pull requests, commenting on issues, and labelling issues in your app repositories. Leave everything else on Grok's default approval.
- **No other secrets** on the bot's VM, such as Pipeline's image-generation key.
- **One routine:** a GitHub-event trigger on issues assigned to the bot or mentioning it, running `/release-test`. Check whether Grok can filter by the `release-test` label; if not, the skill ignores other issues.

## Skills

- [release-test](skills/release-test.md) coordinates one run and writes the report.
- [fresh-install](skills/fresh-install.md) installs the app from the documents alone.
- [journey-test](skills/journey-test.md) works through the user journeys in a browser.
- [upgrade-test](skills/upgrade-test.md) checks that stored data survives an upgrade.

Release testing uses real usage allowance. It runs only when a candidate is tagged, once per candidate commit.
