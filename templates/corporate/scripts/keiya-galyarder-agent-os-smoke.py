#!/usr/bin/env python3
"""Keiya/Galyarder Agent OS smoke tests.
Checks distribution manifests, MCP manifests, relay discipline assets, YouTube transcript tooling, and Honcho sandbox isolation.
"""
from __future__ import annotations
import json, os, subprocess, sys, yaml
from pathlib import Path
HOME=Path('/home/galyarder/.hermes')
GALY=HOME/'profiles/galyarder'
errors=[]

def ok(msg): print('PASS', msg)
def fail(msg): errors.append(msg); print('FAIL', msg)

def check_file(path):
    if path.exists() and path.stat().st_size>0: ok(str(path)); return True
    fail(f'missing/empty {path}'); return False

for p in [HOME/'distribution.yaml', HOME/'mcp.json', GALY/'distribution.yaml', GALY/'mcp.json']:
    check_file(p)
for p in [HOME/'distribution.yaml', GALY/'distribution.yaml']:
    try:
        data=yaml.safe_load(p.read_text()) or {}
        assert data.get('name')
        assert data.get('version')
        assert 'mcp.json' in (data.get('distribution_owned') or [])
        ok(f'valid distribution {p.name}:{data.get("name")}@{data.get("version")}')
    except Exception as e:
        fail(f'invalid yaml {p}: {e}')
for p in [HOME/'mcp.json', GALY/'mcp.json']:
    try:
        data=json.loads(p.read_text())
        servers=data.get('mcp_servers') or {}
        assert {'context7','notebooklm','paperclip'} <= set(servers)
        ok(f'valid mcp manifest {p}')
    except Exception as e:
        fail(f'invalid mcp json {p}: {e}')
# YouTube discipline assets
for p in [HOME/'skills/media/youtube-content/scripts/fetch_transcript.py', HOME/'skills/media/youtube-content/scripts/vtt_to_clean_transcript.py']:
    check_file(p)
# Relay skill must contain split mention pitfall
relay=HOME/'skills/autonomous-ai-agents/discord/SKILL.md'
if relay.exists() and 'raw mention' in relay.read_text().lower(): ok('discord relay raw mention split discipline documented')
else: fail('discord relay discipline text missing')
# Honcho sandbox isolation
hs=HOME/'profiles/honcho-sandbox/config.yaml'
if hs.exists():
    cfg=yaml.safe_load(hs.read_text()) or {}
    if (cfg.get('memory') or {}).get('provider') == 'honcho': ok('honcho sandbox uses honcho')
    else: fail('honcho sandbox does not use honcho')
for prod in [HOME/'config.yaml', GALY/'config.yaml']:
    cfg=yaml.safe_load(prod.read_text()) or {}
    if (cfg.get('memory') or {}).get('provider') == 'hindsight': ok(f'production memory remains hindsight: {prod}')
    else: fail(f'production memory changed: {prod}')
# review queue tool
check_file(HOME/'scripts/agent-os-learning-review-queue.py')
if errors:
    print('\nSUMMARY: FAIL')
    for e in errors: print('-', e)
    sys.exit(1)
print('\nSUMMARY: PASS')
