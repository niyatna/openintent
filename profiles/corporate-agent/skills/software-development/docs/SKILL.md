---
author: Company
description: Use when executing writing manuals, readmes, and codemaps.
license: MIT
metadata:
  hermes:
    category: software-development
    tags:
    - default-framework
    - docs
    - documentation
    - content-architecture
name: docs
version: 1.1.0
---

# Docs

Use this skill when writing, updating, auditing, or syncing documentation, READMEs, codemaps, source-aligned docs, public guides, docs-site content, or content architecture.

## Core rule

Preserve the user's requested **content model** unless they explicitly ask to change it.

A request to `rewrite`, `improve`, `make more complete`, `add what is missing`, or `make it more advanced` usually means:

- keep the existing active docs/pages/slugs/navigation unless the user says to restructure;
- rewrite the current pages in place;
- integrate missing concepts into the existing structure;
- add sections inside existing files before adding new files;
- only add new docs/pages when the current structure cannot hold the required concept;
- never archive/delete/rename existing pages as a side effect of a rewrite unless explicitly approved.

Do not turn a content rewrite into a new IA/site rebuild by default.

If the source/canon explicitly provides a public IA with better chapter names, treat that as an intentional **controlled rename** request once the user confirms the old names do not fit. In that case, rename slugs/titles deliberately while preserving useful body content, and update metadata, i18n, nav, footer, links, and build routes together. Do not keep stale implementation-shaped names just because preserving slugs was the first recovery move.

## Required workflow

1. **Inspect current content model first**
   - list active docs/pages/slugs;
   - identify routing/source-of-truth files (`docs.ts`, content directory, i18n files, nav/footer/site copy);
   - identify generated/build output directories and do not edit them manually.
2. **Read the source/canon docs**
   - use the actual source docs, not memory or summaries;
   - for Company/public guides, read relevant Obsidian/canon files before judging content.
3. **Classify requested change**
   - in-place rewrite;
   - additive section expansion;
   - additive new page;
   - IA restructure;
   - visual/design change.
4. **Protect active slugs — or rename them deliberately**
   - before editing, record active page slugs/files;
   - after editing, verify the active slug set is unchanged unless restructure/rename was explicitly requested or source IA clearly supersedes the old names;
   - if renaming, keep a mapping of old slug -> new slug and update every route/link/i18n/nav/footer reference;
   - if new docs were added, confirm they are intentional additions from the source IA, not accidental replacements.
5. **Rewrite content, not only metadata**
   - update markdown body copy;
   - update doc metadata/titles/descriptions/sections;
   - update i18n/localized content if the site has locale switching;
   - update nav/home/footer only where the old framing leaks.
6. **Verify**
   - run the docs build/check if available;
   - scan for required source concepts;
   - scan for forbidden/framing terms when the user gave language constraints;
   - verify no generated output was hand-edited as source;
   - verify rendered output, not only source markdown, especially when a docs site uses dynamic imports, content manifests, generated `dist/`, generated detail pages, or locale-specific body overrides that can mask expanded source content;
   - for generated sites, inspect `git status --short`, additions/deletions, and generator source discovery before staging; unexpected mass deletions/additions mean diagnose generator behavior and scope before commit/push;
   - for GitHub Pages claims, verify each surface separately: README/raw source, local rendered site, pushed commit, deploy workflow, pages-build-deployment workflow, and live Pages HTML;
   - preserve user-owned untracked/local work. Do not label an unrelated-looking workflow/config/script as noise until provenance is checked through `git status`, reflog/dangling commits, backup patches, and user intent. If a user says a local file was theirs, recover it first and treat it as in-scope state;
   - when the user explicitly broadens scope from README/docs copy to whole-codebase positioning, do not over-narrow back to a small docs-only diff. Treat generated docs, integrations, commands, agent files, editor rules, and package metadata as valid surfaces while still preserving technical identifiers and product truth.

## Public guide / Obsidian-source pattern

When converting Obsidian strategy/source notes into a public docs site:

