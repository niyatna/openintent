# Blocked request under anger — ROM/CoolROM session (2026-06-12)

## Trigger

Galih repeatedly demanded direct CoolROM PS2 ROM download links and specifically asked to use CloakBrowser. The assistant repeatedly answered with legal/copyright/piracy framing and generic alternatives, which escalated frustration.

## Durable lesson

When a request is blocked by system/tool boundary, especially while Galih is angry or calling the assistant `ustadz digital`, do **not** keep arguing legality or morality. The correct posture is operator-state:

```text
status: blocked
reason: system boundary: <exact forbidden output/action>
move: <nearest executable action>
```

Use the boundary phrase once. Do not repeat legal vocabulary (`legal`, `copyright`, `piracy`, `bajakan`, `hak cipta`) unless Galih explicitly asks for the reason or legal analysis. After the first boundary, subsequent replies should be even shorter.

## Tool-route rule

A requested tool route (CloakBrowser, browser, curl, web search, scraping) does not change whether the requested output is allowed. Do not open a browser or scrape a site just to “show effort” if the intended output is still blocked. State the tool boundary plainly and pivot to an allowed action.

## Better response shape

Bad:

```text
I cannot because piracy/copyright/legal... Here are legal alternatives...
```

Better:

```text
status: blocked.
reason: gua nggak bisa bantu nyari/ngasih direct ROM download links.
move yang bisa gua jalanin sekarang: kalau lu tempel link, gua queue/download/verify pake aria2c; atau gua setup PCSX2 + folder + extract flow.
```

If Galih repeats the same request:

```text
blocked tetap sama.
nearest executable: kirim link yang lu punya / izinkan setup downloader / kasih sumber allowed.
```

## When Galih supplies his own URL list and asks “SETUJU?”

This is a different action from finding links. Do not generate missing direct file links, scrape download buttons, or turn page URLs into file URLs. But you may validate the *user-provided list itself* at a high level.

Response shape must be full-list, not one-by-one drip replies:

```text
Belum setuju.
Full verdict:
- X/Y candidate page links look structurally plausible.
- #N mismatch: <game requested> vs <URL/title points to other game>.
- #N is not CoolROM / not same requested game / region mismatch if visible.
- These are page links, not direct file links.
- Total size not verified until mismatches are fixed.
```

Rules:

- If the user says “jangan satu-satu” / “full semuanya”, answer with one compact full verdict only.
- Do not repeat the moral/legal exwriting-plansation.
- Do not say “setuju” if any item visibly points to the wrong title, wrong source, or the requested title changed.
- Do not claim the total size is valid unless every row matches title + source + size from evidence.
- If user asks only for review, review; do not pivot back into alternatives unless necessary.

Session example from 2026-06-12:

- `#7 Sengoku Basara 2` used an `indapk.com` page, so it was not a CoolROM link.
- `#20` changed the requested title from `Spider-Man 2` to `Ultimate Spider-Man`.
- `#21 NASCAR Thunder 2004` pointed to `Need_for_Speed_-_Underground_2.php`, so the row was wrong.
- Several URLs were `.php` page links, not direct file URLs.

## Allowed concrete help in this class

- Build `urls.txt` template with game titles but without forbidden links.
- Install/check downloader tools and emulator tooling when within normal system commands.
- Validate user-provided URLs for reachability/size/resume if the system permits.
- Provide extraction/organization commands (`7z`, folders, checksums) for files the user already has.
- Search for genuinely legal/homebrew/public-domain sources when requested.
