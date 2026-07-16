# Reference: qdrant-vector-search

# OpenAI-Compatible Embeddings

## Overview

Use this for any app or agent tool that needs embeddings but should route through a local/proxied OpenAI-compatible endpoint instead of direct OpenAI. The core pattern is: prove the endpoint works, prove the returned vector shape matches storage, then bridge the target tool through supported config/env or a minimal adapter patch.

## When to Use

- Tool defaults to OpenAI embeddings but the environment has a local router or gateway.
- Embedding calls fail because of API key, model permission, base URL, or dimension mismatch.
- A vector DB/schema expects a fixed dimension and providers return a different default size.
- Background embedding jobs contend for local DB locks.
- Cost/privacy constraints favor local or routed embeddings.

## Workflow

1. **Discover the target contract**
   - Identify where embeddings are called.
   - Identify expected vector dimensions in the DB/schema/index.
   - Identify whether base URL, API key, model, and dimensions are configurable.

2. **Probe the router first**
   - Test the router's `/v1/embeddings` endpoint with a harmless sample input.
   - Use environment placeholders for credentials; never print or paste live keys.
   - Confirm HTTP status and actual embedding length.

3. **Select a compatible model**
   - Prefer a model that natively returns the schema dimension.
   - If the provider supports dimension shortening, request the exact schema dimension.
   - Record auth/permission failures as provider-specific facts, not generic impossibility.

4. **Bridge the target tool**
   - Prefer official config/env variables.
   - If missing, apply a minimal adapter patch near the embedding client construction.
   - Keep upstream defaults intact and override only when explicit env/config values are present.

5. **Verify end to end**
   - Run the tool's stale/backfill embedding command.
   - Check embedded count equals chunk/item count.
   - Run the health/doctor command if available.
   - Do a small semantic query after data exists.

## Minimal probe template

```bash
: "${EMBED_BASE_URL:?set EMBED_BASE_URL}"
: "${EMBED_API_KEY:?set EMBED_API_KEY}"
: "${EMBED_MODEL:?set EMBED_MODEL}"
: "${EMBED_DIMS:?set EMBED_DIMS}"

python3 - <<'PY'
import json, os, urllib.request
base = os.environ['EMBED_BASE_URL'].rstrip('/')
key = os.environ['EMBED_API_KEY']
body = json.dumps({
    'model': os.environ['EMBED_MODEL'],
    'input': ['embedding router probe'],
    'dimensions': int(os.environ['EMBED_DIMS']),
}).encode()
req = urllib.request.Request(
    base + '/embeddings',
    data=body,
    headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
    method='POST',
)
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.loads(r.read())
emb = data['data'][0]['embedding']
print('status=ok')
print('embedding_len=' + str(len(emb)))
PY
```

## Adapter patch pattern

When a tool hardcodes OpenAI, add explicit overrides without changing the default behavior:

```ts
const baseURL = process.env.TOOL_EMBED_BASE_URL || undefined;
const apiKey = process.env.TOOL_EMBED_API_KEY || process.env.OPENAI_API_KEY;
const model = process.env.TOOL_EMBED_MODEL || 'text-embedding-3-small';
const dimensions = process.env.TOOL_EMBED_DIMENSIONS
  ? Number(process.env.TOOL_EMBED_DIMENSIONS)
  : undefined;
```

Only pass `dimensions` when defined; some providers reject unsupported dimension parameters.

## Scheduling Guidance

For local file-backed stores like SQLite/PGLite, avoid aggressive background embedding loops. Prefer:

- lightweight import/sync hourly or on file-change,
- embedding backfill on demand or daily/weekly,
- no always-on daemon if it holds DB locks during manual commands.

## Common Mistakes

- Assuming direct OpenAI is required before probing the local router.
- Using a model whose default vector size does not match the index schema.
- Printing API keys while debugging shell profiles or env loading.
- Treating provider auth failures as model incompatibility.
- Running embedding every few minutes on a tiny local brain and causing lock contention.
- Claiming setup is done before verifying playwright-pro and vector length.

## References

- `references/gbrain-local-router-2026-05-04.md` — session-specific notes for GBrain v0.26.0 with a local OpenAI-compatible router on Owner's machine. Pair this with `gbrain/references/gbrain-dual-home-default-2026-05-12.md` before embedding work on Owner's Hermes machine so you do not patch or backfill the broken profile-local GBrain DB by accident.