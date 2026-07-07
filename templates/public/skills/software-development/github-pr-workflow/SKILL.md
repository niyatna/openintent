---
name: github-pr-workflow
description: Use when executing Git operations, submitting repository Pull Requests, checking github-pr-workflow feedback, or debugging API payloads.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [dev, git, pull-request, github-issues, github-pr-workflow, api-debugging]
    category: software-development
---

# GitHub Workflow

Complete guide for working with GitHub: authentication, repository management, issues, pull requests, code review, and CI/CD. Each section shows the `gh` CLI way first, then the `git` + `curl` API fallback for machines without `gh`.

This umbrella skill consolidates what were previously five separate skills into one class-level resource. Use the references for detailed procedures.

---

## Table of Contents

1. [Authentication](#authentication) — Setup, tokens, SSH, gh CLI
2. [Repository Management](#repository-management) — Clone, create, fork, settings
3. [Issues](#issues) — Create, triage, label, search
4. [Pull Request Lifecycle](#pull-request-lifecycle) — Branch, commit, open, merge
5. [Code Review](#code-review) — Review process, inline comments, approval
6. [Repository Analysis](#repository-analysis) — Codebase inspection (LOC, languages) using pygount
7. [Quick Reference](#quick-reference) — Command cheatsheet

---

## Repository Analysis

**Full guide:** [references/codegraph-codebase-analysis.md](references/codegraph-codebase-analysis.md)

Quick syntax:
```bash
# Language summary + LOC count
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,dist,build" \
  .
```

Always skip dependency dirs to avoid hangs. Check `references/codegraph-codebase-analysis.md` for more configuration options and output formats.

---

## Authentication

**Full guide:** [references/auth.md](references/auth.md)

Quick detection pattern used throughout this skill:

```bash
# Determine which method to use
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
elif command -v gh &>/dev/null && [ -n "${GH_TOKEN:-${GITHUB_TOKEN:-}}" ] \
  && GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}" gh api user --jq .login >/dev/null 2>&1; then
  export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
  AUTH="gh-env"
else
  AUTH="git"
  # Fall back to curl with GITHUB_TOKEN
fi
```

**Key points:**
- HTTPS tokens or SSH keys for git operations
- `gh` CLI for richer GitHub API access
- Token can be in `GITHUB_TOKEN` env var, `~/.hermes/.env`, or git credentials
- Never ask user to `gh auth login` until env token path is tested

**Common setup:**
```bash
# Option 1: gh CLI
gh auth login

# Option 2: Git credential store with personal access token
git config --global credential.helper store
# Then do any git operation and enter username + token when prompted

# Option 3: SSH
ssh-keygen -t ed25519 -C "email@example.com"
# Add public key to GitHub settings
```

See [references/auth.md](references/auth.md) for troubleshooting, multiple accounts, and detailed procedures.

---

## Repository Management

**Full guide:** [references/repo-management.md](references/repo-management.md)

**Cloning:**
```bash
git clone https://github.com/owner/repo.git
# or: gh repo clone owner/repo
```

**Creating:**
```bash
gh repo create my-project --public --clone
# or via API: curl -X POST .../user/repos
```

**Forking:**
```bash
gh repo fork owner/repo --clone
# or via API: curl -X POST .../repos/owner/repo/forks
```

**Other operations:**
- Repository settings (visibility, features, branch protection)
- Secrets management
- Releases and tags
- GitHub Actions workflows
- Gists

See [references/repo-management.md](references/repo-management.md) for complete procedures.

---

## Issues

**Full guide:** [references/issues.md](references/issues.md)

**Creating:**
```bash
gh issue create --title "..." --body "..." --label "bug"
# or: curl -X POST .../repos/owner/repo/issues -d '{...}'
```

**Viewing:**
```bash
gh issue list
gh issue list --label "bug" --state open
gh issue view 42
```

**Managing:**
```bash
gh issue edit 42 --add-label "priority:high"
gh issue comment 42 --body "..."
gh issue close 42
```

**Templates** available:
- `templates/bug-report.md`
- `templates/feature-request.md`

See [references/issues.md](references/issues.md) for triage workflow, bulk operations, and API examples.

---

## Pull Request Lifecycle

This is the core PR workflow that most developers follow daily.

### 1. Branch Creation

```bash
git fetch origin
git checkout main && git pull origin main
git checkout -b feat/add-authentication
```

Branch naming: `feat/`, `fix/`, `refactor/`, `docs/`, `ci/`

### 2. Making Commits

Use file tools (`write_file`, `patch`) to make changes, then:

```bash
git add src/auth.py tests/test_auth.py
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add auth middleware
- Add unit tests"
```

### 3. Pushing and Creating PR

```bash
git push -u origin HEAD
```

**With gh:**
```bash
gh pr create \
  --title "feat: add JWT-based user authentication" \
  --body-file /tmp/pr-body.md
```

Use `--body-file` for multiline Markdown to avoid shell quoting issues.

**With curl:**
```bash
BRANCH=$(git branch --show-current)
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{
    \"title\": \"feat: add JWT-based user authentication\",
    \"body\": \"...\",
    \"head\": \"$BRANCH\",
    \"base\": \"main\"
  }"
```

**Templates** available:
- `templates/pr-body-feature.md`
- `templates/pr-body-bugfix.md`

### 4. Monitoring CI

**With gh:**
```bash
gh pr checks          # One-shot
gh pr checks --watch  # Poll every 10s
```

**With curl:**
```bash
SHA=$(git rev-parse HEAD)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status
```

See [references/ci-troubleshooting.md](references/ci-troubleshooting.md) for auto-fix loop patterns.

### 5. Merging

**With gh:**
```bash
gh pr merge --squash --delete-branch
# or: gh pr merge --auto --squash --delete-branch
```

**With curl:**
```bash
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d '{"merge_method": "squash"}'
```

Merge methods: `"merge"` (merge commit), `"squash"`, `"rebase"`

### Complete Example

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug

# 3. (Agent makes code changes)

# 4. Commit
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login"

# 5. Push
git push -u origin HEAD

# 6. Create PR
gh pr create --title "..." --body-file /tmp/pr-body.md

# 7. Monitor CI
gh pr checks --watch

# 8. Merge when green
gh pr merge --squash --delete-branch
```

---

## Code Review

**Full guide:** [references/code-review.md](references/code-review.md)

### Reviewing Local Changes (Pre-Push)

```bash
# Get the diff
git diff main...HEAD
git diff main...HEAD --stat

# Check for common issues
git diff main...HEAD | grep -n "print(\|console\.log\|TODO"
git diff main...HEAD | grep -in "password\|secret\|api_key"
```

### Reviewing a PR on GitHub

**Check out locally:**
```bash
git fetch origin pull/123/head:pr-123
git checkout pr-123
# Now use read_file, search_files, run tests
```

**Leave comments:**
```bash
# General comment
gh pr comment 123 --body "Looks good overall, a few suggestions."

# Inline comments (via API)
gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="Use list comprehension here" \
  -f path="src/auth.py" \
  -f commit_id="$HEAD_SHA" \
  -f line=45
```

**Submit review:**
```bash
# Approve
gh pr review 123 --approve --body "LGTM"

# Request changes
gh pr review 123 --request-changes --body "See inline comments"
```

### Review Checklist

**Correctness:**
- Logic errors, edge cases, null handling
- Input validation
- Error handling

**Security:**
- SQL injection, XSS, CSRF
- Auth/authz bypasses
- Secrets in code
- Unsafe deserialization

**Code Quality:**
- DRY violations, complexity
- Naming, readability
- Dead code

**Testing:**
- Test playwright-pro for new code
- Edge cases tested

**Documentation:**
- Comments for complex logic
- README updates
- API docs

See [references/code-review.md](references/code-review.md) for the complete 7-step review process and output templates.

---

## Quick Reference

| Action | gh | git + curl |
|--------|-----|-----------|
| **Auth** |
| Login | `gh auth login` | Token in `~/.git-credentials` or SSH |
| **Repos** |
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r` |
| Create | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` |
| **Issues** |
| List | `gh issue list` | `curl GET /repos/o/r/issues` |
| Create | `gh issue create --title ...` | `curl POST /repos/o/r/issues` |
| Comment | `gh issue comment N --body ...` | `curl POST /repos/o/r/issues/N/comments` |
| Close | `gh issue close N` | `curl PATCH /repos/o/r/issues/N` |
| **PRs** |
| Create | `gh pr create --title ...` | `curl POST /repos/o/r/pulls` |
| List | `gh pr list` | `curl GET /repos/o/r/pulls` |
| View | `gh pr view N` | `curl GET /repos/o/r/pulls/N` |
| Check out | `gh pr checkout N` | `git fetch origin pull/N/head:pr-N` |
| Checks | `gh pr checks` | `curl GET /repos/o/r/commits/SHA/status` |
| Merge | `gh pr merge --squash` | `curl PUT /repos/o/r/pulls/N/merge` |
| Comment | `gh pr comment N --body ...` | `curl POST /repos/o/r/issues/N/comments` |
| **Review** |
| Approve | `gh pr review N --approve` | `curl POST /repos/o/r/pulls/N/reviews` |
| Request changes | `gh pr review N --request-changes` | `curl POST /repos/o/r/pulls/N/reviews` |

---

## Related References

- [references/auth.md](references/auth.md) — Complete auth setup guide
- [references/repo-management.md](references/repo-management.md) — Repository operations
- [references/issues.md](references/issues.md) — Issue management
- [references/code-review.md](references/code-review.md) — Review procedures
- [references/ci-troubleshooting.md](references/ci-troubleshooting.md) — CI debugging
- [references/conventional-commits.md](references/conventional-commits.md) — Commit message format
- [references/profile-home-auth-and-pr-body.md](references/profile-home-auth-and-pr-body.md) — Profile/home pitfalls

---

## Pitfalls

- **gh env token first** — if `GH_TOKEN` or `GITHUB_TOKEN` is set, test it with `gh api user` before asking user to `gh auth login`
- **Use --body-file** — avoids shell quoting corruption of Markdown backticks
- **Profile $HOME mismatches** — Hermes profiles may have different `$HOME` than the OS user; see `references/profile-home-auth-and-pr-body.md`
- **PR body corruption** — backticks in PR descriptions can break shell heredocs; always use temp files
- **gh auth status can lie** — even when it fails, an env token may work for `gh pr`, `gh api`, etc.

## References & Sub-playbooks
- `references/github-pr-workflow.md` — Validating PR modifications and regression review tasks
- `references/github-pr-workflow.md` — Querying REST and GraphQL endpoints data layers
