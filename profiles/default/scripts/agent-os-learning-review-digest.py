#!/usr/bin/env python3
"""Human-review digest for Agent OS learning queue.

Queue-only by design: this script never writes memory or skills. It reports
pending candidates so Galih/Keiya/Galyarder can explicitly promote or reject.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HOME = Path('/home/galyarder/.hermes')
QUEUE = HOME / 'learning-review' / 'queue.jsonl'
REPORT_DIR = HOME / 'reports' / 'agent-os'
REPORT_DIR.mkdir(parents=True, exist_ok=True)

items = []
if QUEUE.exists():
    for line in QUEUE.read_text(encoding='utf-8', errors='replace').splitlines():
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            continue
pending = [x for x in items if x.get('status', 'pending') == 'pending']
by_profile = Counter(x.get('profile') or 'unknown' for x in pending)
by_source = Counter(x.get('source') or 'unknown' for x in pending)
latest = pending[-10:]
report = {
    'ts': datetime.now(timezone.utc).isoformat(),
    'queue': str(QUEUE),
    'total_items': len(items),
    'pending_count': len(pending),
    'pending_by_profile': dict(by_profile),
    'pending_by_source': dict(by_source),
    'latest_pending': latest,
    'safety': 'queue-only; no automatic memory/skill promotion',
}
out = REPORT_DIR / ('learning-review-digest-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.json')
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

if not pending:
    # Silent when no review is needed; cron no-agent will not spam.
    raise SystemExit(0)

print(f"LEARNING_REVIEW_PENDING {len(pending)} candidates")
print(f"report={out}")
for profile, count in sorted(by_profile.items()):
    print(f"profile {profile}: {count}")
print('latest:')
for item in latest[-5:]:
    text = (item.get('text') or '').replace('\n', ' ')
    if len(text) > 140:
        text = text[:137] + '...'
    print(f"- {item.get('id')} [{item.get('profile')}] {item.get('source')}: {text}")
