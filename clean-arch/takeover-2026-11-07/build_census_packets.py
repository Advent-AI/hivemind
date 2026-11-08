"""Blind per-article packets: the clean Step 1 answer beside frozen production's answer (draw 1) on the same 49 articles.

Both arms received the same cleaned article text. Each arm's evidence is reduced to {summary, quotes} so field names do not reveal it;
which arm is A or B is drawn per article with a fixed seed and kept in a separate key file the readers never see."""
import json, random, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'poc/data'
PRODUCTION = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark/runs/control-v108-d1/views.sqlite')
OUT = ROOT / 'poc/data/clean-step1-takeover-2026-11-07'

def clean_rows():
    rows = {}
    for folder in ['clean-step1-2026-07-08-09-continuing', 'clean-step1-2026-07-08-09-segment-2']:
        conn = sqlite3.connect(f'file:{RUN / folder / "trace.sqlite"}?mode=ro', uri=True)
        for input_id, request, result in conn.execute("select input_id, request, result from trace where status='complete' order by sequence"):
            payload = json.loads(json.loads(request)['messages'][1]['content'])
            rows[input_id] = (payload['source_item'], json.loads(result))
    return rows

def main():
    ids = json.loads((RUN / 'clean-step1-2026-07-08-09/manifest.json').read_text())['item_ids']
    clean = clean_rows()
    production = sqlite3.connect(f'file:{PRODUCTION}?mode=ro', uri=True)
    chooser = random.Random(20261107)
    packets, key = [], {}
    for number, input_id in enumerate(ids, 1):
        source, result = clean[input_id]
        handover = json.loads(production.execute('select handover_json from handovers where input_id=?', (input_id,)).fetchone()[0])
        clean_items = [{'summary': ev['summary'], 'quotes': ev['source_passages']} for ev in result['evidence']]
        production_items = [{'summary': ev['one_line'], 'quotes': [ev['quote']]} for ev in handover['evidence']]
        clean_is_a = chooser.random() < 0.5
        key[number] = 'clean=A' if clean_is_a else 'clean=B'
        packets.append({'article': number, 'title': source['title'], 'publisher': source['publisher'],
                        'publication_date': source['publication_date'], 'text': source['text'],
                        'A': clean_items if clean_is_a else production_items,
                        'B': production_items if clean_is_a else clean_items})
    for part, (start, end) in enumerate([(1, 12), (13, 25), (26, 37), (38, 49)], 1):
        (OUT / f'census-packet-{part}.json').write_text(json.dumps([p for p in packets if start <= p['article'] <= end], ensure_ascii=False, indent=1))
    (Path(sys.argv[1]) if len(sys.argv) > 1 else OUT / 'census-key.json').write_text(json.dumps(key, indent=1))
    print('packets written:', len(packets), 'clean=A in', sum(v == 'clean=A' for v in key.values()))

if __name__ == '__main__':
    main()
