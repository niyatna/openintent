# Scheduled social posting with platform-operator-router

Use when building cron-driven X/Twitter posting from prepared content and media files.

## Position in the stack

For X/Twitter, use `platform-operator-router` as the primary posting adapter when authenticated. Do not automate X through a browser first unless the API is unavailable for the required action.

## Queue file pattern

```yaml
platform: x
account: galyarder_labs
scheduled_at: 2026-05-09T09:00:00+07:00
media:
  - media/launch-demo.mp4
reply_to:
quote:
dry_run: false
---
Post text here.
```

## Cron loop

1. Scan queue files due at or before now.
2. Validate frontmatter, account, media existence, post length, and duplicate status.
3. If media exists, upload media first:
   ```bash
   platform-operator-router media upload path/to/file.png
   ```
4. Post text with uploaded media IDs:
   ```bash
   platform-operator-router post "text" --media-id MEDIA_ID
   ```
5. Save raw JSON response, post ID, URL, timestamp, and queue file hash.
6. Move the content file to `posted/` or `failed/`.
7. Notify Galih through Telegram/home channel.

## Safety rules

- Never read or print `~/.platform-operator-router`.
- Never pass inline secrets or use verbose auth flags.
- Use `platform-operator-router auth status` and `platform-operator-router whoami` for cheap verification only.
- Confirm any new destructive/write action template before enabling it in cron.
- Keep idempotency: a queue file that already has a successful post ID should not post again.

## Failure handling

- Auth failure: ask Galih to re-auth outside the agent session.
- Media processing failure: write failed status with media ID/status output.
- Rate limit: leave in queue or failed/retry state with next retry timestamp.
- Unknown API error: preserve raw JSON and notify, do not loop-post.
