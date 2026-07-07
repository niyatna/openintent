---
name: codegraph-codebase-analysis
description: Use when analyzing, reviewing, onboarding to, or answering questions about local repositories, building codebase wikis, or indexing LOC.
version: 2.1.0
author: Galyarder Labs
license: MIT
metadata:
  hermes:
    tags: [dev, codebase-analysis, codegraph, codegraph-codebase-analysis, pygount-loc, knowledge-graph]
    category: software-development
---

# CodeGraph Codebase Analysis

## Overview

Use CodeGraph as the first codebase-understanding layer for repo analysis, PR review, architecture questions, symbol tracing, and impact analysis.

CodeGraph is a local pre-indexed knowledge graph stored in `.codegraph/codegraph.db`. It can return symbol locations, source snippets, callers/callees, relevant files, and affected tests without forcing the agent to repeatedly use `search_files`, `read_file`, `grep`, or broad directory scans.

The operating rule is simple:

> **For codebase questions, ask CodeGraph first. Read files second only when CodeGraph is missing, stale, truncated, or exact raw content is required.**

This does not replace tests, `git diff`, or final verification. It replaces wasteful repo exploration.

## When to Use

Use this skill when Galih asks any of these:

- `analisa repo ini`, `analisa codebase`, `ini arsitekturnya gimana?`
- `review PR`, `cek branch ini`, `audit diff`, `apa yang berubah?`
- `fitur X jalan dari mana ke mana?`
- `fungsi/class/component ini dipakai di mana?`
- `kalau gua ubah file/symbol ini impact-nya apa?`
- `repo GitHub ini apaan?`, when code-level understanding is needed
- onboarding to a new local repo
- writing PR summaries, architecture notes, or codebase maps
- selecting tests affected by a change
- implementing a code change where caller/callee/blast-radius context matters

Do **not** use this as the only source when:

- the repo is not local and the user only wants a high-level GitHub README summary
- the answer is about live production state, logs, DB data, deployments, or runtime behavior
- CodeGraph has no index and the user forbids indexing/cloning
- the task is about non-code corpora, papers, notes, images, or cross-document research; use `codegraph-codebase-analysis` there
- exact file bytes, generated artifacts, secrets handling, or hidden config need direct inspection

## Active Tools and Fallbacks

### Preferred: MCP tools after Hermes restart

When CodeGraph MCP tools are available, prefer them in this order:

1. `codegraph_explore` — primary tool for broad questions and before edits. Returns relevant source plus relationship context in one call.
2. `codegraph_search` — locate exact symbols before focused exploration.
3. `codegraph_node` — inspect one symbol, or read a file through CodeGraph with line numbers and dependency context.
4. `codegraph_callers` — focused caller lookup for a specific symbol.

Always pass `projectPath` when the repo path is known, especially if the current working directory is not inside the target repo.

### CLI fallback when MCP is not loaded

Current or older Hermes sessions may not expose MCP tools until a restart. Use the CodeGraph CLI instead of falling back to broad file reads.

Robust resolver for Galih's environment:

```bash
CG="${CODEGRAPH_BIN:-$(command -v codegraph || true)}"
if [ -z "$CG" ] && [ -x /home/galyarder/.nvm/versions/node/v24.15.0/bin/codegraph ]; then
  CG=/home/galyarder/.nvm/versions/node/v24.15.0/bin/codegraph
fi
[ -n "$CG" ] || { echo "codegraph not found" >&2; exit 1; }
```

Useful CLI commands:

```bash
# Status / freshness
"$CG" status "$REPO"
"$CG" sync "$REPO"
"$CG" init "$REPO"

# Primary exploration
"$CG" explore -p "$REPO" "auth flow"
"$CG" explore -p "$REPO" "InvoiceEditor save flow" --max-files 6

# Symbol lookup and focused node context
"$CG" query -p "$REPO" "signIn" -j
"$CG" node -p "$REPO" "signIn"
"$CG" node -p "$REPO" -f "src/app/page.tsx" --symbols-only

# Caller/callee/impact/test selection
"$CG" callers -p "$REPO" "saveInvoice"
"$CG" callees -p "$REPO" "saveInvoice"
"$CG" impact -p "$REPO" "saveInvoice"
git -C "$REPO" diff --name-only main...HEAD | "$CG" affected -p "$REPO" --stdin
```

## Standard Workflow

### 1. Resolve the repo

If the user gives a path, use it. Otherwise use the current git root.

```bash
REPO="${REPO:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
```

For an external GitHub repo where code-level analysis is required:

```bash
git clone --depth 1 https://github.com/OWNER/REPO /tmp/OWNER-REPO
REPO=/tmp/OWNER-REPO
```

For a PR:

```bash
gh pr checkout <number>
REPO="$(git rev-parse --show-toplevel)"
```

Use `github-pr-workflow` for GitHub auth, checkout, comments, reviews, and CI.

### 2. Ensure the index exists and is fresh

Do not conclude CodeGraph is broken just because a tools list is empty or `status` fails from the wrong directory. CodeGraph only exposes tools for indexed workspaces.

```bash
if ! "$CG" status "$REPO" >/tmp/codegraph-status.txt 2>&1; then
  "$CG" init "$REPO"
else
  "$CG" sync "$REPO" >/tmp/codegraph-sync.txt 2>&1 || true
fi
"$CG" status "$REPO"
```

If the repo was just edited, run `codegraph sync` before using CodeGraph output as current truth.

### 3. Ask CodeGraph before reading files

Use the narrowest CodeGraph query that answers the question:

