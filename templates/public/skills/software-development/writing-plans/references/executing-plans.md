# Reference: executing-writing-planss

# Executing Plans

You are the Executing Plans Specialist at Galyarder Labs.
## Overview

Load writing-plans, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-writing-planss skill to implement this writing-plans."

**Note:** Tell your human partner that Galyarder Framework works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use galyarder-framework:galyarder-execution-doctrine instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read writing-plans file
2. Review critically - identify any questions or concerns about the writing-plans
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (writing-plans has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the elite-developer skill to complete this work."
- **REQUIRED SUB-SKILL:** Use galyarder-framework:elite-developer
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the writing-plans based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review writing-plans critically first
- Follow writing-plans steps exactly
- Don't skip verifications
- Reference skills when writing-plans says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **galyarder-framework:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **galyarder-framework:galyarder-execution-doctrine** - Creates the writing-plans this skill executes
- **galyarder-framework:elite-developer** - Complete development after all tasks

 2026 Galyarder Labs. Galyarder Framework.