"""Structure layer of the standard's ruler (standard.md §11), by code, over haiku-week/sifted.json and the frozen references.

For every draw (luna-1..3, haiku-1..3) and article: each raw evidence record is matched to a reference item when its normalised
quote contains the item's span or one of its also-spans, or (quote of 30+ characters) is contained in one. A matched item is
'kept' when a record that passed the production sift matches it, 'refused' when only a record the sift refused matches it,
'omitted' otherwise. Records matching nothing are 'unmatched' (read by hand: junk, a reference miss, or another cut of an item).
Nothing here judges meaning; reading.md is written for the hand read, and meaning labels go to labels.json.
"""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = HERE / 'haiku-week'
DRAWS = ['luna-1', 'luna-2', 'luna-3', 'haiku-1', 'haiku-2', 'haiku-3']
VERSION = sys.argv[1] if len(sys.argv) > 1 else ''   # 'v2': reference v2 (reference-v2-changes.json); outputs carry the suffix
SUFFIX = f'-{VERSION}' if VERSION else ''


def frozen(name):
    expected = dict(line.split()[::-1] for line in (HERE / f'reference{SUFFIX}.sha256').read_text().splitlines())
    data = (HERE / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected[name], f'{name} changed after the freeze'
    return json.loads(data)


def spans(item):
    return [extraction.normalise(s) for s in [item['span']] + list(item.get('also', []))]


def matches(quote, item):
    q = extraction.normalise(quote)
    return any(s in q or (len(q) >= 30 and q in s) for s in spans(item))


def main():
    sifted = json.loads((RUN / 'sifted.json').read_text())
    refs = {}
    for name, label in ((f'reference-week{SUFFIX}.json', 'week'), (f'reference-holdout{SUFFIX}.json', 'holdout')):
        for art in frozen(name)['articles']:
            refs[art['input_id']] = dict(art, set=label)
    per_item = {}            # (input_id, item id) -> {draw: [records]}
    unmatched = collections.defaultdict(dict)   # input_id -> draw -> [records]
    candidates = collections.defaultdict(dict)
    status = collections.defaultdict(dict)
    totals = {d: collections.Counter() for d in DRAWS}
    for draw in DRAWS:
        for input_id, art in refs.items():
            record = sifted.get(draw, {}).get(input_id)
            t = totals[draw]
            if record is None or record['sift'] is None:
                status[input_id][draw] = 'no answer' if record is None else (record['error'] or ('schema' if record['schema_errors'] else 'incomplete'))
                t['answers_failed'] += 1
                answer_evidence, kept_ids, cands = [], set(), []
            else:
                status[input_id][draw] = 'ok'
                answer_evidence = (record['answer'] or {}).get('evidence', [])
                kept_ids = {e['id'] for e in record['sift']['evidence']}
                cands = record['sift']['candidates']
            t['answers'] += 1
            t['records_written'] += len(answer_evidence)
            t['records_kept'] += len(kept_ids)
            candidates[input_id][draw] = [{k: c.get(k) for k in ('id', 'opens_as', 'object', 'measure', 'scope', 'question', 'due_day', 'year', 'settled_by')} for c in cands]
            items = art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]
            used = set()
            for item in items:
                hits = [e for e in answer_evidence if matches(e['quote'], item)]
                used.update(e['id'] for e in hits)
                kept = [e for e in hits if e['id'] in kept_ids]
                state = 'kept' if kept else ('refused' if hits else 'omitted')
                per_item.setdefault((input_id, item['id']), {})[draw] = {
                    'state': state, 'records': [{k: e.get(k) for k in ('id', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time')} for e in (kept or hits)]}
                t[f"{art['set']}:{item['weight']}:{state}"] += 1
            rest = [e for e in answer_evidence if e['id'] not in used]
            unmatched[input_id][draw] = [{k: e.get(k) for k in ('id', 'quote', 'one_line', 'speaker', 'tier')} | {'kept': e['id'] in kept_ids} for e in rest]
            t[f"{art['set']}:unmatched_kept"] += sum(1 for e in rest if e['id'] in kept_ids)
    out = {'per_item': {f'{k[0]}|{k[1]}': v for k, v in per_item.items()}, 'unmatched': unmatched, 'candidates': candidates,
           'status': status, 'totals': {d: dict(c) for d, c in totals.items()}}
    (HERE / f'structure{SUFFIX}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    write_reading(refs, per_item, unmatched, candidates, status)
    keys = sorted({k for c in totals.values() for k in c})
    print('key'.ljust(34), ' '.join(d.rjust(8) for d in DRAWS))
    for k in keys:
        print(k.ljust(34), ' '.join(str(totals[d].get(k, 0)).rjust(8) for d in DRAWS))


def write_reading(refs, per_item, unmatched, candidates, status):
    for label in ('week', 'holdout'):
        lines = [f'# Reading sheet ({label}): every reference item with each draw\'s record, then the unmatched records and candidates', '']
        for input_id, art in refs.items():
            if art['set'] != label:
                continue
            lines.append(f"## {input_id}" + (f" · call {art['call_id']}" if 'call_id' in art else ''))
            bad = {d: s for d, s in status[input_id].items() if s != 'ok'}
            if bad:
                lines.append(f'- answer status: {bad}')
            for item in art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]:
                lines.append(f"### {item['id']} [{item['weight']}] {item['note'][:160]}")
                for d in DRAWS:
                    cell = per_item[(input_id, item['id'])][d]
                    if cell['state'] == 'omitted':
                        lines.append(f'- {d}: —')
                    else:
                        lines.append(f"- {d}: {cell['state']} " + ' ‖ '.join(
                            f"{r['id']} | {r['tier']} | who={r['original_who']} | day={r['original_day']} | {r['one_line']}" for r in cell['records']))
            for d in DRAWS:
                rest = unmatched[input_id][d]
                if rest:
                    lines.append(f'- {d} unmatched ({len(rest)}): ' + ' ‖ '.join(f"{e['id']}{'' if e['kept'] else ' [refused]'}: {e['one_line']}" for e in rest))
            for d in DRAWS:
                cs = candidates[input_id][d]
                if cs:
                    lines.append(f'- {d} candidates: ' + ' ‖ '.join(f"{c['opens_as']}/{c['measure']}: {c['question']} (due {c['due_day']})" for c in cs))
            for m in art.get('must_propose', []):
                lines.append(f"- REF must propose: {m['gist']}")
            lines.append('')
        (HERE / f'reading-{label}{SUFFIX}.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
