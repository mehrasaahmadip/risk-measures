# Skill: github-push

Push the current project to a new or existing GitHub repository.

## When to invoke
Use `/github-push public <repo-name>` or `/github-push private <repo-name>` to create a GitHub repository and push the current project to it.

## Input
- `public` or `private` — repository visibility
- `<repo-name>` — name for the GitHub repository (e.g. `risk-measures`)

## Steps

1. **Check authentication** — run `gh auth status`. If not logged in, tell the user to run `gh auth login` and stop.

2. **Check if remote already exists** — run `git remote -v`. If `origin` already points to GitHub, skip to step 5.

3. **Create the GitHub repository** — run:
   ```
   gh repo create <repo-name> --<visibility> --source=. --remote=origin --description "<description>"
   ```
   Use the project's README first line as the description if available.

4. **Verify remote was set** — run `git remote -v` to confirm `origin` is now set.

5. **Stage and commit any uncommitted changes** — run `git status`. If there are untracked or modified files, ask the user which files to include before staging. Never use `git add .` blindly.

6. **Push** — run `git push -u origin main`. If the branch is not `main`, use the current branch name.

7. **Report** — print the repository URL from `gh repo view --json url`.

## Error handling
- If `gh` is not installed: tell the user to run `brew install gh` then `gh auth login`.
- If the repo name already exists on GitHub: ask the user to choose a different name or confirm pushing to the existing repo.
- Never force push without explicit user confirmation.

## Output
The GitHub repository URL, ready to share or add to the README.
