# GitHub Issues plugin config — UUID false-positive secret-ref blocker

## Date: 2026-05-19

## Symptom

`POST /api/plugins/local.github-issues/config` returns `422 {"error":"Plugin secret references are disabled until company-scoped plugin config lands"}` even though the config does NOT use secret references.

## Root cause

Paperstable-diffusion-image-generation's config validation endpoint scans ALL config values for UUID patterns (36-char with dashes). When a binding includes `companyId` with a UUID value like `43bf734f-bcf3-498a-b86e-a9f9db1418fd`, the backend treats it as a secret reference and rejects the entire config save.

This is a DIFFERENT mechanism from the Discord/Telegram secret-ref blocker:
- Discord/Telegram: the UI submits `discordBotTokenRef: "<secret-uuid>"` which is an actual secret reference.
- GitHub Issues: a plain `companyId` UUID is falsely detected as a secret reference.

## Confirmed by field-by-field testing

| Field added | Value | Result |
|---|---|---|
| No bindings | `{defaultPriority: "high"}` | OK |
| Empty bindings | `{bindings: []}` | OK |
| Binding without companyId | `{id, owner, repo, tokenRef, labelPrefix, defaultStatus}` | OK |
| Binding WITH companyId | `+ companyId: "43bf734f-..."` | **422** |
| Binding with UUID-like tokenRef | `tokenRef: "12345678-1234-..."` | **422** |
| Binding with real GitHub PAT | `tokenRef: "ghp_..."` (40-char, not UUID) | OK |

## Workaround

Save the binding config WITHOUT `companyId`. The GitHub Issues worker defaults to company `"default"` when `companyId` is absent from the binding.

```json
{
  "configJson": {
    "defaultPriority": "medium",
    "bindings": [{
      "id": "gh-ledger-main",
      "owner": "galyarderlabs",
      "repo": "galyarder-ledger",
      "tokenRef": "<actual-github-pat>",
      "labelPrefix": "github:ledger",
      "defaultStatus": "todo"
    }]
  }
}
```

## Worker patch needed

The GitHub Issues worker's `resolveToken` function calls `ctx.secrets.resolve(tokenRef)`. When using plaintext token fallback (same as Discord/Telegram), patch the worker to fall back to using `tokenRef` directly:

```javascript
// BEFORE:
async function resolveToken(tokenRef) {
  try {
    return await ctx.secrets.resolve(tokenRef);
  } catch (err) {
    ctx.logger.error("Failed to resolve token secret", { tokenRef, err });
    return null;
  }
}

// AFTER:
async function resolveToken(tokenRef) {
  try {
    return await ctx.secrets.resolve(tokenRef);
  } catch (err) {
    ctx.logger.warn("Secret ref resolve failed, using tokenRef directly as fallback", { tokenRef: tokenRef ? "[present]" : "[empty]" });
    return tokenRef || null;
  }
}
```

Worker file: `/home/galyarder/.paperstable-diffusion-image-generation/plugins/node_modules/@wil0x91/paperstable-diffusion-image-generation-plugin-github-issues/dist/worker.js`

## Plugin config structure (as of v0.2.3-0.2.4)

The GitHub Issues plugin reads config via `readConfig(await ctx.config.get())` which returns the raw configJson object. Bindings are in `configJson.bindings[]`.

Each binding fields used by the worker:
- `id` — binding identifier
- `owner` — GitHub org/user
- `repo` — GitHub repo name
- `tokenRef` — passed to `resolveToken()` for GitHub API auth
- `companyId` — Paperstable-diffusion-image-generation company ID (omit to avoid UUID false-positive)
- `projectId` — optional Paperstable-diffusion-image-generation project
- `labelPrefix` — optional label prefix for synced issues
- `defaultStatus` — initial Paperstable-diffusion-image-generation status for imported issues (default: `todo`)

## Schedule

The `sync-github-issues` job runs every 10 minutes (`*/10 * * * *`).
