"""Verified counts of the blind field read (fields-2026-10-30): Claude's verdict on every reader flag, read against the
article with the version hidden (adjudication_verdicts.json, written letter by letter), then joined to the letter key.
Verdicts, as in quality-2026-10-30/adjudication.py:
  real      a field a reader uses is wrong, or the summary misstates the source;
  real_low  the report day (or a day inferred from "earlier this week") for something the article covers within days, or an
            empty day the article states;
  not_real  the reader misread the article or the standard (a company's or outlet's own statement dated its own day);
  debatable the standard has no clear row (an unattributed market figure, a company estimating a rival, a named outlet's report).

    python3 adjudication.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ('who_ok', 'day_ok', 'tier_ok', 'one_line_ok')


def main():
    verdicts = json.loads((HERE / 'adjudication_verdicts.json').read_text())
    key = json.loads((HERE / 'letter-key-do-not-open.json').read_text())
    c = collections.defaultdict(collections.Counter)
    records = collections.Counter()
    for f in sorted((HERE / 'verdicts').glob('*.json')):
        r = json.loads(f.read_text())
        iid = r['input_id']
        for letter in 'AB':
            version = key[iid][letter]
            for s in r.get(letter) or []:
                records[version] += 1
                mine = verdicts.get(f.stem, {}).get(f'{letter}.{s["id"]}', {})
                real_fields = [k for k in ('who_ok', 'day_ok', 'tier_ok') if mine.get(k) == 'real']
                for k in FIELDS:
                    if s.get(k) is False:
                        c[version][f'{k[:-3]} flagged'] += 1
                        c[version][f'{k[:-3]} {mine[k]}'] += 1
                if real_fields:
                    c[version]['records with a real who/day/tier error'] += 1
                if real_fields or any(mine.get(k) == 'real_low' for k in ('day_ok',)):
                    c[version]['records with a real or low who/day/tier error'] += 1
                if real_fields or mine.get('one_line_ok') == 'real':
                    c[version]['records with any real field or summary error'] += 1
    versions = sorted(c)
    print('measure'.ljust(46) + ''.join(v.rjust(8) for v in versions))
    print('records'.ljust(46) + ''.join(str(records[v]).rjust(8) for v in versions))
    for k in sorted({k for x in c.values() for k in x}):
        print(k.ljust(46) + ''.join(str(c[v][k]).rjust(8) for v in versions))
    (HERE / 'adjudication.json').write_text(json.dumps({'records': dict(records), 'counts': {v: dict(c[v]) for v in versions}}, indent=1) + '\n')


if __name__ == '__main__':
    main()
