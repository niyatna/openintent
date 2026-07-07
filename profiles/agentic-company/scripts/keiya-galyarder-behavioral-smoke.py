#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, subprocess, sys
from datetime import datetime
from pathlib import Path
import yaml

DEFAULT_HOME=Path('/home/galyarder/.hermes')
GALYARDER_HOME=DEFAULT_HOME/'profiles'/'galyarder'
REPO=DEFAULT_HOME/'hermes-agent'
REPORT=DEFAULT_HOME/'reports'/'agent-os'
REPORT.mkdir(parents=True, exist_ok=True)

def load(path):
    with open(path,'r',encoding='utf-8') as f: return yaml.safe_load(f) or {}
def check(name, ok, detail=''):
    results.append({'name': name, 'ok': bool(ok), 'detail': detail})
results=[]
# Config invariants
kcfg=load(DEFAULT_HOME/'config.yaml'); gcfg=load(GALYARDER_HOME/'config.yaml')
check('default memory provider hindsight', (kcfg.get('memory') or {}).get('provider')=='hindsight')
check('galyarder memory provider hindsight', (gcfg.get('memory') or {}).get('provider')=='hindsight')
check('galyarder discord native toolset enabled', 'discord' in ((gcfg.get('platform_toolsets') or {}).get('discord') or []))
check('galyarder discord_admin intentionally absent', 'discord_admin' not in ((gcfg.get('platform_toolsets') or {}).get('discord') or []))
check('galyarder guard agent-created skills enabled', (gcfg.get('skills') or {}).get('guard_agent_created') is True)
# SOUL / skill text invariants
gsoul=(GALYARDER_HOME/'SOUL.md').read_text(errors='replace')
ksoul=(DEFAULT_HOME/'SOUL.md').read_text(errors='replace')
relay_skill=(DEFAULT_HOME/'skills'/'autonomous-ai-agents'/'hermes-discord-gateway-routing'/'SKILL.md').read_text(errors='replace')
check('Galyarder SOUL mentions raw mention relay', 'raw mention' in gsoul.lower() and 'hermes-discord-gateway-routing' in gsoul)
check('Keiya SOUL has human-first identity', 'Keiya Putri Zeyni' in ksoul and 'human' in ksoul.lower())
check('Discord routing skill warns platform toolsets', 'platform toolsets' in relay_skill.lower())
# Git PR branches preserved locally
for b in ['feat/image-reference-generation','fix/discord-controlled-relay','fix/gateway-transient-timeouts','fix/hindsight-embedded-embeddings-env']:
    p=subprocess.run(['git','show-ref','--verify','--quiet',f'refs/heads/{b}'],cwd=REPO)
    check(f'local branch exists: {b}', p.returncode==0)
out=REPORT/('behavioral-smoke-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.json')
out.write_text(json.dumps({'results':results},indent=2,ensure_ascii=False),encoding='utf-8')
failed=[r for r in results if not r['ok']]
print('Behavioral smoke report:', out)
for r in results:
    print(('PASS' if r['ok'] else 'FAIL'), '-', r['name'], r.get('detail',''))
sys.exit(1 if failed else 0)
