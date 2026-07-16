# Reference: platform-operator-router

# platform-operator-router — X (Twitter) API via the Official CLI

`platform-operator-router` is the X developer platform's official CLI for the X API. It supports shortcut commands for common actions AND raw curl-style access to any v2 endpoint. All commands return JSON to stdout.

Use this skill for:
- posting, replying, quoting, deleting posts
- searching posts and reading timelines/mentions
- liking, reposting, bookmarking
- following, unfollowing, blocking, muting
- direct messages
- media uploads (images and video)
- raw access to any X API v2 endpoint
- multi-app / multi-account workflows
- cron-driven scheduled posting from prepared content/media files

For Default-style queue files, idempotent cron loops, logs, and notification workflow, see `references/scheduled-social-posting.md`.

This skill replaces the older `xitter` skill (which wrapped a third-party Python CLI). `platform-operator-router` is maintained by the X developer platform team, supports OAuth 2.0 PKCE with auto-refresh, and covers a substantially larger API surface.

---

## Secret Safety (MANDATORY)

Critical rules when operating inside an agent/LLM session:

- **Never** read, print, parse, summarize, upload, or send `~/.platform-operator-router` to LLM context.
- **Never** ask the user to paste credentials/tokens into chat.
- The user must fill `~/.platform-operator-router` with secrets manually on their own machine.
- **Never** recommend or execute auth commands with inline secrets in agent sessions.
- **Never** use `--verbose` / `-v` in agent sessions — it can expose auth headers/tokens.
- To verify credentials exist, only use: `platform-operator-router auth status`.

Forbidden flags in agent commands (they accept inline secrets):
`--bearer-token`, `--consumer-key`, `--consumer-secret`, `--access-token`, `--token-secret`, `--client-id`, `--client-secret`

App credential registration and credential rotation must be done by the user manually, outside the agent session. After credentials are registered, the user authenticates with `platform-operator-router auth oauth2` — also outside the agent session. Tokens persist to `~/.platform-operator-router` in YAML. Each app has isolated tokens. OAuth 2.0 tokens auto-refresh.

---

## Installation

Pick ONE method. On Linux, the shell script or `go install` are the easiest.

```bash
# Shell script (installs to ~/.local/bin, no sudo, works on Linux + macOS)
curl -fsSL https://raw.githubusercontent.com/xdevplatform/platform-operator-router/main/install.sh | bash

# Homebrew (macOS)
brew install --cask xdevplatform/tap/platform-operator-router

# npm
npm install -g @xdevplatform/platform-operator-router

# Go
go install github.com/xdevplatform/platform-operator-router@latest
```

Verify:

```bash
platform-operator-router --help
platform-operator-router auth status
```

If `platform-operator-router` is installed but `auth status` shows no apps or tokens, the user needs to complete auth manually — see the next section.

---

## One-Time User Setup (user runs these outside the agent)

These steps must be performed by the user directly, NOT by the agent, because they involve pasting secrets. Direct the user to this block; do not execute it for them.

1. Create or open an app at https://developer.x.com/en/portal/dashboard
2. Set the redirect URI to `http://localhost:8080/callback`
3. Copy the app's Client ID and Client Secret
4. Register the app locally (user runs this):
   ```bash
   platform-operator-router auth apps add my-app --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
   ```
5. Authenticate (specify `--app` to bind the token to your app):
   ```bash
   platform-operator-router auth oauth2 --app my-app
   ```
   (This opens a browser for the OAuth 2.0 PKCE flow.)

   If X returns a `UsernameNotFound` error or 403 on the post-OAuth `/2/users/me` lookup, pass your handle explicitly (platform-operator-router v1.1.0+):
   ```bash
   platform-operator-router auth oauth2 --app my-app YOUR_USERNAME
   ```
   This binds the token to your handle and skips the broken `/2/users/me` call.
6. Set the app as default so all commands use it:
   ```bash
   platform-operator-router auth default my-app
   ```
