# 2026-05-11 YouTube summary grounding miss

## What happened

The assistant fetched and summarized a YouTube video about five future industries. The extraction and summary were grounded, but the answer then connected the video to Galih's company direction and systems from active context without doing a separate memory/skill grounding pass.

Galih corrected this sharply: every substantive response must use available live layers, including SOUL, native memory, `USER.md`, `MEMORY.md`, Hindsight, relevant skills, MCP/tools, and runtime tools when appropriate.

## Reusable lesson

Extraction and interpretation are separate tasks.

- Transcript fetched → summary is grounded.
- Strategic implication for Galih/Galyarder → requires memory/Hindsight + relevant Keiya/Galyarder route.
- Capability/current-state claim → requires live state/tool check.

## Correct future route

For a shared YouTube/video/link when no explicit output is given:

1. Use `youtube-content` or the relevant extraction skill/tool.
2. Summarize the content if that is the obvious default.
3. Before adding implications for Galih/Galyarder, load `tool-grounded-responses` plus relevant router/presence/company skill and check Hindsight/native memory.
4. Keep final wording human and concise; do not expose the full tool inventory unless asked.
