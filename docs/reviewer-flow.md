# Codex Review Agent Flow

The diagram below shows how the current Codex review runner orchestrates a review when `bin/codex-review` is invoked.

```mermaid
graph TD
    A["Run bin/codex-review (optional base ref)"] --> B["Load .codex-review/config.toml"]
    B --> C{"Staged changes?"}
    C --> D["Collect staged file list and diff"]
    C --> E["Fetch remotes"]
    E --> F["Compute merge-base HEAD vs base"]
    F --> G["Diff merge-base to HEAD and collect files"]
    D --> H["Write meta JSON (branch, SHA, timestamp)"]
    G --> H
    H --> I["Read library docs"]
    I --> J["Render review prompt"]
    J --> K["Call codex exec"]
    K --> L["Persist raw output and split JSON/Markdown"]
    L --> M["Store reports under var/reviews"]
    M --> N{"Gate triggered?"}
    N --> O["Exit 2 and block caller"]
    N --> P["Print report paths and exit 0"]
```

## Key Notes
- The runner reads `.codex-review/config.toml` and bundled guidance documents to inject reviewer expectations into the prompt.
- Staged changes are reviewed directly. Otherwise it fetches remotes, enforces a valid `git merge-base`, and builds diffs relative to the configured base branch.
- The assembled diff, metadata, and library excerpts are combined with `.codex-review/templates/review.exec.md` before invoking `codex exec`.
- Raw model output plus parsed Markdown/JSON reports are saved under `var/` for traceability.
- Priority/severity checks enforce policy before returning control to invoking hooks such as the pre-push script.

Update this document whenever the pipeline changes to keep reviewers aligned on the execution path.
