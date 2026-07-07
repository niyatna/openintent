# Local Hermes update plus desktop rebuild verification

## Trigger

Use when Galih asks to update a local Hermes checkout for upstream features and rebuild the Electron desktop app.

## Durable lesson

Do not recommend blind `hermes update` when local patches may exist. Use preserve-then-update, then verify both the core CLI/runtime and the desktop artifact before reporting completion.

## Verification sequence

1. Ground source state before mutation: version, branch, remotes, worktrees, dirty files, and ahead/behind against `upstream/main`.
2. Snapshot before mutation: timestamped backup directory, pre-update state, dirty/staged diffs, untracked inventory/tar when needed, git bundle, and backup branch.
3. Build an integration branch from latest `upstream/main`; reapply Galih's local deltas as explicit local-preserve commits.
4. Verify the requested upstream feature. For `/learn`, check the prompt-builder/source surfaces and run `tests/agent/test_learn_prompt.py`; smoke `build_learn_prompt()` and confirm the generated prompt mentions `/learn` and `skill_manage`.
5. Run focused tests covering preserved local patches and any test adjusted during the rebase.
6. Rebuild desktop with `hermes desktop --build-only --force-build`.
7. Verify desktop artifacts:
   - `apps/desktop/release/linux-unpacked/Hermes` exists and is executable.
   - `apps/desktop/build/install-stamp.json` and `apps/desktop/release/linux-unpacked/resources/install-stamp.json` match `HEAD`.
   - install stamp has `dirty: false`.
   - `git status --short --branch` is clean.

## Pitfalls

- Desktop build can mutate `package-lock.json`. If the first build stamp says `dirty: true`, do not report final success. Inspect/commit the legitimate lockfile change, then rebuild until the stamp is clean.
- A gateway restart from inside a gateway-served chat may be blocked by Hermes' self-restart guard, even if wrapped in a scheduled command. Report `code updated / desktop rebuilt / gateway not restarted` and give an outside-shell restart command rather than implying runtime cutover.
- If version status still says behind after moving to latest upstream, clear stale `.update_check` cache and rerun version before reporting.
- If a preserved local test fails after rebase, compare the test against current upstream behavior before changing production code. When upstream legitimately supports broader behavior, adapt the local test rather than narrowing implementation.
