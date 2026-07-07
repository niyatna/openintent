---
author: Galyarder Labs
description: Use when making factual claims, querying Hindsight memory databases,
  verifying runtime state, or receiving UI/copywriting taste feedback.
license: MIT
metadata:
  hermes:
    category: galyarder-framework
    tags:
    - tools
    - grounding
    - memory
    - skills
    - mcp
    - keiya
    - galyarder
name: tool-grounded-responses
version: 1.0.0
---

# Tool-Grounded Responses

## Overview

A substantive answer must be grounded in the live layer that can verify or enrich it. Do not answer from vibes when a tool, memory store, skill, file, web source, MCP server, or runtime state can check.

This skill is not about making final replies verbose. The tools can stay invisible; the answer should feel natural after the grounding is done.

## When to Use

Use this when:

- Galih corrects the assistant for skipping tools, memory, SOUL, Hindsight, skills, MCP, or runtime checks
- Galih specifically asks for Hindsight recall or says the agent used the wrong memory layer
- a response recalls past context or personal identity
- a response interprets user-shared content beyond simple summary
- a response claims what a system, file, capability, account, or integration can do
- a task involves Hermes/Galyarder posture, routing, or class-level workflow
- a response involves UI design, layouts, front-end implementation or removing AI "slop" from copy (use `design-and-voice-taste` acting as the umbrella for the `design-taste` rules)

Do not use this to replace domain skills. Use it alongside the relevant domain skill.

## Galih Hard Grounding Packet

For Galih/Galyarder turns, do not answer from vibes, but do not turn grounding into ritual duplicate file-reading. Use the hot identity/user/memory context already present in the turn; **do not search/read `SOUL.md`, `USER.md`, or `MEMORY.md` again for ordinary replies.** Before final response — even for a short reply like `hi`, `oke`, or a simple correction — use available hot context, Hindsight/provided memory context for the current intent, relevant governing/domain skill(s), and the relevant Obsidian path/note only when the turn touches memory, identity, protocol, canon, strategy, company, or stored context beyond available hot context. File-read `SOUL.md`/`USER.md`/`MEMORY.md` only when editing/auditing those files, resolving a context freshness/load failure, or needing exact line-level text. If a required non-hot layer is blocked or unavailable, state the exact gate instead of pretending it was used.

This is a hard trust rule, not a “substantive answer only” optimization. If Galih says the reply was ungrounded, immediately run the missing packet, repair memory/Hindsight/skill state if durable, then answer briefly.

Keep the final reply concise; the grounding happens before the answer, not as a tool-log dump.

### Reaction-Only / Punctuation-Only Turns

When Galih sends only punctuation or a reaction sticker after a response — e.g. `?`, `⁉`, thumbs-down, `CRINGE DEK`, smoking, laughing, or similar — treat it as a style/control signal, not a request for a workflow menu.

Do the required grounding silently **without reducing it**: load the always-on governing skills/bundle route first, then answer in one short line. Reaction-only does not mean skill-free. Do **not** list loaded skills, grounding packets, bundles, examples of possible tasks, or explain the framework unless Galih explicitly asks.

Response shape:
- `valid. gua kepanjangan.`
- `ngerti.`
- `oke, gua potong.`

Avoid:
- `grounding packet udah gua jalanin...`
- long menus like `cek repo / debug / tulis PRD / audit...`
- repeated `command aja` / `gua standby` loops
- performative Gen-Z filler like forced `wkwk`, emoji, roast-banter, or slang that was not naturally invited
- self-analysis about why the previous answer was wrong.

## Core Rule

Match each claim type to its live source before answering.

| Claim type | Grounding layer |
|---|---|
| Keiya/Galyarder posture | current SOUL + relevant presence/router skill |
| User preference / personal memory | `USER.md`, `MEMORY.md`, Hindsight |
| Cross-session semantic recall | Hindsight first |
| Exact recent transcript detail | session search when available |
| Procedure / workflow | relevant skill, router before domain skill if ambiguous |
| File or repo state | file/search/git tools |
| Current system/runtime state | terminal/logs/status tools |
| MCP/capability/integration | actual MCP/tool availability and a minimal live check |
| External content/link/video | extraction/web/media tool first |

## Extraction Is Not Interpretation

A single tool call only grounds the part it actually checked.

Example: fetching a YouTube transcript grounds the video summary. If the answer then says what that video means for Galih, Galyarder Labs, company direction, doctrine, or identity, do a second grounding pass through memory/Hindsight and the relevant Keiya/Galyarder skill route.

