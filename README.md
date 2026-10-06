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

Open the project in Cursor, start an Agent chat, attach `@coordinator`, and describe what you want.
