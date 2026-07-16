# Reference: scrapling

# Blogwatcher

Track blog and RSS/Atom feed updates with the `scrapling-cli` tool. Supports automatic feed discovery, HTML scraping fallback, OPML import, and read/unread article management.

## Installation

Pick one method:

- **Go:** `go install github.com/JulienTant/scrapling-cli/cmd/scrapling-cli@latest`
- **Docker:** `docker run --rm -v scrapling-cli:/data ghcr.io/julientant/scrapling-cli`
- **Binary (Linux amd64):** `curl -sL https://github.com/JulienTant/scrapling-cli/releases/latest/download/scrapling-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin scrapling-cli`
- **Binary (Linux arm64):** `curl -sL https://github.com/JulienTant/scrapling-cli/releases/latest/download/scrapling-cli_linux_arm64.tar.gz | tar xz -C /usr/local/bin scrapling-cli`
- **Binary (macOS Apple Silicon):** `curl -sL https://github.com/JulienTant/scrapling-cli/releases/latest/download/scrapling-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin scrapling-cli`
- **Binary (macOS Intel):** `curl -sL https://github.com/JulienTant/scrapling-cli/releases/latest/download/scrapling-cli_darwin_amd64.tar.gz | tar xz -C /usr/local/bin scrapling-cli`

All releases: https://github.com/JulienTant/scrapling-cli/releases

### Docker with persistent storage

By default the database lives at `~/.scrapling-cli/scrapling-cli.db`. In Docker this is lost on container restart. Use `BLOGWATCHER_DB` or a volume mount to persist it:

```bash
# Named volume (simplest)
docker run --rm -v scrapling-cli:/data -e BLOGWATCHER_DB=/data/scrapling-cli.db ghcr.io/julientant/scrapling-cli scan

# Host bind mount
docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/scrapling-cli.db ghcr.io/julientant/scrapling-cli scan
```

### Migrating from the original scrapling

If upgrading from `Hyaxia/scrapling`, move your database:

```bash
mv ~/.scrapling/scrapling.db ~/.scrapling-cli/scrapling-cli.db
```

The binary name changed from `scrapling` to `scrapling-cli`.

## Common Commands

### Managing blogs

- Add a blog: `scrapling-cli add "My Blog" https://example.com`
- Add with explicit feed: `scrapling-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml`
- Add with HTML scraping: `scrapling-cli add "My Blog" https://example.com --scrape-selector "article h2 a"`
- List tracked blogs: `scrapling-cli blogs`
- Remove a blog: `scrapling-cli remove "My Blog" --yes`
- Import from OPML: `scrapling-cli import subscriptions.opml`

### Scanning and reading

- Scan all blogs: `scrapling-cli scan`
- Scan one blog: `scrapling-cli scan "My Blog"`
- List unread articles: `scrapling-cli articles`
- List all articles: `scrapling-cli articles --all`
- Filter by blog: `scrapling-cli articles --blog "My Blog"`
- Filter by category: `scrapling-cli articles --category "Engineering"`
- Mark article read: `scrapling-cli read 1`
- Mark article unread: `scrapling-cli unread 1`
- Mark all read: `scrapling-cli read-all`
- Mark all read for a blog: `scrapling-cli read-all --blog "My Blog" --yes`

## Environment Variables

All flags can be set via environment variables with the `BLOGWATCHER_` prefix:

| Variable | Description |
|---|---|
| `BLOGWATCHER_DB` | Path to SQLite database file |
| `BLOGWATCHER_WORKERS` | Number of concurrent scan workers (default: 8) |
| `BLOGWATCHER_SILENT` | Only output "scan done" when scanning |
| `BLOGWATCHER_YES` | Skip confirmation prompts |
| `BLOGWATCHER_CATEGORY` | Default filter for articles by category |

## Example Output

```
$ scrapling-cli blogs
Tracked blogs (1):

  xkcd
    URL: https://xkcd.com
    Feed: https://xkcd.com/atom.xml
    Last scanned: 2026-04-03 10:30
```

```
$ scrapling-cli scan
Scanning 1 blog(s)...

  xkcd
    Source: RSS | Found: 4 | New: 4

Found 4 new article(s) total!
```

```
$ scrapling-cli articles
Unread articles (2):

  [1] [new] Barrel - Part 13
       Blog: xkcd
       URL: https://xkcd.com/3095/
       Published: 2026-04-02
       Categories: Comics, Science

  [2] [new] Volcano Fact
       Blog: xkcd
       URL: https://xkcd.com/3094/
       Published: 2026-04-01
       Categories: Comics
```

## Notes

- Auto-discovers RSS/Atom feeds from blog homepages when no `--feed-url` is provided.
- Falls back to HTML scraping if RSS fails and `--scrape-selector` is configured.
- Categories from RSS/Atom feeds are stored and can be used to filter articles.
- Import blogs in bulk from OPML files exported by Feedly, Inoreader, NewsBlur, etc.
- Database stored at `~/.scrapling-cli/scrapling-cli.db` by default (override with `--db` or `BLOGWATCHER_DB`).
- Use `scrapling-cli <command> --help` to discover all flags and options.