"""Write the post-run reader packet for the acceptance set's Step 1 run (no model calls).

The packet lists, per article in manifest order:
- the source (title, publisher, date, text);
- the frozen settled matters;
- the theses open before the article;
- every kept item the run wrote, with its summary, passages, party, date, tier, figures and links (each with its thesis question);
- the theses the article opened, with the opening reason, the settling material, the period and the stated separate bet.

A failed article is listed with its failure and no items. The packet carries no configuration label.

Usage: build_acceptance_judging.py <manifest.json> <settled.json> <trace.sqlite> <packet.json>"""
import json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
import runner  # noqa: E402


def main():
    manifest, settled = json.loads(Path(sys.argv[1]).read_text()), json.loads(Path(sys.argv[2]).read_text())
    conn = sqlite3.connect(f'file:{sys.argv[3]}?mode=ro', uri=True)
    rows = {row[0]: row[1:] for row in conn.execute('select input_id, status, error, result, before_state, after_state from trace')}
    items = {item['input_id']: item for item in runner.selected_items(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite', manifest)}
    questions = {}
    packet = []
    for number, input_id in enumerate(manifest['item_ids'], 1):
        item = items[input_id]
        entry = {'article': number, 'id': input_id, 'title': item['title'], 'publisher': item['publisher'],
                 'publication_date': item['publication_day'], 'text': item['text'],
                 'settled_matters': settled['matters'].get(input_id, [])}
        status, error, result, before, after = rows.get(input_id, ('not run', None, None, '[]', '[]'))
        before_theses, after_theses = json.loads(before or '[]'), json.loads(after or '[]')
        questions.update({t['id']: t['description'] for t in before_theses + after_theses})
        entry['open_theses_before'] = [{'id': t['id'], 'question': t['description']} for t in before_theses]
        if status != 'complete':
            entry.update(status=status, failure=error, kept_items=[], opened_theses=[])
            packet.append(entry)
            continue
        answer = json.loads(result)
        local = answer.get('new_thesis_ids', {})
        entry['kept_items'] = [{
            'item': f"{number}:{ev['local_id']}", 'summary': ev['summary'], 'passages': ev['source_passages'],
            'original_party': ev['original_party'], 'reporting_speaker': ev['reporting_speaker'],
            'statement_date': ev['statement_date'], 'tier': ev['tier'], 'figures': ev.get('figures') or [],
            'links': [{'thesis': local.get(l['target_id'], l['target_id']),
                       'question': questions.get(local.get(l['target_id'], l['target_id']), '(not opened)'),
                       'relevance': l['relevance']} for l in ev['links']]} for ev in answer['evidence']]
        entry['opened_theses'] = [{
            'thesis': local[t['local_id']], 'question': t['description'], 'outcome': t['outcome'], 'period': t['period'],
            'opens_as': t.get('opens_as'), 'settled_by': t.get('settled_by'), 'closest_open_thesis': t.get('closest_open_thesis'),
            'why_a_separate_bet': t.get('why_a_separate_bet')} for t in answer['new_theses'] if t['local_id'] in local]
        packet.append(entry)
    Path(sys.argv[4]).write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    print(f"{len(packet)} articles; {sum(e.get('status') not in (None, 'complete') for e in packet)} not complete; "
          f"{sum(len(e['kept_items']) for e in packet)} kept items; {sum(len(e['opened_theses']) for e in packet)} opened theses; "
          f"{sum(len(e['settled_matters']) for e in packet)} settled matters")


if __name__ == '__main__':
    main()
