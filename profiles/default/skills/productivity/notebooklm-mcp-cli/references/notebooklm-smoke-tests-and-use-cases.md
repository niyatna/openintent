# Default NotebookLM smoke tests and use cases

Use this reference after auth/setup changes or when proving NotebookLM can do real work for the Default profile.

## Canonical CLI path

Current single-home setup uses the OS-home CLI directly:

```bash
export HOME=~/.hermes
NLM=~/.hermes/.local/bin/nlm
```

Do not recreate `~/.hermes/profiles/default/home` or the old profile-local `nlm-default` wrapper. Credentials intentionally live under `~/.hermes/.notebooklm-mcp-cli/profiles/default`.

## Minimal access smoke test

```bash
"$NLM" login --check
"$NLM" list notebooks
```

Expected current-good signals:

```text
✓ Authentication valid!
Account: default@gmail.com
Notebooks found: 2
```

Notebook list should return JSON-like records with IDs, titles, source counts, and update times.

## Read/query smoke test

Use a notebook with at least one source:

```bash
NB=6045158c-d662-4997-980b-a6e9b600387c
"$NLM" notebook get "$NB"
"$NLM" list sources "$NB"
"$NLM" notebook query "$NB" \
  'Jawab singkat satu kalimat dalam bahasa Indonesia: notebook ini membahas apa?'
```

Current observed working notebook:

- id: `6045158c-d662-4997-980b-a6e9b600387c`
- title: `The $100 Million Monthly Income Roadmap`
- source id: `8245b388-275f-4c29-a545-9c7c51826d0f`
- source type: YouTube

Successful query returns `value.answer`, `conversation_id`, `sources_used`, `citations`, and `references`.

## Create/add/query smoke test

Use this to prove writes and source ingestion work. This creates a real NotebookLM notebook, so only run when a visible smoke notebook is acceptable.

```bash
TITLE="Default NotebookLM Smoke Lab $(date +%Y-%m-%d-%H%M%S)"
"$NLM" notebook create "$TITLE"

NB=<created-notebook-id>
"$NLM" source add "$NB" \
  --title 'Default Operating Note' \
  --text 'Company builds infrastructure for human intent and continuity. NotebookLM should be used as a source-grounded digestion layer for long inputs: videos, PDFs, market reports, transcripts, and founder notes. GBrain should keep durable memory and operational knowledge. The ideal flow is raw source into NotebookLM, extracted playbook and cited insight into GBrain or implementation docs. The test use case is to ask NotebookLM to turn this note into concrete workflows.' \
  --wait --wait-timeout 120

"$NLM" notebook get "$NB"
"$NLM" notebook query "$NB" \
  'Dari source ini, buat 4 workflow konkret untuk Default. Format singkat: workflow, input, output, kapan dipakai.'
```

Known session-created example:

- notebook id: `efea0456-944c-4b40-9fc9-c8d6bb9706de`
- title: `Default NotebookLM Smoke Lab 2026-05-04-091905`
- source id: `359f5f59-b194-401f-85bf-57c527a15459`
- source title: `Default Operating Note`

## Useful Default workflows

NotebookLM is best used as a source-grounded digestion layer, not as primary memory.

Ideal flow:

```text
raw source panjang
→ NotebookLM
→ extracted playbook / cited insight / workflow
→ GBrain, docs, PRD, content, or decision log
```

High-value use cases:

- Source-grounded strategy extraction from videos, PDFs, market reports, transcripts, courses, and founder notes.
- Turning raw learning into an execution menu: playbooks, product ideas, risk maps, validation steps.
- Founder decision support: ask which ideas are high leverage, low capital, directly applicable, or questionable.
- Content-to-product pipeline: source → pain points/workflows → PRD, landing copy, outbound angle, prototype scope, lead magnet.
- Personal/company knowledge packs by domain: strategy, AI agents market, content factory research, sales/offers/pricing, life operating system.
- Source-cited writing for threads, essays, decks, pitch materials, or internal memos.
- Audio/study workflows for long sources when reading bandwidth is low.

## Current practical verdict

GBrain = durable memory / knowledge graph / operational brain.

NotebookLM = cited source digestion workspace for heavy inputs before committing distilled knowledge to permanent systems.

## Safety and cleanup

- Notebook creation is not destructive but leaves visible artifacts. If the user asks for a disposable test, create with a timestamped `Smoke Lab` title and ask before deleting unless deletion was explicitly requested up front.
- Do not pipe untrusted NotebookLM output into `python`, shell, or other interpreters. Save output to a file or inspect it as text first if parsing is needed.
- Avoid repeated query loops on free-tier accounts; use a single representative query for verification.
- User-facing reports of NotebookLM tests should be concise and answer the direct ask first; avoid long raw JSON dumps unless the user requests evidence.
