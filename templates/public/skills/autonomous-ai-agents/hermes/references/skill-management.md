# Hermes Skills & Curation Management

### File: skills-hub-install-2026-05-12.md

# Skills Hub Curated Install — 2026-05-12

## Context

Galih authorized installing the best high-signal skills from the Hermes Skills Hub as reusable human-expertise knowledge for Keiya/Galyarder workflows, not installing every visible card indiscriminately.

Selection principle:

- prioritize agent ops, Hermes/MCP, browser/testing, docs/artifacts, codebase intelligence, security, finance modeling, MLOps/AI infrastructure, and creative/product pipeline;
- avoid mass-installing low-signal LobeHub persona prompts, macOS-only skills on Galih's Linux host, and generic duplicate “guru” skills.

## Install execution summary

From the prior visible-page audit, `69` skills were marked `perlu diambil`.

Final verification:

```text
VERIFY intended_perlu 69 installed_exact_by_frontmatter 69 missing_exact []
VERIFY local frontmatter name 3-statement present True
VERIFY path exists True
hermes skills list --source hub -> 56 hub-installed, 56 enabled
hermes skills list --source all -> 56 hub-installed, 84 builtin, 293 local, 431 enabled, 2 disabled
```

Artifacts produced during the session:

- `/tmp/hermes_skill_audit/install_skills.log`
- `/tmp/hermes_skill_audit/install_results.json`
- `/tmp/hermes_skill_audit/retry_*.log`
- `/tmp/hermes_skill_audit/force_*.log`

These are temporary and may not survive reboot; this reference captures the reusable lessons.

## Critical pitfalls discovered

### `hermes skills install` can exit 0 while doing nothing

Some failed installs returned process exit `0` while stdout contained errors such as:

```text
Error: No skill named 'teams-meeting-pipeline' found in any source.
Error: Could not fetch 'official/finance/xlsx' from any source.
```

Do not treat exit code alone as proof. After batch install, parse output for `Error:`, `Could not fetch`, `No skill named`, `Installation blocked`, `Failed`, or `Traceback`, then verify by reading local `SKILL.md` frontmatter names.

### Hub/index identifiers can inspect but fail to fetch

Some visible docs/API entries resolved through `hermes skills inspect` but `hermes skills install <short-name>` or `official/...` failed to fetch from the local/registered source.

Working fallbacks:

- Direct raw URL for NousResearch Hermes repo skills:
  - `https://raw.githubusercontent.com/NousResearch/hermes/main/skills/productivity/teams-meeting-pipeline/SKILL.md`
  - `https://raw.githubusercontent.com/NousResearch/hermes/main/optional-skills/finance/xlsx/SKILL.md`
- Explicit GitHub identifier for Anthropic skill:
  - `anthropics/skills/skills/mcp-builder`

### Direct raw URLs are treated as community source

Installing from a raw URL can cause the security scanner to mark even official/known source content as `community`, which may block caution/dangerous scans.

Use `--force` only after reading the scanner findings and deciding they are acceptable. In this session, force was used for:

- `teams-meeting-pipeline` — scanner flagged env/cron text in SKILL.md;
- `xlsx` / `powerpoint` — scanner flagged pip install instructions;
- `mcp-builder` — scanner flagged example evaluation/env/reference text.

### `--name` validation rejects names starting with digits

`hermes skills install <raw-url> --name financial-analyst` failed because `--name` must start with a letter. Workaround: install with a letter-starting folder/name override such as `--name three-statement-model`; the installed `SKILL.md` can still have frontmatter `name: financial-analyst`, and `skill_view` / `hermes skills inspect financial-analyst` can resolve by frontmatter.

## Verification recipe

After any curated skill install batch:

```bash
python - <<'PY'
import pathlib, yaml, csv
roots = [pathlib.Path('/home/galyarder/.hermes/skills'), pathlib.Path('/home/galyarder/.hermes/profiles/galyarder/skills')]
local = set()
for root in roots:
    if root.exists():
        for p in root.rglob('SKILL.md'):
            txt = p.read_text(errors='replace')
            name = p.parent.name
            if txt.startswith('---'):
                end = txt.find('\n---', 3)
                if end != -1:
                    try:
                        name = (yaml.safe_load(txt[3:end]) or {}).get('name') or name
                    except Exception:
                        pass
            local.add(name.lower())
# replace this with the intended list/CSV from the audit
print('local skill names:', len(local))
PY

hermes skills list --source hub | tail -5
hermes skills list --source all | tail -5
hermes skills inspect mcp-builder | sed -n '1,20p'
hermes skills inspect financial-analyst | sed -n '1,20p'
```

A successful batch requires exact frontmatter-name playwright-pro of the intended set, not just hub counts or installer exit codes.

### File: skills-hub-lobehub-curation-2026-05-12.md

# Skills Hub LobeHub curation correction — 2026-05-12

Use this reference when auditing or importing Skills Hub LobeHub/community skills for Galih/Galyarder.

## Correction captured

Initial mistake: treating LobeHub mostly as persona noise because it is less procedural than official/Anthropic skills.

User correction: some LobeHub skills are valuable as **human-expertise taste layers**, e.g. `gen-z`, marketing, copywriting, brand, social, trend, prompt/media, and market-voice skills. Do not blanket-skip LobeHub just because the source is community/persona-oriented.

Correct stance:

- Official/optional skills = procedural/tool capability.
- Anthropic skills = document/artifact/agent-building procedural capability.
- LobeHub/community skills = advisory human-expertise, market voice, internet-native taste, culture, copy, trend, and persuasion layers.
- Never mass-install all LobeHub. Curate.
- Never let LobeHub override canonical Galyarder doctrine, company docs, security boundaries, legal/financial verification, or procedural official skills.

## Curation workflow

1. Extract the full Skills Hub index, not just search results or visible categories.
2. Filter LobeHub with a broader human-expertise lens, not only a tool/workflow lens.
3. Prefer cross-work value:
   - Gen-Z/culture/trend sense
   - copywriting, advertising, TikTok/Xiaohongshu/short-form distribution
   - social media, brand, logo/visual content-generator
   - prompt/media generation taste
   - business communication, legal-style startup framing
   - website/content/GitHub/paper review
   - writing polish
