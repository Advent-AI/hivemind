"""The blind reading of the six contested answers and two controls, joined to the key ($0). It judges nothing.

  python3 tally_trace.py <key folder>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def rows_of(path):
    if not path.exists():
        return {}
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), {}, 0
    while True:
        start = text.find('{"question"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out[row['question']] = row
        except json.JSONDecodeError:
            position = start + 1


def main(keys):
    key = json.loads((Path(keys) / 'key-trace.json').read_text())
    rows = {f: {q: r for n in (1, 2) for q, r in rows_of(HERE / f'{f}-trace-{n}.jsonl').items()} for f in FAMILIES}
    for f in FAMILIES:
        print(f'{f}: {len(rows[f])} of {len(key)} questions')
    for question, source in sorted(key.items(), key=lambda kv: int(kv[0][1:])):
        print(f'\n{question} = {source}')
        for f in FAMILIES:
            r = rows[f].get(question)
            if not r:
                print(f'   {f}: no answer')
                continue
            named = ', '.join(f"{c['ref']}:{c['effect']}" for c in r.get('candidates', []))
            print(f"   {f}: follows {r.get('follows')} | form {r.get('form')} | insufficient {r.get('insufficient')} | together {r.get('together')} "
                  f"| causes {r.get('causes')} | named [{named}]")
            print(f"      why: {r.get('why')}")
            for c in r.get('candidates', []):
                print(f"      {c['ref']} {c['effect']}: {c.get('why')}")


if __name__ == '__main__':
    main(sys.argv[1])
