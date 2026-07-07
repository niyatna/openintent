# Discord Troubleshooting & API Mutations

# Discord REST API Mutations — Session Reference

## Why This Exists

The Hermes `discord_admin` tool is read-only for channel properties (position, topic, name, parent_id). It can: list_channels, channel_info, list_pins, send_message, pin_message. It **cannot** edit channel properties or create channels. For those, use Discord REST API v10 directly via curl.

## Token Retrieval

```bash
TOKEN=$(grep DISCORD_BOT_TOKEN /home/galyarder/.hermes/.env | sed 's/DISCORD_BOT_TOKEN=//')
```

The token is base64-encoded in the .env file. Do NOT use `python3` to parse — it can hang/timout in execute_code. Use grep+sed.

## Edit Channel Properties

```bash
# Move channel to new position
curl -s -X PATCH "https://discord.com/api/v10/channels/$CHANNEL_ID" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"position": 11}'

# Set topic
curl -s -X PATCH "https://discord.com/api/v10/channels/$CHANNEL_ID" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Channel description text."}'

# Move to different category
curl -s -X PATCH "https://discord.com/api/v10/channels/$CHANNEL_ID" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"parent_id": "NEW_CATEGORY_ID"}'
```

Returns 200 with full channel JSON on success.

## Create Channel

```bash
curl -s -X POST "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"channel-name","type":0,"parent_id":"CATEGORY_ID","topic":"Description."}'
```

Channel types: 0=text, 2=voice, 4=category, 5=announcement, 15=forum.

## Batch Topic Set

```bash
declare -A TOPICS
TOPICS["CH_ID_1"]="Topic text 1"
TOPICS["CH_ID_2"]="Topic text 2"

for CHID in "${!TOPICS[@]}"; do
  TOPIC="${TOPICS[$CHID]}"
  RESULT=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH \
    "https://discord.com/api/v10/channels/$CHID" \
    -H "Authorization: Bot $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"topic\": \"$TOPIC\"}")
  echo "Channel $CHID: $RESULT"
done
```

## Forum Channels (type 15)

Forum channels reject `POST /channels/{id}/messages` (returns empty/error). Must create threads:

```bash
# Create thread with embedded message
curl -s -X POST "https://discord.com/api/v10/channels/$FORUM_ID/threads" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "📌 Guide Title",
    "message": {"content": "Guide content here..."},
    "auto_archive_duration": 1440
  }'
# Returns thread object with id

# Pin the guide in the thread
curl -s -X PUT "https://discord.com/api/v10/channels/$THREAD_ID/pins/$THREAD_ID" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json"
# Note: thread_id == first message_id for forum threads
# Returns 204 on success
```

## Delete + Recreate (Type Change Pattern)

Discord API does **not** support changing a channel's `type` (e.g., text→forum). You must **delete + recreate**. This is a destructive operation — history will be lost. Always warn the user before executing.

```bash
# 1. Delete old channel (returns 200)
curl -s -w "\n%{http_code}" -X DELETE "https://discord.com/api/v10/channels/$OLD_CHANNEL_ID" \
  -H "Authorization: Bot $TOKEN"

# 2. Recreate as new type (returns 201)
curl -s -w "\n%{http_code}" -X POST "https://discord.com/api/v10/guilds/$GUILD/channels" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"channel-name","type":15,"parent_id":"CATEGORY_ID","topic":"Description.","position":0}'
```

### Positioning Gotcha
When creating a channel with a `position` value that already exists, Discord **swaps** the positions. To avoid swapping, batch your operations: delete all old channels first, then create all new ones, then explicitly set positions via PATCH.

## Pitfalls

- **Token extraction:** Don't use `python3 -c "import os; ..."` to read .env — it can timeout. Use `grep | sed`.
- **Position conflicts:** Setting a channel to an already-taken position swaps them. To insert without swap, batch-update all affected positions.
- **Forum pin ID:** For forum threads, the thread ID IS the first message ID. Don't fetch messages separately.
- **Rate limits:** Discord rate limits at ~50 requests/second per guild. For batch operations (20+ channels), add small delays if hitting 429s.
- **Context compaction corrupts IDs:** Always re-fetch `list_channels` for fresh IDs before retrying 404s. 19-digit IDs get corrupted during context window compaction.

## Tested On

Galyarder Labs server (guild 1315637547736764426), 2026-05-11. All endpoints verified working with bot token from profile .env.

## Peer Side-Effect Verification

# Discord peer side-effect verification

## Session signal

Galih asked Keiya to confirm Galyarder's router/skill state, then approved Galyarder to perform a non-destructive V2 sync. Galyarder reported `DONE`. Keiya did not stop at the report: she verified the profile-local files, backup path, and ran the target profile verifier before telling Galih the sync was complete.

## Reusable pattern

When a peer Discord bot/agent claims persistent work is done:

1. Treat the reply as a report, not proof.
2. Identify the side-effect class:
   - file writes / copies / backups
   - memory updates
   - config changes
   - cron/scheduled jobs
   - external messages/posts/emails
   - profile sync or runtime state changes
3. Verify with read-only evidence when tools are available:
   - check expected files exist
   - inspect changed frontmatter/status lines
   - run the relevant verifier/test from the target profile or target working directory
   - check backup paths exist for non-destructive sync
   - inspect logs/status for runtime or scheduled work
4. Only report `done` to Galih after verification passes.
5. If verification cannot be performed, say `target reported done` and list what remains unverified.

## Example from the sync session

After Galyarder reported the V2 sync, Keiya verified:

