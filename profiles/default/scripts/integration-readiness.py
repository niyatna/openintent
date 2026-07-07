#!/usr/bin/env python3
"""Read-only readiness check for Linear/Notion MCP integration.

Linear and Notion are configured as remote MCP servers, not direct REST/API-key
skills. This script checks the Hermes MCP config/listing surfaces and reports the
correct OAuth/shared-page readiness path. It does not require or print
LINEAR_API_KEY / NOTION_API_KEY.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

HOME = Path('/home/galyarder/.hermes')
REPORT_DIR = HOME / 'reports/agent-os'
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CONFIGS = {
    'default': HOME / 'config.yaml',
    'galyarder': HOME / 'profiles/galyarder/config.yaml',
}
EXPECTED = {
    'linear': {
        'url': 'https://mcp.linear.app/mcp',
        'auth_mode': 'remote_mcp_oauth',
        'user_action': 'complete Linear OAuth in an interactive MCP-capable session if tools are not discovered/usable',
    },
    'notion': {
        'url': 'https://mcp.notion.com/mcp',
        'auth_mode': 'remote_mcp_oauth_plus_shared_pages',
        'user_action': 'complete Notion OAuth and share the target workspace/pages/databases with the Notion MCP connection',
    },
}


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def run(cmd: list[str]) -> dict[str, Any]:
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    return {
        'exit_code': p.returncode,
        'stdout': p.stdout[-4000:],
        'stderr': p.stderr[-1200:],
    }


def config_check(path: Path) -> dict[str, Any]:
    cfg = load_yaml(path)
    servers = cfg.get('mcp_servers') or {}
    out: dict[str, Any] = {}
    for name, expected in EXPECTED.items():
        server = servers.get(name) or {}
        out[name] = {
            'configured': bool(server),
            'enabled': server.get('enabled') is True,
            'url_ok': server.get('url') == expected['url'],
            'url': server.get('url'),
            'auth_mode': expected['auth_mode'],
            'auth_note': server.get('auth_note', ''),
            'required_user_action_if_not_usable': expected['user_action'],
        }
    return out


def main() -> int:
    result: dict[str, Any] = {
        'status': 'pass',
        'note': 'Linear/Notion use remote MCP OAuth, not LINEAR_API_KEY/NOTION_API_KEY direct API-key readiness.',
        'profiles': {},
        'mcp_list': {},
        'remaining_user_actions': {
            'linear': EXPECTED['linear']['user_action'],
            'notion': EXPECTED['notion']['user_action'],
        },
    }
    errors: list[str] = []

    for label, path in CONFIGS.items():
        checks = config_check(path)
        result['profiles'][label] = checks
        for server_name, check in checks.items():
            if not (check['configured'] and check['enabled'] and check['url_ok']):
                errors.append(f'{label}.{server_name} MCP config incomplete: {check}')

    result['mcp_list']['default'] = run(['hermes', 'mcp', 'list'])
    result['mcp_list']['galyarder'] = run(['hermes', '--profile', 'galyarder', 'mcp', 'list'])
    for label, listing in result['mcp_list'].items():
        if listing['exit_code'] != 0:
            errors.append(f'{label} mcp list failed')
            continue
        stdout = listing.get('stdout') or ''
        for server_name in EXPECTED:
            if server_name not in stdout or '✓ enabled' not in stdout:
                errors.append(f'{label} mcp list does not show {server_name} enabled')

    result['errors'] = errors
    if errors:
        result['status'] = 'fail'

    out = REPORT_DIR / 'integration-readiness-latest.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print('REPORT', out)
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