4. Reject or defer:
   - roleplay/persona entertainment
   - medical/therapy/regulated advice without a real workflow
   - platform/region-only niche skills with no current Galyarder use
   - generic coding personas when stronger local/official skills exist
   - anything that increases router noise without adding a distinct taste lens
5. If scanner blocks a community skill, read the finding. Only `--force` when the source is understood and the finding is prompt-text/noise rather than executable risk. Record forced installs.
6. Report LobeHub as advisory layers, not authority layers.

## 2026-05-12 curated LobeHub set installed

Final verified status after correction:

- Local skills: 425
- Enabled: 382
- Disabled: 43
- Hub lock entries: 110
- Optional installed: 68
- Anthropic installed: 14
- LobeHub installed: 28 total
  - 26 normal LobeHub
  - 2 legacy/source-label `clawhub`

Curated LobeHub installed:

### Culture / Gen-Z / trend
- `gen-z`
- `copywriting`

### Copywriting / ads / conversion
- `advertising-copywriting-master`
- `copywriting`
- `amazon-listing-copywriter`
- `xiao-hong-shu-wenan-id`
- `xiaohongshu-style-writer`

### Social / brand / market voice
- `social-media-sage`
- `brand-pioneer`
- `mdx-seo`

### Visual / logo / prompt/media
- `logo-creativity`
- `svg-logo`
- `image-prompter`
- `ultra-flux-prompter`
- `flux-prompt-generator`
- `runway-gen-3-prompt-generator`

### Prompt engineering / structured prompt
- `json-prompt-generator`
- `prompt-architect`

### Business / comms / legal-style
- `business-guru`
- `business-email`
- `tech-lawyer`

### Research / analysis
- `tech-explorer-ai`
- `website-audit-assistant`
- `web-github-analyze`
- `paper-understanding`

### Writing / polish
- `resume-editing`
- `grammar-corrector`
- `essay-improver`

## Scanner notes from this session

Initially blocked, then force-installed after reading scanner findings:

- `xiao-hong-shu-wenan-id` — zero-width joiner / prompt-text finding
- `json-prompt-generator` — prompt example flagged as exfiltration-like text
- `prompt-architect` — reference text flagged as exfiltration-like text
- `essay-improver` — instruction wording flagged as exfiltration-like text

Treat forced community skills as advisory. Do not use them to authorize external actions, legal/financial advice, secrets handling, or security-sensitive operations.

## Future reporting language

Use this framing:

> Do not mass-install all LobeHub. But do not blanket-skip it either. Curated LobeHub is useful as a market/culture/taste layer; official and Anthropic skills remain the procedural execution layer.

If Galih challenges a classification, re-audit with the human-expertise lens before defending the previous filter.

### File: skills-hub-live-audit.md

# Hermes Skills Hub live audit

Use this when Galih asks to list/extract all skills from `https://hermes.nousresearch.com/docs/skills`, compare them against the active profile, and classify what to install.

## Session finding

The Skills Hub page is a Docusaurus/React app. A browser snapshot only shows the visible cards; it does **not** prove the full skill index was extracted. In the May 2026 run, the page reported:

- total remote skills: 687
- sources: built-in 87, optional 79, Anthropic 16, LobeHub 505
- local profile inventory: 317 skill directories from the active Galyarder profile filesystem, 274 enabled, 43 disabled
- exact remote/local name overlap: 87
- remote missing by exact name: 600

Treat these counts as historical evidence, not constants. Recompute live each time.

## Workflow

1. Load `hermes`, browser routing, Camofox, and verification skills first.
2. Open the page with Camofox/native browser for live proof:
   ```text
   browser_navigate("https://hermes.nousresearch.com/docs/skills")
   ```
3. Do **not** rely on the viewport/snapshot to enumerate all skills. Use it only to verify the page loaded and the advertised total/source counts are visible.
4. Extract the actual skill index from the Docusaurus JS bundle. The useful bundle contains a `JSON.parse('...')` payload with every skill card. A robust extraction pattern is:
   ```python
   import ast, json, re, requests

   js = requests.get("https://hermes.nousresearch.com/docs/assets/js/b5cfa250.f36c58aa.js", timeout=60).text
   m = re.search(r"JSON\\.parse\\('((?:\\\\.|[^'])*)'\\)", js)
   skills = json.loads(ast.literal_eval("'" + m.group(1) + "'"))
   ```
   If the chunk hash changes, inspect browser network resources or search fetched JS assets for `apple-notes` and `JSON.parse`.
5. Inventory local skills from the active profile filesystem, not only the rendered CLI table. For Galyarder, the runtime root is usually:
   ```text
   /home/galyarder/.hermes/profiles/galyarder/skills
   /home/galyarder/.hermes/profiles/galyarder/config.yaml
   ```
   Parse `skills.disabled` from config to separate installed-enabled from installed-disabled.
6. Compare by exact `name` first, then manually account for semantic overlap. Exact-name overlap misses local umbrella replacements such as Galyarder-specific framework, growth, finance-legal, security, and QA skills.
7. Classify missing remote skills into:
   - `ambil`: high ROI, official/optional/Anthropic, directly useful for Hermes/dev/research/ops/ML/document workflows.
   - `optional`: situational, platform/tool-specific, or community skills worth inspecting only when a use case appears.
   - `ga_perlu`: low-signal LobeHub/persona skills, macOS-only skills on Linux hosts, translation/roleplay/general persona noise, or redundant skills already covered by stronger local umbrellas.
8. Write raw artifacts to `/tmp` and attach them in Discord if needed:
   ```text
   /tmp/hermes_skills_audit.json
   /tmp/hermes_skills_audit.md
   ```
9. Verify before reporting: JSON exists, Markdown exists, remote count equals parsed list length, classification counts sum to missing count, and Camofox health still answers.

## Classification policy

Default policy for Galih/Galyarder:

