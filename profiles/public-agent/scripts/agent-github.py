#!/usr/bin/env python3
"""Run gh with a dedicated Keiya/Galyarder GitHub token without printing secrets.

Usage:
  agent-github.py keiya --check
  agent-github.py galyarder repo list --limit 5

Token file:
  /home/galyarder/.hermes/private/credentials/agents/<owner>/github/token.env
  containing one line: GITHUB_TOKEN=<fine-grained PAT>
"""
from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/galyarder/.hermes/private/credentials/agents')
ALLOWED = {'keiya', 'galyarder'}


def parse_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding='utf-8', errors='replace').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def account_fields(owner: str) -> dict[str, str]:
    path = ROOT / owner / 'github' / 'account.txt'
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw in path.read_text(encoding='utf-8', errors='replace').splitlines():
        if '=' in raw and not raw.lstrip().startswith('#'):
            key, value = raw.split('=', 1)
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def ensure_private_paths(owner: str) -> tuple[Path, Path]:
    base = ROOT / owner / 'github'
    base.mkdir(parents=True, exist_ok=True)
    os.chmod(base, 0o700)
    token_file = base / 'token.env'
    if not token_file.exists():
        token_file.write_text(
            '# Local-only GitHub token file. Do not commit, paste, screenshot, or log.\n'
            '# Use a fine-grained PAT for this dedicated agent-owned GitHub account.\n'
            'GITHUB_TOKEN=\n'
            'TOKEN_KIND=fine-grained-pat\n'
            'TOKEN_STATUS=pending\n',
            encoding='utf-8',
        )
    os.chmod(token_file, 0o600)
    gh_config = base / 'gh-config'
    gh_config.mkdir(parents=True, exist_ok=True)
    os.chmod(gh_config, 0o700)
    return token_file, gh_config


def sanitized_error(owner: str, status: str, detail: str = '') -> int:
    print(json.dumps({'owner': owner, 'ok': False, 'status': status, 'detail': detail}, indent=2))
    return 2


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ALLOWED:
        print('Usage: agent-github.py {keiya|galyarder} [--check|gh args...]', file=sys.stderr)
        return 2

    owner = sys.argv[1]
    args = sys.argv[2:]
    token_file, gh_config = ensure_private_paths(owner)
    env_data = parse_env(token_file)
    token = env_data.get('GITHUB_TOKEN') or env_data.get('GH_TOKEN') or env_data.get('TOKEN')
    if not token:
        return sanitized_error(owner, 'token-missing', f'fill {token_file} with GITHUB_TOKEN=<fine-grained PAT>')

    env = os.environ.copy()
    env['GH_TOKEN'] = token
    env['GITHUB_TOKEN'] = token
    env['GH_CONFIG_DIR'] = str(gh_config)
    env.setdefault('HOME', '/home/galyarder')

    if not args or args == ['--check']:
        expected = account_fields(owner).get('USERNAME', '')
        proc = subprocess.run(
            ['gh', 'api', 'user', '--jq', '.login'],
            text=True,
            capture_output=True,
            env=env,
            timeout=60,
        )
        login = proc.stdout.strip()
        ok = proc.returncode == 0 and bool(login) and (not expected or login == expected)
        result = {
            'owner': owner,
            'ok': ok,
            'status': 'github-token-valid' if ok else 'github-token-invalid-or-wrong-account',
            'expected_login': expected,
            'actual_login': login if login else None,
            'token_file': str(token_file),
            'token_file_mode': oct(stat.S_IMODE(token_file.stat().st_mode)),
            'gh_config_dir': str(gh_config),
        }
        if not ok and proc.stderr.strip():
            result['gh_error'] = proc.stderr.strip().splitlines()[-1][:200]
        print(json.dumps(result, indent=2))
        return 0 if ok else 1

    proc = subprocess.run(['gh', *args], env=env)
    return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())
