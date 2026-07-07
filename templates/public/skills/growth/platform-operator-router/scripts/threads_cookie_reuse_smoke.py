#!/usr/bin/env python3
"""Compatibility wrapper.
Canonical Threads cookie-reuse smoke script lives under threads-operator.
"""
from pathlib import Path
import runpy

CANONICAL = Path('/home/galyarder/.hermes/profiles/galyarder/skills/growth/threads-operator/scripts/threads_cookie_reuse_smoke.py')
if not CANONICAL.exists():
    raise SystemExit(f'Missing canonical Threads smoke script: {CANONICAL}')
runpy.run_path(str(CANONICAL), run_name='__main__')