- Do **not** mass-install the 600 missing remote skills.
- Do **not** blanket-skip LobeHub. It often loses as procedural tooling, but it can add valuable human-expertise/taste layers for culture, Gen-Z, copywriting, social media, brand, trends, and prompt/media work. Curate instead of dismissing.
- Do **not** install LobeHub/persona packs by default. They create router noise and usually lose to local class-level Galyarder skills unless they add a distinct market/culture/taste lens.
- Do not install macOS-only built-ins (`apple-notes`, `apple-reminders`, `findmy`, `imessage`, `macos-computer-use`) on the Linux/CachyOS host unless Galih explicitly introduces a macOS workflow.
- Keep disabled design-system skills disabled unless a specific brand/reference is being used.
- Ask before mutating the skill library. Audit/extraction is read-only; install/update is a side effect.

High-value missing categories to consider first:

- Dev/tools: Docker, FastMCP, REST/GraphQL debug, codebase graph, watcher/polling utilities.
- Research/extraction: DuckDuckGo/SearXNG/Parallel/Scrapling/domain intelligence.
- Security/ops: supply-chain forensics, 1Password, Sherlock when OSINT is explicitly in scope.
- MLOps: PEFT, Accelerate, Tokenizers, Chroma/FAISS/Qdrant/Pinecone, Instructor/Guidance, Whisper, CLIP/LLaVA.
- Documents: Anthropic `pdf`, `xlsx`, `xlsx`, `pptx`, coauthoring, theme/artifact skills.
- LobeHub/community: do not mass-install, but do not blanket-skip. Curate high-signal market/culture/taste layers such as `gen-z`, copywriting/ads, social media, brand, TikTok/Xiaohongshu, logo/visual content-generator, prompt/media, business communication, and writing polish.

Reference: `references/skills-hub-lobehub-curation-2026-05-12.md` records the correction that LobeHub should be evaluated as a human-expertise/advisory layer, not only as procedural tooling.

## Camofox pitfall observed

`browser_navigate` may fail with `500 Server Error ... /tabs` while `curl /health` returns `ok: true` but `browserConnected:false` / `browserRunning:false`. This means the Camofox server is alive but no browser is attached. See `hermes-camofox-browser` for the recovery checklist; do not conclude the website is unreachable from the first `/tabs` failure.

## Minimal verification commands

```bash
python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('/tmp/hermes_skills_audit.json').read_text())
assert j['summary']['remote_total'] == len(j['remote_skills']) if 'remote_skills' in j else j['summary']['remote_total'] > 0
assert j['summary']['missing_class_counts']['ambil'] == len(j['missing_take'])
assert j['summary']['missing_class_counts']['optional'] == len(j['missing_optional'])
assert j['summary']['missing_class_counts']['ga_perlu'] == len(j['missing_unneeded'])
print('skills audit counts ok')
PY
curl -fsS --max-time 5 http://localhost:9377/health
```

### File: approved-prune-cleanup-pattern-2026-05-18.md

# Approved prune cleanup pattern — 2026-05-18

## Context

Galih asked for a skill-library audit focused on redundant and low-value skills, then gave explicit cleanup decisions. The correct behavior was direct execution, not more debate.

## Durable pattern

When Galih approves a skill cleanup list:

1. Treat it as authorization for the named non-destructive skill moves.
2. Execute directly with minimal visible wording.
3. For delete/merge actions, archive skill directories to a timestamped rollback path before removing from active tree.
4. If Galih says `delete but improve X`, patch the canonical umbrella first, then archive/delete the narrow skill.
5. If Galih says `merge`, preserve the old SKILL.md as `references/absorbed-<skill>-<date>.md` under the target umbrella, add a one-line pointer in the target SKILL.md, then archive the source skill.
6. Respect explicit keep overrides even if the heuristic says prune.
7. Verify before reporting: active skill count, unique names, duplicate names, bad frontmatter, deleted skills absent, kept overrides present, newly created skills present, and representative `skill_view` loads for patched/created skills.

## Galih-specific cleanup preferences observed

- He prefers class-level umbrella skills, not many narrow one-session or one-prompt skills.
- For redundant prompt skills, improve canonical skills such as `copywriting`, `content-generator`, `copywriting`, `superdesign`, and resume skills rather than keeping tiny stubs.
- LobeHub is not automatically bad; curate by value. Delete generic/stub skills, keep unique taste/procedure skills.
- Avoid yapping after approval. Run the operations and return verified counts.

## Known pitfall

Heuristic alias detection can false-positive on canonical skills that mention `source of truth`. Do not prune protected baseline/router skills from heuristic output. Manual review is mandatory before recommending deletion.

### File: design-skill-stack-bundles-2026-05-31.md

# Design skill stack and lean bundles (2026-05-31)

## Trigger

Galih asked whether the installed `design-taste` / `taste` design skills were actually bundled correctly. A Threads post then surfaced the current external design-agent stack:

- Impeccable — `design-taste.style`
- Taste Skill — `tasteskill.dev`
- Layers — `layers.jamiemill.com`
- Superdesign — `app.superdesign.dev`

The correction: the local library had strong visual/frontend taste skills, but lacked the product-design decision layer (`layers-*`) and Superdesign canvas workflow. The broad `/creative` bundle was too noisy to use as the default design route.

## Correct target shape

Keep `/creative` as a category bundle only. Normal design routing should use lean route bundles:

| Bundle | Purpose | Skills |
|---|---|---|
| `product-design-thinking` | Product/UX decision work before surface polish | `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking`, `product-design-thinking` |
| `design-taste-core` | Default UI/frontend design and polish | `design-taste`, `design-taste`, `design-taste`, `design-taste`, `design-taste`, `verification-before-completion` |
| `frontend-style-variants` | Push visual direction and escape generic UI | `design-styles`, `design-styles`, `design-styles`, `design-taste`, `web-widgets`, `design-styles` |
| `design-canvas-and-visual-gen` | Design comps, canvas workflows, brand boards, image references | `superdesign`, `superdesign`, `superdesign`, `superdesign`, `superdesign`, `diagram-design` |

Routing rule: `galyarder-core` first, then one of these lean design bundles or the exact skill. Do not default to `/creative` unless Galih explicitly wants the whole creative folder/category context.

