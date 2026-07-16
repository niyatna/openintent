---
author: Hermes Agent
description: Use when sandboxing mockups, building React/Tailwind component widgets,
  or configuring typographic pretext layouts.
license: MIT
metadata:
  hermes:
    category: creative
    tags:
    - design
    - html
    - css
    - mockup
    - prototype
    - pretext
    - design-system
    - tokens
    - creative
name: web-widgets
version: 1.0.0
---


# Creative Web Prototyping

This class-level skill provides a comprehensive guide to designing, mocking up, and prototyping frontend web interfaces. It combines rapid throwaway mockups (sketch), high-fidelity HTML/CSS artifacts (claude-design), pretext kinetic layouts, design token validation (design-md), and a catalog of modern design systems (popular-web-designs).

---

## 1. Throwaway HTML Mockups (Sketch)
Use this workflow when you need to quickly feel out visual options or layouts before implementing a formal page.

### Core Method
1. **Intake**: Understand the user's constraints, target audience, and layout requirements.
2. **Variants**: Generate 2-3 design variants demonstrating different visual "stances" or aesthetics (e.g., minimalist vs. brutalist).
3. **Draft HTML**: Build self-contained HTML mockups using CSS frameworks (Tailwind/UnoCSS via CDN) or plain CSS inside single files.
4. **Compare**: Create a head-to-head comparison explaining tradeoffs of each option.

### Rules & Pitfalls
- Hardcode initial data and mock images/icons. Do not spend time on heavy scripting.
- Provide clear visual differentiation in the stances.

---

## 2. Desktop & Guide Sites (Claude Design)
For serious HTML artifacts, documentation directories, guide sites, or presentations.

### Standards
- **CSS**: Prefer Tailwind/UnoCSS CDN. Rely on semantic layout classes (CSS Grid, Flexbox).
- **Component Polish**: Clean spacing, micro-interactions, dark/light mode toggle helper.
- **Portability**: Keep the artifact self-contained or reference robust static resources (Lucide Icons, Unsplash for images).
- **Anti-Slop**: Avoid generic placeholders. Write context-appropriate content (real copy, no lorem ipsum).

---

## 3. Pretext Kinetic Demos (Pretext)
For graphic text layouts, kinetic typography, DOM-free text games, and text-based interactive layouts.

### Implementation Checklist
- Leverage standard DOM layouts or render custom graphics inside canvas/pre tags.
- Refer to templates:
  - `templates/donut-orbit.html`
  - `templates/hello-orb-flow.html`
- Refer to `references/patterns.md` for specific pretext kinetic rules.

---

## 4. Design Tokens & Google's DESIGN.md Spec (Design Specs)
For compiling, diffing, and validating token formats (DTCG format, Tailwind mapping, WCAG contrast).

### Workflow
- Author specs mapping color, spacing, typography, and theme components.
- Run validator script or verify contrast gates.
- Refer to `templates/starter.md` under this skill directory.

---

## 5. Popular Design Catalog Reference (Popular Web Designs)
A reference list of font substitutions and themes modeled on 54 visual design systems (like Stripe, Vercel, Linear, etc.). Use the templates under `templates/` to kickstart layouts.

### Reference Font Stack Substitutes
- **Minimal Serif (Apple-style)**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`
- **Developer Mono (Linear-style)**: `"JetBrains Mono", Fira Code, monospace`
- **Warm Editorial**: `Georgia, Cambria, serif`

### Showcase Catalog
Check detailed template systems under `templates/<design_name>.md` to clone patterns (e.g., Stripe's animated gradients, Linear's dark dashboard layouts, Vercel's stark terminal borders).


## References & Sub-playbooks
Detailed instructions for design methodologies/extensions are modularly stored, load them selectively via `skill_view` references:
- `references/claude-design.md` — Instruction set for Claude Design
- `references/design-md.md` — Instruction set for Design Md
- `references/popular-web-designs.md` — Instruction set for Popular Web Designs
- `references/pretext.md` — Instruction set for Pretext
- `references/sketch.md` — Instruction set for Sketch
- `references/web-artifacts-builder.md` — Instruction set for Web Artifacts Builder
