# Same-Origin Dashboard Proxying and Authentication Routing

This reference outlines proven debugging paths, workarounds, and tool/process routing patterns for SAME-ORIGIN proxy setups (e.g. running local developer dashboards on ports 3100, 7457, 9119 via a Telegram Mini App proxy).

## Core Mechanisms & Context

When proxying local webapp dashboards under a unified client-facing server (e.g., Express/Node proxy server on port 9122):
- **Path Candicacy Matching**: The proxy routes incoming absolute root request paths (such as `/api/*`, `/assets/*`, `/auth/*`) directly to the target dashboard service (such as Paperclip or OmniRoute) using rules in `isPaperclipRootCandidate` or `isDefaultDesignRootCandidate`.
- **Referer Scoping**: Assets/requests without explicit subpath prefixes are mapped back to their respective targets using the browser `Referer` headers.

---

## 1. Cookie Path Scoping on Sub-directory Proxies

### The Pitfall
Replacing `Path=/` in the upstream `Set-Cookie` header with a scoped path like `Path=/p/target/` will break cookie-based authentication frameworks (like Better-Auth). The browser will store the session cookie under the scoped path `/p/target/`, but when the SPA client makes root-level API/Auth requests (like `/auth/session` or `/api/company`), the browser omits the cookie. This forces the client to land on a blank setup/onboarding screen from scratch.

### The Solution
Exempt auth-scoping targets (such as `paperclip-root` or `omniroute`) from subpath prefix injection. Allow their cookies to be stored natively under `Path=/`:
```javascript
if (targetName === 'omniroute' || targetName === 'paperclip-root') {
  res.append('set-cookie', stripped.replace(/;\s*Path=\/[^;]*/ig, '; Path=/'));
} else {
  res.append('set-cookie', stripped.replace(/;\s*Path=\//ig, `; Path=/p/${targetName}/`));
}
```

---

## 2. Agent Token Auto-Injection vs. Human Sessions

### The Pitfall
Automatically injecting background system credentials/board tokens (`Bearer ${token}` compiled from local files like `auth.json`) into proxy headers for human-facing browser frames overrides the browser's own session cookies. The Paperclip backend receives the agent API key and logs the session in as a board/system Agent instead of the actual human user. System agents do not have a default company selected in the browser view, dropping the developer onto a blank Acme Corp onboarding layout.

### The Solution
Keep human-facing web proxies entirely transparent to Authorization headers. Do *not* auto-inject system tokens in client proxy code; authorize requests solely via browser cookies, and keep system tokens isolated to developer tool wrappers (like stdout / CLI executions).

---

## 3. Safe WebSocket Upgrade Router Checks

### The Pitfall
In Node.js HTTP servers, the upgrade handler (`server.on('upgrade')`) receives a raw HTTP request object that does not guarantee standard Express middleware properties. Accessing nested fields like `req.headers.cookie` directly without optional chaining will throw a `TypeError: Cannot read properties of undefined` and crash the entire node miniapp/proxy process when a client attempts to connect without cookies.

### The Solution
Always guard raw request property access in the upgrade listener with optional chaining:
```javascript
const cookieToken = parseCookie(req.headers?.cookie || '').gmini_access_token;
const isGd = req.originalUrl?.startsWith('/gd');
```

---

## 4. Host Resource Hijacking (Candidate Overlap)

### The Pitfall
Declaring generic files (such as `/favicon.svg`, `/icons/`, or the active PWA manifest `/site.webmanifest`) in `isDefaultDesignRootCandidate` or `isPaperclipRootCandidate` causes the main Mini App shell's own asset requests to be hijacked by the proxy target. If the target has no such assets, the shell's inline SVG icons and icons.svg sprite fail to load, rendering the host app completely empty.

### The Solution
Validate both the candidate name and the active Referer. If a main-shell asset like `/favicon.svg` or `/icons/` is requested, and the Referer is `/` (the main shell itself, not Default Design `/gd/`), return `next()` to let the Express static router serve the file locally instead of proxying it.
