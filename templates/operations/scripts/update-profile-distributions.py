#!/usr/bin/env python3
"""Refresh local profile distribution repos from live profile files.

Copies only curated distribution-owned files. It never copies secrets, memory,
sessions, DBs, logs, caches, or token files.
"""
from __future__ import annotations
import os, shutil, subprocess, sys
from pathlib import Path

import yaml

HOME=Path('/home/galyarder/.hermes')
DIST=HOME/'profile-distributions'
REPOS={
    'keiya': DIST/'keiya-profile',
    'galyarder': DIST/'galyarder-profile',
    'niyatna': DIST/'niyatna-profile',
}
SOURCES={
    'keiya': HOME,
    'galyarder': HOME/'profiles/galyarder',
    'niyatna': HOME/'profiles/niyatna',
}
FILES=['SOUL.md','distribution.yaml','mcp.json','config.yaml']
# Keep this aligned with distribution.yaml distribution_owned. These are profile-layer
# artifacts only; runtime homes, sessions, DBs, logs, caches, and credentials stay out.
DIRS=['hooks','cron','skills','skill-bundles','hindsight']
ROOT_COPY_DIRS=['behavior-tests']
IGNORE_PATTERNS=(
    '__pycache__','*.pyc','.env','.env.*','*.db','*.sqlite','*.log','sessions',
    'memory','cache','logs','state.db','response_store.db','.tick.lock',
    '.hub','audit.log','index-cache','.curator_backups',
    # Skill Hub metadata is local runtime/editor state, not portable profile source.
    '.usage.json','.usage.json.lock','.bundled_manifest',
    # gstack runtime bundles contain binary/shim/cache-like artifacts and are not
    # portable profile-layer source. Keep SKILL.md references, not executable dist trees.
    'gstack-runtime',
)
ROOT_SCRIPTS=[
    'agent-os-quick',
    'profile-audit.py',
    'relay-smoke-test.py',
    'voice-smoke.py',
    'agent-os-behavioral-regression.py',
    'agent-os-access-hardening-audit.py',
    'agent-os-health-audit.py',
    'agent-os-learning-review-queue.py',
    'agent-os-learning-review-digest.py',
    'agent-github.py',
    'keiya-gh',
    'galyarder-gh',
    'honcho-ab-sandbox-eval.py',
    'integration-readiness.py',
    'keiya-galyarder-agent-os-smoke.py',
    'keiya-galyarder-behavioral-smoke.py',
    'update-profile-distributions.py',
]

def copy_file(src:Path,dst:Path):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src,dst)

def copy_dir(src:Path,dst:Path):
    if src.exists():
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(src,dst,ignore=shutil.ignore_patterns(*IGNORE_PATTERNS), symlinks=True)

def write_env_example(source:Path, repo:Path):
    """Render .env.EXAMPLE from distribution.yaml env_requires without secret values."""
    manifest = source/'distribution.yaml'
    out = repo/'.env.EXAMPLE'
    header = [
        '# Environment variables required by this Hermes profile distribution.',
        '# Copy to .env locally and fill values. Do not commit real .env.',
        '',
    ]
    if not manifest.exists():
        out.write_text('\n'.join(header + ['# Fill locally; never commit real .env', '']), encoding='utf-8')
        return
    data = yaml.safe_load(manifest.read_text(encoding='utf-8')) or {}
    lines = header[:]
    for item in data.get('env_requires') or []:
        if not isinstance(item, dict) or not item.get('name'):
            continue
        desc = str(item.get('description') or '').strip()
        if desc:
            for part in desc.splitlines():
                lines.append(f'# {part}')
        lines.append('# required' if item.get('required') else '# optional')
        if 'default' in item:
            lines.append(f"# default: {item.get('default')}")
        lines.append(f"{item['name']}=")
        lines.append('')
    out.write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')

def refresh(name:str):
    repo=REPOS[name]; source=SOURCES[name]
    if not repo.exists():
        raise SystemExit(f'missing repo: {repo}')
    for f in FILES: copy_file(source/f, repo/f)
    for d in DIRS: copy_dir(source/d, repo/d)
    scripts_dir=repo/'scripts'; scripts_dir.mkdir(exist_ok=True)
    for s in ROOT_SCRIPTS: copy_file(HOME/'scripts'/s, scripts_dir/s)
    for d in ROOT_COPY_DIRS: copy_dir(HOME/d, repo/d)
    mem_src=source/'memories'
    if mem_src.exists(): copy_dir(mem_src, repo/'memories')
    # Render env template from manifest without copying real .env values.
    write_env_example(source, repo)
    subprocess.run(['git','add','.'], cwd=repo, check=True)
    diff=subprocess.run(['git','diff','--cached','--quiet'], cwd=repo)
    if diff.returncode==0:
        print(f'{name}: no staged changes')
    else:
        env=os.environ.copy()
        if name == 'keiya':
            author_name = 'Keiya Putri'
            author_email = 'keiyazeyniputri@gmail.com'
        elif name == 'niyatna':
            author_name = 'Niyatna Agent'
            author_email = 'galyarderlabs@gmail.com'
        else:
            author_name = 'Galyarder Labs'
            author_email = 'galyarderlabs@gmail.com'
        env.setdefault('GIT_AUTHOR_NAME', author_name)
        env.setdefault('GIT_AUTHOR_EMAIL', author_email)
        env.setdefault('GIT_COMMITTER_NAME', env['GIT_AUTHOR_NAME'])
        env.setdefault('GIT_COMMITTER_EMAIL', env['GIT_AUTHOR_EMAIL'])
        subprocess.run(['git','commit','-m','chore: refresh profile distribution artifacts'], cwd=repo, env=env, check=True)
        print(f'{name}: committed refresh')

for name in sys.argv[1:] or ['keiya','galyarder','niyatna']:
    refresh(name)
