#!/usr/bin/env python3
from __future__ import annotations
import json, yaml, sys
from pathlib import Path
HOME=Path('/home/galyarder/.hermes')
errors=[]
for label,p in [('default',HOME/'config.yaml'),('galyarder',HOME/'profiles/galyarder/config.yaml')]:
    cfg=yaml.safe_load(p.read_text()) or {}
    stt=cfg.get('stt') or {}
    provider=stt.get('provider')
    print(label, 'stt.provider=', provider, 'enabled=', stt.get('enabled'))
    if label=='default' and provider!='groq': errors.append('default stt not groq')
    if label=='galyarder' and provider!='groq': errors.append('galyarder stt not groq')
if errors:
    print('SUMMARY: FAIL', errors); sys.exit(1)
print('SUMMARY: PASS')
