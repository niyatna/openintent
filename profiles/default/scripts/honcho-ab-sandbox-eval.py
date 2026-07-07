#!/usr/bin/env python3
"""Honcho A/B sandbox evaluation guard.

This does not migrate production memory. It records a daily boundary/evaluation
snapshot comparing production Hindsight profiles with the Honcho sandbox.
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

import yaml

HOME = Path('/home/galyarder/.hermes')
REPORT_DIR = HOME / 'reports' / 'agent-os'
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str], timeout: int = 120) -> dict:
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    return {
        'cmd': cmd,
        'exit_code': p.returncode,
        'stdout': p.stdout[-4000:],
        'stderr': p.stderr[-4000:],
    }


def provider(config_path: Path) -> str | None:
    cfg = yaml.safe_load(config_path.read_text()) or {}
    return (cfg.get('memory') or {}).get('provider')


def main() -> int:
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S')
    local_stamp = dt.datetime.now().isoformat(timespec='seconds')
    checks = {
        'default_provider': provider(HOME / 'config.yaml'),
        'galyarder_provider': provider(HOME / 'profiles/galyarder/config.yaml'),
        'honcho_sandbox_provider': provider(HOME / 'profiles/honcho-sandbox/config.yaml'),
    }
    commands = {
        'default_memory_status': run(['hermes', 'memory', 'status']),
        'galyarder_memory_status': run(['hermes', '--profile', 'galyarder', 'memory', 'status']),
        'honcho_sandbox_memory_status': run(['hermes', '--profile', 'honcho-sandbox', 'memory', 'status']),
    }
    errors = []
    if checks['default_provider'] != 'hindsight':
        errors.append('default/Keiya production memory is not hindsight')
    if checks['galyarder_provider'] != 'hindsight':
        errors.append('Galyarder production memory is not hindsight')
    if checks['honcho_sandbox_provider'] != 'honcho':
        errors.append('honcho-sandbox memory is not honcho')
    for name, result in commands.items():
        if result['exit_code'] != 0:
            errors.append(f'{name} command failed')
    report = {
        'timestamp_utc': stamp,
        'timestamp_local': local_stamp,
        'purpose': 'Honcho A/B sandbox boundary evaluation without production migration',
        'checks': checks,
        'commands': commands,
        'errors': errors,
        'status': 'fail' if errors else 'pass',
        'production_migration': 'not_performed',
        'notes': [
            'Production Keiya/default and Galyarder must remain on Hindsight during A/B.',
            'honcho-sandbox is the only profile expected to use Honcho.',
            'This script records boundary evidence; it does not alter config or memory provider.',
        ],
    }
    out = REPORT_DIR / f'honcho-ab-sandbox-eval-{stamp}.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if errors:
        print('HONCHO_AB_EVAL FAIL', out)
        for e in errors:
            print('-', e)
        return 1
    print('HONCHO_AB_EVAL PASS', out)
    print('default=hindsight galyarder=hindsight honcho-sandbox=honcho')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
