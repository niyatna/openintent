# Galyarder Framework README repositioning pattern (2026-06-01)

## Trigger
Use this reference when updating README, repo description, docs-site landing copy, or public application copy for Galyarder Framework or similar Galyarder Labs developer-facing repos.

## Lesson
Do not frame Galyarder Framework as a generic “coding-agent maintainer tool”, “prompt pack”, or “AGI/1-Man Army” project. That language is too narrow or too grandiose for public OSS review.

The stronger category is:

> open-source Agentic Company Framework / Intelligence Layer

Meaning: a framework that turns founder/operator intent into coordinated multi-domain execution across engineering, product, growth, sales, finance, legal, security, documentation, operations, and strategy.

## README edit posture
When improving this README:

1. Preserve high-value technical content.
   - Keep install paths, Codex/OpenCode directives, marketplace/plugin instructions, Neural Link, agents, commands, departments, verification gates, diagrams, release/deploy details.
   - Do not wipe the technical surface just to make positioning cleaner.
2. Remove edgy/cosplay-heavy public language.
   - Avoid leading with `AGI`, `1-Man Army`, `zero-slop`, `empire`, `swarms`, `sentient`, “elite”, “clinical”, or “high-integrity” as marketing posture.
   - Keep `Autonomous Goal Integration` only as a secondary/internal exwriting-plansation if needed, and explicitly say it is not an artificial-general-intelligence claim.
3. Lead with category and mechanism.
   - Hero: `Open-source Agentic Company Framework.`
   - Explain the mechanism: intent intake -> routing -> blueprinting -> implementation -> verification -> reporting/distribution/memory.
4. Show domain breadth.
   - Engineering, product, growth/marketing, sales, finance, legal, security, documentation, operations, strategy/writing-plansning/brainstorming.
5. Add tasteful badges when polishing public READMEs.
   - Useful badge classes: npm version/downloads, docs workflow, CodeQL/security, license, GitHub stars/forks, category badge, human-directed execution badge.
   - Badges should reinforce trust and status without turning the README into vanity-metric cosplay.
6. Verify raw source and deployed docs separately.
   - GitHub page/web extracts can be cached or summarize stale content.
   - Verify current README via raw.githubusercontent.com or GitHub API content, plus `git ls-remote`/HEAD match.
   - If docs deploy runs, wait for deploy workflow and pages-build-deployment success before claiming public docs are updated.

## Repo description pattern
Good:

```text
An Agentic Company Framework: skills, commands, agents, and protocols for turning founder intent into coordinated execution across engineering, finance, marketing, sales, ops, security, docs, and strategy.
```

Avoid:

```text
Advanced Agentic Orchestration for the 1-Man Army implementing AGI.
```

## Application/copywriting note
For OSS funding or program applications, do not lead with small metrics like low stars/downloads unless the form explicitly requires metrics. Reviewers can inspect those. Lead with ecosystem role, mechanism, maintainer burden, and why support improves safer/reproducible agentic company execution.