```text
python /home/galyarder/.hermes/profiles/galyarder/skills/galyarder-framework/galyarder-framework-router/scripts/verify_router_status.py
```

Expected verifier shape:

```text
skills=360
top_categories=30
duplicate_skill_names=0
bad_frontmatter=0
core_daily_pack=yes
v2_noise_audit=yes
v2_fresh_hub_comparison=yes
v2_stale_archive_writing-plans=yes
separate_session_verification=yes
required_router_files=yes
status=V2 final / non-destructive
PASS
```

She also checked expected files and the backup path existed before summarizing to Galih.

## Pitfalls

- Do not re-mention the peer bot in the human-facing summary; that can restart a loop.
- Do not trust a `DONE` report for persistent state if the target profile/root differs from the current profile/root.
- Use target-context verification: profile-local scripts should be run from or against the profile they claim to modify.
- Keep the human-facing summary short: status, evidence, remaining gap.

## Gateway Channels & PR PRDs

# Discord channel auto-skill + bundle PR pattern (2026-06-11)

## Trigger

Use this reference when Discord/Slack gateway sessions do not receive expected channel-bound skills, profile core bundles, or per-channel grounding instructions.

Observed failure class:
- config used legacy dict-form `discord.channel_skills`;
- gateway bridge/resolver only handled list-form `channel_skill_bindings`;
- fresh Discord sessions missed auto-loaded skills/bundles;
- bundle names like `/keiya-core` or `/galyarder-core` were treated as ordinary skills, so `skill_view('keiya-core')` failed even though the bundle existed;
- Discord slash-command events carried `channel_prompt` but not `auto_skill`.

## Durable diagnosis sequence

1. Check the process profile and env, not just files on disk:
   - default/Keiya gateway should have `HERMES_HOME=/home/galyarder/.hermes`.
   - Galyarder gateway should have `HERMES_HOME=/home/galyarder/.hermes/profiles/galyarder`.
2. Check config bridge output, not only `config.yaml`:
   ```python
   from gateway.config import load_gateway_config, Platform
   cfg = load_gateway_config()
   extra = cfg.platforms[Platform.DISCORD].extra
   print(extra.get('channel_skills'), extra.get('channel_skill_bindings'))
   ```
3. Check resolver behavior:
   ```python
   from gateway.platforms.base import resolve_channel_skills
   resolve_channel_skills(extra, channel_id, parent_id)
   ```
4. Remember bundle semantics:
   - `skill_view('keiya-core')` / `skill_view('galyarder-core')` failing is expected if those are bundles.
   - Bundle loading must use slash dispatch or `agent.skill_bundles.build_bundle_invocation_message()`.

## Upstreamable fix shape

Patch class-level behavior, not local config only:

- `gateway/config.py`: bridge `channel_skills` into Discord/Slack platform `extra`, normalizing dict keys to strings.
- `gateway/platforms/base.py`: `resolve_channel_skills()` should support both:
  - `channel_skill_bindings: [{id, skill/skills}]`
  - `channel_skills: {channel_id: skill_or_skills}`
  and preserve channel-id before parent-id priority.
- `gateway/run.py`: channel auto-load entries should resolve bundle names before falling back to individual skills.
- `plugins/platforms/discord/adapter.py`: slash-command `MessageEvent` should include `auto_skill`, matching normal message/thread dispatch.
- Tests should cover config bridge, dict alias, parent fallback, slash `auto_skill`, and bundle auto-load.

## PR hygiene

If the fix is in Hermes source code, create an upstream PR so local patches do not disappear on update.

Safe pattern:

```bash
cd /home/galyarder/.hermes/hermes
git fetch upstream --tags --prune
git worktree add -b fix/discord-channel-skills-bundles /tmp/hermes-discord-autoskills-pr upstream/main
# Reapply minimal patch in the clean worktree; do not copy whole files from long-lived local checkout.
python -m py_compile gateway/config.py gateway/platforms/base.py gateway/run.py plugins/platforms/discord/adapter.py ...
uv run --with pytest --with pytest-asyncio pytest <targeted tests> -q -o 'addopts='
git add <intended files>
git commit -m "Fix gateway channel auto-skill bundles"
git push fork fix/discord-channel-skills-bundles
```

Use `gh pr create --body-file pr-body.md` or `gh pr edit --body-file pr-body.md` for Markdown bodies containing backticks. Inline `--body "...` can execute shell substitutions from backticks and corrupt the body.

## 2026-06-11 evidence

Upstream PR created: `https://github.com/NousResearch/hermes/pull/43954`

Branch: `muhamadgalihsaputra:fix/discord-channel-skills-bundles`

Commit: `4143b9fb1 Fix gateway channel auto-skill bundles`

Targeted verification:

```bash
python -m py_compile gateway/config.py gateway/platforms/base.py gateway/run.py plugins/platforms/discord/adapter.py tests/gateway/test_discord_channel_skills.py tests/gateway/test_gateway_channel_auto_bundles.py tests/gateway/test_discord_channel_config.py

uv run --with pytest --with pytest-asyncio pytest \
  tests/gateway/test_discord_channel_skills.py \
  tests/gateway/test_slack_channel_skills.py \
  tests/gateway/test_gateway_channel_auto_bundles.py \
  tests/gateway/test_discord_channel_config.py \
  tests/gateway/test_discord_channel_prompts.py \
  tests/gateway/test_fresh_reset_skill_injection.py \
  -q -o 'addopts='
```

Result: `41 passed`.