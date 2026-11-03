#!/usr/bin/env python3
"""Is the NVDA stream of an items database clean and complete for a window? Prints a Markdown summary: items the pipeline
would read (feed = 1, object NVDA) per day with empty days named, per channel and month, text length quartiles, duplicate
texts, a publication day more than one day from the source's own timestamp, non-English rows, rows outside the window.

  python3 docs/research/2026-10-27-nvda-3m/check_corpus.py --db /abs/items.sqlite --from 2026-07-01 --until 2026-10-27
"""
import argparse
import collections
import datetime
import email.utils
import json
import sqlite3


def day_of(published_at):
    if not published_at:
        return None
    try:
        return datetime.datetime.fromisoformat(published_at.replace('Z', '+00:00')).date().isoformat()
    except ValueError:
        try:
            return email.utils.parsedate_to_datetime(published_at).date().isoformat()
        except (TypeError, ValueError):
            return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', required=True); ap.add_argument('--from', dest='from_day', required=True); ap.add_argument('--until', required=True)
    a = ap.parse_args()
    conn = sqlite3.connect(f'file:{a.db}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute("select input_id, channel, publication_day, published_at, language, text_chars, content_sha256, feed, copy_of, coverage, title from items where object_identifiers like '%\"NVDA\"%'")]
    in_window = [r for r in rows if r['feed'] == 1 and a.from_day <= r['publication_day'] <= a.until]
    fed = [r for r in in_window if not r['copy_of']]                      # a copy is routed as merged, never extracted (dispatch.py)
    per_day = collections.Counter(r['publication_day'] for r in fed)
    day = datetime.date.fromisoformat(a.from_day); last = datetime.date.fromisoformat(a.until); empty = []
    while day <= last:
        if per_day[day.isoformat()] == 0:
            empty.append(day.isoformat())
        day += datetime.timedelta(days=1)
    by_ch = collections.Counter((r['channel'], r['publication_day'][:7]) for r in fed)
    lengths = sorted(r['text_chars'] or 0 for r in fed)
    q = lambda p: lengths[int(p * (len(lengths) - 1))] if lengths else 0
    dup = collections.Counter(r['content_sha256'] for r in fed)
    dups = sum(n - 1 for n in dup.values() if n > 1)
    drift = [r for r in fed if day_of(r['published_at']) and abs((datetime.date.fromisoformat(r['publication_day']) - datetime.date.fromisoformat(day_of(r['published_at']))).days) > 1]
    non_en = [r for r in fed if (r['language'] or 'en') != 'en']
    outside = [r for r in rows if r['feed'] == 1 and not (a.from_day <= r['publication_day'] <= a.until)]
    print(f'# NVDA stream check: {a.db}\n\nwindow {a.from_day}..{a.until}: NVDA rows {len(rows)}, fed in window {len(fed)}, copies among NVDA rows {sum(1 for r in rows if r["copy_of"])}\n')
    print('| month | ' + ' | '.join(sorted({c for c, _ in by_ch})) + ' | total |\n|---|' + '---|' * (len({c for c, _ in by_ch}) + 1))
    chans = sorted({c for c, _ in by_ch})
    for m in sorted({m for _, m in by_ch}):
        print(f'| {m} | ' + ' | '.join(str(by_ch[(c, m)]) for c in chans) + f' | {sum(by_ch[(c, m)] for c in chans)} |')
    print(f'\n- days with no fed NVDA item: {len(empty)} ' + (f'({", ".join(empty[:30])}{"…" if len(empty) > 30 else ""})' if empty else ''))
    print(f'- items per day: min {min(per_day.values()) if per_day else 0}, median {sorted(per_day.values())[len(per_day)//2] if per_day else 0}, max {max(per_day.values()) if per_day else 0}')
    print(f'- text chars: p10 {q(0.1):,}, median {q(0.5):,}, p90 {q(0.9):,}, max {q(1.0):,}; under 500 chars: {sum(1 for n in lengths if n < 500)}')
    print(f'- duplicate texts among fed rows (same sha256, copies excluded): {dups}; copies in the window routed as merged: {len(in_window) - len(fed)}')
    print(f'- publication day more than one day from the source timestamp: {len(drift)}' + (f' e.g. {drift[0]["input_id"]} {drift[0]["publication_day"]} vs {drift[0]["published_at"]}' if drift else ''))
    print(f'- non-English fed rows: {len(non_en)}')
    print(f'- fed NVDA rows outside the window: {len(outside)} (bootstrap material; the replay reads only the window)')


if __name__ == '__main__':
    main()
