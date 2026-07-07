#!/usr/bin/env python3
"""Static Discord relay regression smoke.
Live bot-to-bot smoke is performed from chat when needed; this script verifies local routing prerequisites.
"""
from __future__ import annotations
import json, yaml, sys
from pathlib import Path
HOME=Path('/home/galyarder/.hermes')
errors=[]

def fail(x): errors.append(x); print('FAIL', x)
def ok(x): print('PASS', x)
for label,cfgp in [('default',HOME/'config.yaml'),('galyarder',HOME/'profiles/galyarder/config.yaml')]:
    cfg=yaml.safe_load(cfgp.read_text()) or {}
    disc=cfg.get('discord') or {}
    if disc.get('require_mention') is True: ok(f'{label} require_mention')
    else: fail(f'{label} require_mention not true')
    if disc.get('thread_require_mention') is True: ok(f'{label} thread_require_mention')
    else: fail(f'{label} thread_require_mention not true')
    prompts=disc.get('channel_prompts') or {}
    if len(prompts) >= 5: ok(f'{label} channel_prompts {len(prompts)}')
    else: fail(f'{label} channel_prompts too few')
    tools=(cfg.get('platform_toolsets') or {}).get('discord') or []
    if 'discord' in tools: ok(f'{label} native discord toolset')
    else: fail(f'{label} missing discord toolset')
    if 'discord_admin' not in tools: ok(f'{label} discord_admin disabled')
    else: fail(f'{label} discord_admin enabled')
skill=HOME/'skills/autonomous-ai-agents/discord/SKILL.md'
text=skill.read_text().lower()
for phrase in ['raw mention','split','mentions']:
    if phrase in text: ok(f'relay skill phrase {phrase}')
    else: fail(f'missing relay phrase {phrase}')
if ('ping-pong' in text) or ('ping pong' in text):
    ok('relay skill anti ping-pong language')
else:
    fail('missing relay anti ping-pong language')
if errors:
    print('SUMMARY: FAIL'); sys.exit(1)
print('SUMMARY: PASS')
