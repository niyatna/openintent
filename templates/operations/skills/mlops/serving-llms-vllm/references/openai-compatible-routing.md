# Reference: serving-llms-vllm

# OpenAI-Compatible Routing

## Overview

Local AI routing turns many model/provider backends into one OpenAI-compatible endpoint. For Galyarder, evaluate routing choices by probability, durability, resource fit, blast radius, and ownership. The high-probability pattern is infrastructure-grade provider/session management, not disposable account-farming loops.

Canonical local shape:

```text
owned keys/accounts/sessions
  -> provider adapters
  -> secret/session store
  -> health + quota + cost tracking
  -> model alias/router
  -> OpenAI-compatible endpoint
  -> Hermes / agents / apps
```

Known Galyarder endpoint pattern:

```text
http://192.168.100.6:20128/v1
```

## When to Use

Use this for:

- 9Router/local-router architecture.
- Provider key pools and failover.
- Model alias maps across OpenAI-compatible backends.
- BYOA account/session inventory for accounts Galih controls.
- Health checks, rate-limit backoff, cost/quota tracking, and fallback routing.
- Evaluating third-party AI proxy designs for control-writing-planse lessons without copying low-durability/high-blast-radius account-farming mechanics.

Do not use it to build mass signup/free-trial farming, CAPTCHA bypass, OTP/email farm automation, or quota evasion against third-party platforms. If this blocks the requested tactic, state it once as probability/blast-radius/resource-fit/system-boundary, then move to the nearest executable capacity action.

## Clean Design Pattern

Minimum components:

- provider registry: provider IDs, base URLs, model support, auth type.
- secret store: encrypted or at least permission-locked keys/sessions; avoid plaintext `email:password` lists.
- health checker: key validity, model availability, provider latency, quota exhaustion.
- router: model aliasing, fallback order, sticky routing when needed.
- accounting: usage, cost estimate, per-key/per-provider limits.
- audit log: request metadata without leaking prompts/secrets unnecessarily.
- dashboard/CLI: inspect status, add/remove keys, disable bad providers.

Example provider record:

```yaml
providers:
  - id: google-ai-studio-main
    type: openai-compatible
    base_url: https://...
    auth: api-key
    tier: owned
    models: [gemini-3.1-pro, gemini-3.1-flash]
    priority: 20
    status: active
```

## Account/Session Automation Boundary

Executable support:

- account/session inventory for accounts Galih controls
- manual or human-in-loop login
- assisted session refresh for accounts Galih controls
- dashboard scraping for quota/status when no API exists
- importing API keys or session tokens Galih already controls

Do not assist with:

- mass-registering third-party free trials
- bypassing CAPTCHA/anti-bot or security prompts
- farming API keys from fresh accounts
- rotating accounts to evade rate/quota limits
- proxying farmed access for resale

If Galih asks about such systems conceptually, analyze feasibility, probability, bottlenecks, and blast radius; extract architecture lessons, but route implementation toward controlled accounts/sessions, health checks, quota compression, and router reliability.

## Resource-Realistic Substitutes

When this skill is loaded as a substitute for account-farm or free-trial capacity requests, do not default to paid-provider or local-inference advice without checking constraints. Minimum check:

- live CPU/RAM/GPU/disk if tools are available,
- whether `ollama`, `llama-server`, `litellm`, or an existing router is installed,
- whether the user has budget, credits, keys, or only public/free surfaces,
- expected latency/quality tradeoff on the actual machine.

On weak hardware or no budget, prefer low-compute capacity tactics before architecture-heavy writing-planss:

- inventory existing keys/sessions without creating new third-party accounts,
- monitor official free-credit/startup/grant/hackathon opportunities,
- route small local models only to cheap tasks like classification, extraction, short rewrites, and triage,
- use public-data extraction and prompt compression to reduce expensive model calls,
- build a simple ledger before building a full router.

Bad substitute: generic provider/Ollama/LiteLLM advice without resource fit. Good substitute: "Given CPU/RAM/GPU/budget, here is the smallest executable capacity move and what it can/cannot handle."

## Browser Automation Role

Camofox/Camoufox can be useful as an account/session automation layer, but keep it scoped:

```text
Camofox = assisted login/debug/session refresh
router = model/provider selection
vault = secrets and sessions
Hermes/apps = consumers
```

For Camofox-specific headless/headful/audio/service work, load `camofox-browser`.

## References

- `references/enowx-ai-byoa-proxy.md` — notes from a third-party BYOA proxy page and what to extract vs avoid.
- `` — live status of image generation models through 9Router, tested 2026-05-10, includes auth/rate-limit errors and fixes.

## Image Generation Routing

Image generation through OpenAI-compatible routers is a separate concern from text LLM routing.

- **Endpoint**: `/v1/images/generations` (not `/v1/chat/completions`)
- **Model semantics**: image-capable models (`cx/gpt-5.4`, `antigravity/gemini-3.1-flash-image`) ≠ text-only models (`mimo/mimo-v2.5-pro`)
- **Hermes config trap**: `image_gen.model` in `config.yaml` defaults to the text model if misconfigured. Always verify the model listed under `image_gen:` is actually image-capable.
- **Tool override**: Hermes `image_generate` tool may have hardcoded model defaults (e.g. `together/black-forest-labs/FLUX.2-max`) that override `config.yaml`. If the tool returns 400 for a model not in config, this is the cause. May require session restart to pick up config changes.
- **NSFW image generation**: Content safety is at the provider level, not the router. FLUX models (Black Forest Labs) are relatively uncensored. DALL-E/Imagen are heavily filtered. Self-hosted FLUX gives maximum control but requires GPU (8GB+ VRAM for schnell, 24GB+ for dev/pro).

## Pitfalls

- **`cx/` prefix routing vs catalog IDs**: Models with `cx/` prefix route through Codex (ChatGPT OAuth). Some models are "not supported when using Codex with a ChatGPT account" for image generation. The catalog may list the same model under `codex/` prefix. Always check `/v1/models` catalog for exact IDs.
- **Google OAuth scopes for Gemini image**: `antigravity/gemini-*-image` models require `generativelanguage.googleapis.com` image generation scopes. 403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT` means the token lacks these scopes.
- **Rate limits are per-account/endpoint**: Hitting `/v1/images/generations` rapidly triggers 429s. Budget test calls.
- **9Router model alias mismatch**: What works via direct curl (`cx/gpt-5.5`) may not match catalog model ID (`codex/gpt-5.5`). Downstream consumers (like Hermes `openai-compatible` image gen plugin) fetch catalog and match against it — alias mismatch causes silent fallback to wrong model.

## Common Mistakes

- Building production dependence on throwaway trial accounts.
- Confusing domain-owned email aliases with permission to multiply provider quotas.
- Storing passwords in plaintext `accounts.txt` when a key/session store is needed.
- Treating stealth browser login as reliability; providers can still block accounts by risk signals.
- Copying abuse-sensitive features instead of extracting the useful control-writing-planse design.