## Install pattern for external design packs

If repo-level install fails, do not stop at the failed repo identifier. Install raw `SKILL.md` URLs one by one after source review and security scan output.

Example shape:

```bash
HOME=/home/galyarder hermes --profile galyarder skills install \
  https://raw.githubusercontent.com/jamiemill/layers-skills/main/skills/product-design-thinking/SKILL.md \
  --category creative --yes

HOME=/home/galyarder hermes --profile galyarder skills install \
  https://raw.githubusercontent.com/superdesigndev/superdesign-skill/main/skills/superdesign/SKILL.md \
  --category creative --yes
```

For Layers, install all 9 `layers-*` skill files individually. For Superdesign, install `skills/superdesign/SKILL.md`.

Important: installer command can exit `0` while printing `Error: Could not fetch`. Read stdout, not just exit code.

## Bundle/catalog update pattern

After installing new skills:

1. Regenerate the relevant category bundle and `_catalog` entry so `/creative` and `_catalog/creative.yaml` reflect the installed skills.
2. Create lean route bundles under `skill-bundles/*.yaml`; do not add these as mandatory baseline.
3. Patch `galyarder-framework-router` with the design routing hotbar, not each hub-installed design skill.
4. Avoid editing hub-installed or bundled skills directly. Wrap them with local bundles/router outlines or a local class-level skill/reference.

## Cross-profile propagation pattern

When Galih asks whether the new design skills are also in Keiya/default, do not assume parity from prior taste/design-taste sync. Verify both active roots separately:

- Galyarder profile skills: `/home/galyarder/.hermes/profiles/galyarder/skills`.
- Keiya/default skills: `/home/galyarder/.hermes/skills`.
- Galyarder profile bundles: `/home/galyarder/.hermes/profiles/galyarder/skill-bundles`.
- Keiya/default bundles: `/home/galyarder/.hermes/skill-bundles`.

If the user says to add the new design layer to Keiya/default, copy the 9 `layers-*` skills plus `superdesign` into Keiya/default `skills/creative/`, copy the four lean design route bundles into Keiya/default `skill-bundles/`, regenerate Keiya/default `/creative` and `_catalog/creative.yaml` from actual `skills/creative/**/SKILL.md` frontmatter names, and patch `keiya-capability-router` with a concise design route hotbar. Do not mass-sync all Galyarder-only skills or overwrite Keiya posture.

Keiya/default design route hotbar should mirror the capability, not the persona: `product-design-thinking` for product/UX decision debt, `design-taste-core` for normal UI polish, `frontend-style-variants` for visual-direction variants, and `design-canvas-and-visual-gen` / `superdesign` for comps, brand boards, and image-reference workflows. Keep `/creative` as an intentional whole-category bundle only.

## Verification pattern

Minimum proof before reporting done:

```bash
HOME=/home/galyarder hermes --profile galyarder bundles list
HOME=/home/galyarder python -m pytest tests/agent/test_skill_bundles.py -q -o 'addopts='
```

Then run a Python validator that checks:

- all `SKILL.md` frontmatter parses;
- all skill names are unique;
- all target design skills exist by frontmatter name;
- every root `skill-bundles/*.yaml` skill reference resolves;
- new design bundles have the exact expected member lists;
- no newly installed design skill is listed under `skills.disabled`.

For bundle invocation smoke tests, use `reload_bundles()` before `build_bundle_invocation_message(...)`; `get_skill_bundles(force_reload=True)` is not the current API shape.

## Pitfalls

- `hermes skills list` table truncates long names like `design-taste`; use `skill_view` or local frontmatter parsing for exact proof.
- Superdesign's description is close to the 1024-character frontmatter limit; validate description lengths after install.
- `creative` is useful as a category inventory but is context-noisy as a default design mode.
- Layers is a decision layer, not a visual taste layer. Use it when UX/product decisions are unresolved, not as a substitute for Impeccable/Taste visual polish.

### File: local-skill-loadability-vs-registry-inspect-2026-05-21.md

# Local skill loadability vs registry inspect — 2026-05-21

## Trigger

During a Paseo skill-library update, local `paseo` skill visibility produced a confusing split:

- `skill_view("paseo")` loaded the active local skill successfully.
- `hermes --profile galyarder skills list --source all` and `hermes --profile default skills list --source all` showed local `paseo` enabled.
- `hermes --profile <profile> skills inspect paseo` returned `No skill named 'paseo' found in any source`.

## Lesson

For local/personal skills, `hermes skills inspect <name>` may behave like a hub/registry preview path, not the same loader path used by runtime skill invocation. Do not treat `inspect` failure as proof the local skill is unavailable when `skills list` and `skill_view` prove otherwise.

## Recommended verification ladder

For local skill edits:

1. Parse local `SKILL.md` frontmatter directly if file tools are available.
2. Use `skill_view(<name>)` as the strongest runtime loadability check inside Hermes.
3. Use `hermes --profile <profile> skills list --source all` to confirm installed/enabled visibility in each target profile.
4. Use `hermes skills inspect <name>` only for hub/registry preview checks unless current Hermes docs/source prove it reads local skills.

## Reporting rule

When this split appears, report it as a command-surface distinction, not as a broken skill. Example:

`skill_view + skills list prove the local skill is enabled; skills inspect appears registry-oriented here, so it is not the completion oracle for local skills.`

### File: local-skill-package-zip-install-2026-05-25.md

# Local Skill Package Zip Install — 2026-05-25

## Trigger

Galih uploads a zip that looks like a HAR/capture artifact, but inspection shows it contains installable Hermes skills such as `skill-*/SKILL.md` directories plus helper scripts.

## Lesson

Do not ask what to do with it or analyze it as HAR content once the archive structure proves it is a skill package. If Galih says it is the new one and complains that the earlier path was slow, install the skills directly and verify.

## Fast workflow

