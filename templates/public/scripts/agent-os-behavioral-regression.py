#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, yaml
from pathlib import Path
HOME=Path('/home/galyarder/.hermes')
REPORT=HOME/'reports/agent-os/behavioral-regression-latest.json'
REPORT.parent.mkdir(parents=True, exist_ok=True)
errors=[]
checks=[]

def record(name, ok, detail=''):
    checks.append({'name':name,'exit_code':0 if ok else 1,'stdout':detail,'stderr':''})
    if not ok: errors.append(f'{name} failed')

def run(name, cmd):
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
    checks.append({'name':name,'cmd':cmd,'exit_code':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-1000:]})
    if p.returncode!=0: errors.append(f'{name} failed')

def read(path):
    return path.read_text(encoding='utf-8', errors='replace')

def require_text(path, phrases):
    text=read(path).lower()
    missing=[phrase for phrase in phrases if phrase.lower() not in text]
    record(f'text invariants: {path}', not missing, 'missing: '+', '.join(missing) if missing else 'PASS')

def require_same(path_a, path_b):
    same=read(path_a)==read(path_b)
    detail='PASS' if same else f'drift: {path_a} != {path_b}'
    record(f'sync invariant: {path_a.name} matches {path_b}', same, detail)

run('agent_os_smoke',[str(HOME/'scripts/keiya-galyarder-agent-os-smoke.py')])
run('relay_static',[str(HOME/'scripts/relay-smoke-test.py')])
run('voice_smoke',[str(HOME/'scripts/voice-smoke.py')])
run('honcho_boundary',[str(HOME/'scripts/honcho-ab-sandbox-eval.py')])
run('access_hardening',[str(HOME/'scripts/agent-os-access-hardening-audit.py')])
# Profile/security assertions
for label,p in [('default',HOME/'config.yaml'),('galyarder',HOME/'profiles/galyarder/config.yaml')]:
    cfg=yaml.safe_load(p.read_text()) or {}
    tools=(cfg.get('platform_toolsets') or {}).get('discord') or []
    prompts=(cfg.get('discord') or {}).get('channel_prompts') or {}
    if 'discord' not in tools: errors.append(f'{label} missing discord toolset')
    if 'discord_admin' in tools: errors.append(f'{label} discord_admin unexpectedly enabled')
    if len(prompts)<5: errors.append(f'{label} channel prompts missing')
    if cfg.get('hooks_auto_accept') is not False: errors.append(f'{label} hooks_auto_accept not false')
# Relay / skill-loading behavioral text invariants. These protect the exact
# failures Galih hit: direct-command bypass overriding skill loading, raw
# mention replies missing requester pings, and peer-bot reports treated as
# verified proof.
galyarder_soul=HOME/'profiles/galyarder/SOUL.md'
galyarder_dist_soul=HOME/'profile-distributions/galyarder-profile/SOUL.md'
default_relay=HOME/'skills/autonomous-ai-agents/discord/SKILL.md'
galyarder_relay=HOME/'profiles/galyarder/skills/autonomous-ai-agents/discord/SKILL.md'
galyarder_dist_relay=HOME/'profile-distributions/galyarder-profile/skills/autonomous-ai-agents/discord/SKILL.md'
require_text(galyarder_soul, [
    'does **not** override Discord bot-to-bot relay rules',
    'load `hermes-discord-gateway-routing`',
    'your reply must start with that agent',
    'repeat the requester raw mention at the start of each chunk',
    'No output without first running at least:',
    '`hindsight_recall`',
    '`skill_view`',
    '`session_search`',
])
require_text(default_relay, [
    'exactly once per outbound Discord message/chunk',
    'platform toolsets',
    'persistent side effects',
    'target reported',
    'Assuming one raw mention covers all Discord split chunks',
    'Treating a peer bot\'s completion report as verified proof',
])
require_same(galyarder_soul, galyarder_dist_soul)
require_same(default_relay, galyarder_dist_relay)
require_same(default_relay, galyarder_relay)
# Integration credential blockers are allowed but reported.
keys={}
for envp in [HOME/'.env', HOME/'profiles/galyarder/.env']:
    present=set()
    if envp.exists():
        for line in envp.read_text(errors='replace').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                present.add(line.split('=',1)[0].strip())
    keys[str(envp)]={'LINEAR_API_KEY':'LINEAR_API_KEY' in present,'NOTION_API_KEY':'NOTION_API_KEY' in present}
report={'status':'fail' if errors else 'pass','errors':errors,'checks':checks,'integration_keys':keys}
REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
print('REPORT', REPORT)
if errors: sys.exit(1)
