# Reference: platform-operator-router

# Instagram Operator

## Speed-first execution contract

Default route is direct Camofox persistent-profile frontend execution from a saved session. CloakBrowser is a legacy/fallback route while existing proven scripts are still CloakBrowser-based or Camofox is blocked. No UI discovery while holding a live/public action.

Fast path:

1. Pick target account: `co-founder` or `default`; use only that account's Instagram paths.
2. Reuse cookies/persistent profile first; password login is fallback only.
3. Open Instagram home/profile as owner; prove owner-state before touching public actions.
4. Execute the requested CRUD path directly with known controls/selectors below.
5. Hard gate before public action: owner-state + media preview when media exists + exact caption/profile field value + correct original-post menu.
6. Verify final live state from profile/permalink before saying done.

Stop rule: if owner-state is absent, media preview is absent, caption counter stays `0/2,200`, a modal blocks Share/Create, or the visible menu is not the original post menu, stop before posting/deleting. Patch/reference the trap, then retry. Do not live-post first and repair later unless Owner explicitly asks for emergency repair.

Runtime: if using legacy CloakBrowser scripts, prefer Node v24 (`~/.hermes/.nvm/versions/node/v24.15.0/bin/node`) when using `camoufox-js`; Node v26 can break native modules such as `better-sqlite3`.

## Default first move: reuse session

For Instagram tasks, do **not** start with password login. Try saved cookies/session first, then login only if owner-state fails.

Fast route:

1. Load account/cookie state from `~/.hermes/private/credentials/agents/<agent>/instagram/`.
2. Open the dedicated Camofox persistent profile first; use CloakBrowser cookie import only as fallback.
3. Open `https://www.instagram.com/` or `https://www.instagram.com/accounts/login/`.
4. If owner controls appear (`Create`, `Messages`, `Edit profile`, `View archive`, profile/account switcher), skip login.
5. If login gate remains, do Camofox login/TOTP first; use CloakBrowser login/TOTP fallback only if Camofox is blocked, then save/update cookies and retest owner-state.

## Absolute rule

For Owner's dedicated agent-owned Instagram accounts, the workflow is **Camofox persistent profile first** for login/upload/posting. CloakBrowser is legacy/fallback only while proven scripts remain CloakBrowser-based or Camofox is blocked. No API-first route. No Hermes native browser. No random Brave route.

Public/destructive actions require exact Owner approval unless he gave exact action in the current turn. Never print secrets/cookies/tokens.

## Account/session paths

```text
~/.hermes/private/credentials/agents/<agent>/instagram/account.txt
~/.hermes/private/credentials/agents/<agent>/instagram/cookies.json
~/.hermes/private/credentials/agents/<agent>/instagram/backup-codes.txt
~/.hermes/private/browser-profiles/agents/<agent>/instagram-camofox/
~/.hermes/private/browser-profiles/agents/<agent>/instagram-cloakbrowser/  # legacy fallback
```

Known handles:

- Co-Founder: `co-founder`
- Default: `yourcompany`

Entrypoints:

- Login/session: `https://www.instagram.com/accounts/login/`
- Home: `https://www.instagram.com/`
- Profile verify: `https://www.instagram.com/<username>/`

## Frontend platform access

Use these direct frontend surfaces; do not waste time rediscovering navigation.

- Home/composer surface: `https://www.instagram.com/`
- Login/session fallback: `https://www.instagram.com/accounts/login/`
- Owner profile: `https://www.instagram.com/<username>/`
- Post permalink: `https://www.instagram.com/<username>/p/<shortcode>/` or returned live URL
- Reels permalink: `https://www.instagram.com/reel/<shortcode>/`

Known owner-state controls:

- `Create` / left-sidebar plus / DOM text like `New postCreate`
- observed CloakBrowser controls: `Instagram`, `Home`, `Reels`, `Messages`, `Search`, `Explore`, `Notifications`, `New post`, `Settings`
- Default business account may also show `Professional dashboard`
- `Edit profile`
- `View archive`
- account switcher / logged-in navigation

Known blockers to clear fast:

- `Turn on Notifications` -> click `Not Now`
- `Save login info` -> usually `Not now` unless Owner requested persistence change
- compact sidebar icon-only -> use the plus/Create icon, not text search

## Frontend CRUD

### Create post/media

Fastest safe create route:

1. Prove owner-state.
2. Clear notification/save-login modals with `Not Now` if they cover the UI.
3. Click Create/New post/left-sidebar plus.
4. Attach media through the frontend file input/file chooser.
5. Wait for crop/edit screen and visible media preview.
6. Use default crop/settings unless Owner specified otherwise.
7. Click Next/Continue to caption stage.
8. Fill only the create-dialog caption textbox. Preferred selector pattern: `[role="dialog"] [role="textbox"][aria-label="Write a caption..."]`.
9. Verify exact caption text is inside that field. If the visible counter is still `0/2,200`, the caption is in the wrong place: stop, refocus the real field, and re-fill.
10. Verify media preview still visible.
11. Click Share/Post.
12. Verify final permalink/profile: handle + media + exact caption.

No preview = no post. `Post shared` toast is not proof.

### Read

- Session read: fresh owner-state controls, not cookie-file existence.
- Profile read: `https://www.instagram.com/<username>/`.
- Post read: exact permalink; verify handle, caption, media, timestamp/header, URL.
- Inbox/DM read only with explicit scope.

### Update / repair

- Caption/profile edits only with explicit scope.
- Caption repair route:
  1. Open exact authenticated post permalink.
  2. Click the original post `More options` menu.
  3. Choose `Edit`.
  4. In edit dialog, fill `[role="dialog"][aria-label="Edit info"] [role="textbox"][aria-label="Write a caption..."]`.
  5. Verify field value exactly before `Done`.
  6. Verify final permalink caption.
- Media replacement is delete/archive + repost; verify final state.
- Bio/avatar/privacy changes require explicit approval and profile verification.

### Delete / archive

1. Open exact post/reel permalink as owner.
2. Use the original post menu, not comment/reply/menu from another object.
3. Prefer Archive for non-destructive cleanup; delete only with explicit approval or exact current-turn instruction.
4. Confirm the action.
5. Verify profile absence/archive result. For delete, profile feed absence is stronger proof than a possibly cached permalink.

### Interactions

Like, comment, follow/unfollow, DM, story reactions, and profile changes are public actions. Execute only with exact approval and verify visible state.

## Login fallback

1. Open `https://www.instagram.com/accounts/login/`.
2. Fill username/email and password from private account file.
3. If fields do not fill, inspect DOM or use focus-order typing.
4. If TOTP appears, generate locally; backup code only with approval.
5. Handle `Save login info` / notifications prompts conservatively (`Not now`) unless Owner specified otherwise.
6. Save/update cookies; rerun owner-state check.

## References

- `references/instagram-cloakbrowser-posting-caption-edit-2026-05-18.md` — live Co-Founder Instagram posting lesson: compact Create control, notification modal, media preview, caption field targeting, and owner-menu caption repair.

## User-facing report

- Success: `live: <permalink>`
- Reuse success: `cookies/session active; no login needed.`
- Blocked: `blocker: <one gate>. stopped before wrong public action.`