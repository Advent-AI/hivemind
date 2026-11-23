"""The six-call test: the outcome by the rule written before the send (EFFECT-TEST-DESIGN.md version 2). It joins the two blind readers'
rankings to the key and prints, for every answer, its condition, its answer, whether it cites the added statement and how it marks
it, and each reader's rank and `uses_precedent`; then the outcome: moved, confidence fell (a complete separation in both readers'
rankings with the precedent used), or inconclusive. It judges nothing itself.

  python3 tally_effect.py <output folder of the sends> <key file outside the repository> <added statement id>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"judgement"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def main():
    output, key_path, added = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    key = json.loads(key_path.read_text())
    answers = {f"{r['condition']}-{r['send']}": r for r in json.loads((output / 'answers.json').read_text())}
    readers = {family: {row['judgement']: row for row in objects(HERE / f'{family}-stance.jsonl')} for family in ('codex', 'claude')}
    for family, rows in readers.items():
        missing = [label for label in key if label not in rows]
        if missing:
            raise SystemExit(f'{family} did not rank {missing}: refused')
    valid = {name: r for name, r in answers.items() if r['valid']}
    print('EVERY ANSWER')
    for label, name in sorted(key.items(), key=lambda kv: kv[1]):
        answer = answers[name]['answer']
        push = {p['evidence_id']: p['push'] for p in answer.get('pushes') or []}
        print(f"  {name} ({label}): answer {answer['rung']}; cites {added}: {added in answer['cites']}; marks {added}: {push.get(added)}; "
              + '; '.join(f"{family} rank {readers[family][label]['rank']}, uses precedent {readers[family][label]['uses_precedent']}" for family in readers))
        for family in readers:
            print(f"      {family}: {readers[family][label].get('words')}")
    control = [name for name in valid if name.startswith('control')]
    treated = [name for name in valid if name.startswith('with_fact')]
    label_of = {name: label for label, name in key.items()}
    not_one = lambda names: sum(1 for name in names if valid[name]['answer']['rung'] != 1)
    if len(control) < 3 or len(treated) < 3:
        outcome = f'inconclusive: fewer than three valid answers in a condition (control {len(control)}, with the fact {len(treated)})'
    elif not_one(treated) >= 2 and (len(control) - not_one(control)) >= 2:
        outcome = 'the answer moved'
    else:
        separated, used = {}, {}
        for family, rows in readers.items():
            separated[family] = min(rows[label_of[name]]['rank'] for name in treated) > max(rows[label_of[name]]['rank'] for name in control)
            used[family] = sum(1 for name in treated if str(rows[label_of[name]]['uses_precedent']).lower().startswith('yes'))
        print(f"\ncomplete separation (every answer with the fact ranked less firm than every control): {separated}; answers with the fact using the precedent: {used}")
        outcome = 'confidence in "yes" fell' if all(separated.values()) and all(count >= 2 for count in used.values()) else 'inconclusive'
    print(f'\nOUTCOME by the rule written before the send: {outcome}')
    print('answers: control', [valid[name]['answer']['rung'] for name in sorted(control)], '| with the fact', [valid[name]['answer']['rung'] for name in sorted(treated)])


if __name__ == '__main__':
    main()
