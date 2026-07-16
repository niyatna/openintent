# X status read-only extraction session — 2026-05-31

Use this as an example of extracting a user-shared X status link when public metadata and video tools are not enough.

## Trigger

User shared:

```text
https://x.com/i/status/2056703191409131705
```

The task was source reading, not public posting.

## What failed or was insufficient

- `web_extract` can return little useful tweet body for X status pages.
- `yt-dlp` may say no video or only handle media, not tweet text. In this case it returned: `No video could be found in this tweet`.
- Browser automation may be unavailable if the configured browser backend is not running. Do not turn that into a durable negative claim; use authenticated read-only fallback when cookies exist.

## Working pattern

Use the existing `platform-operator-router` authenticated GraphQL fallback:

1. Load saved X cookies for the relevant owned-agent account.
2. Build a Cookie header from X/Twitter cookies and read `ct0` for CSRF.
3. Fetch `https://x.com/i/status/<id>` with a normal browser user-agent.
4. Extract the current `main.<hash>.js` bundle URL from the HTML.
5. Fetch that JS and extract:
   - current web bearer token;
   - `TweetResultByRestId` query id;
   - `featureSwitches` and `fieldToggles` near the operation block.
6. Call `https://x.com/i/api/graphql/<queryId>/TweetResultByRestId` with:
   - `authorization: Bearer ...`;
   - `x-csrf-token: <ct0>`;
   - `x-twitter-auth-type: OAuth2Session`;
   - `x-twitter-active-user: yes`;
   - `x-twitter-client-language: en`;
   - same cookies and a status-page referer.
7. Parse `legacy.full_text`, author, timestamps, metrics, expanded URLs, and media.
8. If the tweet includes image media, OCR/vision the image before summarizing.

## Sanitization rule

Do not print cookies, `auth_token`, `ct0`, or full bearer tokens. It is acceptable to report `cookies_loaded`, `ct0 present`, query id, tweet text, metrics, and media URLs when non-secret.

## Example result from this session

Tweet `2056703191409131705` resolved to:

- author: `oji` / `@OjiAntto`
- created: `Tue May 19 11:47:07 +0000 2026`
- text: tutorial about making motion graphic footage that sells on microstock; mentions `40K+ views` and step-by-step from zero to upload.
- visible metrics during extraction: `41` likes, `14` reposts, `1` reply, `1` quote, `79` bookmarks.
- media: one image at `pbs.twimg.com/media/...jpg`.

Vision/OCR on the media extracted the thumbnail text:

```text
PASSIVE
INCOME
DARI
FOTO
VIDEO
FOOTAGE
ANIMASI
MOTION GRAPHIC
MICROSTOCK TUTORIAL
```

## Response lesson

For X links that are used as strategic evidence, do not stop at tweet text when the attached image carries the value proposition. Extract both tweet body and media OCR, then connect to the user's current strategy only after the source is grounded.
