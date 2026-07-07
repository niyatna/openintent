# Profile distribution git verification

Session signal: Galih asked to sync curated Galyarder hot memory into the profile distribution repo, then commit and push only after proving no runtime state or secrets were included.

## Lesson

For profile-distribution work, a successful `git push` is not enough evidence. Verify three layers before claiming completion:

1. profile files are internally consistent;
2. staged repo content excludes runtime/private state;
3. pushed remote equals local `HEAD` after a fetch.

## Checklist

Before commit:

- Stage only intended files, not `git add .` by habit.
- Inspect staged names with `git diff --cached --name-status`.
- Check staged diff stats with `git diff --cached --stat`.
- Scan staged paths for forbidden runtime state patterns: env files, auth files, session/log/cache dirs, runtime DBs, gateway/process state, provider state, browser state, private backups.
- Scan staged text for obvious secret-like patterns.
- If copying profile hot memory, verify curated memory fits configured limits and compatibility mirrors are strip-equal when mirrors are present.

After push:

- Fetch the pushed branch.
- Compare local `HEAD` with the remote branch head.
- Require a clean branch status relative to upstream before saying “clean vs origin”.

## Report shape

Keep the user-facing summary concise:

- files/classes of files changed;
- verification results (`forbidden runtime paths: none`, `secret-like scan: none`, limit checks passed);
- commit hash and subject;
- remote branch equality evidence.

Do not paste full sensitive scans or long memory contents into chat unless the user asks.
