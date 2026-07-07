#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, yaml
from pathlib import Path
HOME=Path('/home/galyarder/.hermes')
PROFILES={'default':HOME, 'galyarder':HOME/'profiles/galyarder', 'honcho-sandbox':HOME/'profiles/honcho-sandbox'}

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    return {'cmd':cmd,'exit_code':p.returncode,'stdout':p.stdout[-3000:],'stderr':p.stderr[-1000:]}

def main():
    report={'profiles':{},'checks':{}}
    for name,root in PROFILES.items():
        cfgp=root/'config.yaml'
        cfg=yaml.safe_load(cfgp.read_text()) if cfgp.exists() else {}
        report['profiles'][name]={
            'root':str(root),'exists':root.exists(),
            'distribution_yaml':(root/'distribution.yaml').exists(),
            'mcp_json':(root/'mcp.json').exists(),
            'git_repo':(root/'.git').exists(),
            'memory_provider':(cfg.get('memory') or {}).get('provider'),
            'discord_toolsets':(cfg.get('platform_toolsets') or {}).get('discord'),
            'discord_prompts':len((cfg.get('discord') or {}).get('channel_prompts') or {}),
            'hooks_auto_accept':cfg.get('hooks_auto_accept'),
        }
    report['checks']['profile_list']=run(['hermes','profile','list'])
    report['checks']['mcp_default']=run(['hermes','mcp','list'])
    report['checks']['mcp_galyarder']=run(['hermes','--profile','galyarder','mcp','list'])
    out=HOME/'reports/agent-os/profile-audit-latest.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print('REPORT', out)
if __name__=='__main__': main()
