#!/usr/bin/env python3
"""
Clean repeated/rolling cue lines and inline time tags from WebVTT auto-captions.

Usage:
    python3 vtt_to_clean_transcript.py <vtt_path> [--text-only]
"""

import argparse
import html
import re
import sys
from pathlib import Path


def clean_vtt(vtt_text: str) -> list[tuple[str, str]]:
    blocks = re.split(r'\n\s*\n', vtt_text)
    entries = []
    seen = set()
    for block in blocks:
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            if '-->' in line:
                start = line.split('-->')[0].strip()
                # Extract HH:MM:SS format
                start_match = re.match(r'(\d{2}:\d{2}:\d{2})', start)
                time_label = start_match.group(1) if start_match else start
                
                raw = ' '.join(lines[i+1:])
                # Clean inline time tags like <00:00:01.000><c>
                raw = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>', ' ', raw)
                raw = re.sub(r'</c>|<[^>]+>', ' ', raw)
                raw = re.sub(r'\s+', ' ', html.unescape(raw)).strip()
                
                # Check for duplicates or empty
                if raw and raw not in seen:
                    entries.append((time_label, raw))
                    seen.add(raw)
                break
    return entries


def main():
    parser = argparse.ArgumentParser(description="Convert WebVTT auto-captions to clean text.")
    parser.add_argument("vtt_path", help="Path to input WebVTT file")
    parser.add_argument("--text-only", action="store_true", help="Output raw text only without timestamps")
    args = parser.parse_args()

    vtt_path = Path(args.vtt_path)
    if not vtt_path.exists():
        print(f"Error: file not found: {vtt_path}", file=sys.stderr)
        sys.exit(1)

    vtt_text = vtt_path.read_text(encoding='utf-8', errors='replace')
    entries = clean_vtt(vtt_text)

    if args.text_only:
        print(" ".join(raw for _, raw in entries))
    else:
        for time_label, raw in entries:
            print(f"[{time_label}] {raw}")


if __name__ == "__main__":
    main()
