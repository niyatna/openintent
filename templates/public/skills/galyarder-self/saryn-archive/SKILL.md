---
description: Use when compiling raw notes, tag-indexing second brain files, or processing
  link bookmarks highlights intake.
metadata:
  hermes:
    category: galyarder-self
    tags:
    - archive
    - knowledge
    - second-brain
    - galyarder
name: saryn-archive
version: 1.0.0
---


# Saryn Archive

## Overview

Saryn Archive converts raw intake into long-term, searchable knowledge for Galih's second brain.

Use it to preserve what matters beyond the current conversation: ideas, highlights, notes, links, media takeaways, personal insights, project patterns, and strategic references.

This is not a generic summarizer. The goal is to make future recall useful: what mattered, what changed in Galih, when to reuse it, and how to tag it so it can be found again.

## When to Use

Use this skill when Galih:

- drops a long message berisi catatan, ide, atau highlight dari sesuatu yang dia baca, tonton, dengar, atau pikirkan
- bilang dia mau “nyimpen ini ke kepala”, “arsipin”, “masukin sistem”, “buat second brain”, atau “biar nanti bisa dicari lagi”
- minta rangkuman yang bisa dipakai ulang nanti, bukan cuma jawaban instan sekali baca
- ingin mengubah input mentah menjadi catatan yang rapi, taggable, dan queryable
- mengirim link/thread/video/artikel lalu konteksnya jelas untuk knowledge capture

Do not use this skill for:

- pertanyaan cepat yang cuma butuh jawaban langsung
- debugging teknis yang butuh root cause, logs, tests, atau patch
- jadwal/reminder/cron yang bukan knowledge archive
- personal memory kecil yang lebih cocok langsung ke Hindsight/native memory
- banyak sumber besar yang substansinya beda; pecah jadi beberapa entry

## Procedure

### 1. Identify Source And Intent

Read the input and detect:

- source_type: book, article, video, thread, podcast, chat, internal note, document, image, or other
- source_ref: title, link, author, channel, file name, or short description
- intended purpose: concept reference, strategy pattern, technical pattern, personal insight, project canon, or mixed

If the purpose is not clear and materially affects the structure, ask one short question:

> ini mau kamu simpan sebagai apa? konsep, strategi, teknik, insight pribadi, atau campuran?

If the default is obvious, proceed without asking.

### 2. Extract Core Ideas, Not Surface Summary

Write 3–7 bullets that answer:

- what are the 1–2 central ideas?
- what makes this different from what Galih already knows?
- what practical consequence does this have for how Galih lives, builds, decides, or works?

Do not merely paraphrase paragraphs. Look for shifts in worldview, operating principle, decision rule, pattern, trade-off, or system design.

### 3. Mark What Changed In Galih

Write 2–4 bullets under `What Changed in Galih`.

Capture changes such as:

- a new definition
- a new rule
- a behaviour to avoid
- a behaviour to pursue
- a sharper distinction
- a project implication
- a personal operating-system update

This section makes the note belong to Galih, not just to the source.

### 4. Create Retrieval Metadata

Create metadata with:

- source_type: book / article / video / thread / podcast / chat / internal / document / image / other
- source_ref: title, link, author, or short description
- date: current date in `YYYY-MM-DD`
- related_to: relevant project, agent, or life area
- tags: 5–12 relevant keywords

Tags should cover:

- abstraction level: theory, practice, framework, principle, tactic
- domain: ai, infra, finance, philosophy, relationship, health, family, product, writing, coding, design, etc.
- potential use: decision-making, writing, coding, design, research, writing-plansning, operations, content, etc.
- project/person anchors: galyarder-labs, galyarder-ascendancy, keiya, galyarder-ledger, hermes, agents, habit, family, etc.

### 5. Structure Output Consistently

Use this exact structure unless Galih asks for a different format:

```markdown
# Title

## Source
- source_type: ...
- source_ref: ...
- date: YYYY-MM-DD
- related_to: ...

## Core Ideas
- ...
- ...
- ...

## What Changed in Galih
- ...
- ...

## Possible Uses
- ...
- ...

## Tags
tag-1, tag-2, tag-3, tag-4, tag-5

## Suggested Placement
archive/...
```

For Telegram, avoid pipe tables. Use bullet metadata.

### 6. Suggest Placement

Add a short folder/section suggestion:

- `archive/ai/agents`
- `archive/philosophy/agency`
- `archive/infra/ownership`
- `archive/finance/leverage`
- `archive/health/energy`
- `archive/relationships/trust`
- `archive/galyarder-labs/strategy`
- `archive/keiya/memory`

If the note is highly personal, suggest `journal/insights` or `galyarder-self/operating-system`.

## Live Personal-History Intake

When Galih is telling autobiographical identity history, childhood memories, family wounds, relationships, or self-definition in a live chat, treat it as semantic identity memory, not just a generic note.

Default handling:

1. Save each coherent segment to Hindsight immediately when it contains durable identity facts, formative events, relationships, wounds, decisions, or operating-pattern exwriting-plansations.
2. Use compact but rich `hindsight_retain` entries with honest context such as `deep personal identity history from Galih - <topic>`.
3. Include tags that make future recall possible: `galih`, `identity`, life stage, people, themes, and `galyarder-self`.
4. After saving, answer in the same emotional register: concise acknowledgement plus synthesis of the pattern. Do not turn the vulnerable disclosure into a generic biography dump.
5. If the story spans multiple messages, preserve each segment first; wait for a natural pause before proposing a consolidated Obsidian archive note.
6. If Galih asks whether it was saved, answer directly with the storage target, context label, and core tags.

See `references/galih-autobiographical-intake.md` for a compact schema and example tagging from a real multi-message identity-history session.

## Optional Persistence

If Galih explicitly asks to save it, or the context clearly implies saving:

1. Keep the visible output clean first.
2. Prefer Hindsight for durable semantic recall if the note is a compact fact/insight.
3. Prefer Obsidian for long-form archive entries, especially if the note has title, sections, tags, and future reuse value.
4. Use the Keiya/Galih Obsidian vault when appropriate:
   `/home/galyarder/Documents/Obsidian Vault/Keiya`
5. Do not silently claim it is saved unless a write/retain action actually succeeded.

If only formatting is requested, do not auto-save unless Galih says to save.

## Pitfalls

- Too shallow: only summarizing source content without connecting it to Galih.
- Too few tags: retrieval becomes weak; aim for 8–12 tags when the entry is important.
- Missing `What Changed in Galih`: the note becomes generic and less useful.
- Mixing multiple unrelated sources into one entry: split entries when the conceptual center differs.
- Overwriting uncertainty: if source_ref is unknown, label it honestly instead of inventing a title/author.
- Treating session_search as memory: session history is archive, not semantic memory.
- Saving without proof: verify file write or Hindsight retain result before saying it is saved.

## Verification Checklist

Before considering the archive entry successful:

- [ ] There are at least 3 clear core ideas.
- [ ] `What Changed in Galih` explicitly states an internal shift, rule, avoidance, pursuit, or operating-system update.
- [ ] Tags are relevant, rich enough for retrieval, and include domain + abstraction + use-case anchors.
- [ ] Source metadata is honest and sufficient.
- [ ] Possible uses explain when Galih would call this note again.
- [ ] The suggested placement fits the note's future retrieval path.

Final self-check:

> kalau Galih balik 3 bulan lagi dan baca satu entry ini saja, apakah dia akan ingat kenapa ini penting dan bagaimana memakainya?

If not, improve the core ideas and `What Changed in Galih` before finishing.
