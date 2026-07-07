# Quality-bar-first advanced docs rewrite — 2026-05-23

## Trigger

Use this when a docs/public-guide rewrite technically has enough pages or words but the user says it still feels shallow, fake-advanced, messy, mediocre, or like filler.

Session signal: Galih rejected the Agentic Company guide with “isinya pendek pendek banget ampas sampah apanya yang advanced?” and later approved fixing the first three pages only as a quality bar before propagating.

## Lesson

Word count is not depth. Repeating impressive labels like `Evidence Contracts`, `Failure Taxonomies`, `Maturity Levels`, `Policy Matrices`, `Red-Team Checks`, or `Operating Loops` across many pages can make a guide feel *less* advanced when those blocks are not tied to the page’s real decision and artifact.

Advanced docs must produce usable decisions and artifacts, not generic taxonomy theater.

## Required workflow

1. Do not defend the previous pass or the word count.
2. Audit the actual source docs and rendered/active pages enough to identify quality failures.
3. Classify failure modes before editing:
   - fake-advanced repeated skeleton terms;
   - source IA not actually absorbed;
   - human-first language drifting back to engineering posture words;
   - missing concrete artifact per page;
   - renderer/markdown contract issues;
   - locale/body parity gaps;
   - public-safety risk.
4. Rewrite a small quality bar first, usually 2–3 representative pages, before mass-propagating to all pages.
5. For each page, force this shape:
   - What this page decides;
   - Why it matters;
   - the model/rule;
   - concrete example;
   - decision table or checklist;
   - template/scorecard/artifact;
   - done-when/proof gate.
6. Kill generic advanced labels unless they are immediately backed by a concrete artifact in that page.
7. Verify source markdown and rendered output.
8. Only then propagate the pattern to the remaining docs.

## Quality-bar example from Agentic Company guide

The first three pages were rewritten as the quality standard:

- `manifesto`: founding contract, five parts, proof rule, no-publish list, starting contract.
- `reality-check`: Agentic SaaS vs agentic company category matrix, Revocation/State-Change/Proof/Budget tests, scorecard.
- `business-first`: Business Reality Map, loop template, action-class matrix, first workflow checklist, example filled artifact.

The useful pattern was not “make pages longer”; it was “make each page decide something and leave the reader with a usable artifact.”

## Verification package

A strong check includes:

- word counts only as a secondary signal;
- banned/vibe-term scan when language lock exists;
- repeated-skeleton-term scan;
- broken heading/renderer marker scan (`#`, `####` when the renderer does not support them);
- private path/ID/secret/wallet scan;
- required source concept scan;
- rendered HTML check for key sections and absence of literal frontmatter/broken markdown;
- docs build/check.

## Reporting style

When the user is angry about quality, answer short and evidence-first:

```text
done. patched first 3 pages as quality bar.
changed: <files>
verified: <build/scan evidence>
next: propagate pattern to <next batch>
```

No process theater. No “should be better.” No victory claim without the build and scans.
