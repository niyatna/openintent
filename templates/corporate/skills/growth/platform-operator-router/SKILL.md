---
name: platform-operator-router
description: Use when executing automated postings to X, Threads, or Instagram, using the platform-operator-router API utility, managing community engagement, or writing-plansning email automation.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [platform, platform-operator-router, platform-operator-router, platform-operator-router, platform-operator-router, platform-operator-router, email-marketing]
    category: growth
---

# Platform Operator Router

## Absolute rule

For Galih's dedicated agent-owned platform accounts, the route is **CloakBrowser persistent profile first**.

Camofox/Camoufox is legacy/fallback only when CloakBrowser is blocked or a platform-specific skill still has a verified Camofox-only CRUD flow. No official API route for social account operation unless a platform skill explicitly names it as the chosen route. No Hermes native browser. No random Brave. No “API-first” reasoning.

Mandatory pattern:

```text
platform-specific operator → agent-accounts → cloakbrowser-browser → CloakBrowser persistent profile/frontend/login/OAuth → verify → act → verify live
```

The point of each platform skill is to capture actual frontend mechanics: which URL opens, where username/password goes, when to generate TOTP, when backup codes are allowed, where the composer/upload button is, how to attach media, what preview must appear, and how to verify the result.

## Mandatory routing table

| Platform/task | Load first | Execution route |
|---|---|---|
| Threads login/post/repost/delete/media | `platform-operator-router` first | Prefer CloakBrowser persistent profile when the platform flow is verified; use existing Camofox CRUD only while the operator skill remains Camofox-verified |
| Instagram login/post/reel/story/media | `platform-operator-router` first | Prefer CloakBrowser persistent profile when the platform flow is verified; use existing Camofox CRUD only while the operator skill remains Camofox-verified |
| X/Twitter login/post/reply/DM/media | `platform-operator-router` first | Prefer CloakBrowser persistent profile when the platform flow is verified; use existing Camofox CRUD only while the operator skill remains Camofox-verified |
| Google login/OAuth | `google-workspace` first | Existing auth/session check first; CloakBrowser credential/TOTP login/OAuth only if needed; Camofox fallback if CloakBrowser is blocked |
| Gmail/Calendar/Drive/Docs/Sheets after CloakBrowser auth | `google-workspace` + `google-workspace` | `gws` may execute after live auth is healthy |
| Generic dedicated account login/TOTP/cookies | `agent-accounts` + `cloakbrowser-browser` | Private account files + CloakBrowser persistent profile/session |
| Browser route troubleshooting | `browser-routing` | Select CloakBrowser first for owned-agent accounts; fall back only with evidence |

## Fast execution sequence

1. Identify platform and action type.
2. Load the platform operator skill first; load `agent-accounts` and `cloakbrowser-browser` as support. Load `camofox-browser` only for a legacy/fallback flow.
3. Run the platform operator's default session-reuse smoke script when it exists. If no platform-specific script exists, run this router probe:

```bash
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/platform_frontend_probe.py --agent keiya --platform threads
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/platform_frontend_probe.py --agent keiya --platform instagram
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/platform_frontend_probe.py --agent galyarder --platform x
python /home/galyarder/.hermes/profiles/galyarder/skills/growth/platform-operator-router/scripts/platform_frontend_probe.py --agent galyarder --platform google
```

4. If status is `owner-state` or `cookies-active`, do not login. Execute frontend CRUD directly.
5. If reuse fails, run the platform login/OAuth fallback, save/update cookies, then rerun the smoke/probe.
6. For public or destructive actions, confirm scope unless Galih already gave the exact action in this turn.
7. For media post: attach file and verify composer preview before posting.
8. Verify live result on profile/permalink or in the authorized API/tool layer.
9. Patch the platform skill with any new frontend labels/selectors/failure modes.

## Verified frontend owner-state map

Read-only browser probes verified these surfaces for both Keiya and Galyarder where credentials/cookies exist:

| Platform | Direct URL | Owner-state controls | Fast create/control |
|---|---|---|---|
| Threads | `https://www.threads.com/` after cookie import from `https://www.threads.com/login` | `Threads`, `For you`, `New thread`, `Search`, `Activity`/`Messages`, `Notifications`, `Profile`, `Insights`, `Saved`, `Edit` | `New thread` or composer text `What's new?`, then `Post` |
| Instagram | `https://www.instagram.com/` | `Instagram`, `Home`, `Reels`, `Messages`, `Search`, `Explore`, `Notifications`, `New post`, `Professional dashboard` when business account | `New post` / Create sidebar icon; caption textbox inside create dialog |
| X/Twitter | `https://x.com/home` | `Home`, `Notifications`, `Direct Messages`/`Chat`, `Grok`, `Bookmarks`, `Premium`, `Profile`, `Post` | composer on home or `Post`; textbox aria `Post text`; media input type `file` |
| Google Account | `https://myaccount.google.com/` | `Akun Google`, account avatar, `Info pribadi`, `Keamanan & login`, `Data & privasi`, `Aplikasi Google` | Google login/OAuth only; after auth use `gws` for Workspace CRUD |

The router probe is read-only and sanitized: imports `cookies.json` or uses the persistent profile, opens one frontend URL, records visible controls/input labels, then closes the browser session. It must not print cookies, password, TOTP, backup codes, tokens, localStorage, or sessionStorage.

## Stop conditions

Stop instead of improvising when:

- CloakBrowser cannot open or hold the logged-in session and the Camofox fallback is also blocked/unverified;
- the platform asks for CAPTCHA/anti-abuse intervention;
- TOTP fails twice and backup-code use is not approved;
- required media cannot be attached or preview cannot be verified;
- the action is public/destructive and approval is missing;
- a credential/token/cookie would have to be printed into chat.

## Browser boundary

- CloakBrowser persistent profile is the primary isolated browser for dedicated agent-owned accounts.
- Camofox is legacy/fallback only when CloakBrowser is blocked or the platform skill still has a verified Camofox-only flow.
- Hermes native browser is not the route for these account operations.
- Brave CDP is Galih's real human browser; do not use it for agent-owned account automation unless Galih explicitly overrides the architecture.

## Skill maintenance rule

If a platform flow is slow, failed, or Galih had to explain a step, patch the platform-specific skill immediately with the exact correction. Do not write another vague generic router note.

## References

- `references/threads-first-post-media-failure-2026-05-17.md` — session lesson: Threads media-required post failed because Camofox frontend media attach/preview was not verified and a text-only post went live.
- `references/camofox-credential-frontend-correction-2026-05-17.md` — historical correction: agent-owned platform accounts must use isolated credential/frontend workflows, not API/native-browser drift. Superseded for primary browser choice by the current CloakBrowser-first rule.
- `references/frontend-probe-before-skill-update-2026-05-18.md` — session correction: before patching platform operator skills, probe the live frontend with cookies/Camofox and record real controls, not hypotheses.

## Common mistakes

- Treating Camofox as primary after CloakBrowser persistent profiles became the owned-agent default.
- Saying official API/API-first for agent-owned social account operation.
- Opening Hermes native browser instead of CloakBrowser/Camofox.
- Treating `platform-operator-router` as the answer to an X credential/browser-profile task.
- Treating `gws` as the Google login route instead of CloakBrowser login/OAuth, then gws after auth.
- Writing or patching platform skills from hypothesis instead of probing the live frontend first.
- Treating a vague instruction like “use browser automation” as enough; the skill must say which URL/control/textbox/menu to use.
- Posting before media preview verification.

## User-facing reporting

For Galih, report only route and result/blocker:

- `route: CloakBrowser Threads. blocker: media preview belum bisa diverifikasi.`
- `route: CloakBrowser Google OAuth. status: login berhasil, gws auth healthy.`
- `route: CloakBrowser Instagram. live: <url>`

## References & Sub-playbooks
- `references/platform-operator-router.md` — Twitter/X CLI posting protocols and platform-operator-router utility
- `references/platform-operator-router.md` — Threads posting parameters and workflow details
- `references/platform-operator-router.md` — Instagram visual assets workflows
- `references/platform-operator-router.md` — Meta sso tokens, cookies, and TOTP gateways
- `references/platform-operator-router.md` — Email automated workflows and deliverability rules
- `references/platform-operator-router.md` — Viral referral loops and invites programs
- `references/platform-operator-router.md` — Audience conversation engagement strategies