1. Inspect zip entries without dumping secrets or full file bodies.
2. If it contains one or more `SKILL.md` files under skill directories, treat it as a local skill package.
3. Read each SKILL frontmatter name and choose the smallest sane class-level category path under the active profile skill root.
4. Install/copy the skill directories into the active profile's `$HERMES_HOME/skills/<category>/<skill-name>/`.
5. Put helper scripts under profile scripts or OS-home bin according to the single-home rule; do not recreate profile `home/`.
6. Patch bundled docs that point at stale `~/scripts/...` or profile-home paths to the actual installed script/cache paths.
7. If the package includes browser/capture tooling, align it with active browser routing before finalizing. For HAR capture on Galih's workstation, prefer Cloak/Chrome CDP by default, keep Playwright as explicit `--standalone`, and reject Camofox as CDP because it is REST-only.
8. Verify:
   - `skill_view(<new-skill>)` loads each skill.
   - Any command wrapper exits cleanly for `--help` or equivalent smoke.
   - New names are not duplicated.
   - Frontmatter still parses.
   - `/home/galyarder/.hermes/profiles/galyarder/home` was not recreated.
8. Final reply should be terse: installed paths + verification evidence. No long apology or process dump.

## Scope boundary

If Galih says `install jadi skill doang`, do exactly that. Do not also run capture, debug endpoints, audit performance, or ask a broad clarification unless the package is ambiguous or unsafe to install.

### File: prune-audit-2026-05-18.md

# Skill Prune Audit — 2026-05-18

Full redundancy audit of the Galyarder profile skill library.

## Inventory

- **509** active `SKILL.md` files
- **509** unique frontmatter names (0 duplicates)
- **1** bad frontmatter: `platform-operator-router` (unquoted colon in description)
- **89** LobeHub-sourced, **420** local/official
- **30** candidates flagged by heuristic, manually reviewed to **39 prune + 5 merge + 2 disable-route**

## PRUNE — 39 skills safe to delete

### Redundant naming/variable (3)
- `variable-naming` — LobeHub stub 1.5k, IDE/LLM native
- `variable-name-conversion` — LobeHub stub 1.6k, overlaps above
- `name-assistant` — LobeHub stub 1.8k, same domain

### Redundant UX copy (2)
- `better-ux-writer` — 977 chars stub, `copywriting` covers this
- `metaphor-ux-writer` — 469 chars stub

### Redundant SEO (1)
- `seo-helper` — LobeHub stub 1.1k, `seo` + `seo-audit` canonical

### Redundant ads/copywriting (3)
- `advertising-copywriting-master` — 2.1k generic
- `facebook-ads-expert` — 626 chars stub
- `facebook-advertising-writing-expert` — 4k, overlaps above two

### Chinese platform — not Galih's market (4)
- `xiaohongshu`, `xiaohongshu-style-writer`, `xiao-hong-shu-wenan-id`, `xhs-evl-cl`

### Lifestyle/hobby (2)
- `soccer` — 1.3k discussion bot
- `boxing-master` — 1.8k training

### Redundant resume (2)
- `resume-editing` — 831 chars stub
- `resume-analyzer` — Chinese-language, niche

### Redundant writing (4)
- `grammar-corrector` — 713 chars, `content-generator`/`copywriting` stronger
- `essay-improver` — 1k stub
- `ghostwriter-pro-ai` — 1k stub
- `top-copywriting-master` — 1.8k, `copywriting` canonical

### Redundant logo/graphic (2)
- `logo-creativity` — 1.5k stub, `superdesign` stronger
- `graphic-creativity` — 1k stub

### Generic business (3)
- `business-guru` — 5.6k generic consultant, `galyarder-ceo`/`galyarder-cfo-coo` canonical
- `entrepreneurship-and-competitiveness-expert` — 2.6k generic
- `finance-news-analyser` — 1.1k stub, `financial-analyst`/`stocks` canonical

### Generic with stronger canonical (8)
- `cyber-specialist` → `cybersecurity` (26k procedures)
- `it-system-architect` → `architect`/`architect`
- `web-expert` → `elite-developer`
- `linux-shell-assistant` → terminal/LLM native
- `markdown-layout` → `obsidian`
- `ocr-markdown` → `pdf`
- `q-a-helper` → LLM native
- `meeting` → LLM native / `internal-comms`

### Niche low-value (5)
- `thesis-overview` — 672 chars
- `meaningful-name` — 1.1k artistic naming
- `kpi-hero` — 1.4k performance review
- `title-expansion-writer` — 626 chars
- `ruipingshi` — 1.1k Chinese critic

## MERGE — 5 skills

| Skill | Target | What to keep |
|---|---|---|
| `galyarder-specialist` | `galyarder-framework-router` | Legacy domain-map table examples |
| `suno-music-creator` | `content-generator` | Suno-specific prompt patterns |
| `social-media-sage` | `copywriting` | Any unique framework |
| `brand-pioneer` | `copywriting` | Brand strategy framework bits |
| `onekr-docker-2-compose` | `docker-management` | Docker run → compose recipe |

## KEEP but disable route — 2 skills

- `honcho` — Honcho setup/troubleshoot reference; production memory is Hindsight
- `Vibecoder` — harmless, optional tone layer

## Heuristic pitfalls discovered

1. Alias regex `"source of truth"` matches canonical skills that describe themselves as source of truth. True aliases say "load X and follow it" with minimal body.
2. gstack-workflow skills internally reference each other — not aliases.
3. Protected baseline skills must be exempt from score-based pruning regardless of heuristic.

## Platform / Account Skill Layering (also clarified this session)

```
agent-accounts     = strategic account state
agent-accounts      = credential/session mechanics
platform operator              = frontend action (threads/instagram/x/google-workspace)
browser-routing                = which browser runtime (canonical; galyarder-browser-routing is compat alias)
platform-operator-router = Meta SSO/cookie support layer
```

Routing: lifecycle for audit → owned-login for auth → operator for action → browser-routing for runtime.

## Compatibility aliases confirmed

- `galyarder-browser-routing` → `browser-routing` (do not extend alias)
- `galyarder-specialist` → `galyarder-framework-router` (merge candidate)

## Memory provider routing

`honcho` skill: reference only. Production memory = Hindsight (local). Do not route daily to Honcho.

### File: prune-cleanup-executed-2026-05-18.md