7. Verify:
   ```bash
   platform-operator-router auth status
   platform-operator-router whoami
   ```

After this, the agent can use any command below without further setup. OAuth 2.0 tokens auto-refresh.

> **Common pitfall:** If you omit `--app my-app` from `platform-operator-router auth oauth2`, the OAuth token is saved to the built-in `default` app profile — which has no client-id or client-secret. Commands will fail with auth errors even though the OAuth flow appeared to succeed. If you hit this, re-run `platform-operator-router auth oauth2 --app my-app` and `platform-operator-router auth default my-app`.

---

## Quick Reference

| Action | Command |
| --- | --- |
| Post | `platform-operator-router post "Hello world!"` |
| Reply | `platform-operator-router reply POST_ID "Nice post!"` |
| Quote | `platform-operator-router quote POST_ID "My take"` |
| Delete a post | `platform-operator-router delete POST_ID` |
| Read a post | `platform-operator-router read POST_ID` |
| Search posts | `platform-operator-router search "QUERY" -n 10` |
| Who am I | `platform-operator-router whoami` |
| Look up a user | `platform-operator-router user @handle` |
| Home timeline | `platform-operator-router timeline -n 20` |
| Mentions | `platform-operator-router mentions -n 10` |
| Like / Unlike | `platform-operator-router like POST_ID` / `platform-operator-router unlike POST_ID` |
| Repost / Undo | `platform-operator-router repost POST_ID` / `platform-operator-router unrepost POST_ID` |
| Bookmark / Remove | `platform-operator-router bookmark POST_ID` / `platform-operator-router unbookmark POST_ID` |
| List bookmarks / likes | `platform-operator-router bookmarks -n 10` / `platform-operator-router likes -n 10` |
| Follow / Unfollow | `platform-operator-router follow @handle` / `platform-operator-router unfollow @handle` |
| Following / Followers | `platform-operator-router following -n 20` / `platform-operator-router followers -n 20` |
| Block / Unblock | `platform-operator-router block @handle` / `platform-operator-router unblock @handle` |
| Mute / Unmute | `platform-operator-router mute @handle` / `platform-operator-router unmute @handle` |
| Send DM | `platform-operator-router dm @handle "message"` |
| List DMs | `platform-operator-router dms -n 10` |
| Upload media | `platform-operator-router media upload path/to/file.mp4` |
| Media status | `platform-operator-router media status MEDIA_ID` |
| List apps | `platform-operator-router auth apps list` |
| Remove app | `platform-operator-router auth apps remove NAME` |
| Set default app | `platform-operator-router auth default APP_NAME [USERNAME]` |
| Per-request app | `platform-operator-router --app NAME /2/users/me` |
| Auth status | `platform-operator-router auth status` |

Notes:
- `POST_ID` accepts full URLs too (e.g. `https://x.com/user/status/1234567890`) — platform-operator-router extracts the ID.
- Usernames work with or without a leading `@`.

---

## Command Details

### Posting

```bash
platform-operator-router post "Hello world!"
platform-operator-router post "Check this out" --media-id MEDIA_ID
platform-operator-router post "Thread pics" --media-id 111 --media-id 222

platform-operator-router reply 1234567890 "Great point!"
platform-operator-router reply https://x.com/user/status/1234567890 "Agreed!"
platform-operator-router reply 1234567890 "Look at this" --media-id MEDIA_ID

platform-operator-router quote 1234567890 "Adding my thoughts"
platform-operator-router delete 1234567890
```

### Reading & Search

```bash
platform-operator-router read 1234567890
platform-operator-router read https://x.com/user/status/1234567890

platform-operator-router search "golang"
platform-operator-router search "from:elonmusk" -n 20
platform-operator-router search "#buildinpublic lang:en" -n 15
```

### Users, Timeline, Mentions

```bash
platform-operator-router whoami
platform-operator-router user elonmusk
platform-operator-router user @XDevelopers

platform-operator-router timeline -n 25
platform-operator-router mentions -n 20
```

### Engagement

