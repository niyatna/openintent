# OmniRoute Image Generation Model Status

Tested: 2026-05-10 via `POST http://localhost:20128/v1/images/generations`

## Model Status

| Model | Status | Error | Fix |
|---|---|---|---|
| `codex/gpt-5.5` | ✅ WORKS | — | Model ID in catalog is `codex/gpt-5.5`, not `cx/gpt-5.5` |
| `cx/gpt-5.5` | ✅ WORKS (curl) | — | Alias works via curl but NOT in Hermes plugin (catalog mismatch) |
| `cx/gpt-5.5-xhigh` | ❌ 400 | "not supported when using Codex with a ChatGPT account" | OmniRoute routes through Codex ChatGPT OAuth; this model isn't supported via that auth path |
| `cx/gpt-5.4` | ❌ 429 | Usage limit reached (~5 day reset) | Rate limited, not broken |
| `antigravity/gemini-3.1-flash-image` | ❌ 403 | `ACCESS_TOKEN_SCOPE_INSUFFICIENT` | Google OAuth token lacks `generativelanguage.googleapis.com` image generation scopes |
| `antigravity/gemini-3-pro-image-preview` | ❌ 403 | Same as above | Same fix |
| `nebius/black-forest-labs/flux-schnell` | ❌ 500 | Internal Server Error | Nebsius image endpoint broken or misconfigured |

## Working Configuration (Default profile)

```yaml
# config.yaml
image_gen:
  provider: openai-compatible    # NOT openai-codex
  model: codex/gpt-5.5           # Must match catalog ID exactly
  base_url: http://localhost:20128/v1
  api_key: ${OMNIROUTE_API_KEY}
  timeout: 180
  use_gateway: false
```

```bash
# .env — NO /images/generations suffix (plugin appends it)
OPENAI_COMPATIBLE_IMAGE_BASE_URL=http://localhost:20128/v1
```

## Key Insight

The `openai-compatible` Hermes plugin fetches `/v1/models` catalog and matches `image_gen.model` against it. If the configured model doesn't match any catalog entry, plugin silently falls back to `together/black-forest-labs/FLUX.2-max` (which doesn't work via this routing). Always verify catalog IDs.