# Prune cleanup executed 2026-05-18

Galih approved the cleanup with exceptions: keep lifestyle skills and the 8 canonical-stub skills; improve copywriting/resume/content-generator/copywriting/superdesign; create `business-strategy-operator`; merge five approved skills.

```json
{
  "created_at": "2026-05-18T11:09:40.978068",
  "root": "/home/galyarder/.hermes/profiles/galyarder/skills",
  "backup_dir": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved",
  "deleted_or_archived": [
    {
      "name": "galyarder-specialist",
      "from": "galyarder-framework/galyarder-specialist",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/galyarder-framework/galyarder-specialist",
      "absorbed_into": "galyarder-framework-router"
    },
    {
      "name": "suno-music-creator",
      "from": "product-management/suno-music-creator",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/product-management/suno-music-creator",
      "absorbed_into": "content-generator"
    },
    {
      "name": "social-media-sage",
      "from": "growth/social-media-sage",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/social-media-sage",
      "absorbed_into": "copywriting"
    },
    {
      "name": "brand-pioneer",
      "from": "growth/brand-pioneer",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/brand-pioneer",
      "absorbed_into": "copywriting"
    },
    {
      "name": "onekr-docker-2-compose",
      "from": "devops/onekr-docker-2-compose",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/devops/onekr-docker-2-compose",
      "absorbed_into": "docker-management"
    },
    {
      "name": "variable-naming",
      "from": "software-development/variable-naming",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/software-development/variable-naming",
      "absorbed_into": ""
    },
    {
      "name": "variable-name-conversion",
      "from": "software-development/variable-name-conversion",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/software-development/variable-name-conversion",
      "absorbed_into": ""
    },
    {
      "name": "name-assistant",
      "from": "software-development/name-assistant",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/software-development/name-assistant",
      "absorbed_into": ""
    },
    {
      "name": "better-ux-writer",
      "from": "growth/better-ux-writer",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/better-ux-writer",
      "absorbed_into": "copywriting"
    },
    {
      "name": "metaphor-ux-writer",
      "from": "growth/metaphor-ux-writer",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/metaphor-ux-writer",
      "absorbed_into": "copywriting"
    },
    {
      "name": "xiaohongshu",
      "from": "growth/xiaohongshu",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/xiaohongshu",
      "absorbed_into": ""
    },
    {
      "name": "xiaohongshu-style-writer",
      "from": "growth/xiaohongshu-style-writer",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/xiaohongshu-style-writer",
      "absorbed_into": ""
    },
    {
      "name": "xiao-hong-shu-wenan-id",
      "from": "growth/xiao-hong-shu-wenan-id",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/xiao-hong-shu-wenan-id",
      "absorbed_into": ""
    },
    {
      "name": "xhs-evl-cl",
      "from": "growth/xhs-evl-cl",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/xhs-evl-cl",
      "absorbed_into": ""
    },
    {
      "name": "grammar-corrector",
      "from": "growth/grammar-corrector",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/grammar-corrector",
      "absorbed_into": "content-generator/copywriting"
    },
    {
      "name": "essay-improver",
      "from": "growth/essay-improver",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/essay-improver",
      "absorbed_into": "content-generator/copywriting"
    },
    {
      "name": "ghostwriter-pro-ai",
      "from": "creative/ghostwriter-pro-ai",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/ghostwriter-pro-ai",
      "absorbed_into": "content-generator/copywriting"
    },
    {
      "name": "top-copywriting-master",
      "from": "growth/top-copywriting-master",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/top-copywriting-master",
      "absorbed_into": "content-generator/copywriting"
    },
    {
      "name": "logo-creativity",
      "from": "creative/logo-creativity",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/logo-creativity",
      "absorbed_into": "superdesign"
    },
    {
      "name": "graphic-creativity",
      "from": "creative/graphic-creativity",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/graphic-creativity",
      "absorbed_into": "superdesign"
    },
    {
      "name": "business-guru",
      "from": "growth/business-guru",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/business-guru",
      "absorbed_into": "business-strategy-operator"
    },
    {
      "name": "entrepreneurship-and-competitiveness-expert",
      "from": "growth/entrepreneurship-and-competitiveness-expert",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/entrepreneurship-and-competitiveness-expert",
      "absorbed_into": "business-strategy-operator"
    },
    {
      "name": "finance-news-analyser",
      "from": "finance-legal/finance-news-analyser",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/finance-legal/finance-news-analyser",
      "absorbed_into": "business-strategy-operator"
    },
    {
      "name": "thesis-overview",
      "from": "creative/thesis-overview",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/thesis-overview",
      "absorbed_into": ""
    },
    {
      "name": "meaningful-name",
      "from": "creative/meaningful-name",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/meaningful-name",
      "absorbed_into": ""
    },
    {
      "name": "kpi-hero",
      "from": "creative/kpi-hero",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/creative/kpi-hero",
      "absorbed_into": ""
    },
    {
      "name": "title-expansion-writer",
      "from": "growth/title-expansion-writer",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/title-expansion-writer",
      "absorbed_into": ""
    },
    {
      "name": "ruipingshi",
      "from": "growth/ruipingshi",
      "to": "/home/galyarder/.hermes/profiles/galyarder/tmp/skill-cleanup-20260518-approved/growth/ruipingshi",
      "absorbed_into": ""
    }
  ],
  "merged": [
    {
      "from": "galyarder-specialist",
      "into": "galyarder-framework-router",
      "reference": "galyarder-framework/galyarder-framework-router/references/absorbed-galyarder-specialist-2026-05-18.md"
    },
    {
      "from": "suno-music-creator",
      "into": "content-generator",
      "reference": "creative/content-generator/references/absorbed-suno-music-creator-2026-05-18.md"
    },
    {
      "from": "social-media-sage",
      "into": "copywriting",
      "reference": "growth/copywriting/references/absorbed-social-media-sage-2026-05-18.md"
    },
    {
      "from": "brand-pioneer",
      "into": "copywriting",
      "reference": "growth/copywriting/references/absorbed-brand-pioneer-2026-05-18.md"
    },
    {
      "from": "onekr-docker-2-compose",
      "into": "docker-management",
      "reference": "devops/docker-management/references/absorbed-onekr-docker-2-compose-2026-05-18.md"
    }
  ],
  "patched": [
    "growth/copywriting/SKILL.md",
    "creative/content-generator/SKILL.md",
    "growth/copywriting/SKILL.md",
    "creative/superdesign/SKILL.md",
    "growth/resume-editing/SKILL.md",
    "productivity/resume-analyzer/SKILL.md",
    "galyarder-framework/galyarder-framework-router/SKILL.md",
    "creative/content-generator/SKILL.md",
    "growth/copywriting/SKILL.md",
    "growth/copywriting/SKILL.md",
    "devops/docker-management/SKILL.md",
    "galyarder-framework/galyarder-framework-router/SKILL.md",
    "galyarder-framework/using-galyarder-framework/SKILL.md"
  ],
  "created": [
    "galyarder-company/business-strategy-operator/SKILL.md"
  ],
  "kept_by_user": [
    "soccer",
    "boxing-master",
    "cyber-specialist",
    "it-system-architect",
    "web-expert",
    "linux-shell-assistant",
    "markdown-layout",
    "ocr-markdown",
    "q-a-helper",
    "meeting"
  ]
}
```

