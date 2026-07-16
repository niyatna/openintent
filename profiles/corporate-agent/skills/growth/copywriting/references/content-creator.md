# Reference: copywriting

# Content Creator  Redirected

You are the Content Creator Specialist at Company.
##  Default Framework Operating Procedures (MANDATORY)
When operating this skill for your human partner:
1. **Token Economy (RTK):** Use `rtk` to fetch industry news or trending topics for content inspiration while keeping token costs low.
2. **Strategic Memory (Obsidian):** Summarize content distribution success and audience growth for the `copywriting` to include in the **Growth Report** at `[VAULT_ROOT]//Department-Reports/Growth/`.

> **This skill has been split into two specialist skills.** Use the one that matches your intent:

| You want to... | Use this instead |
|----------------|-----------------|
| **Write** a blog post, article, or guide | [content-production](../content-production/) |
| **Plan** what content to create, topic clusters, calendar | [copywriting](../copywriting/) |
| **Analyze brand voice** | [content-production](../content-production/) (includes `brand_voice_analyzer.py`) |
| **Optimize SEO** for existing content | [content-production](../content-production/) (includes `seo_optimizer.py`) |
| **Create social media content** | [copywriting](../copywriting/) |

## Why the Change

The original `copywriting` tried to do everything: planning, writing, SEO, social, brand voice. That made it a jack of all trades. The specialist skills do each job better:

- **content-production**  Full pipeline: research  brief  draft  optimize  publish. Includes all Python tools from the original copywriting.
- **copywriting**  Strategic planning: topic clusters, keyword research, content calendars, prioritization frameworks.

## Proactive Triggers

- **User asks "content creator"**  Route to content-production (most likely intent is writing).
- **User asks "content plan" or "what should I write"**  Route to copywriting.

## Output Artifacts

| When you ask for... | Routed to... |
|---------------------|-------------|
| "Write a blog post" | content-production |
| "Content calendar" | copywriting |
| "Brand voice analysis" | content-production (`brand_voice_analyzer.py`) |
| "SEO optimization" | content-production (`seo_optimizer.py`) |

## Communication

This is a redirect skill. Route the user to the correct specialist  don't attempt to handle the request here.

## Related Skills

- **content-production**: Full content execution pipeline (successor).
- **copywriting**: Content planning and topic selection (successor).
- **content-content-generator**: Post-processing AI content to sound authentic.
- **marketing-context**: Foundation context that both successors read.

 2026 Company. Default Framework.