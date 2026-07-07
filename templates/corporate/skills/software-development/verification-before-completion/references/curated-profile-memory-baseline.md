# Curated profile memory baseline verification

Session signal: Galih corrected a profile-memory distribution pass because the first `USER.md` and `MEMORY.md` baseline was too thin/basic. For profile continuity, he expects all important durable context from Hindsight and native memory to be synthesized, not a token starter subset.

## Scope

Use this with profile distribution / restore / memory packaging tasks involving:

- `HERMES_HOME/memories/USER.md`
- `HERMES_HOME/memories/MEMORY.md`
- root compatibility mirrors `HERMES_HOME/USER.md` and `HERMES_HOME/MEMORY.md` when present
- private profile distribution copies of curated memory files

## Core correction

Curated hot memory is not a raw archive, but it must be rich enough to restore the profile's practical operating baseline. A small summary is insufficient when the user asked to preserve profile continuity.

Before rewriting profile memory, gather from all available durable layers:

1. current native injected memory/user profile
2. existing profile memory files
3. broad Hindsight recall by domain
4. relevant Obsidian protocol/canon files
5. loaded skill references governing the workflow
6. live verification for current counts/config/status

If `hindsight_reflect` fails, use several targeted `hindsight_recall` queries and synthesize manually. Do not stop after one broad recall result.

## Domain playwright-pro checklist

For a Galyarder/Keiya profile baseline, check whether the new files cover:

- user identity, tone, preferences, values, role split
- tool-grounding and verification expectations
- Discord relay/raw mention protocol
- memory architecture: Hindsight vs USER/MEMORY vs Obsidian vs session_search vs skills
- product/company canon and positioning guardrails
- runtime paths and profile-home caveats
- major integrations: MCP, Paperstable-diffusion-image-generation, NotebookLM, browser/Camofox, gstack, GBrain
- profile distribution / disaster recovery / secret exclusion rules
- durable failure modes and open system gaps
- media/persona references only when they affect future output

## USER.md vs MEMORY.md routing

Put in `USER.md`:

- stable facts about Galih and how to work with him
- language/tone/format preferences
- role split and direct-command handling
- recurring workflow corrections
- durable media/persona preferences that shape user-facing output

Put in `MEMORY.md`:

- profile identity and SOUL path
- canonical paths, repos, vault locations
- Galyarder Labs canon/product terminology
- runtime/tool/MCP architecture
- memory/storage/recovery caveats
- Discord relay mechanics
- profile distribution and verification rules
- durable known failure modes

Do not include secrets, raw sessions, runtime DB contents, raw logs, temporary task progress, one-off issue/PR numbers, or stale command outputs.

## External ChatGPT/Gemini memory-pack routing

When curating memory for external assistants (ChatGPT, Gemini, Mistral/Vibe, etc.), do **not** copy Hermes-specific operating requirements as memory. Treat the external assistant's Custom Instructions / Gem instructions / system prompt as the place for:

- role/mode behavior rules and doctrine
- response format and tone defaults
- tool-use expectations that only make sense in that platform
- Hermes-only grounding rules such as reading `SOUL.md`, `USER.md`, `MEMORY.md`, Hindsight, Obsidian, or loading skills
- runtime verification protocols and agent workflow discipline

Use external Memory only for stable, high-value facts that improve second-brain continuity:

- who Galih is and what he is building
- durable values, taste, communication style, and decision tendencies stated as facts, not commands
- active/project map context and why each project matters
- Galyarder Labs product/canon essentials such as Ledger/HQ/Framework/Agent, without temporary brand/design details that are not final
- relevant personal/human context that affects advice quality
- stable constraints, preferences, and history that should survive across conversations

Key distinction: **instructions say how the assistant should behave; memory says what the assistant should know.** If a line starts acting like a command (`must`, `always`, `use this format`, `check these files`), route it to instructions/system prompt unless the user explicitly wants it stored as memory.

## Verification before completion

Before claiming the profile memory baseline is done:

1. backup existing memory files
2. write `memories/USER.md` and `memories/MEMORY.md`
3. sync root compatibility mirrors if present
4. adjust configured char limits with enough margin
5. sync distribution copies only after explicit approval
6. verify live profile files, mirrors, and distribution copies match or intentionally strip-match
7. verify sizes fit configured limits
8. scan staged distribution paths for forbidden runtime state
9. scan staged text for obvious secrets
10. commit/push only intended files
11. fetch remote and compare local HEAD to remote branch

## Concise report shape

Report evidence, not the full memory dump:

```text
expanded USER.md: X KB / N entries
expanded MEMORY.md: Y KB / M entries
limits: user A, memory B
verified: equality, limits, forbidden paths none, secret scan none
commit: <hash> <subject>
remote: local_head == remote_head
```
