"""Claude's verdict on every reader flag, read against the article text (2026-10-30, Alex: "那你找到的这些问题验证是真的问题吗？").
Rule for the date and speaker fields, from the request ("for a retelling, the original speaker and statement day"), the
standard (5.4: an unknown day is unknown, never the report day; D203: an ISO day or empty) and the readers of the fields
(judging and matching read original_who and original_day; event_time is stored and read by no step):
  real      the record is wrong on a field a reader uses, or the summary misstates the source;
  real_low  the report day stands for a company announcement or wire report the article covers within days (wrong under 5.4,
            small effect);
  event     only event_time is wrong (read by no step);
  not_real  the reader misread the field (the outlet's own claim dated the report day; a month-only date left empty per D203);
  debatable the standard has no clear row (tier of a company forecasting its own industry, a paraphrase on TV).
Noise: agree or disagree with the reader. Writes adjudication.json and prints the verified counts.

    python3 adjudication.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V = {
 'gnews_085b1e1a1543437edb9756d6': {'e5': {'day_ok': 'event'}, 'e6': {'day_ok': 'event'}, 'e7': {'day_ok': 'not_real'},
     'e8': {'one_line_ok': 'real', 'who_ok': 'real', 'day_ok': 'real'}, 'e10': {'day_ok': 'real'},
     'e11': {'who_ok': 'real', 'day_ok': 'real'}, 'e12': {'who_ok': 'real', 'day_ok': 'real', 'dup': 'real'},
     'e13': {'who_ok': 'real', 'day_ok': 'real'}, 'e14': {'who_ok': 'real', 'day_ok': 'real'},
     'e16': {'who_ok': 'real', 'day_ok': 'real', 'NOISE': 'agree'}, 'e17': {'day_ok': 'debatable'}, 'e18': {'day_ok': 'not_real', 'dup': 'real'}},
 'gnews_1de20d5db04664ca26cc79dc': {**{e: {'NOISE': 'agree'} for e in ('e1', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8')}, 'e9': {'dup': 'debatable'}},
 'gnews_1eeceeb212a2c82c2e75e806': {'e1': {'day_ok': 'real', 'NOISE': 'agree'}, 'e3': {'NOISE': 'agree'}, 'e4': {'NOISE': 'agree'}},
 'gnews_22600bb2364224897320ffba': {'e1': {'who_ok': 'real', 'day_ok': 'real'}, 'e2': {'who_ok': 'real', 'day_ok': 'real'}, 'e3': {'NOISE': 'agree'}},
 'gnews_2957e5c79a365952140c8cce': {'e1': {'one_line_ok': 'real', 'day_ok': 'real_low'}, 'e2': {'day_ok': 'real_low', 'dup': 'real'},
     'e3': {'who_ok': 'real', 'tier_ok': 'real', 'dup': 'real'}, 'e4': {'day_ok': 'not_real'}, 'e6': {'day_ok': 'real', 'tier_ok': 'debatable'}},
 'gnews_4249e0578b11cedf5a71ff08': {'e2': {'NOISE': 'agree'}},
 'gnews_4f3a1d09e90b8fec9c86d2ba': {'e1': {'dup': 'real', 'NOISE': 'agree'}, 'e2': {'NOISE': 'agree'}, 'e3': {'NOISE': 'agree'}},
 'gnews_621e1b678a037049c86a70af': {'e1': {'one_line_ok': 'not_real'}, 'e2': {'day_ok': 'event'}, 'e3': {'one_line_ok': 'real', 'day_ok': 'event', 'NOISE': 'agree'},
     'e5': {'day_ok': 'event', 'tier_ok': 'debatable'}},
 'gnews_a96a4cbf6aae35d01d0d285b': {'e1': {'day_ok': 'debatable', 'NOISE': 'agree'}, 'e2': {'tier_ok': 'debatable', 'NOISE': 'agree'}, 'e3': {'tier_ok': 'debatable', 'NOISE': 'agree'}},
 'gnews_ad47330f25c9d5ff84ced7e2': {'e2': {'dup': 'real'}, 'e3': {'NOISE': 'agree'}, 'e4': {'dup': 'real'}, 'e5': {'NOISE': 'agree'}, 'e6': {'NOISE': 'agree'}, 'e7': {'NOISE': 'agree'}},
 'gnews_bc86d298ecece0269dc9e856': {'e1': {'day_ok': 'event', 'NOISE': 'agree'}, 'e2': {'who_ok': 'real', 'day_ok': 'real'}, 'e3': {'day_ok': 'event', 'NOISE': 'agree'}},
 'gnews_bf158d067256a39f02f7c7ce': {'e2': {'one_line_ok': 'real', 'tier_ok': 'real'}, 'e3': {'one_line_ok': 'real', 'tier_ok': 'real'}},
 'gnews_c2924b0380602940d68de7ff': {'e1': {'one_line_ok': 'real', 'day_ok': 'real_low'}, 'e2': {'day_ok': 'real_low', 'tier_ok': 'real', 'NOISE': 'agree'},
     'e3': {'day_ok': 'real_low'}, 'e4': {'NOISE': 'agree'}, 'e5': {'day_ok': 'real_low', 'dup': 'real'}, 'e6': {'day_ok': 'real_low', 'NOISE': 'agree'},
     'e7': {'day_ok': 'real_low', 'NOISE': 'agree'}},
 'gnews_c3e020d179ab025bf3ba56b0': {'e2': {'one_line_ok': 'real'}, 'e3': {'one_line_ok': 'real'}, 'e4': {'tier_ok': 'debatable'}, 'e5': {'one_line_ok': 'real'},
     'e6': {'one_line_ok': 'real', 'day_ok': 'event'}},
 'gnews_c6445931955f107b551cce85': {'e1': {'day_ok': 'event', 'NOISE': 'agree'}, 'e2': {'dup': 'real', 'NOISE': 'agree'}, 'e3': {'who_ok': 'real', 'day_ok': 'event', 'NOISE': 'agree'},
     'e4': {'who_ok': 'real', 'NOISE': 'agree'}, 'e5': {'NOISE': 'agree'}, 'e6': {'NOISE': 'agree'}, 'e8': {'day_ok': 'not_real', 'NOISE': 'agree'},
     'e9': {'NOISE': 'agree'}, 'e11': {'NOISE': 'agree'}},
 'gnews_d1a7a7f18dce5c8ae5e4d0ae': {'e1': {'tier_ok': 'real'}, 'e2': {'tier_ok': 'real', 'dup': 'debatable'}, 'e3': {'tier_ok': 'real'}},
 'gnews_f0d529209a91c7a237e117f1': {'e1': {'tier_ok': 'real'}},
 'nvblog_geforce-now-thursday-july-2026-games-list': {'e1': {'NOISE': 'agree'}},
 'nvblog_nemotron-langchain-agents-open-stack': {'e1': {'one_line_ok': 'real', 'tier_ok': 'real', 'NOISE': 'agree'}, 'e3': {'NOISE': 'agree'}},
}

rows, missing = [], []
for f in sorted((HERE / 'verdicts').glob('*.json')):
    v = json.loads(f.read_text())
    mine = V.get(f.stem, {})
    for s in v['statements']:
        flags = [k for k in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok') if s.get(k) is False] + (['dup'] if s.get('duplicate_of') else []) + (['NOISE'] if s['worth'] == 'noise' else [])
        for flag in flags:
            verdict = mine.get(s['id'], {}).get(flag)
            if verdict is None:
                missing.append((f.stem, s['id'], flag))
            rows.append({'article': f.stem, 'id': s['id'], 'flag': flag, 'verdict': verdict})
assert not missing, missing
extra = [(a, e, k) for a, ids in V.items() for e, ks in ids.items() for k in ks if not any(r['article'] == a and r['id'] == e and r['flag'] == k for r in rows)]
assert not extra, extra
table = collections.defaultdict(collections.Counter)
for r in rows:
    table[r['flag']][r['verdict']] += 1
records_real = {(r['article'], r['id']) for r in rows if r['flag'] in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok') and r['verdict'] == 'real'}
records_real_or_low = {(r['article'], r['id']) for r in rows if r['flag'] in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok') and r['verdict'] in ('real', 'real_low')}
summary = {'flags read': len(rows), 'by flag': {k: dict(c) for k, c in table.items()},
           'records with a real field error (of 102)': len(records_real), 'records with a real or low field error (of 102)': len(records_real_or_low)}
(HERE / 'adjudication.json').write_text(json.dumps({'summary': summary, 'rows': rows}, ensure_ascii=False, indent=1) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=1))
