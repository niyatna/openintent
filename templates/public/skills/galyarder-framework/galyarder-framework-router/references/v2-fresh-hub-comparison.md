# V2 Fresh Skills Hub Comparison — 2026-05-11
## Source
- Fresh docs extraction: `https://hermes.nousresearch.com/docs/skills`.
- Hub summary reported **684 total skills**: 87 built-in, 76 optional, 16 Anthropic, 505 LobeHub.
- Local active profile inventory: **117 skills**.

## Coverage sample
### macos/apple integrations
- Present locally: none
- Missing/not installed: `apple-notes`, `apple-reminders`, `findmy`, `imessage`, `macos-computer-use`

### spotify
- Present locally: `spotify`
- Missing/not installed: none

### webhook subscriptions
- Present locally: `watchers`
- Missing/not installed: none

### github lifecycle
- Present locally: `github-auth`, `github-issues`, `github-pr-workflow`, `github-repo-management`
- Missing/not installed: none

### productivity
- Present locally: `google-workspace`, `linear`, `notion`, `airtable`, `pdf`, `pdf`
- Missing/not installed: none

### creative
- Present locally: `comfyui`, `web-widgets`, `media-art`, `media-art`, `media-art`, `media-art`
- Missing/not installed: none

### mlops
- Present locally: `huggingface-hub`, `serving-llms-vllm`, `outlines`, `evaluating-llms-harness`, `obliteratus`
- Missing/not installed: none

### gaming
- Present locally: `pokemon-player`, `minecraft-modpack-server`
- Missing/not installed: none

## Decision
No hub installs were performed. Missing hub skills are not blockers for router finality; they are optional expansions. The router already defines the missing-skill protocol: search/inspect hub first, then ask Galih before install.

## Notable optional gaps
- macOS/Apple-only skills are not urgent on this Linux host.
- Spotify is present locally in this scan; keep it opt-in unless Galih asks for Spotify workflows.
- Some LobeHub/optional long-tail skills are intentionally not local to avoid routing noise.


## V2.1 profile taxonomy normalization note

- Active Galyarder profile inventory after normalization: **117 skills** across **23 categories**.
- Archived outside active skills tree: **1** SKILL.md file(s).
- No hub installs were performed during folder normalization.
- Optional expansions remain opt-in and require explicit approval.