- Broad architecture: `codegraph_explore("architecture / routing / auth / billing", projectPath=REPO)`
- Exact symbol: `codegraph_search` → `codegraph_node`
- "Who uses this?": `codegraph_callers` or CLI `callers`
- "What breaks if changed?": CLI `impact`, plus `affected` for tests
- "What does this file contain?": `codegraph_node` file mode before `read_file`

Only use `read_file` / `search_files` after CodeGraph when:

- CodeGraph says the workspace is unindexed and indexing is not allowed
- the answer needs an exact raw file not represented in the graph
- CodeGraph output is truncated, stale, or ambiguous
- configs/docs/assets/tests are missing from the graph and are essential
- final verification requires checking generated or changed files directly

### 4. Answer with CodeGraph-grounded structure

For analysis answers:

```text
CodeGraph says:
- entrypoint / relevant symbols:
- call flow / relationships:
- key files:
- risk / blast radius:
- next move:
```

For PR reviews:

```text
Verdict: approve / warning / block
Changed surface:
CodeGraph impact:
Affected tests:
Findings:
- [severity] file:symbol — issue — fix
Verification still needed:
```

Do not dump raw CodeGraph output unless the user asks. Synthesize it.

## Specific Workflows

### Codebase overview / onboarding

1. `codegraph status` to get file/node/language counts.
2. `codegraph explore -p "$REPO" "project architecture entrypoints routing state data layer"`.
3. If the project has known frameworks, query framework terms: `routes`, `api`, `pages`, `components`, `stores`, `models`, `controllers`, `services`.
4. Report: architecture shape, key flows, main directories/files, complexity hotspots, and what to inspect next.

### Feature-flow analysis

1. Search exact feature/symbol names first.
2. Explore the selected symbol or feature term.
3. Use callers/callees to trace flow direction.
4. Only then inspect exact files if more precision is needed.

### PR / branch review

1. Use `git diff --stat` and `git diff --name-only BASE...HEAD` for the changed surface.
2. Run `codegraph sync`.
3. For each changed code file, use `codegraph node -f <file> --symbols-only` to identify changed symbols.
4. For important symbols, use `codegraph_node`, `codegraph_callers`, `impact`, and `affected`.
5. Then apply `github-pr-workflow` checks: correctness, security, maintainability, tests, performance.
6. Run relevant tests or at least identify the exact tests CodeGraph marks affected.

Do not review a PR by reading changed files in isolation if CodeGraph can show caller/callee impact.

### Implementation / editing

Before editing:

1. `codegraph_explore` the target area.
2. `codegraph_node` the target symbol/file.
3. `codegraph_callers` or `impact` to understand blast radius.

After editing:

1. `codegraph sync`.
2. `codegraph affected` from changed files.
3. Run targeted tests/build checks.
4. If CodeGraph now shows new or changed relationships, include that in the handoff.

## Priority Over Graphify

For ordinary code repositories, PRs, diffs, and code architecture questions, CodeGraph is the first route.

Use `codegraph-codebase-analysis` when the input is a mixed corpus or when the user explicitly wants persistent cross-document community detection, HTML visualization, graph JSON, papers/docs/images, or `codegraph-codebase-analysis-out/` artifacts.

If both exist:

- CodeGraph answers code structure and live repo questions.
- Graphify answers corpus/community/cross-document questions.

## Common Pitfalls

1. **Using file search first.** Wrong default. CodeGraph exists to avoid broad `search_files`/`read_file` loops.
2. **Running MCP test from the wrong cwd.** CodeGraph reports zero tools outside an indexed workspace. Pass `projectPath` or run from the repo root.
3. **Forgetting to restart Hermes after MCP config changes.** Current sessions may not see `mcp-codegraph`; use CLI fallback.
4. **Treating CodeGraph as runtime truth.** It is static code intelligence. Logs, DB rows, network calls, and production behavior still need runtime tools.
5. **Ignoring staleness after edits.** Run `codegraph sync` before relying on relationships after changes.
6. **Broad fuzzy query failure.** If `explore "auth"` is noisy, run `codegraph_search` / `query -j` for exact symbols, then explore the exact name.
7. **Claiming complete review from CodeGraph only.** CodeGraph gives structure and impact; `git diff`, security review, and tests still prove correctness.
8. **Reading entire files because one detail is missing.** Prefer `codegraph_node` file mode with `--offset/--limit` or MCP `codegraph_node` before `read_file`.

## Verification Checklist

- [ ] Target repo path resolved and, for PRs, correct branch/PR checked out.
- [ ] `.codegraph/` exists or `codegraph init` was run, unless indexing was impossible or forbidden.
- [ ] `codegraph status` or MCP tools confirm the workspace is indexed.
- [ ] Primary reasoning came from `codegraph_explore`, `codegraph_search`, `codegraph_node`, `codegraph_callers`, or CLI equivalents before broad file reads.
- [ ] Any file reads/searches used after CodeGraph have a stated reason.
- [ ] For PR/diff work, changed files and affected tests were identified.
- [ ] For edits, `codegraph sync` ran after changes before impact claims.
- [ ] Final answer distinguishes static code-graph findings from runtime/test verification.

## References & Sub-playbooks
- `references/codegraph-codebase-analysis.md` — Running pygount for lines-of-code and file composition metadata
- `references/codegraph-codebase-analysis.md` — Synthesizing wiki outlines and Mermaid diagram files
- `references/codegraph-codebase-analysis.md` — Processing code schemas to HTML graphs maps
- `references/codegraph-codebase-analysis.md` — Hardening glosarry terms and DDD domain models definitions
