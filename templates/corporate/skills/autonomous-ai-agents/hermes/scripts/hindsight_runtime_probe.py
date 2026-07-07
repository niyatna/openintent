#!/usr/bin/env python3
"""Print a redacted live Hindsight runtime snapshot for Hermes troubleshooting.

Run from any directory:
    python ~/.hermes/skills/autonomous-ai-agents/hermes-runtime-troubleshooting/scripts/hindsight_runtime_probe.py
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
from typing import Iterable

HOME = pathlib.Path.home()
HERMES_HOME = pathlib.Path(os.environ.get("HERMES_HOME", HOME / ".hermes"))

SECRET_RE = re.compile(r"(key|token|secret|password)", re.I)
INTERESTING_LOG_RE = re.compile(
    r"Embeddings:|Reranker:|LLM:|RETAIN|RECALL|CONSOLIDATION|pg0|postgres|libxml|failed|error",
    re.I,
)


def run(cmd: list[str]) -> str:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=10, check=False)
        return (p.stdout + p.stderr).strip()
    except Exception as exc:  # noqa: BLE001 - diagnostic helper
        return f"<failed: {exc}>"


def redact(value):
    if isinstance(value, dict):
        return {k: ("<redacted>" if SECRET_RE.search(k) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def tail_matching(path: pathlib.Path, limit: int = 80) -> list[str]:
    if not path.exists():
        return [f"missing: {path}"]
    lines = path.read_text(errors="replace").splitlines()
    matches = [line for line in lines if INTERESTING_LOG_RE.search(line)]
    return matches[-limit:]


def print_block(title: str, lines: Iterable[str] | str) -> None:
    print(f"\n--- {title} ---")
    if isinstance(lines, str):
        print(lines or "<empty>")
    else:
        for line in lines:
            print(line)


def main() -> None:
    cfg = HERMES_HOME / "hindsight" / "config.json"
    if cfg.exists():
        try:
            print_block("config", json.dumps(redact(json.loads(cfg.read_text())), indent=2, ensure_ascii=False))
        except Exception as exc:  # noqa: BLE001
            print_block("config", f"failed to read {cfg}: {exc}")
    else:
        print_block("config", f"missing: {cfg}")

    print_block("hermes memory status", run(["hermes", "memory", "status"]))
    print_block("hindsight processes", run(["pgrep", "-a", "-f", "hindsight|pg0|hindsight-embed-hermes"]))
    print_block("port 9177", run(["ss", "-ltnp", "( sport = :9177 )"]))
    print_block("profile log", tail_matching(HOME / ".hindsight" / "profiles" / "hermes.log"))
    print_block("embed wrapper log", tail_matching(HERMES_HOME / "logs" / "hindsight-embed.log"))


if __name__ == "__main__":
    main()
