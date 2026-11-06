"""Reading packet for `benchmark-design.md` §3 (AGENTS §7.2: the raw answer beside the article for every missed helpful entry), $0. For every
helpful gold matter (core or supporting) missed in at least one draw of an arm: the gold entry (span, meaning, weight, the standard's line), its
article (id, title, the source paragraph holding the span), and per draw whether it was handed over and written, the item's raw answers (the frozen
extraction's answer; the split's A and B answers), the item's checked handover statements, its drops and its written records. A reader puts each
miss down as the architecture's error (not written, dropped by a check, lost after the handover) or the measure's (the matter is there in other
words; the gold entry is not in the source).

    python3 bench_traces.py <out.json> <hits-arm.json> [--test]"""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))
from hivemind import split  # noqa: E402  (the sections each item is read in)
if not Path(split.__file__).resolve().is_relative_to(Path(__file__).resolve().parents[3] / 'src'):
    raise SystemExit(f'refused: hivemind.split would come from another tree ({split.__file__})')

HERE = Path(__file__).resolve().parent
GOLDS = {'dev': '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json',
         'test': '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json'}
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'


def paragraph(text, span):
    position = text.find(span[:60])
    if position < 0:
        return 'NOT FOUND: the gold span is not in the stored source text (read the source in full)'
    start = text.rfind('\n', 0, position) + 1
    end = text.find('\n', position + len(span))
    return text[start:end if end > 0 else len(text)][:1500]


def raw_answers(archive, input_id, text):
    """Every archived extraction-stage answer of the item, in full, with its call id and request hash: the frozen extraction's, the split's A and B
    (each section) and its record preparation (matched by the item's A passages, which its request carries)."""
    out, a_quotes = {}, []
    rows = list(archive.execute('select call_id, purpose, request_sha256, request_json, answer_json from model_calls where purpose in '
                                "('extract', 'split_a', 'split_b', 'split_preparation') order by call_id"))
    for call_id, purpose, sha, request_json, answer_json in rows:
        user = json.loads(request_json)['messages'][-1]['content']
        if purpose != 'split_preparation' and (f'id {input_id},' in user or f'id {input_id};' in user):
            answer = json.loads(answer_json) if answer_json else None
            out.setdefault(purpose, []).append({'call_id': call_id, 'request_sha256': sha, 'answer': answer, 'user': user})
            if purpose == 'split_a' and answer:
                a_quotes += [e['quote'] for q in answer.get('questions', []) for e in q.get('evidence', [])]
    article = '[Article]\n' + text[:split.extraction.MAX_TEXT_CHARS] + '\n\n[Questions]'      # record preparation carries the whole article
    prepared = [(call_id, sha, answer_json) for call_id, purpose, sha, request_json, answer_json in rows
                if purpose == 'split_preparation' and article in json.loads(request_json)['messages'][-1]['content']]
    if len(prepared) == 1:
        call_id, sha, answer_json = prepared[0]
        out['split_preparation'] = [{'call_id': call_id, 'request_sha256': sha, 'answer': json.loads(answer_json) if answer_json else None, 'user': ''}]
    elif len(prepared) > 1:
        out['split_preparation'] = [{'call_id': c, 'request_sha256': s, 'answer': None, 'user': '', 'ambiguous': True} for c, s, _ in prepared]
    unread = [f'{stage}: archived call {c["call_id"]} ' + ('cannot be tied to this article alone' if c.get('ambiguous') else 'has no answer')
              for stage, calls in out.items() for c in calls if c['answer'] is None]
    if not out:
        unread.append('no archived extraction-stage answer for this item')
    elif 'extract' not in out:
        for number, part in enumerate(split.sections(text), 1):
            marker = part[:300]
            for stage in ('split_a', 'split_b'):
                if not any(c['answer'] is not None and marker in c['user'] for c in out.get(stage, [])):
                    unread.append(f'{stage}: no answer for section {number}')
        if a_quotes and not [c for c in out.get('split_preparation', []) if c['answer'] is not None]:
            unread.append('split_preparation: A proposed questions but no record-preparation answer was found')
    for calls in out.values():
        for c in calls:
            c.pop('user', None)
    if unread:
        out['UNREAD'] = unread
    return out


def main():
    out_path, hits_path, *flags = sys.argv[1:]
    test = '--test' in flags
    hits = json.load(open(hits_path))
    gold = {a['input_id']: a for a in json.load(open(GOLDS['test' if test else 'dev']))['articles']}
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    packet = []
    for key, by_draw in hits['matters'].items():
        if all(state['written'] for state in by_draw.values()):
            continue
        input_id, index = key.rsplit('#', 1)
        article, entry = gold[input_id], gold[input_id]['items'][int(index)]
        title, text = items.execute('select title, text from items where input_id=?', (input_id,)).fetchone()
        draws = {}
        for draw, run in zip(sorted(by_draw), hits['runs']):
            state = by_draw[draw]
            record = {'handed_over': state['handed_over'], 'written': state['written']}
            if test:
                handover = json.load(open(Path(run) / 'handovers.json')).get(input_id, {})
                record.update(handover=handover)
            else:
                views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
                row = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (input_id,)).fetchone()
                handover = json.loads(row[0]) if row else {}
                views.row_factory = sqlite3.Row
                written = [dict(r) for r in views.execute('select e.*, (select group_concat(view_id) from evidence_links l where l.evidence_id=e.evidence_id) as links '
                                                         'from evidence e join evidence_sources s using(evidence_id) where s.input_id=?', (input_id,))]
                views.row_factory = None
                record.update(handover=handover or 'NOT FOUND: no stored handover for this item', written_records=written)
            archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
            record['raw'] = raw_answers(archive, input_id, text)
            if not test:
                record['steps'] = [list(r) for r in views.execute('select step, result, reason from processing_steps where input_id=? order by id', (input_id,))]
            draws[draw] = record
        packet.append({'matter': key, 'weight': entry['weight'], 'standard_line': entry.get('rule') or entry.get('row'), 'span': entry['span'],
                       'meaning': entry.get('meaning'), 'article': {'id': input_id, 'title': title, 'day': article['publication_day'],
                                                                     'source_paragraph': paragraph(text, entry['span'])},
                       'missed_in': sum(1 for s in by_draw.values() if not s['written']), 'draws': draws})
    packet.sort(key=lambda m: (-m['missed_in'], m['matter']))
    json.dump(packet, open(out_path, 'w'), ensure_ascii=False, indent=1)
    print(f'{len(packet)} helpful matters missed in at least one draw; {sum(1 for m in packet if m["missed_in"] >= 2)} in two or more')


if __name__ == '__main__':
    main()
