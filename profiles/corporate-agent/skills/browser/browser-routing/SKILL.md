---
name: browser-routing
description: "Configure and troubleshoot which browser stack handles web automation. Camofox (stealth browser) is the primary route; default Chromium is the native fallback."
version: 1.0.0
author: Company
license: MIT
metadata:
  hermes:
    category: browser
---

# Browser Routing

Determine how web automation requests are executed within the OpenIntent environment.

---

## 1. Core Routing Rules

OpenIntent does not support external user browsers or manual desktop cockpit configurations.

- **Primary Route**: **Camofox** persistent profiles for all automated logins, multi-account automation (X, Threads, GWS), and traffic cap/CDP debugging.
- **Stealth Verification**: Load `camofox-browser` for specific commands. Use persistent profiles scoped to `~/.hermes/private/browser-profiles/agents/<owner>/`.
- **Legacy & Fallback**: **CloakBrowser** is the secondary fallback for legacy workflows where Camofox is not fully tested.
- **Native Browser**: Standard headless Chromium is used exclusively for lightweight page reads and fast scraper fallback tests.

---

## 2. Decision Matrix

| Task / Context | Target Configuration |
|---|---|
| User session check / Multi-account login | Camofox persistent profile |
| Headless scraping / API traffic check (HAR) | Camofox with CDP debugging |
| Simple Markdown fetches | Native scraper / curl-md |
| Legacy platform operations | CloakBrowser (disposable sandbox) |

---

## 3. Same-Origin Dashboard Proxying & Auth Routing

When proxying local developer dashboards (such as Paperclip or Hindsight):
- **Cookie Path Scoping**: Do not prepend custom subpaths (like `/p/target/`) to `Set-Cookie` path specs. Session cookies must stay scoped to `Path=/` so the browser sends them on absolute `/auth` and `/api` requests.
- **Deter Token Auto-Injection**: Avoid automatically embedding system/board tokens (`Bearer ${token}`) into browser-facing proxy requests. Let the browser handle transparent cookie sessions.
- **WebSocket Upgrade Verification**: Raw request headers in Socket `upgrade` listeners are unsafe. Always wrap headers/URL check with optional chaining (`req.headers?.cookie`, `req.originalUrl?.startsWith`) to prevent server crashes on socket attempts.
- **Resource Scope Exclusions**: Guard common assets (like `/icons/`, `/favicon`, `/manifest`) from candidate scope hijacking. If a request lacks design referrers, let it fall through (`next()`) to static file local rendering.
- For detailed step-by-step auth proxying playbooks, see `references/same-origin-dashboard-proxying-and-auth.md`.
