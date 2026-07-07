# Authenticated X status GraphQL extraction fallback — 2026-05-30

Use this when an X/Twitter status URL must be read exactly, but normal browser tools, `web_extract`, or `yt-dlp` do not return the tweet body.

## Trigger

A user shares a status link such as:

```text
https://x.com/i/status/<tweet_id>
```

Observed failure modes:

- `web_extract` returns little or only a linked page summary.
- `yt-dlp` follows the linked URL instead of the tweet and extracts unrelated website videos.
- Plain HTML fetch shows X app shell and empty `entities.tweets` state.

## Read-only fallback flow

1. Load saved account cookies from the appropriate agent X store:

```text
/home/galyarder/.hermes/private/credentials/agents/<agent>/x/cookies.json
```

2. Fetch the status page with those cookies and a normal web User-Agent.
3. Extract the current `main.<hash>.js` script URL from the page.
4. Fetch that JS and extract:
   - current bearer token (`Bearer ...`)
   - `TweetResultByRestId` query id
   - feature switch list / field toggles from the same operation block
5. Read `ct0` from cookies.
6. Call:

```text
https://x.com/i/api/graphql/<query_id>/TweetResultByRestId?variables=...&features=...&fieldToggles=...
```

with headers:

```text
authorization: <bearer from current main JS>
x-csrf-token: <ct0 cookie>
x-twitter-active-user: yes
x-twitter-auth-type: OAuth2Session
x-twitter-client-language: en
referer: https://x.com/i/status/<tweet_id>
cookie: <cookie header>
user-agent: <same browser-like UA>
```

Minimum variables shape that worked:

```json
{"tweetId":"<tweet_id>","withCommunity":false,"includePromotedContent":false,"withVoice":false}
```

7. Parse:
   - author: `result.core.user_results.result.core.name` + `screen_name`
   - text: `result.legacy.full_text`
   - timestamp: `result.legacy.created_at`
   - expanded URLs: `result.legacy.entities.urls[].expanded_url`
   - media: `result.legacy.extended_entities.media[]` or `entities.media[]`
   - metrics: favorites/retweets/replies/quotes/bookmarks
8. If media is image-based proof or contains commands/logs/UI, run vision/OCR on each `media_url_https` before summarizing.

## Session example

Tweet `2060230364057260128` initially caused `yt-dlp` to extract the linked `modal.com` website, not the tweet. The GraphQL fallback returned the actual tweet by `@direkturcrypto`, including text about getting `24 PRL` using Modal free credit, repo link `github.com/direkturcrypto/modal-pearl`, and three media images.

Follow-up checks found the linked repo's `akoya_modal.py` uses Modal to run `registry.akoyapool.com/akoya-miner:latest`, and Modal Terms prohibit cryptocurrency mining / blockchain-related activities. Final judgment: technically plausible, but account/payment-risky and not suitable for a main account.

## Pitfall

Do not hardcode the old web bearer token or query id. X rotates web bundles. Extract both from the live `main.<hash>.js` for the current page/session.

Do not print raw cookies, `auth_token`, `ct0`, or full bearer token in user-facing output.
