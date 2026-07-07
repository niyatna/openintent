---
name: gbrain
description: Use when querying GBrain vector memory database indexes, searching local vault nodes graphs, or structuring LaTeX research papers.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [research, gbrain, local-db, gbrain, gitnexus, gbrain, paper-writing]
    category: research
---

# GBrain

## Purpose

This is the thin Hermes routing skill for GBrain.

Do **not** import GBrain's internal skillpack into Hermes skills. GBrain has its own skill ecosystem under the GBrain repo. This Hermes skill only tells the assistant when and how to call the canonical GBrain CLI safely.

## Canonical Instance

For Galih/Galyarder, use the single healthy OS-home GBrain instance:

```text
tool repo: /home/galyarder/gbrain
data repo: /home/galyarder/brain
DB:        /home/galyarder/.gbrain/brain.pglite
CLI:       /home/galyarder/.bun/bin/gbrain
```

The old Galyarder profile-local duplicate was archived. From the Galyarder Hermes profile, `gbrain` is a wrapper that forces `HOME=/home/galyarder` and executes `/home/galyarder/.bun/bin/gbrain`.

Do not recreate a profile-local GBrain unless Galih explicitly asks for isolated profile-local brain state.

## When To Use

Use this skill when the request involves:

- "gbrain", "brain", "personal brain", "project brain", or DB-backed memory
- importing notes/markdown into GBrain
- searching/querying the brain
- checking GBrain health, migrations, stats, embeddings, or skillpack
- deciding whether to use GBrain vs Hindsight vs Hermes memory vs Obsidian
- GBrain minions/autopilot/cron-like behavior
- GBrain local OpenAI-compatible embeddings / 9Router

## Routing Decision

Use this split:

```text
Need durable fact about user/preferences/environment? -> Hermes memory / Hindsight retain
Need recall of past conversations? -> session_search / Hindsight recall
Need long-form notes/vault files? -> Obsidian skills
Need project-scale markdown brain for Claude Code/coding agents? -> GBrain
Need DB-backed markdown brain search/query over /home/galyarder/brain? -> GBrain
Need software-factory QA/review/ship/browser workflow? -> gstack, not GBrain
```

GBrain is useful, but it is not the first tool for every memory request. Galih's default intent is to use GBrain as a **project-scale brain for Claude Code / coding agents**, not as the main OS memory layer. Prefer GBrain for repo/project context, imported operational markdown, implementation decisions, and agent/minion experiments. Do not route quick recall ("lu inget gak kemarin?"), simple preferences, or transient chat/session questions into GBrain unless Galih explicitly asks.

## Safe Commands

Run from any profile with the canonical wrapper/path:

```bash
gbrain --version
gbrain stats
gbrain doctor --json
gbrain skillpack-check
gbrain search "<query>"
gbrain query "<question>" --no-expand
```

For import/embed work:

```bash
gbrain import /home/galyarder/brain --no-embed
gbrain embed --stale
gbrain stats
```

Before embedding, verify local OpenAI-compatible routing if needed. Use `gbrain` reference `` and `qdrant-vector-search` notes.

## Approval Gates

Ask before:

- enabling/installing GBrain autopilot or recurring jobs
- running GBrain internal `skillpack install --all`
- destructive DB resets, migrations beyond normal `apply-migrations`, or deleting brain files
- bulk imports/embeddings that may cost API credits or mutate many records
- syncing/exporting private brain content externally

## Verification Checklist

Before claiming GBrain works, verify with fresh outputs:

```bash
command -v gbrain
gbrain --version
gbrain stats
gbrain doctor --json
gbrain skillpack-check
```

Healthy expected baseline after 2026-05-12 dedupe:

```text
version: gbrain 0.26.0
stats: 21 pages, 42 chunks, 42 embedded
skillpack-check: healthy true
migrations: all up to date
doctor: warnings acceptable if resolver_health warns outside repo cwd; embeddings should be OK
```

## Related References

- `gbrain/references/gbrain-profile-dedupe-2026-05-12.md` — canonical path and archived duplicate details.
- `gbrain/references/gbrain-agent-setup.md` — setup protocol.
- `gbrain/` — local embedding gateway pattern.
- `gstack-local` — gstack vs GBrain vs Hermes cron distinction.

## References & Sub-playbooks
- `references/gbrain.md` — Custom BM25 local hybrid search parameters
- `references/gbrain.md` — Interactive visual graph servers via Cloudflare tunnels
- `references/gbrain.md` — Compiling wiki knowledge directories and folder links
- `references/gbrain.md` — Drafting papers for academic conferences (NeurIPS/ICML)
