"""Merge-check packets for any Step 2 forward run over a clean Step 1 trace (no model calls): the same entry shape and prompts as
build_final_check.py's merge packets and the third reader's packet, built from the run's own Step 1 records and article text instead of
the validation folder's items.

  first    every repeat in decisions.json as a pair (the chosen group's original record, the incoming record), 26 per packet, with the
           prompt for two blind readers (MA, MB);
  third    the pairs either reader rejected (merge-disputed.json, written by score_final.py), with the third reader's prompt.

Usage: build_merge_packets.py first|third <step1 trace> <forward run folder>"""
import json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'step2'))
import run_forward  # noqa: E402

PROMPT = (HERE.parents[1] / 'poc/data/clean-step2-forward-2026-11-08/merge-prompt-1.md').read_text()
THIRD = (HERE.parents[1] / 'poc/data/clean-step2-forward-2026-11-08/merge-third-prompt.md').read_text()
OLD_RUN = '/Users/lchingen/hivemind/poc/data/clean-step2-forward-2026-11-08/'


def context(text, passage, width=300):
    at = text.find(passage)
    return text[max(0, at - width):at + len(passage) + width] if at >= 0 else passage


def entries(trace):
    articles, questions, _opened = run_forward.step1_records(trace)
    texts, position = {}, None   # articles numbered as run_forward.step1_records numbers them: by first-manifest position
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        if position is None:
            position = {iid: n for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
        for iid, req in conn.execute("select input_id, request from trace where status='complete'"):
            texts[position[iid]] = json.JSONDecoder().raw_decode(json.loads(req)['messages'][1]['content'])[0]['source_item']['text']
    out = {}
    for records in articles:
        for r in records:
            out[r['id']] = {'summary': r['summary'], 'original_party': r['original_party'],
                            'statement_date': r['statement_date'] or r['statement_date_text'], 'period': r['evidence_period'],
                            'publication_date': r['publication_date'], 'tier': r['tier'], 'reporting_speaker': r['reporting_speaker'],
                            'publisher': r['publisher'], 'title': r['title'], 'passages': r['passages'],
                            'source_context': [context(texts[r['article']], p) for p in r['passages']],
                            'theses': [questions[t] for t in r['thesis_ids']]}
    return out


def main():
    mode, trace, run = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    items = entries(trace)
    if mode == 'first':
        decisions = json.loads((run / 'decisions.json').read_text())
        pairs = [(d['outcome']['repeat_of'][0], d['id']) for d in decisions if d['outcome']['kind'] == 'repeat' and 'refused' not in d]
        key = {}
        for start in range(0, len(pairs), 26):
            n = start // 26 + 1
            packet = []
            for original, incoming in pairs[start:start + 26]:
                mid = f'X{len(key) + 1}'
                key[mid] = {'earlier': original, 'later': incoming}
                packet.append({'id': mid, 'earlier': items[original], 'later': items[incoming]})
            (run / f'merge-packet-{n}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
            (run / f'merge-prompt-{n}.md').write_text(PROMPT.replace(OLD_RUN + 'merge-packet-1.json', f'{run.resolve()}/merge-packet-{n}.json'))
        (run / 'merge-key.json').write_text(json.dumps(key, indent=1))
        print(f'merge pairs {len(pairs)} in {(len(pairs) + 25) // 26} packets')
    else:
        key = json.loads((run / 'merge-key.json').read_text())
        disputed = json.loads((run / 'merge-disputed.json').read_text())
        packet = [{'id': mid, 'earlier': items[key[mid]['earlier']], 'later': items[key[mid]['later']]} for mid in disputed]
        (run / 'merge-third-packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
        (run / 'merge-third-prompt.md').write_text(THIRD.replace(OLD_RUN + 'merge-third-packet.json', f'{run.resolve()}/merge-third-packet.json'))
        print(f'third-reader pairs {len(packet)}')


if __name__ == '__main__':
    main()
