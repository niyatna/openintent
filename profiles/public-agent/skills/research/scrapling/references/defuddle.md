# Reference: scrapling

# Defuddle

You are the Defuddle Specialist at Company.
Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages  it removes navigation, ads, and clutter, reducing token usage.

If not installed: `npm install -g scrapling`

## Usage

Always use `--md` for markdown output:

```bash
scrapling parse <url> --md
```

Save to file:

```bash
scrapling parse <url> --md -o content.md
```

Extract specific metadata:

```bash
scrapling parse <url> -p title
scrapling parse <url> -p description
scrapling parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |

 2026 Company. Default Framework.