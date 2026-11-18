"""The loss trace's "extracted" reading (census design point 7; D454): for every lost graded answer (outcome iii or vi) of the full run, each
of reader B's decisive items, beside every evidence item the run kept from that item's own article. A reader marks which kept item states
the decisive item's fact, or none. One packet a draw, under the matching's neutral run names; the key back to the draws is the matching key.
Items shared by two lost questions of one draw are read once. Checks ($0): every (draw, decisive item) of a lost question appears exactly
once; a decisive item whose article the run never processed is listed with no candidates and said so.

  python3 build_trace_packets.py
"""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
E = HERE.parent
DATA = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
GRADED = ['q04', 'q05', 'q08', 'q09', 'q13', 'q18', 'q23']
TRACES = {'c1': DATA / 'c1/step1/trace.sqlite', 'c2': DATA / 'c2/step1-redo/trace.sqlite', 'c3': DATA / 'c3/step1/trace.sqlite'}


def lost(outcomes, mapping):
    """{draw: [questions lost at opening: not opened (iii) or opened, not eligible (vi)]}."""
    unresolved = mapping['unresolved (the third readers split)']
    out = {}
    for draw in ('c1', 'c2', 'c3', 'p1', 'p2', 'p3'):
        rows = outcomes.get(draw, {})
        out[draw] = [q for q in GRADED
                     if (q in rows and rows[q][1].startswith('opened, not eligible'))
                     or (q not in rows and q not in unresolved.get(draw, {}).values())]
    return out


def kept_clean(draw):
    conn = sqlite3.connect(f'file:{TRACES[draw]}?mode=ro', uri=True)
    kept = {}
    for input_id, result in conn.execute("select input_id, result from trace where status='complete'"):
        answer = json.loads(result)
        kept[input_id] = [{'ref': f"{input_id}#{e['local_id']}", 'summary': e['summary'], 'passages': e['source_passages']}
                          for e in answer.get('evidence', [])]
    conn.close()
    return kept


def kept_prod(draw):
    """Production's kept evidence by article: every article an evidence item was taken from (`evidence_sources`, repeats included)."""
    conn = sqlite3.connect(f"file:{DATA / draw / 'prod' / 'views.sqlite'}?mode=ro", uri=True)
    kept = {}
    for evidence_id, input_id, one_line, quote in conn.execute(
            'select e.evidence_id, s.input_id, e.one_line, e.quote from evidence e join evidence_sources s on s.evidence_id = e.evidence_id'):
        kept.setdefault(input_id, []).append({'ref': f'{input_id}#{evidence_id}', 'summary': one_line, 'passages': [quote]})
    conn.close()
    return kept


def build():
    outcomes = json.loads((E / 'full-eligibility-answers/census-outcomes.json').read_text())
    mapping = json.loads((E / 'full-matching-answers/mapping-full.json').read_text())
    key = json.loads((DATA / 'matching-key.json').read_text())
    neutral = {entry['draw']: name.split('/')[0] for name, entry in key.items()}
    gold = {e['question_id']: e for e in json.loads((GOLD / 'gold-v1.json').read_text())['entries']}
    items = {i['id']: i for i in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    losses = lost(outcomes, mapping)
    out_folder = E / 'full-trace'
    out_folder.mkdir(exist_ok=False)
    index, total = {}, 0
    for draw, questions in losses.items():
        kept = kept_clean(draw) if draw.startswith('c') else kept_prod(draw)
        wanted = []
        for q in questions:
            for item_id in gold[q].get('decisive_items', []):
                if item_id not in wanted:
                    wanted.append(item_id)
        packet = []
        for number, item_id in enumerate(wanted, 1):
            item = items[item_id]
            packet.append({'point': number, 'decisive_item': {k: item[k] for k in ('day', 'title', 'who', 'passage', 'meaning')},
                           'kept_from_that_article': kept.get(item['input_id'], []),
                           **({} if item['input_id'] in kept else {'note': 'the run kept nothing from this article'})})
            index[f'{neutral[draw]}/{number}'] = {'draw': draw, 'item': item_id, 'questions': [q for q in questions if item_id in gold[q].get('decisive_items', [])]}
        (out_folder / f'trace-packet-{neutral[draw]}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
        total += len(packet)
    expected = sum(len({i for q in qs for i in gold[q].get('decisive_items', [])}) for qs in losses.values())
    if total != expected or len(index) != expected:
        raise SystemExit('check failed: not every (draw, decisive item) of a lost question is a point exactly once')
    (E / 'full-trace-answers').mkdir(exist_ok=True)
    (E / 'full-trace-answers' / 'trace-key.json').write_text(json.dumps(index, indent=1) + '\n')
    print(json.dumps({d: qs for d, qs in losses.items()}))
    print(f'{total} points over {len(losses)} draws; every (draw, decisive item) exactly once')


if __name__ == '__main__':
    build()
