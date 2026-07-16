# Advanced Docs Fake-Depth Quality Gate (2026-05-23)

## Trigger

Use this when a public guide/docs-site expansion technically has many words but the user rejects it as shallow, fake-advanced, generic, or “ampas”. Do not defend word count. Treat the rejection as a quality signal.

## Session lesson

In the Agentic Company guide session, the active docs had 23 pages and averaged roughly 1,500+ words per page, but the result still felt weak because the depth was produced by recurring advanced-sounding scaffolding instead of page-specific operational value.

Observed failure patterns:

- repeated generic section labels across pages: `Evidence Contracts`, `Failure Taxonomies`, `Maturity Levels`, `Policy Matrices`, `Red-Team Checks`, `Operating Loops`;
- source IA required plain, human-first language, but repo content drifted back into public-facing vibe words like `stack`, `OS`, `layer`, `operator`, `control plane`, `infrastructure`, `framework`, and `runtime`;
- advanced source concepts were mentioned but not converted into usable decisions, worksheets, matrices, schemas, examples, or gates;
- rendered site quality was lower than markdown quality because the custom renderer only handled some heading levels, while source files used unsupported `#` / `####` headings;
- locale metadata existed, but body parity was fake because localized body overrides were empty and fell back to English;
- some files had frontmatter and others did not, creating inconsistent content contracts.

## Read-only audit before rewriting again

Before touching content after this kind of complaint:

1. List active docs/pages/slugs and confirm the intended IA.
2. Read source/canon notes again, not only the repo markdown.
3. Check renderer/content contract:
   - supported heading levels;
   - frontmatter handling;
   - table/code/list handling;
   - generated content manifest behavior;
   - locale body source.
4. Scan for fake-depth repetition:
   - recurring expert-sounding section names reused across many pages;
   - page sections that could be swapped between pages without losing meaning;
   - generic “maturity” or “failure taxonomy” language with no concrete artifact.
5. Scan for language-lock violations and forbidden public-facing vibe words when the source specifies them.
6. For each page, identify the concrete artifact it gives the reader: worksheet, checklist, template, schema, policy, example record, decision gate, or verification test.
7. Produce diagnosis and rewrite plan before editing.

## Real advanced page shape

A serious guide page is advanced only if it helps the reader make or verify a decision.

Default page structure:

1. **What this page decides** — the concrete decision the reader can make after reading.
2. **Why it matters** — the failure prevented or leverage gained.
3. **The model** — the plain-language concept or architecture.
4. **Rules** — clear if/then boundaries, thresholds, or policy.
5. **Example** — a realistic sanitized example, not private user state.
6. **Failure modes** — specific ways this page’s system breaks.
7. **Checklist / template** — copyable artifact or exact inspection list.
8. **Done when** — verification criteria.

## Repair pattern for broad docs sets

For 15+ pages, do not rewrite the whole set blindly in one pass. Establish a quality bar first:

1. Pick the first 2–3 foundation pages.
2. Rewrite them to the real advanced page shape.
3. Verify source alignment, language lock, renderer behavior, and artifact usefulness.
4. Only then propagate the pattern to the rest.

## Anti-patterns

Do not use word count as the primary proof of depth.
Do not paste the same advanced section pattern into every page.
Do not use `Evidence Contract`, `Failure Taxonomy`, `Maturity Level`, or `Red-Team Check` unless the page gives a concrete, page-specific artifact under that heading.
Do not call a docs site bilingual if the body content falls back to the same English markdown.
Do not claim public-guide completion without checking rendered output, not just source files.
