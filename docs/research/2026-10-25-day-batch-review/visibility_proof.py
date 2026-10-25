"""Replay saved extraction answers through the real checks with day-start IDs.

This counterfactual isolates reference loss from changing model answers. It
does not claim what a model would produce from a different prompt.
"""
import argparse
import collections
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit import ARMS, ITEM, VIEW, GROUP, ROOT, connect  # noqa: E402
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe  # noqa: E402


def compare(folder, config):
    base = ROOT / 'poc/data' / folder
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    with connect(base / 'views.sqlite') as db, connect(base / 'archive.sqlite') as arc, connect(ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite') as source:
        dates = {r['input_id']: r['day'] for r in db.execute('select input_id,min(publication_day) day from processing_steps group by input_id')}
        views = {r['view_id']: dates[r['created_from_input']] for r in db.execute('select * from views')}
        groups = {r['group_id']: dates[r['created_from_input']] for r in db.execute('select * from thesis_groups')}
        hands = {r['input_id']: json.loads(r['handover_json']) for r in db.execute('select * from handovers order by id')}
        counts = collections.Counter()
        examples = []
        for call in arc.execute("select call_id,request_json,answer_json from model_calls where config_version=? and purpose='extract' order by call_id", (config,)):
            user = json.loads(call['request_json'])['messages'][1]['content']
            input_id, day = ITEM.search(user).groups()
            item = dict(source.execute('select * from items where input_id=?', (input_id,)).fetchone())
            context = user.split('[Existing theses of these objects]', 1)[1].split('[Item]', 1)[0]
            ids, gids = set(VIEW.findall(context)), set(GROUP.findall(context))
            baseline = extraction.sift_with_groups(json.loads(call['answer_json']), item, item['text'], ids, uni, english=True, shown_group_ids=gids)
            expected = hands[input_id]
            for field, values in [('evidence', baseline[0]), ('candidates', baseline[1])]:
                if {x['id'] for x in values} != {x['id'] for x in expected[field]}:
                    raise ValueError(f'baseline differs for {input_id} {field}')
            day_start = extraction.sift_with_groups(json.loads(call['answer_json']), item, item['text'],
                {v for v in ids if views[v] < day}, uni, english=True, shown_group_ids={g for g in gids if groups[g] < day})
            counts['answers_checked'] += 1
            before = {e['id']: e for e in baseline[0]}
            after = {e['id']: e for e in day_start[0]}
            lost = sorted(before.keys() - after.keys())
            removed_links = [(eid, v) for eid, e in before.items() for v in e['links'] if eid not in after or v not in after[eid]['links']]
            counts['retained_evidence_control'] += len(before)
            counts['retained_evidence_day_start'] += len(after)
            counts['lost_evidence'] += len(lost)
            counts['lost_links'] += len(removed_links)
            counts['answers_with_lost_links'] += bool(removed_links)
            counts['lost_candidates'] += len({c['id'] for c in baseline[1]} - {c['id'] for c in day_start[1]})
            if removed_links and len(examples) < 3:
                examples.append({'input_id': input_id, 'day': day, 'lost_evidence': lost,
                                 'lost_links': removed_links, 'first_quote': before[removed_links[0][0]]['quote']})
        cs = [c['id'] for h in hands.values() for c in h['candidates']]
        es = [e['id'] for h in hands.values() for e in h['evidence']]
        counts['candidate_records'] = len(cs)
        counts['unique_local_candidate_ids'] = len(set(cs))
        counts['evidence_records'] = len(es)
        counts['unique_local_evidence_ids'] = len(set(es))
        return {'counts': dict(counts), 'examples': examples,
                'interpretation': 'same stored answers, only allowed references reduced; not a fresh model comparison'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = {arm: compare(*spec) for arm, spec in ARMS.items()}
    with args.out.open('x') as handle:
        json.dump(result, handle, indent=2)
    for arm, values in result.items():
        print(arm, values['counts'])


if __name__ == '__main__':
    main()
