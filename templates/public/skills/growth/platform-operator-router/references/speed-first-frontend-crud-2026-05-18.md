# Threads speed-first frontend CRUD flow — 2026-05-18

Purpose: preserve the fastest verified Threads execution route after a successful Keiya media-post repair session.

## Proven final-state pattern

A bad post can require cleanup before final success:

1. old text-only post deleted,
2. wrong uppercase/media post deleted,
3. final lowercase + media post created,
4. final permalink verified live.

Report shape Galih accepted:

```text
done.

Final live:
<threads permalink>

Old text-only deleted.
Uppercase media post deleted.
Final post lowercase + media visible.
```

## Fastest create path

1. Choose exact agent (`keiya` or `galyarder`).
2. Run only that account's smoke:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/threads_cookie_reuse_smoke.py --agent keiya
```

3. If `cookies-active`, open `https://www.threads.com/` and do not login.
4. Confirm owner-state controls: `New thread`, `What's new?`, `Post`, `Insights`, `Saved`, `Profile`.
5. Click `New thread` / composer.
6. Paste exact caption text.
7. Attach media through the frontend file input/file chooser using the local absolute path.
8. Wait for thumbnail/preview. If preview is missing, do not post.
9. Click `Post` once.
10. Verify exact permalink/profile feed: caption casing, media visible, correct account.

## CRUD map

### Create

- Entry: `https://www.threads.com/`
- Control: `New thread` or composer `What's new?`
- Publish: `Post`
- Gate: media preview before post; permalink/profile after post.

### Read

- Owner/session read: smoke + owner-state controls.
- Profile read: `https://www.threads.com/@<username>` after auth.
- Exact post read: permalink.
- Evidence: URL, handle, exact caption, media visible/count, timestamp/header if visible.

### Update

- Treat caption/media mistakes as delete + repost unless a real edit path is clearly visible and final state can be verified.
- Media update is delete + repost.
- Profile/bio/avatar/privacy changes require explicit approval and post-save verification.

### Delete

1. Open exact permalink while authenticated.
2. Use the **original post** `More` menu.
3. Correct menu contains `Insights`, `Pin to profile`, `Reply options`, `Delete`.
4. Wrong menu clue: `Pin reply`, `Hide for everyone`, reply-scoped options.
5. Click `Delete`, confirm.
6. Verify absence on profile feed. Deleted permalink behavior can be misleading, so feed absence wins.

### Interactions

Replies, repost/rethread, likes, follows/unfollows, DMs, and profile changes are public actions. Execute only with exact current-turn approval. Verify visible final state.

## Speed rules

- Do not rediscover the frontend on every run.
- Do not open the public profile before cookie proof.
- Do not run both accounts if the task names one account.
- Do not explain the whole process to Galih; execute and report live URL/blocker.
- If a wrong public artifact exists, clean it only if deletion is within the user's explicit instruction or current correction context.
