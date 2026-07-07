#!/usr/bin/env python3
"""Reviewed promotion queue for Hermes Agent OS learning.

This script is intentionally conservative: it queues candidate learnings for
human review instead of auto-writing native memory or skills.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, sys
from pathlib import Path

HOME = Path(os.environ.get('HERMES_HOME', '/home/galyarder/.hermes')).expanduser()
QUEUE_DIR = HOME / 'learning-review'
QUEUE_FILE = QUEUE_DIR / 'queue.jsonl'
REVIEWED_FILE = QUEUE_DIR / 'reviewed.jsonl'


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def _load_jsonl(path: Path):
    if not path.exists():
        return []
    rows=[]
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try: rows.append(json.loads(line))
        except Exception: pass
    return rows

def _append(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True)+'\n')

def add(args):
    text = args.text.strip()
    if not text:
        raise SystemExit('empty learning text')
    h = hashlib.sha256((args.kind+'\0'+text).encode()).hexdigest()[:16]
    existing = {r.get('id') for r in _load_jsonl(QUEUE_FILE)}
    if h in existing:
        print(f'already queued: {h}')
        return
    item = {
        'id': h,
        'created_at': _now(),
        'status': 'pending',
        'kind': args.kind,
        'source': args.source,
        'profile': args.profile,
        'text': text,
        'suggested_target': args.target,
        'risk': args.risk,
    }
    _append(QUEUE_FILE, item)
    print(f'queued: {h}')

def list_items(args):
    rows=[r for r in _load_jsonl(QUEUE_FILE) if args.all or r.get('status')=='pending']
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if not rows:
        print('no pending learning-review items')
        return
    for r in rows:
        print(f"{r.get('id')} [{r.get('kind')}] {r.get('profile')} → {r.get('suggested_target')} :: {r.get('text')[:180]}")

def mark(args):
    rows=_load_jsonl(QUEUE_FILE)
    found=False
    for r in rows:
        if r.get('id') == args.id:
            r['status']=args.status
            r['reviewed_at']=_now()
            r['review_note']=args.note
            found=True
            _append(REVIEWED_FILE, r)
    if not found:
        raise SystemExit(f'not found: {args.id}')
    # rewrite queue without approved/rejected item unless --keep
    if not args.keep:
        remaining=[r for r in rows if r.get('id') != args.id]
    else:
        remaining=rows
    QUEUE_FILE.write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n' for r in remaining), encoding='utf-8')
    print(f'{args.status}: {args.id}')

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('add')
    a.add_argument('--text', required=True)
    a.add_argument('--kind', default='candidate')
    a.add_argument('--source', default='session')
    a.add_argument('--profile', default=os.environ.get('HERMES_PROFILE','default'))
    a.add_argument('--target', default='memory-or-skill')
    a.add_argument('--risk', default='review-required')
    a.set_defaults(func=add)
    l=sub.add_parser('list')
    l.add_argument('--all', action='store_true')
    l.add_argument('--json', action='store_true')
    l.set_defaults(func=list_items)
    m=sub.add_parser('mark')
    m.add_argument('id')
    m.add_argument('--status', choices=['approved','rejected','deferred'], required=True)
    m.add_argument('--note', default='')
    m.add_argument('--keep', action='store_true')
    m.set_defaults(func=mark)
    args=p.parse_args(); args.func(args)
if __name__=='__main__': main()
