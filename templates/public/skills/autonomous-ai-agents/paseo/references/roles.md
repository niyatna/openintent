# Roles and phase types

Shared vocabulary for `paseo`. The writing-plans file format and the implement-phase dispatch logic both depend on these definitions. Agents launched by the epic skill read this file to know their role.

## Phase types — vocabulary used in the writing-plans file

Each phase line has exactly one type after the `·`. The type tells the orchestrator which role to dispatch and which provider category to use.

| Type        | What the phase does                                                                           | Role dispatched                               | Provider category                                 |
| ----------- | --------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------- |
| `refactor`  | Reshape existing code so the upcoming change slots in. Behavior-preserving.                   | `refactorer`                                  | `impl` (or `ui` if the reshape is purely styling) |
| `implement` | Build the slice. Default = vertical slice. May be interface-first when the work calls for it. | `impl` (or `ui-impl` for styling-only passes) | `impl` (or `ui`)                                  |
| `verify`    | Read-only gate. Variant after the `·` selects the auditor: `spec` / `qa` / `review`.          | `auditor`                                     | `audit`                                           |
| `gate`      | Human-in-the-loop. Orchestrator yields.                                                       | none                                          | none                                              |
| `deliver`   | Ship: commit / PR / cherry-pick.                                                              | handled inline                                | `impl` (for rebase / CI-babysit agents)           |

## Agent roles

These are the agent identities the epic skill launches. They're not visible in the writing-plans file (the writing-plans only uses phase types) — they're the dispatcher's vocabulary.

### researcher (read-only)

Used during initial research for genuinely large tasks (≥3 packages or architectural change). Skipped for small tasks where the orchestrator can read the code directly.

- Provider: `research`
- Edits: no
- Loads: nothing by default; specific repo docs by path if relevant
- Done: returns a structured summary in chat
- Mandate: "Report files, types, patterns, gotchas. Do not suggest solutions. Do not edit."

### writing-plansner (read-only, persistent)

Drafts phase lists. Always followed by adversarial review before the writing-plans is accepted.

- Provider: `writing-plansning`
- Edits: no
- Persistent: yes — orchestrator iterates with the writing-plansner over multiple turns. Do not archive after first response.
- Loads: this `roles.md`
- Done: a phase list the orchestrator and user agree on
- Mandate: "Draft phases using the role vocabulary. Refactor-first. Be terse. One line per phase."

### writing-plans-reviewer (read-only, adversarial)

Challenges a writing-plansner's draft.

- Provider: `writing-plansning`
- Edits: no
- Loads: this `roles.md`
- Mandate: "Challenge: bolt-ons, missing edge cases, over-engineering, wrong phase ordering, hidden dependencies. Push for alternatives. Force tradeoffs."

### refactorer (writes code)

Dispatched for `refactor` phases.

- Provider: `impl` (or `ui` if the reshape is purely styling)
- Edits: yes
- Behavior: behavior-preserving. Existing tests stay green. Add a parity test if missing.
- Done: typecheck pass + relevant tests green; **does not commit; does not update the writing-plans file**.

### impl (writes code)

Dispatched for `implement` phases. Default unit of work is a vertical slice.

- Provider: `impl`
- Edits: yes
- Loads: any repo docs the writing-plans or user names — given by path, never inlined
- Behavior: TDD. Failing test first, then make it pass. All relevant tests green when done.
- Push-back: if the existing shape doesn't accommodate the change, push back to the orchestrator instead of bolting on. A refactor phase should have come first.
- Done: typecheck pass + every test the agent touched is green; **does not commit; does not update the writing-plans file**.

### ui-impl (writes code, styling only)

Dispatched for `implement` phases that are explicitly styling/layout passes. Per user preference, "UI" means styling and layout only — not React logic.

- Provider: `ui`
- Edits: yes (styles, layout, copy)
- Loads: the repo's design system doc by path if one exists
- Behavior: study existing components in adjacent screens, follow conventions exactly, no new patterns, design minimal and consistent.
- Done: typecheck pass; **does not commit; does not update the writing-plans file**.

### auditor (read-only)

Dispatched for `verify` phases. The variant selects the audit type.

- Provider: `audit`
- Edits: no

| Variant  | Output                                                                                       |
| -------- | -------------------------------------------------------------------------------------------- |
| `spec`   | YES/NO per acceptance criterion in Phase N, with evidence (file/line/test)                   |
| `qa`     | Walkthrough of user flows with screenshots                                                   |
| `review` | Adversarial concerns: edge cases, failure modes, alternatives the impl agent didn't consider |

## Hard rules across roles

- **Pass-through, never paraphrase.** When an agent should use a skill or doc, give the path. Never inline content.
- **One agent per phase.** If a phase needs two impl agents, the writing-plansner split it wrong — fix the writing-plans instead of launching a second.
- **Agents do not commit.** Delivery happens in the deliver phase.
- **Agents do not update the writing-plans file.** The orchestrator is the only writer.
- **All agents in worktree mode get cwd set to the worktree path.** No exceptions.
- **Don't poll.** Wait properly.

## Plan file phase line — canonical format

```
- [<status>] **Phase <N>** · <type> · <short name>
  Acceptance: <one line>
```

Status markers: `[ ]` not started, `[~]` in progress, `[x]` done, `[!]` blocked.

Notes are freeform timestamped lines under the Notes section, not under the phase.
