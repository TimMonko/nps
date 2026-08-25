"""Regenerate progressive "as-of" states of the compiled WG meeting notes.

The plugin sustainability WG notes are kept as a single growing file
(``Community Meeting Notes/2026-08-25_WG_Notes.md``). The rebuilt git history
records one commit per meeting, and each such commit must contain the notes
from the first meeting through that date. This script rewrites the notes file
to that exact "as-of" state.

The file is stored newest-meeting-first (matching how the notes were kept), so
an "as-of" state keeps the blocks whose meeting date is on or before the
requested date, preserving file order.

Usage::

    python scripts/build_wg_notes_prefix.py --list
    python scripts/build_wg_notes_prefix.py --as-of 2025-12-04
    python scripts/build_wg_notes_prefix.py --as-of 2025-12-04 --target notes.md

``--as-of`` with no ``--target`` overwrites the canonical notes file in place.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES = REPO_ROOT / "Community Meeting Notes" / "2026-08-25_WG_Notes.md"

_DATE_RE = re.compile(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})")


def _date_of(header: str) -> date | None:
    m = _DATE_RE.search(header)
    if not m:
        return None
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def parse(text: str) -> tuple[str, list[tuple[date, str]]]:
    """Return (title, blocks) where blocks are (meeting_date, section_text)."""
    lines = text.splitlines(keepends=True)
    first_hdr = next(i for i, l in enumerate(lines) if l.startswith("## "))
    title = "".join(lines[:first_hdr])
    blocks: list[tuple[date, str]] = []
    cur: list[str] = []
    cur_date: date | None = None
    for line in lines[first_hdr:]:
        if line.startswith("## "):
            if cur:
                blocks.append((cur_date, "".join(cur)))
            cur_date = _date_of(line)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        blocks.append((cur_date, "".join(cur)))
    return title, [(d, b) for d, b in blocks if d is not None]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true",
                    help="Print the ordered meeting dates (oldest first).")
    ap.add_argument("--as-of", type=str, default=None,
                    help="Write the notes as of this meeting date (YYYY-MM-DD).")
    ap.add_argument("--target", type=Path, default=None,
                    help="Output path (default: overwrite the canonical notes file).")
    args = ap.parse_args()

    text = NOTES.read_text(encoding="utf-8")
    title, blocks = parse(text)

    if args.list:
        for d, _ in sorted(blocks, key=lambda x: x[0]):
            print(d.isoformat())
        return 0

    if args.as_of:
        d = date.fromisoformat(args.as_of)
        kept = [b for b in blocks if b[0] <= d]
        if not kept:
            raise SystemExit(f"no meetings on or before {args.as_of}")
        out = title + "".join(b for _, b in kept)
        target = args.target or NOTES
        target.write_text(out, encoding="utf-8")
        n = len(kept)
        print(f"  Wrote {target} with {n} meeting(s) through {args.as_of}")
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
