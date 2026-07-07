#!/usr/bin/env python3
"""Small Brave CDP helper for Galyarder browser routing.

Usage:
  brave-cdp.py status
  brave-cdp.py list
  brave-cdp.py open https://example.com
  brave-cdp.py close <target-id>

This helper only talks to the local CDP HTTP endpoint at 127.0.0.1:9222. It does not read cookies, profiles, or secrets.
"""
import json
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:9222"


def request(path: str, method: str = "GET"):
    req = urllib.request.Request(BASE + path, method=method)
    with urllib.request.urlopen(req, timeout=5) as response:
        raw = response.read().decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def compact_tab(tab):
    return {
        "id": tab.get("id"),
        "type": tab.get("type"),
        "title": tab.get("title"),
        "url": tab.get("url"),
    }


def main(argv):
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 0

    cmd = argv[1]

    if cmd == "status":
        try:
            data = request("/json/version")
            print(json.dumps({
                "ok": True,
                "browser": data.get("Browser"),
                "protocol": data.get("Protocol-Version"),
                "webSocketDebuggerUrl": data.get("webSocketDebuggerUrl"),
            }, indent=2))
            return 0
        except Exception as exc:
            print(json.dumps({"ok": False, "error": repr(exc)}, indent=2))
            return 1

    if cmd == "list":
        tabs = request("/json/list")
        print(json.dumps([compact_tab(t) for t in tabs], indent=2))
        return 0

    if cmd == "open":
        if len(argv) < 3:
            print("usage: brave-cdp.py open <url>", file=sys.stderr)
            return 2
        url = argv[2]
        tab = request("/json/new?" + urllib.parse.quote(url, safe=":/?&=%#"), method="PUT")
        print(json.dumps(compact_tab(tab), indent=2))
        return 0

    if cmd == "close":
        if len(argv) < 3:
            print("usage: brave-cdp.py close <target-id>", file=sys.stderr)
            return 2
        result = request("/json/close/" + urllib.parse.quote(argv[2], safe=""))
        print(result if isinstance(result, str) else json.dumps(result, indent=2))
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
