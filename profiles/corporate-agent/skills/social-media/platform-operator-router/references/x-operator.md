# Reference: platform-operator-router

# X Operator

## Default first move: reuse session

For X tasks, do **not** start with login. Try saved cookies/session first.

Fast route:

1. Load `~/.hermes/private/credentials/agents/<agent>/x/cookies.json` or dedicated profile.
2. Open `https://x.com/home` in Camofox persistent profile first; use CloakBrowser as fallback if needed.
3. If home/composer/profile owner-state appears, skip login.
4. If login gate appears, open `https://x.com/i/flow/login`, login/TOTP, save cookies, retest.

## Absolute rule

For Owner's dedicated agent-owned X/Twitter accounts, workflow is **Camofox persistent profile first** for account operation. CloakBrowser is legacy/fallback only while proven scripts remain CloakBrowser-based or Camofox is blocked. No official API-first, no platform-operator-router route, no Hermes native browser, no random Brave route.

Public/destructive actions require exact Owner approval unless he gave exact action in current turn. Never print secrets/cookies/token files.

## Account/session paths

```text
~/.hermes/private/credentials/agents/<agent>/x/account.txt
~/.hermes/private/credentials/agents/<agent>/x/cookies.json
~/.hermes/private/credentials/agents/<agent>/x/backup-codes.txt
~/.hermes/private/browser-profiles/agents/<agent>/x-camofox/
~/.hermes/private/browser-profiles/agents/<agent>/x-cloakbrowser/  # legacy fallback
```

Entrypoints:

- Home: `https://x.com/home`
- Login fallback: `https://x.com/i/flow/login`
- Profile verify: `https://x.com/<username>`

## Frontend platform access

Use the direct frontend. Do not rediscover X every run.

Observed owner-state via CloakBrowser cookie probe:

- URL: `https://x.com/home`
- title examples: `Home / X`, `X`
- visible controls: `Home`, `Search and explore`, `Notifications`, `Direct Messages`/`Chat`, `Grok`, `Bookmarks`, `Premium`, `Profile`, `More`, `Post`
- composer/input: `Post text`; media upload is visible as input type `file` when composer is present
- caveat: X may show transient `Something went wrong` after a successful post; profile/status verification wins

## Frontend CRUD

### Create

- Post:
  1. Open `https://x.com/home`.
  2. Click home composer or `Post` button.
  3. Fill textbox with aria/placeholder `Post text` or the active composer textbox.
  4. Attach media through the visible file input when needed.
  5. Verify media preview before posting.
  6. Click `Post` once.
  7. Verify status URL/profile item with exact text/media.
- Reply: open target post -> `Reply` -> exact text/media -> verify preview -> `Reply` -> verify reply visible.
- DM: only with explicit approval and target verification.

### Read

- Session read: `https://x.com/home` with owner controls (`Home`, `Profile`, `Post`, `Grok`, `Premium`).
- Post read: status URL, text/media/handle/time.
- Notification/DM read only with explicit scope.

#### Authenticated post extraction fallback

When browser REST/CDP is unavailable or logged-out extraction only returns app shell/metadata, use the X web GraphQL route with saved cookies as a read-only fallback:

1. Fetch the status page with saved X cookies and current web User-Agent.
2. Extract current `main.<hash>.js` from the HTML.
3. Extract the bearer token from that JS (`Bearer ...`) and the `TweetResultByRestId` query id/feature list from the same bundle.
4. Read `ct0` from cookies and call `https://x.com/i/api/graphql/<queryId>/TweetResultByRestId` with `authorization`, `x-csrf-token`, `x-twitter-auth-type: OAuth2Session`, `x-twitter-active-user: yes`, `x-twitter-client-language`, `referer`, and the same cookie header.
5. Parse `legacy.full_text`, expanded URLs, media URLs, author, timestamp, and metrics from JSON.
6. If the tweet has images that contain important text, run image/vision OCR on the `pbs.twimg.com/media/...` assets before summarizing or judging.

Do not treat `web_extract` or `yt-dlp` redirects to linked websites as proof of tweet content; X status links may redirect/fallback to linked pages. For source-grounded answers, verify the tweet JSON/status content itself.

### Update

X editing may be unavailable depending account/subscription. If edit is not clearly available/verifiable, delete + repost only after approval.

### Delete

Open status URL -> owner `More` menu -> Delete -> confirm -> verify profile/status absence. Destructive; require explicit approval unless Owner explicitly ordered cleanup.

### Interactions

Like, repost, quote, follow/unfollow, reply, DM are public actions; require exact approval and verify final visible state. Follow-back must handle `Follow back`, not only generic `Follow`.

## Login fallback

1. Open `https://x.com/i/flow/login`.
2. Fill username/email/phone as requested from account file.
3. Fill password.
4. If X asks for extra identifier, use username/email metadata.
5. If TOTP appears, generate locally; backup code only after approval.
6. Verify account identity by profile/username.
7. Save/update cookies; rerun owner-state check.

## Common X caveat

X can show transient `Something went wrong` after successful post. Verify profile/status URL before assuming failure.

Reference detail: `references/authenticated-x-status-graphql-extraction-2026-05-30.md` documents the read-only authenticated GraphQL fallback for exact tweet/status extraction when browser or generic extractors return only app shell or linked-page content. `references/x-status-readonly-extraction-session-2026-05-31.md` gives a concrete session example, including media OCR, for a microstock tutorial tweet.

## User-facing report

- Success: `live: <url>`
- Reuse success: `cookies/session active; no login needed.`
- Blocked: `blocker: <one gate>. stopped before wrong public action.`