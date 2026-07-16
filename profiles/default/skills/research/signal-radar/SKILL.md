---
name: signal-radar
description: Use when checking real-time social sentiment signals on Reddit/X (signal-radar), querying Polymarket prediction prices, or managing signal routers.
version: 2.1.0
author: Company
license: MIT
metadata:
  hermes:
    tags: [research, signals, signal-radar, social-search, signal-radar, signal-radar]
    category: research
---

# Signal Radar

## Role

Signal Radar is the local Default/Co-Founder research route over the vendor `signal-radar` engine.

Use this instead of loading `signal-radar` directly for normal work. `signal-radar` stays installed as the engine; Signal Radar owns our routing, account boundaries, browser choice, and OmniRoute web-search layer.

## When to Use

Use for:

- “what are people saying lately about X?”
- market/competitor/trend/social signal scans;
- community consensus across Reddit, HN, YouTube, GitHub, Polymarket;
- read-only X signal using Co-Founder/Default-owned cookies when Owner explicitly wants that source;
- combining OmniRoute search (`brave-search`, `exa-search`) with social/community evidence.

Do **not** use this for posting, replying, liking, DM, deleting, or login work. Those route through `platform-operator-router` and the platform-specific operator skills.

## Default Source Order

1. **OmniRoute search first for broad web discovery**
   - Local endpoint: `http://localhost:20128/v1/search`.
   - Prefer `brave-search` for general web/news recall.
   - Use `exa-search` for semantic/discovery-style research and higher-signal pages.
   - This avoids giving third-party skills raw Brave/Exa keys; OmniRoute owns provider credentials.

2. **`signal-radar` engine for social/community/market synthesis**
   - Default safe sources: Reddit, YouTube, Hacker News, Polymarket, GitHub.
   - Run with `FROM_BROWSER=off` and no `~/.config/signal-radar/.env` unless explicitly overridden.
   - This prevents accidental browser-cookie probing.

3. **Owned-account X signal only on explicit request**
   - Co-Founder/Default X cookies already live under private credential files.
   - Signal Radar can export `AUTH_TOKEN`/`CT0` ephemerally for one `signal-radar` subprocess.
   - Never write those cookies to `.env`, memory, skill files, profile distributions, or chat.
   - For official X API reads/writes, prefer `platform-operator-router` when authenticated and sufficient.

4. **Instagram / Threads / TikTok**
   - `signal-radar` uses ScrapeCreators-style API access for these sources, not our browser cookies by default.
   - Co-Founder/Default Instagram/Threads cookies are for owned-account frontend operations, not bulk scraping.
   - If the task is account operation or owner-state validation, route to `platform-operator-router` → Camofox.

## Browser Choice

- **Camofox persistent profile**: primary route for dedicated agent-owned account login, OAuth, posting, media upload, frontend owner-state checks, and cookie/session maintenance.
- **OmniRoute / Brave / Exa search APIs**: primary route for generic web research/search.
- **Hermes browser tool**: neutral web interaction when a page must be clicked/read and no owned-agent account session is involved.
- **Brave CDP / Owner human browser**: only when Owner explicitly overrides the architecture for a specific task. Do not use it as the default agent-owned account route.
- **CloakBrowser/CloakBrowser**: retired on this workstation; do not use unless Owner explicitly asks for rollback.

## Commands

Use the wrapper script; it redacts secret handling and keeps cookies ephemeral.

```bash
# List OmniRoute search providers
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py providers

# Broad web search via OmniRoute
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py search "AI phone agents" --provider brave-search --limit 5
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py search "Hermes agent skills" --provider exa-search --limit 5

# Safe signal-radar diagnostics: no browser cookie probing
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py diagnose

# signal-radar public/community scan
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py signal-radar "AI phone agents" -- --search=reddit,youtube,hackernews,signal-radar,github

# signal-radar with one owner’s X cookies, only when Owner explicitly wants X signal
python ~/.hermes/skills/research/signal-radar/scripts/signal_radar.py signal-radar --owner default --use-x-cookies "AI phone agents" -- --search=reddit,x,youtube,hackernews,signal-radar,github
```

For Default profile runs, use the profile-local path:

```bash
python ~/.hermes/profiles/default/skills/research/signal-radar/scripts/signal_radar.py diagnose
```

## Reporting Shape

For Owner, keep it short:

- route used: `OmniRoute brave-search`, `OmniRoute exa-search`, `signal-radar public`, or `signal-radar + default X cookies`;
- sources actually available;
- main findings + confidence;
- exact blockers: missing key, expired cookie, OmniRoute down, X auth missing, etc.

Do not claim a source was used unless the command output proves it.

## Safety Rules

- No permanent `.env` write for X cookies.
- No automatic browser-cookie extraction. `FROM_BROWSER=off` is the default.
- No printing cookies, tokens, localStorage, sessionStorage, or account files.
- Public/destructive social actions are outside this skill and require the platform operator route.
- If a cookie/API source fails, degrade to public sources and report the missing source plainly.

## Common Mistakes

- Loading `signal-radar` directly and letting its generic setup wizard decide our account/browser workflow.
- Treating Camofox as a generic search engine. It is for owned-account frontend state and actions.
- Treating Brave CDP as the default owned-account browser. It is Owner’s human browser unless explicitly overridden.
- Assuming Instagram/Threads cookies unlock `signal-radar` social search. They do not; use ScrapeCreators or the platform frontend route depending on task.
- Saying “X was included” when `AUTH_TOKEN`/`CT0`, `platform-operator-router`, or another X backend was not actually available.

## References & Sub-playbooks
- `references/signal-radar.md` — Mining community posts and engagement indices
- `references/signal-radar.md` — Scraping Polymarket orderbooks, prices, and event histories