### File: skill-bundles-ntfy-followup-2026-05-30.md

## Correction: bundle semantics (Galih, 2026-05-30)

Galih corrected that active Hermes skill bundles are not a place to preload every domain skill. Because invoking a bundle loads every listed skill into the turn, broad 10-20 skill bundles are inefficient and can pollute context.

Use this split instead:

- **Active root bundles** (`skill-bundles/*.yaml`): tiny response-shaping hotbar only.
  - Keiya: `keiya-core` = `using-galyarder-framework`, `keiya-capability-router`, `tool-grounded-responses`, `godmode`, `gen-z`.
  - Galyarder: `galyarder-core` = `using-galyarder-framework`, `galyarder-framework-router`, `galyarder-execution-doctrine`, `tool-grounded-responses`, `verification-before-completion`, `godmode`, `gen-z`.
- **Domain classification catalogs** (`skill-bundles/_catalog/*.yaml`): broad folder/category-style indexes of installed skills. These are for navigation and audit, not slash-command loading.
- When a task arrives: load the lean core/persona bundle if useful, then route and load the smallest relevant domain skill(s) only.
- If adding a new installed skill like `evm`, add it to the category catalog (e.g. blockchain), not to a broad active domain slash bundle unless the user explicitly wants that bundle to preload it.

Do not recreate many active bundles that load 10+ skills each unless Galih explicitly asks for a specific heavyweight mode.

## Correction 2: category bundles should exist, but be used intentionally

Galih clarified the intended shape again: besides the tiny persona/core bundle, there should still be many active bundles that mirror top-level skill categories/folders — e.g. `autonomous-ai-agents`, `engineering`/`software-development`, `productivity`, `security`, `creative`, etc. The mistake was not “having category bundles”; the mistake was treating them as mandatory/default for every response.

Current desired model:

- **Core bundles** shape the persona/response baseline:
  - `/keiya-core` for Keiya.
  - `/galyarder-core` for Galyarder.
- **Category bundles** mirror skill folders and are available when the user intentionally wants that whole category context:
  - examples: `/autonomous-ai-agents`, `/engineering` (alias for `/software-development`), `/mcp`, `/browser`, `/productivity`, `/security`, `/finance-legal`, `/creative`, `/growth`, `/research`, etc.
- Normal routing still should not blindly load a huge category bundle. Default pattern: core bundle → router → exact skill(s). Category bundle is for broad category mode or when Galih explicitly asks for the whole folder/category bundle.

Implementation state after correction: root `skill-bundles/*.yaml` contains category bundles plus the lean core bundle; `_catalog/` remains as a readable indexed catalog.

### File: skill-authoring.md

---
name: hermes-skill-authoring
description: 'Author in-repo SKILL.md: frontmatter, validator, structure.'
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - skills
    - authoring
    - hermes
    - conventions
    - skill-md
    related_skills:
    - writing-writing-planss
    - writing-plans
    category: software-development
---

# Authoring Hermes-Agent Skills (in-repo)

## Overview

There are two places a SKILL.md can live:

1. **User-local:** `~/.hermes/skills/<maybe-category>/<name>/SKILL.md` — personal, not shared. Created via `skill_manage(action='create')`.
2. **In-repo (this skill is about this case):** `<hermes-repo>/skills/<category>/<name>/SKILL.md` — committed, shipped with the package. Use file writes + `git add`. `skill_manage(action='create')` does NOT target this tree. Discover the actual checkout first (`pwd`, `git rev-parse --show-toplevel`, or the active source path); do not assume `/home/bb/hermes`.

## When to Use

- User asks you to add a skill "in this branch / repo / commit"
- You're committing a reusable workflow that should ship with hermes
- You're editing an existing skill under the active Hermes Agent checkout's `skills/` tree (use `patch` for small edits, file writes for rewrites; `skill_manage` still works for patch on in-repo skills, but not for `create`)

## Required Frontmatter

Source of truth: `tools/skill_manager_tool.py::_validate_frontmatter`. Hard requirements:

- Starts with `---` as the first bytes (no leading blank line).
- Closes with `\n---\n` before the body.
- Parses as a YAML mapping.
- `name` field present.
- `description` field present, ≤ **1024 chars** (`MAX_DESCRIPTION_LENGTH`).
- Non-empty body after the closing `---`.

Peer-matched shape used by every skill under `skills/software-development/`:

```yaml
---
name: my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)
description: Use when <trigger>. <one-line behavior>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill, another-skill]
---
```

`version` / `author` / `license` / `metadata` are NOT enforced by the validator, but every peer has them — omit and your skill sticks out.

## Size Limits

- Description: ≤ 1024 chars (enforced).
- Full SKILL.md: ≤ 100,000 chars (enforced as `MAX_SKILL_CONTENT_CHARS`, ~36k tokens).
- Peer skills in `software-development/` sit at **8-14k chars**. Aim for that range. If you're pushing past 20k, split into `references/*.md` and reference them from SKILL.md.