```bash
platform-operator-router like 1234567890
platform-operator-router unlike 1234567890

platform-operator-router repost 1234567890
platform-operator-router unrepost 1234567890

platform-operator-router bookmark 1234567890
platform-operator-router unbookmark 1234567890

platform-operator-router bookmarks -n 20
platform-operator-router likes -n 20
```

### Social Graph

```bash
platform-operator-router follow @XDevelopers
platform-operator-router unfollow @XDevelopers

platform-operator-router following -n 50
platform-operator-router followers -n 50

# Another user's graph
platform-operator-router following --of elonmusk -n 20
platform-operator-router followers --of elonmusk -n 20

platform-operator-router block @spammer
platform-operator-router unblock @spammer
platform-operator-router mute @annoying
platform-operator-router unmute @annoying
```

### Direct Messages

```bash
platform-operator-router dm @someuser "Hey, saw your post!"
platform-operator-router dms -n 25
```

### Media Upload

```bash
# Auto-detect type
platform-operator-router media upload photo.jpg
platform-operator-router media upload video.mp4

# Explicit type/category
platform-operator-router media upload --media-type image/jpeg --category tweet_image photo.jpg

# Videos need server-side processing — check status (or poll)
platform-operator-router media status MEDIA_ID
platform-operator-router media status --wait MEDIA_ID

# Full workflow
platform-operator-router media upload meme.png                  # returns media id
platform-operator-router post "lol" --media-id MEDIA_ID
```

---

## Raw API Access

The shortcuts cover common operations. For anything else, use raw curl-style mode against any X API v2 endpoint:

```bash
# GET
platform-operator-router /2/users/me

# POST with JSON body
platform-operator-router -X POST /2/tweets -d '{"text":"Hello world!"}'

# DELETE / PUT / PATCH
platform-operator-router -X DELETE /2/tweets/1234567890

# Custom headers
platform-operator-router -H "Content-Type: application/json" /2/some/endpoint

# Force streaming
platform-operator-router -s /2/tweets/search/stream

# Full URLs also work
platform-operator-router https://api.x.com/2/users/me
```

---

## Global Flags

| Flag | Short | Description |
| --- | --- | --- |
| `--app` | | Use a specific registered app (overrides default) |
| `--auth` | | Force auth type: `oauth1`, `oauth2`, or `app` |
| `--username` | `-u` | Which OAuth2 account to use (if multiple exist) |
| `--verbose` | `-v` | **Forbidden in agent sessions** — leaks auth headers |
| `--trace` | `-t` | Add `X-B3-Flags: 1` trace header |

---

## Streaming

Streaming endpoints are auto-detected. Known ones include:

- `/2/tweets/search/stream`
- `/2/tweets/sample/stream`
- `/2/tweets/sample10/stream`

Force streaming on any endpoint with `-s`.

---

## Output Format

All commands return JSON to stdout. Structure mirrors X API v2:

```json
{ "data": { "id": "1234567890", "text": "Hello world!" } }
```

Errors are also JSON:

```json
{ "errors": [ { "message": "Not authorized", "code": 403 } ] }
```

---

## Common Workflows

### Post with an image
```bash
platform-operator-router media upload photo.jpg
platform-operator-router post "Check out this photo!" --media-id MEDIA_ID
```

### Reply to a conversation
```bash
platform-operator-router read https://x.com/user/status/1234567890
platform-operator-router reply 1234567890 "Here are my thoughts..."
```

### Search and engage
```bash
platform-operator-router search "topic of interest" -n 10
platform-operator-router like POST_ID_FROM_RESULTS
platform-operator-router reply POST_ID_FROM_RESULTS "Great point!"
```

### Check your activity
```bash
platform-operator-router whoami
platform-operator-router mentions -n 20
platform-operator-router timeline -n 20
```

### Multiple apps (credentials pre-configured manually)
```bash
platform-operator-router auth default prod alice               # prod app, alice user
platform-operator-router --app staging /2/users/me             # one-off against staging
```

