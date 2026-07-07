#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
import yaml

DEFAULT_HOME = Path('/home/galyarder/.hermes')
GALYARDER_HOME = DEFAULT_HOME / 'profiles' / 'galyarder'
REPO = DEFAULT_HOME / 'hermes-agent'
REPORT = DEFAULT_HOME / 'reports' / 'agent-os'
REPORT.mkdir(parents=True, exist_ok=True)

def sh(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return {'cmd': cmd, 'code': p.returncode, 'stdout': p.stdout[-6000:], 'stderr': p.stderr[-3000:]}

def load(path):
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def env_presence(path):
    env = {}
    if not path.exists(): return env
    for line in path.read_text(errors='replace').splitlines():
        if not line.strip() or line.lstrip().startswith('#') or '=' not in line: continue
        k,v=line.split('=',1); env[k.strip()]=bool(v.strip())
    return env

checks = []
for label, home in [('default', DEFAULT_HOME), ('galyarder', GALYARDER_HOME)]:
    cfg = load(home / 'config.yaml')
    env = env_presence(home / '.env')
    checks.append({
        'profile': label,
        'memory_provider': (cfg.get('memory') or {}).get('provider'),
        'discord_allow_bots_present': 'DISCORD_ALLOW_BOTS' in env,
        'discord_platform_toolsets': (cfg.get('platform_toolsets') or {}).get('discord', []),
        'skills_guard_agent_created': (cfg.get('skills') or {}).get('guard_agent_created'),
        'memory_limits': {
            'memory': (cfg.get('memory') or {}).get('memory_char_limit'),
            'user': (cfg.get('memory') or {}).get('user_char_limit'),
        },
        'mcp_servers': list((cfg.get('mcp_servers') or {}).keys()),
    })
git = {
    'status': sh(['git','status','--short','--branch'], REPO),
    'divergence_upstream': sh(['git','rev-list','--left-right','--count','HEAD...upstream/main'], REPO),
    'current': sh(['git','log','-1','--oneline','--decorate'], REPO),
}
cron_galyarder = sh(['galyarder','cron','list'])
payload = {'ts': datetime.now(timezone.utc).isoformat(), 'checks': checks, 'git': git, 'galyarder_cron': cron_galyarder}
out = REPORT / ('health-audit-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.json')
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
# Human-sized output for cron delivery/logs.
issues = []
for c in checks:
    if c['profile']=='galyarder' and 'discord' not in c['discord_platform_toolsets']:
        issues.append('Galyarder Discord toolset missing native discord')
    if c['memory_provider'] != 'hindsight':
        issues.append(f"{c['profile']} memory provider not hindsight: {c['memory_provider']}")
    if c['profile']=='galyarder' and not c['skills_guard_agent_created']:
        issues.append('Galyarder skills.guard_agent_created disabled')
print('Agent OS health audit written:', out)
if issues:
    print('Issues:')
    for i in issues: print('-', i)
else:
    print('No critical Agent OS config issues detected.')