- map source claims into the current page model first;
- keep public language human-first unless the section is explicitly technical;
- preserve exact technical names when they are real parts of the setup (`Hermes Agent`, `MCP`, `Paperclip`, config files, etc.);
- do not publish private paths, raw profile instructions, private memories, credentials, tokens, cookies, TOTP/backup codes, raw sessions, private Discord IDs, wallet private keys/seed phrases, or account recovery details;
- use templates/policies/examples instead of real private state.
- **Field-Manual Depth Formatting:** When requested to expand guides to "serious" or "field manual" depth, structure each page to be highly comprehensive (1,450+ words) using concrete, actionable sections instead of generic filler:
  - **Context/Philosophy:** Why this matters.
  - **Operating Loops:** Continuous cycles of telemetry, intervention, or state updates.
  - **Decision Rules/Policy Matrices:** Use tables to define exact boundaries (e.g., Action Classes, Privilege Escalation).
  - **Evidence Contracts:** Audit trails, logs, or cryptographic proof mechanisms required to verify execution.
  - **Checklists/Templates:** Exact operational steps and example records.
  - **Role Boundaries & Red-Team Checks:** Explicit limits of agent/human authority and simulated tests (e.g. Sabotage Test, Identity Drift Test) to verify isolation.
  - **Advanced Failure Taxonomies:** Symptoms, root causes, and remediations for complex failures (e.g. Psychological Capture, Context Bleed).
  - **Maturity Levels:** Progression (Level 1/2/3) from fragile manual setup to autonomous/enterprise state.
  - **Verification/Proof Gates:** Hard criteria to prove the work is complete.
- **Bulk Expansion Strategy:** When generating massive volume (e.g. 10,000+ words across 8+ files), use Python scripting and template injection rather than attempting to stream the edits in a single LLM output. This circumvents truncation limits and ensures fast, precise file patching.
- **Second-pass depth correction:** If the user rejects an expanded docs pass as still not advanced enough, do not defend the previous word count. Raise the target and add real operating depth: policy matrices, evidence contracts, red-team checks, failure taxonomies, maturity levels, operating loops, example records, and proof gates. For broad public guides, a useful advanced threshold is 1,450+ words per active page unless the page is intentionally narrow.
- **Quality-bar-first correction:** If a previous “advanced” pass feels fake, messy, or filler-heavy, do not mass-rewrite all pages immediately. First audit the actual source/rendered pages, name the quality failures, then rewrite 2–3 representative pages as the new quality bar. Each page must decide something and leave a usable artifact (matrix, checklist, scorecard, template, proof gate). Kill repeated taxonomy labels unless backed by page-specific substance. See `references/quality-bar-first-advanced-docs-rewrite-2026-05-23.md`.
- **Locale/body parity:** For bilingual docs, locale toggles must not silently render old short summaries after the canonical source pages are expanded. If the user asks to fix depth, remove shallow locale body overrides, replace them with parity content, or wire the locale to the expanded canonical body. Do not call the guide fixed while one visible locale remains outline-length.
- **Safe adversarial examples:** Public security/red-team docs may describe attack classes, but examples must be synthetic and bounded. Do not include realistic credential-exfiltration prompts, real-looking private paths, live domains, wallet addresses, or step-by-step account recovery abuse. Verify examples are safe patterns, not reusable attack payloads.

## Subagent delegation guard

If delegating docs/content rewrite work to a subagent:

- include the exact active file/slug list in the prompt;
- state whether restructuring is allowed;
- explicitly forbid archive/delete/rename of active docs unless requested;
- require the subagent to report active slugs before/after;
- verify the diff yourself before accepting the report.

Subagent reports are self-reports. A successful build does not prove the content model stayed aligned with the user's instruction.

## Common mistakes

