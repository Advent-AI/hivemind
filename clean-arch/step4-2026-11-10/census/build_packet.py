"""Census packet for the Step 4 design ($0, read-only): every thesis the three stored unseeded draws opened, as the ladder step would
meet it. For each thesis: the fields Step 1 wrote for it (from the model's checked answer in the trace, `trace.result`; the library
state keeps only description, outcome and period), the opening article's date, title and full text, and the evidence statements that
article linked to it. Writes packet.json and packet.md beside this file.

Usage: python3 build_packet.py"""
import json, sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DRAWS = ROOT / 'poc/data/clean-unseeded-2026-11-10'
RUNS = {'u1': ['draw-d1/trace.sqlite'], 'u2': ['draw-d2/trace.sqlite'], 'u3': ['draw-d3/trace.sqlite', 'draw-d3-segment-2/trace.sqlite']}
EXPECTED = {'u1': 12, 'u2': 10, 'u3': 12}


def theses_of(run, parts, draws=DRAWS, expected=None):
    """The theses a stored draw opened, each with the fields Step 1 wrote and its opening article. `expected`, when given, is the
    count the caller knows the draw to hold; a different count stops the build."""
    expected = EXPECTED[run] if expected is None else expected
    seen, out = set(), []
    for part in parts:
        conn = sqlite3.connect(f'file:{Path(draws) / part}?mode=ro', uri=True)
        try:
            rows = conn.execute("select before_state, request, result, after_state from trace where status='complete' order by sequence").fetchall()
        finally:
            conn.close()
        for before, request, result, after in rows:
            before_ids = {t['id'] for t in json.loads(before)}
            new = [t for t in json.loads(after) if t['id'] not in before_ids and t['id'] not in seen]
            if not new:
                continue
            answer = json.loads(result)
            item = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']
            by_description = {t['description']: t for t in answer['new_theses']}
            if len(by_description) != len(answer['new_theses']):
                raise SystemExit(f'{run}: two new theses share a description in one answer')
            for thesis in new:
                seen.add(thesis['id'])
                written = by_description[thesis['description']]          # KeyError: the state and the answer disagree
                linked = [e for e in answer['evidence']
                          if any(l['target_type'] == 'new' and l['target_id'] == written['local_id'] for l in e['links'])]
                out.append({
                    'run': run, 'id': thesis['id'],
                    'thesis': {k: written[k] for k in ('description', 'outcome', 'period', 'opens_as', 'settled_by', 'why_a_separate_bet')},
                    'article': {k: item[k] for k in ('id', 'publisher', 'publication_date', 'title', 'text')},
                    'linked_evidence': [{'summary': e['summary'], 'source_passages': e['source_passages'], 'original_party': e['original_party'],
                                         'tier': e['tier'], 'statement_date': e['statement_date'], 'figures': e['figures']} for e in linked],
                })
    if len(out) != expected:
        raise SystemExit(f'{run}: {len(out)} theses, expected {expected}')
    return out


def main():
    packet = [t for run, parts in RUNS.items() for t in theses_of(run, parts)]
    (HERE / 'packet.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False))
    lines = ['# Step 4 census packet: the 34 theses the three unseeded draws opened, each with its opening article', '']
    for n, t in enumerate(packet, 1):
        th, art = t['thesis'], t['article']
        lines += [f'## Case {n}: {t["run"]} {t["id"]}', '',
                  f'- **Opening article:** {art["publication_date"]}, {art["publisher"]}, "{art["title"]}" (`{art["id"]}`)',
                  f'- **description:** {th["description"]}', f'- **outcome:** {th["outcome"]}', f'- **period:** {th["period"]}',
                  f'- **opens_as:** {th["opens_as"]}', f'- **settled_by:** {th["settled_by"]}',
                  f'- **why_a_separate_bet:** {th["why_a_separate_bet"]}', '', '**Evidence the opening article linked to this thesis:**', '']
        for e in t['linked_evidence']:
            lines.append(f'- [{e["tier"]}; {e["original_party"]}; {e["statement_date"]}] {e["summary"]}')
        lines += ['', '**Article text:**', '', '```', art['text'], '```', '']
    (HERE / 'packet.md').write_text('\n'.join(lines))
    print(len(packet), 'theses;', sum(len(t['linked_evidence']) for t in packet), 'linked evidence items;',
          sum(1 for t in packet if not t['linked_evidence']), 'theses with none;', (HERE / 'packet.md').stat().st_size, 'bytes of packet.md')


if __name__ == '__main__':
    main()
