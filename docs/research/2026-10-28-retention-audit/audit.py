"""Reconcile the frozen, read-only week with explicit semantic labels and source claims.

The program verifies accounting, not the analyst's semantic labels. Those labels
are inspectable beside their article/record identities in records.tsv.
"""
import collections
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def validate(ledgers, labels, coverage, reference):
    for version, articles in ledgers.items():
        assert len(articles) == 98
        assert len({a['input_id'] for a in articles}) == 98
        assert set(labels[version]) == {str(a['article_no']) for a in articles}
        for article in articles:
            records = article['records']
            actual = {r['id'] for r in records}
            judged = labels[version][str(article['article_no'])]['records']
            assert len(actual) == len(records)
            assert actual == set(judged), (version, article['article_no'])
            assert all(x['label'] in ('M', 'C', 'J') for x in judged.values())
            assert hashlib.sha256(article['source'].encode()).hexdigest() == article['source_sha256']
            assert all(bool(r['stored_id']) == (r['final_status'] == 'written') for r in records)
        assert sum(len(a['records']) for a in articles) > 0
    expected = {c['id'] for a in reference['articles'] for c in a['claims']}
    assert expected and expected == {c['id'] for c in coverage}
    for claim in coverage:
        for version, cell in claim['versions'].items():
            records = {r['id']: r for r in ledgers[version][claim['article_no'] - 1]['records']}
            assert set(cell['raw_ids']) <= set(records)
            stored = [r for r in cell['raw_ids'] if records[r]['stored_id']]
            assert stored == cell['stored_ids']
            assert cell['fully_written'] == (cell['complete'] and len(stored) == len(cell['raw_ids']))


def measure(ledgers, labels, coverage):
    result = {}
    for version, articles in ledgers.items():
        counts = collections.Counter()
        for article in articles:
            for record in article['records']:
                label = labels[version][str(article['article_no'])]['records'][record['id']]['label']
                counts[f'{label}_{"written" if record["stored_id"] else "lost"}'] += 1
        written = sum(counts[f'{label}_written'] for label in ('M', 'C', 'J'))
        useful = counts['M_written'] + counts['M_lost']
        nonessential = sum(counts[f'{label}_{status}'] for label in ('C', 'J') for status in ('written', 'lost'))
        source = [c['versions'][version] for c in coverage]
        result[version] = {
            'counts': dict(counts), 'written': written,
            'useful_fraction_written': [counts['M_written'], written],
            'useful_retention_after_extraction': [counts['M_written'], useful],
            'nonessential_removed': [counts['C_lost'] + counts['J_lost'], nonessential],
            'strict_junk_removed': [counts['J_lost'], counts['J_written'] + counts['J_lost']],
            'discard_precision_including_context': [counts['C_lost'] + counts['J_lost'], sum(counts[f'{k}_lost'] for k in ('M', 'C', 'J'))],
            'source_claims': len(source),
            'source_raw_full': sum(c['complete'] for c in source),
            'source_raw_partial': sum(bool(c['raw_ids']) and not c['complete'] for c in source),
            'source_raw_absent': sum(not c['raw_ids'] for c in source),
            'source_final_full': sum(c['fully_written'] for c in source),
            'source_core_total': sum(c['core'] for c in coverage),
            'source_core_final_full': sum(c['core'] and c['versions'][version]['fully_written'] for c in coverage),
        }
    return result


def main():
    manifest = read('manifest.json')
    assert hashlib.sha256((HERE / 'ledger.json').read_bytes()).hexdigest() == manifest['ledger_sha256']
    expected_hash = (HERE / 'source-reference.sha256').read_text().split()[0]
    assert hashlib.sha256((HERE / 'source-reference.json').read_bytes()).hexdigest() == expected_hash
    ledgers = read('ledger.json')
    labels = read('labels-earlier.json')
    labels['v38'] = read('labels-v38.json')
    coverage, reference = read('coverage.json'), read('source-reference.json')
    validate(ledgers, labels, coverage, reference)
    # Positive control: losing one judged record must invalidate the census.
    mutant = copy.deepcopy(labels)
    del mutant['v38']['2']['records']['e1']
    try:
        validate(ledgers, mutant, coverage, reference)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing-label control was not caught')
    results = measure(ledgers, labels, coverage)
    loss = read('loss-traces-v38.json')
    assert len(loss) == results['v38']['counts']['M_lost']
    results['loss_causes_v38'] = dict(collections.Counter(x['cause'] for x in loss))
    results['accounting_check'] = {'articles_per_version': 98, 'records_judged': sum(sum(x['counts'].values()) for x in results.values() if isinstance(x, dict) and 'counts' in x), 'missing_label_mutant_caught': True}
    (HERE / 'metrics.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    lines = ['version\tarticle\trecord\tlabel\tfinal_status\tstored_id\tstored_links\ttext']
    for version, articles in ledgers.items():
        for article in articles:
            for record in article['records']:
                label = labels[version][str(article['article_no'])]['records'][record['id']]['label']
                fields = [version, article['article_no'], record['id'], label, record['final_status'], record['stored_id'] or '', ','.join(record['stored_links']), record['one_line']]
                lines.append('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in fields))
    (HERE / 'records.tsv').write_text('\n'.join(lines) + '\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