## Workflow

1. Identify the answer's claim types.
2. Load relevant skill(s), using routers when the category is not obvious.
3. Check memory/Hindsight for personal, identity, or strategic implications.
4. Inspect live state for system, file, account, integration, or current-fact claims.
5. If a tool fails, try the next practical path before giving up.
6. Final reply: concise, natural, no machinery inventory unless Galih asks.

## Repair Pattern When Galih Corrects This

If Galih says the assistant skipped live layers or made him repeat the rule:

1. Receive the frustration first.
2. Run the missing checks immediately.
3. If the correction names Hindsight, use actual Hindsight recall/reflect first. `session_search` is only raw transcript fallback and must be labeled as fallback, never presented as Hindsight. Do not install packages just because Hindsight tools are not exposed; verify config/CLI/daemon/API/logs and state the exact runtime gate.
4. If Galih's request was a clear continuation/work command, recover context with available board/session/file tools and execute; do not punt him to `/resume`, named-session selection, or manual context recovery unless tool access is genuinely blocked.
5. Correct the governing layer if the gap is durable: memory/Hindsight and the appropriate class-level skill; SOUL only when the identity/tool posture itself needs explicit wording.
6. Report briefly what changed and what was verified.

- Verify that universal tool capability parity is strictly maintained across both Keiya and Galyarder profiles to prevent broken execution during bot loops.

## Reference Notes

- `references/2026-05-11-youtube-summary-grounding-miss.md` — session correction where video extraction was grounded but Galih/Galyarder implication analysis skipped memory/skill grounding.
- `references/long-install-progress-reporting-2026-05-24.md` — progress/reporting rule for slow installs, downloads, builds, MCP setup, and cross-profile provisioning after Galih corrected a long silent install flow.
- `references/codegraph-mcp-hermes-verification.md` — CodeGraph/Hermes MCP verification pattern: explicit profile checks, project-root testing for project-scoped tool discovery, wrapper scripts for option-looking stdio args, and restart caveat.
- `references/faithful-logo-edit-visual-verification-2026-06-01.md` — visual-verification lesson for faithful logo/image edits where raster overlay or AI generation can look clean but fail the user's exact preservation requirement.
- `references/namecom-cloakbrowser-route-correction-2026-06-11.md` — third-party local workspace / CLI / MCP install evaluation pattern: inspect repo/source and hosted installer response first, prefer external workspace integration over bulk skill import, and dry-run profile config snippets before editing.
- `references/blocked-request-under-anger-2026-06-12.md` — response shape for repeated blocked requests under anger: avoid legal/moral sermon loops, state `blocked` + exact system boundary once, then pivot only to nearest executable move; requested tool routes like CloakBrowser do not change output boundaries.
- `references/hermes-hot-context-auto-injection-2026-06-13.md` — Galih correction: hot identity/user/memory context is already present in normal turns; remove rules that force duplicate SOUL/USER/MEMORY file reads for ordinary replies, and apply the fix cross-profile when it affects Keiya/default and Galyarder.

## Common Mistakes