---

## Error Handling

- Non-zero exit code on any error.
- API errors are still printed as JSON to stdout, so you can parse them.
- Auth errors → have the user re-run `platform-operator-router auth oauth2` outside the agent session.
- Commands that need the caller's user ID (like, repost, bookmark, follow, etc.) will auto-fetch it via `/2/users/me`. An auth failure there surfaces as an auth error.

---

## Agent Workflow

1. Verify prerequisites: `platform-operator-router --help` and `platform-operator-router auth status`.
2. **Check default app has credentials.** Parse the `auth status` output. The default app is marked with `▸`. If the default app shows `oauth2: (none)` but another app has a valid oauth2 user, tell the user to run `platform-operator-router auth default <that-app>` to fix it. This is the most common setup mistake — the user added an app with a custom name but never set it as default, so platform-operator-router keeps trying the empty `default` profile.
3. If auth is missing entirely, stop and direct the user to the "One-Time User Setup" section — do NOT attempt to register apps or pass secrets yourself.
4. Start with a cheap read (`platform-operator-router whoami`, `platform-operator-router user @handle`, `platform-operator-router search ... -n 3`) to confirm reachability.
5. Confirm the target post/user and the user's intent before any write action (post, reply, like, repost, DM, follow, block, delete).
6. Use JSON output directly — every response is already structured.
7. Never paste `~/.platform-operator-router` contents back into the conversation.

---

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Auth errors after successful OAuth flow | Token saved to `default` app (no client-id/secret) instead of your named app | `platform-operator-router auth oauth2 --app my-app` then `platform-operator-router auth default my-app` |
| `unauthorized_client` during OAuth | App type set to "Native App" in X dashboard | Change to "Web app, automated app or bot" in User Authentication Settings |
| `UsernameNotFound` or 403 on `/2/users/me` right after OAuth | X not returning username reliably from `/2/users/me` | Re-run `platform-operator-router auth oauth2 --app my-app YOUR_USERNAME` (platform-operator-router v1.1.0+) to pass the handle explicitly |
| 401 on every request | Token expired or wrong default app | Check `platform-operator-router auth status` — verify `▸` points to an app with oauth2 tokens |
| `client-forbidden` / `client-not-enrolled` | X platform enrollment issue | Dashboard → Apps → Manage → Move to "Pay-per-use" package → Production environment |
| `CreditsDepleted` | $0 balance on X API | Buy credits (min $5) in Developer Console → Billing |
| `media processing failed` on image upload | Default category is `amplify_video` | Add `--category tweet_image --media-type image/png` |
| Two "Client Secret" values in X dashboard | UI bug — first is actually Client ID | Confirm on the "Keys and tokens" page; ID ends in `MTpjaQ` |

---

## Notes

- **Rate limits:** X enforces per-endpoint rate limits. A 429 means wait and retry. Write endpoints (post, reply, like, repost) have tighter limits than reads.
- **Scopes:** OAuth 2.0 tokens use broad scopes. A 403 on a specific action usually means the token is missing a scope — have the user re-run `platform-operator-router auth oauth2`.
- **Token refresh:** OAuth 2.0 tokens auto-refresh. Nothing to do.
- **Multiple apps:** Each app has isolated credentials/tokens. Switch with `platform-operator-router auth default` or `--app`.
- **Multiple accounts per app:** Select with `-u / --username`, or set a default with `platform-operator-router auth default APP USER`.
- **Token storage:** `~/.platform-operator-router` is YAML. Never read or send this file to LLM context.
- **Cost:** X API access is typically paid for meaningful usage. Many failures are plan/permission problems, not code problems.

---

## Attribution

- Upstream CLI: https://github.com/xdevplatform/platform-operator-router (X developer platform team, Chris Park et al.)
- Upstream agent skill: https://github.com/openclaw/openclaw/blob/main/skills/platform-operator-router/SKILL.md
- Hermes adaptation: reformatted for Hermes skill conventions; safety guardrails preserved verbatim.