# Using Codex Review Across Repos

1. **Expose the runner on your PATH**
   ```bash
   ln -s ~/projects/codex-review/bin/codex-review ~/.local/bin/codex-review
   ```
   (Or add `~/projects/codex-review/bin` to your shell `PATH`.)

2. **Ensure each target repo has policy files**
   Copy the `.codex-review/` directory into the project or add it as a submodule. The runner now exports `CODEX_HOME` to that folder so `codex exec` reads `AGENTS.md`, rubrics, templates, etc.

3. **Run a review**
   ```bash
   codex-review            # staged diff
   codex-review origin/main # compare against a base branch
   ```
   Reports land in `var/reviews/` inside the repo.

4. **Gate pushes (optional)**
   Link the pre-push hook:
   ```bash
   ln -s ../../codex-review/bin/pre-push .git/hooks/pre-push
   ```
   Update the base branch in the hook if your default is not `origin/main`.

5. **Troubleshooting**
   - If `codex` is missing, install or alias the CLI first.
   - For missing base refs, pass a local ref (`codex-review main`).
   - To inspect the prompt, read `var/_codex_input/prompt.txt`.

Smoke-test by editing a file in a scratch repo, staging the change, and running `codex-review`; confirm `var/reviews/*.md` prints findings and the exit status reflects gating.