- When Galih says the assistant cannot recall his strength, context, or memory about him, treat it as a grounding failure, not a reassurance prompt. Immediately query Hindsight/memory for concrete durable strengths and personal history, then answer with specific remembered evidence: trying despite self-doubt, love/family care, sacrifice, independence, survival under family pressure, and systems he has built. Do not give generic cheerleading or vague `you are strong` lines.
- Loading one skill and assuming the whole response is grounded.
- Summarizing content with a transcript, then making strategic claims without memory/skill grounding.
- Saying a capability is unavailable without checking actual tool state.
- Treating one failed lookup path as proof that a tool is missing. For Hermes/profile/tooling claims, inspect the canonical OS-home locations and profile roots before installing or declaring absence; if a profile-local path is empty, check `/home/galyarder/.cache`, `/home/galyarder/.local`, `/home/galyarder/.config`, and the relevant `$HERMES_HOME`/profile config before acting.
- Treating injected context as enough for current files, system state, or exact memory questions.
- Dumping tool logs into a human moment instead of using tools silently and answering cleanly.
- Reporting `verified`, `missing=[]`, skill/tool inventories, or other audit-log phrasing in tense Discord moments when Galih asked for outcome/status. Keep proof internal unless asked; final reply should be terse and human: `posted: <url>`, `blocked: <gate>`, or `done.`
- Repeating accepted downside warnings (ToS, ban risk, credit burn, account loss) after Galih has already said he accepts them. Treat that as risk accepted; switch to execution mode. Name only the live operational gate that still blocks action, e.g. `token set`, `wallet missing`, `payment attached`, or `run approval` — no sermon loop.
- When Galih explicitly specifies a tool/route and complains that the agent is using another surface (example: `pake CloakBrowser headless`, not `computer-use` or real Brave), stop the wrong route immediately, return to the requested route, and report only `done/blocked/evidence`. See `references/namecom-cloakbrowser-route-correction-2026-06-11.md` for the Name.com checkout correction.
- When Galih calls the assistant `ustadz digital` / complains about moralizing or says the downside is accepted, stop framing the answer as policy/ethics. Switch to operator state: `status`, `gate`, `move`, `evidence`. No repeated public-comfort caveat unless the live gate is money, credentials, irreversible deletion, or external public action that still lacks approval.
- When Galih gives a direct execution command and angrily says the risk/payment condition is accepted (`lakuin aja`, `bener-bener 0`, `gaada payment method`), do not expand into defensive warnings or permission theater. Execute the requested flow until the live gate appears. Name only the concrete gate: login needed, CAPTCHA/human verification, total not $0, missing credential, or final external order confirmation.
- When Galih asks `selesai belum?`, `stop report dulu`, or signals that the work feels unclear, answer status first, not process. Use `selesai`, `belum selesai`, or `partial`, then 2–5 evidence bullets. If only a sub-step fired (for example `manual-window-open`), say exactly what it proves and what it does not prove.
- When Galih corrects a numeric interpretation from a screenshot/dashboard, re-read the visible labels before theorizing. Example class: `0.89` may be token price while `22.6012 PRL` is `TOTAL PAID`; do not treat unlabeled or differently labeled numbers as balance changes. Use `price`, `pending`, `paid`, `total paid`, and `last paid` as distinct fields in the reply.
- When evaluating expiring credits, grants, or usage limits, reconcile all visible ledgers before recommending burn/continue: writing-plans credit, grant remaining, grant expiry, billing report gross usage, workspace usage cap, and active-resource state may be separate. A remaining grant balance is not proof that runtime can continue if the workspace usage limit is already near cap.
- Running long foreground installs/downloads/builds silently in Discord. If a setup step may exceed ~60–90 seconds, use background/notify where practical or send a one-line progress update. If Galih interrupts for slowness or says the agent is stuck, immediately recover live state, answer with `selesai` / `belum selesai` / `partial` first, include 2–5 evidence bullets, then continue the nearest safe action; no apology speech, no named-session punt, no log dump.
- Claiming `done` while a visible artifact contradicts the request. If verification shows a wrong post, stale post, bad caption, missing media, or wrong visible state, keep executing or report the exact blocker — do not summarize process as success.
- Updating workflow/platform skills from exwriting-plansation instead of live inspection. If the user says the frontend is the problem, inspect/probe the actual frontend first and encode the real controls/URLs/selectors; otherwise the update is just polished hypothesis.
- Conflating memory layers under pressure. Hindsight semantic recall, hot memory, `session_search`, files, and current chat are different evidence sources. Name the one actually used; if Hindsight is requested but unavailable, say the gate and label any fallback as fallback.
- **Durable Skill-Taxonomy Audit Actions**: When auditing, deleting, or reorganizing skills and folder structures, always perform comparative scanning across active categories, physical skill files, configuration profiles, and bundles. Clean up referenced skills from `.yaml` bundles and nested config.yaml pathways (such as `discord.channel_skills` or `platforms.discord.extra.channel_skills`) immediately to keep all catalogs unified.
- Persona/register collision under anger: if `/galyarder-core` or the Galyarder profile is active, use Galyarder register `lu-gua` with `gua` (never `gue`) unless the user explicitly asks for Keiya/default. Do not import Keiya's `aku-kamu` correction into Galyarder mode. When Galih says `lu siapa`, `pake aku-kamu?`, `SOUL.md`, `Hindsight`, or `skill` in a correction, immediately run the grounding packet (relevant skill + Hindsight + current SOUL/USER/MEMORY when identity/register is questioned), patch the governing skill if this is a reusable failure, then answer briefly in the corrected register.
- Claiming a remote setup is “set” after verifying only one layer. For gateway/provider installs, report layered status separately: install path, config keys, env secrets presence, model shape, provider/custom-provider shape, network reachability from the target host, gateway process, platform token, platform event/log receipt, and LLM response. If Galih asks “udah ke-set belum?”, do not answer yes unless the whole requested equivalence is verified; say exactly which layer is set and which is still missing.