- Treating `rewrite all content` as permission to replace the whole docs IA.
- Creating many new docs when existing pages should have been expanded.
- Archiving old docs and generating replacement slugs without approval.
- Updating `docs.ts` metadata but leaving markdown content thin or stale.
- Updating English while leaving i18n/localized content outdated.
- Editing `dist/` instead of source files.
- Reporting build success while the user's requested structure was broken.
- Reporting `partial` while the next step is still executable. In interrupted Discord/docs-site work, recover the real task from live chat/session context plus repo state, then keep executing until a real approval gate or blocker. See `references/discord-interruption-recovery-for-docs-work-2026-06-01.md`.
- Trusting named-session resume or stale compacted state instead of inspecting the actual repo/task state after a reset.
- Rushing generator regex rewrites and corrupting output with control characters such as `\x01`; verify generator snippets with `repr()`, compile/run the generator, and inspect rendered/output links before staging.
- Keeping stale implementation-shaped doc names after the user/source IA has made clear the public chapter names should change.
- Renaming markdown files without updating `docs.ts`, i18n metadata/content, nav/footer links, and static `/docs/<slug>/` references.

## Reference notes

- `references/default-framework-readme-repositioning-2026-06-01.md` — Default Framework README/repo-description pattern: reposition as an Agentic Company Framework / Intelligence Layer, preserve technical install/runtime content, remove edgy AGI/1-Man Army/public-cosplay tone, add trust badges, and verify raw README + docs deploy separately.
- `references/mkdocs-generated-site-repositioning-and-scope-control.md` — MkDocs whole-site rewrite pattern: separate authored pages, generated detail pages, and runtime source; inspect generator discovery before running it; sanitize copied support Markdown; verify parity, narrow staging scope, rendered HTML, deploy workflow, and live Pages separately.
- `references/discord-interruption-recovery-for-docs-work-2026-06-01.md` — interruption recovery pattern for docs/GH Pages work in Discord: recover real task state from session/chat, back up diffs, unstage/restore overbroad generated changes, fix generator regex corruption, respect cleanup approval gates, and report terse status-first evidence.
- `references/default-framework-agentic-company-repositioning-recovery-2026-06-01.md` — Default Framework-specific recovery lesson: preserve user-owned local files like publish workflows, recover from dangling commits when needed, respect broad codebase-wide Agentic Company repositioning when Owner confirms it, and verify source/rendered/live surfaces separately.
- `references/content-rewrite-without-ia-replacement-2026-05-22.md` — session pitfall where a docs rewrite was incorrectly delegated as replacement IA/new pages; recovery pattern preserves existing active docs and integrates advanced source material in place.
- `references/advanced-docs-depth-and-renderer-source-2026-05-23.md` — session pitfall where IA/slugs were correct but pages were too thin; includes field-manual depth targets, Astro raw-markdown manifest pattern, rendered HTML verification, and public-safety scans.
- `references/advanced-field-manual-expansion-1450w.md` — guidelines for achieving 1,450+ word field-manual depth (Operating Loops, Red-Team Checks, Failure Taxonomies) and using Python scripting for massive multi-file expansions.
- `references/advanced-agentic-company-docs-depth-2026-05-23.md` — second-pass Agentic Company docs correction pattern: 1,450+ word threshold, locale/body parity, Astro content manifest, and public-safety scans for advanced red-team/security examples.
- `references/quality-bar-first-advanced-docs-rewrite-2026-05-23.md` — correction pattern for fake-advanced docs: audit quality failures, rewrite 2–3 pages as a quality bar, require concrete page artifacts, and verify source + rendered output before propagating.
- `references/advanced-docs-fake-depth-quality-gate-2026-05-23.md` — quality gate for when docs are long but still feel fake/shallow: detect repeated expert-sounding skeletons, renderer/content-contract mismatch, language-lock drift, fake i18n parity, and require page-specific artifacts before rewriting further.
- `references/rendered-concept-contract-verification-2026-05-23.md` — verification pattern for advanced docs: define required page concepts, scan source and rendered HTML, patch missing operating primitives, then rerun build/crawl/leak checks before reporting completion.

## Completion checklist

Before saying docs work is complete:

- [ ] Active docs/pages/slugs match requested scope.
- [ ] Existing docs were rewritten in place when the user asked rewrite, not silently replaced.
- [ ] Required source concepts are present in content, not only metadata.
- [ ] Old/framing-forbidden terms are scanned where relevant.
- [ ] i18n/localized content is updated or explicitly marked as a remaining gap.
- [ ] Build/check passes, or exact blocker is reported.
- [ ] No private/secrets/raw personal state was introduced.
