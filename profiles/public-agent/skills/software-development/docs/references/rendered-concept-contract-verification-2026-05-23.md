# Rendered concept-contract verification for advanced docs

Use this reference when a documentation rewrite is long, builds successfully, but still may be too thin for the promised advanced guide.

## Lesson

Depth is not proved by word count or a green build. A page can be long and still miss the concrete records, policy nouns, role boundaries, proof artifacts, and decision vocabulary that make it useful.

Before reporting completion on an advanced public guide, define a page-specific concept contract and verify it twice:

1. **Source contract** — scan the markdown/source file for the required concepts, artifacts, and policy vocabulary promised by that page.
2. **Rendered contract** — scan the built HTML or crawled page text for the same concepts, because custom renderers, content manifests, generated output, or locale overrides can hide source content.

If the contract fails, make a small semantic patch in the correct section. Do not keyword-stuff. Add the missing concept as a real operating rule, table field, template field, failure mode, or proof requirement.

## Reusable pattern

A useful verification pass for a batch of advanced docs is:

- line and word count;
- heading depth rules for the renderer;
- frontmatter/body leak check;
- forbidden framing vocabulary check when the user gave word constraints;
- public-safety scan for private paths, secret-shaped strings, wallet-shaped values, private IDs, and credential examples;
- required concept list per page;
- build/check command;
- rendered route status;
- rendered text concept scan;
- rendered broken-heading/frontmatter scan;
- same-origin crawl.

## When the first scan fails

Treat the failing scan as useful signal, not embarrassment. Patch the missing concept, then rerun the whole verification ladder. Report the final evidence, including that the first scan found gaps and the final scan is clean.

## Reporting rule

Do not call a docs batch complete after only a source markdown scan or a build. For advanced docs, completion requires source + rendered verification against the page-specific concept contract.