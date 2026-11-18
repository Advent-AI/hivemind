#!/usr/bin/env python3
"""Tally the blind readers over the carried links: how each reader placed the controls, and for every carried link the two filing
verdicts, the verdicts on each relation that carried it, and what removing the link would do.

Usage: tally_readers.py <census json> <key folder> <readers folder> <output json> [reader names, default: codex claude]"""
import collections, json, re, sys
from pathlib import Path


def load_answers(path):
    """A reader's JSON array; a reader may wrap it in a code fence."""
    text = Path(path).read_text()
    start, end = text.find('['), text.rfind(']')
    return {row['id']: row for row in json.loads(text[start:end + 1])}


def main(census_path, key_folder, readers_folder, output_path, readers=('codex', 'claude')):
    census = json.loads(Path(census_path).read_text())
    filing_key = json.loads((Path(key_folder) / 'key-filing.json').read_text())
    relation_key = json.loads((Path(key_folder) / 'key-relation.json').read_text())
    filing = {reader: load_answers(Path(readers_folder) / f'filing-{reader}.json') for reader in readers}
    relation = {reader: load_answers(Path(readers_folder) / f'relation-{reader}.json') for reader in readers}
    for reader in readers:
        missing = [k['id'] for k in filing_key if k['id'] not in filing[reader]] + [k['id'] for k in relation_key if k['id'] not in relation[reader]]
        if missing:
            raise SystemExit(f'{reader} gave no verdict for {missing}')

    controls = {}
    for reader in readers:
        filed = collections.Counter(filing[reader][k['id']]['verdict'] for k in filing_key if k['kind'] == 'control: filed by Step 1')
        elsewhere = collections.Counter(filing[reader][k['id']]['verdict'] for k in filing_key if k['kind'] == 'control: no record of the article filed there')
        calibration = collections.Counter()
        for k in relation_key:
            if k['kind'].startswith('calibration') or k.get('labelled on 2026-11-09'):
                earlier = k.get('labelled on 2026-11-09') or re.search(r'labelled (\w+) on', k['kind']).group(1)
                calibration[earlier, relation[reader][k['id']]['verdict']] += 1
        controls[reader] = {'a record under a question Step 1 filed it under': dict(filed),
                            'a record under a question no record of its article was filed under': dict(elsewhere),
                            'relations labelled on 2026-11-09 (earlier label, this reader)': {f'{a} -> {b}': n for (a, b), n in sorted(calibration.items())}}

    filing_id = {(k['draw'], k['record'], k['question']): k['id'] for k in filing_key if k['kind'] == 'carried'}
    relation_id = {(k['draw'], k['incoming'], k['stored']): k['id'] for k in relation_key if k['kind'] == 'carried'}
    rows = []
    for link in census['carried']:
        case = filing_id[link['draw'], link['new']['record'], link['question']]
        filing_verdicts = [filing[reader][case]['verdict'] for reader in readers]
        relation_verdicts = {old['record']: [relation[reader][relation_id[link['draw'], link['new']['record'], old['record']]]['verdict'] for reader in readers]
                             for old in link['carried_by']}
        belongs = 'both evidence' if set(filing_verdicts) == {'evidence'} else 'neither evidence' if 'evidence' not in filing_verdicts else 'split'
        later_version = any(set(verdicts) == {'revision'} for verdicts in relation_verdicts.values())
        possibly_later = any('revision' in verdicts for verdicts in relation_verdicts.values())
        already = bool(link['same_statement_already_under_the_question_by_its_own_link'])
        if belongs == 'neither evidence':
            effect = 'removes a link neither reader would file as evidence'
        elif already:
            effect = 'the same statement stays under the question through another record'
        elif belongs == 'both evidence':
            effect = 'loses a link both readers would file as evidence'
        else:
            effect = 'loses a link one reader would file as evidence'
        rows.append({'draw': link['draw'], 'record': link['new']['record'], 'evidence': link['new']['evidence'], 'question': link['question'],
                     'record has a question of its own': bool(link['new']['step1_theses']), 'step 1 theses': [t['id'] for t in link['new']['step1_theses']],
                     'filing case': case,
                     'filing': dict(zip(readers, filing_verdicts)), 'relation': {old: dict(zip(readers, v)) for old, v in relation_verdicts.items()},
                     'a later version by both readers': later_version, 'a later version by one reader': possibly_later and not later_version,
                     'already there': already, 'effect of removing': effect, 'shown': link['shown_to_the_judge'], 'cited': link['cited'],
                     'summary': link['new']['summary'], 'question_text': link['question_text'],
                     'why': {reader: filing[reader][case]['why'] for reader in readers}})
    by_effect = collections.Counter((row['record has a question of its own'], row['effect of removing']) for row in rows)
    summary = {'readers': list(readers), 'controls': controls, 'carried links': len(rows),
               'by class and effect': [{'record has a question of its own': own, 'effect of removing': effect, 'links': n}
                                       for (own, effect), n in sorted(by_effect.items(), key=lambda item: (-item[0][0], item[0][1]))],
               'filing agreement on carried links': sum(len(set(row['filing'].values())) == 1 for row in rows),
               'relations judged a later version by both readers': sum(row['a later version by both readers'] for row in rows)}
    Path(output_path).write_text(json.dumps({'summary': summary, 'rows': rows}, ensure_ascii=False, indent=1))
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for row in rows:
        relations = '; '.join(f"{old}: {'/'.join(v.values())}" for old, v in row['relation'].items())
        print(f"d{row['draw']} {row['record']:>9} -> {row['question']:<4} own-question {str(row['record has a question of its own']):<5} filing {'/'.join(row['filing'].values()):<22} "
              f"relation [{relations}] already {str(row['already there']):<5} => {row['effect of removing']}")


if __name__ == '__main__':
    main(*sys.argv[1:5], readers=tuple(sys.argv[5:]) or ('codex', 'claude'))