## Peer-Matched Structure

Every in-repo skill follows roughly:

```
# <Title>

## Overview
One or two paragraphs: what and why.

## When to Use
- Bulleted triggers
- "Don't use for:" counter-triggers

## <Topic sections specific to the skill>
- Quick-reference tables are common
- Code blocks with exact commands
- Hermes-specific recipes (tests via scripts/run_tests.sh, ui-tui paths, etc.)

## Common Pitfalls
Numbered list of mistakes and their fixes.

## Verification Checklist
- [ ] Checkbox list of post-action verifications

## One-Shot Recipes (optional)
Named scenarios → concrete command sequences.
```

Not every section is mandatory, but `Overview` + `When to Use` + actionable body + pitfalls are the minimum for the skill to feel like a peer.

## Directory Placement

```
skills/<category>/<skill-name>/SKILL.md
```

Categories currently in repo (confirm with `ls skills/`): `autonomous-ai-agents`, `creative`, `data-science`, `devops`, `dogfood`, `email`, `gaming`, `github`, `leisure`, `mcp`, `media`, `mlops/*`, `note-taking`, `productivity`, `red-teaming`, `research`, `smart-home`, `social-media`, `software-development`.

Pick the closest existing category. Don't invent new top-level categories casually.

## Workflow

1. **Survey peers** in the target category:
   ```
   ls skills/<category>/
   ```
   Read 2-3 peer SKILL.md files to match tone and structure.
2. **Check validator constraints** in `tools/skill_manager_tool.py` if unsure.
3. **Draft** with `write_file` to `skills/<category>/<name>/SKILL.md`.
4. **Validate locally**:
   ```python
   import yaml, re, pathlib
   content = pathlib.Path("skills/<category>/<name>/SKILL.md").read_text()
   assert content.startswith("---")
   m = re.search(r'\n---\s*\n', content[3:])
   fm = yaml.safe_load(content[3:m.start()+3])
   assert "name" in fm and "description" in fm
   assert len(fm["description"]) <= 1024
   assert len(content) <= 100_000
   ```
5. **Git add + commit** on the active branch.
6. **Note:** the CURRENT session's skill loader is cached — `skill_view` / `skills_list` will not see the new skill until a new session. This is expected, not a bug.

## Cross-Referencing Other Skills

`metadata.hermes.related_skills` unions both trees (`skills/` in-repo and `~/.hermes/skills/`) at load time. You CAN reference a user-local skill from an in-repo skill, but it won't resolve for other users who clone the repo fresh. Prefer referencing only in-repo skills from in-repo skills. If a frequently-referenced skill lives only in `~/.hermes/skills/`, consider promoting it to the repo.

## Editing Existing In-Repo Skills

- **Small fix (typo, added pitfall, tightened trigger):** `skill_manage(action='patch', name=..., old_string=..., new_string=...)` works fine on in-repo skills.
- **Major rewrite:** `write_file` the whole SKILL.md. `skill_manage(action='edit')` also works but requires supplying the full new content.
- **Adding supporting files:** `write_file` to `skills/<category>/<name>/references/<file>.md`, `templates/<file>`, or `scripts/<file>`. `skill_manage(action='write_file')` also works and enforces the references/templates/scripts/assets subdir allowlist.
- **Always commit** the edit — in-repo skills are source, not runtime state.

## Common Pitfalls

1. **Using `skill_manage(action='create')` for an in-repo skill.** It writes to `~/.hermes/skills/`, not the repo tree. Use `write_file` for in-repo creation.

2. **Leading whitespace before `---`.** The validator checks `content.startswith("---")`; any leading blank line or BOM fails validation.

3. **Description too generic.** Peer descriptions start with "Use when ..." and describe the *trigger class*, not the one task. "Use when debugging X" > "Debug X".

4. **Forgetting the author/license/metadata block.** Not validator-enforced, but every peer has it; omitting makes the skill look half-finished.

5. **Writing a skill that duplicates a peer.** Before creating, `ls skills/<category>/` and open 2-3 peers. Prefer extending an existing skill to creating a narrow sibling.

6. **Expecting the current session to see the new skill.** It may not. The skill loader can cache listings at session/runtime boundaries. Verify with a fresh session, `/reload-skills` when available, or direct source-loader checks with explicit `HERMES_HOME`.

7. **Changing `name` without renaming the directory.** Hermes lists by frontmatter name but direct `skill_view(<new-name>)` first tries paths/directories. When normalizing local/profile skills, rename the directory to match the new slug.

8. **Linking to skills that don't exist in-repo.** `related_skills: [some-user-local-skill]` works for you but breaks for other clones. Prefer only in-repo links.

## Profile Skill Index Validation

For profile-local skill creation, import, or consolidation, use `references/profile-skill-index-validation.md` to verify the active `$HERMES_HOME/skills` tree: exclude `.archive/`, check YAML frontmatter, duplicate names, directory/name mismatches, disabled skill entries, new skill enabled status, and fresh-session index visibility.

## Verification Checklist

- [ ] File is at `skills/<category>/<name>/SKILL.md` for in-repo work, or active profile `$HERMES_HOME/skills/<category>/<name>/SKILL.md` for user-local/profile work
- [ ] Directory name matches `frontmatter.name` when the skill should load by bare name
- [ ] Frontmatter starts at byte 0 with `---`, closes with `\n---\n`
- [ ] `name`, `description`, `version`, `author`, `license`, `metadata.hermes.{tags, related_skills}` all present
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Description ≤ 1024 chars and starts with "Use when ..."
- [ ] Total file ≤ 100,000 chars (aim for 8-15k)
- [ ] Structure: `# Title` → `## Overview` → `## When to Use` → body → `## Common Pitfalls` → `## Verification Checklist`
- [ ] `related_skills` references resolve in the intended distribution context
- [ ] Loader verification completed with explicit active `HERMES_HOME`
- [ ] `git add skills/<category>/<name>/ && git commit` completed when editing in-repo bundled skills