#!/usr/bin/env python3
"""Agent OS learning review hook: queue candidates, never auto-promote."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
from typing import Any

HOME = Path(os.environ.get('HERMES_HOME', '/opt/data')).expanduser()
QUEUE = HOME / 'scripts' / 'agent-os-learning-review-queue.py'


def _extract_text(data: dict[str, Any], raw: str = '') -> tuple[str, str]:
    profile = data.get('profile') or os.environ.get('HERMES_PROFILE', 'default')
    text = data.get('learning') or data.get('summary') or data.get('message') or data.get('prompt') or ''
    context = data.get('context')
    if not text and isinstance(context, dict):
        text = context.get('summary') or context.get('message') or context.get('prompt') or ''
        profile = context.get('profile') or profile
    if not text and isinstance(data.get('messages'), list):
        joined = '\n'.join(str(m.get('content','')) for m in data['messages'][-6:] if isinstance(m, dict))
        text = joined[-2000:]
    if not text and raw:
        text = raw[-2000:]
    return profile, (text or '').strip()


def queue_learning(profile: str, text: str, source: str = 'agent-os-learning-review-hook') -> None:
    if not text:
        return
    if len(text) > 2500:
        text = text[:2500] + '…'
    subprocess.run([
        str(QUEUE), 'add', '--profile', profile, '--source', source,
        '--kind', 'candidate', '--target', 'reviewed-promotion', '--text', text
    ], check=False)


def main() -> int:
    raw = sys.stdin.read() if not sys.stdin.isatty() else ''
    try:
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    profile, text = _extract_text(data, raw)
    queue_learning(profile, text)
    return 0


def handle(event_type: str, context: dict[str, Any] | None = None) -> None:
    context = context or {}
    profile = context.get('profile') or os.environ.get('HERMES_PROFILE', 'default')
    bits = [f'event={event_type}']
    for key in ('session_id', 'platform', 'source', 'summary'):
        if context.get(key):
            bits.append(f'{key}={context.get(key)}')
    text = context.get('summary') or context.get('message') or '; '.join(bits)
    queue_learning(profile, text, source=f'hook:{event_type}')


if __name__ == '__main__':
    raise SystemExit(main())
