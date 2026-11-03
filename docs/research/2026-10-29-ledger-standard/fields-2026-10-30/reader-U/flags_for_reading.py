"""Prints every reader flag with the record, the reader's note and the article passage around the quote, by letter only
(the version stays hidden until every flag has a verdict).

    python3 flags_for_reading.py <first> <last>      # packet index range, sorted by file name
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLAGS = ('who_ok', 'day_ok', 'tier_ok', 'one_line_ok')


def passage(text, quote, width=280):
    head = quote[:60]
    i = text.find(head)
    if i < 0:
        words = re.findall(r'\w+', quote)[:6]
        i = text.find(' '.join(words[:3])) if words else -1
    if i < 0:
        return '(quote start not found)'
    return text[max(0, i - width): i + len(quote) + 120].replace('\n', ' / ')


def main(first, last):
    files = sorted((HERE / 'packets').glob('*.json'))[first:last]
    for f in files:
        p = json.loads(f.read_text())
        v = json.loads((HERE / 'verdicts' / f.name).read_text())
        print(f'\n######## {f.stem} | {p["title"][:90]} | pub {p["publication_day"]} | {p["publisher"]} ({p["publisher_type"]}, {p["category"]})')
        for letter in 'AB':
            recs = {e['id']: e for e in (p['answers'][letter] or [])}
            for s in v.get(letter) or []:
                bad = [k for k in FLAGS if s.get(k) is False]
                if not bad:
                    continue
                e = recs.get(s['id'], {})
                print(f'-- {letter}.{s["id"]} flags={bad} worth={s["worth"]}')
                print(f'   rec: who={e.get("original_who")!r} day={e.get("original_day")!r} tier={e.get("tier")} spk={e.get("speaker")!r}')
                print(f'   one_line: {e.get("one_line")}')
                for k in ('who_note', 'day_note', 'tier_note', 'one_line_problem'):
                    if s.get(k):
                        print(f'   R.{k}: {s[k]}')
                print(f'   TEXT: ...{passage(p["text"], e.get("quote", ""))}...')


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
