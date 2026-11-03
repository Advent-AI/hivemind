"""Record an analyst's retrospective reading; this is not an acceptance scorer."""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Hand-read against the source and the complete extraction answer. A quote is
# part of the retained evidence, so its meaning is checked alongside one_line.
# States: complete, partial, absent. These are not mechanical quote matches.
REVIEWS = {
    'a04-1': ('complete', ['e1'], ''),
    'a04-2': ('partial', ['e2'], 'NVL8 is missing from the quote and summary.'),
    'a04-3': ('complete', ['e3'], ''),
    'a18-1': ('complete', ['e1'], ''),
    'a18-2': ('absent', [], 'e2 says startups cannot finance compute but omits signed customer commitments and lenders.'),
    'a18-3': ('complete', ['e6'], 'User: supply/demand support; exact question not adjudicated.'),
    'a18-4': ('complete', ['e8'], ''),
    'a18-5': ('complete', ['e9'], 'Same record also expresses a18-6.'),
    'a18-6': ('complete', ['e9'], 'Same record also expresses a18-5.'),
    'a22-1': ('complete', ['e1'], ''),
    'a22-2': ('complete', ['e2'], ''),
    'a22-3': ('complete', ['e3'], 'Both years appear in one record; whether each has a proper destination is separate.'),
    'a33-1': ('complete', ['e1', 'e4', 'e5'], 'User: colour. Parts in separate records, none written.'),
    'a41-1': ('complete', ['e3', 'e4'], ''),
    'a41-2': ('complete', ['e5'], 'A later account of Sharon, not all six-year/72 MW terms in a18-3.'),
    'a41-3': ('complete', ['e6'], ''),
    'a64-1': ('complete', ['e1'], 'User: core. Source does not specify which hyperscalers; target population must not be assumed identical.'),
    'a64-2': ('partial', ['e2'], 'User: core. Quote and summary omit revenue; summary says metric unspecified.'),
    'a70-1': ('partial', ['e1'], 'No qualification that NVIDIA did not clarify whether the original timing still holds.'),
    'a70-2': ('partial', ['e2'], 'Report of delay is present, but PCB manufacturing cause is absent from the extracted quote and summary.'),
    'a70-3': ('complete', ['e7'], 'User: product progress; exact question not adjudicated. Source says largest customers, not hyperscalers.'),
    'a70-4': ('complete', ['e8'], ''),
    'a70-5': ('complete', ['e9'], ''),
    'a70-6': ('complete', ['e10'], ''),
    'a70-7': ('complete', ['e11'], ''),
    'a70-8': ('partial', ['e2'], 'Affected Rubin Ultra and 2027 Kyber are stated; exclusion of 2026 Rubin is missing.'),
    'a71-1': ('complete', ['e1', 'e2'], ''),
    'a71-2': ('complete', ['e3'], ''),
    'a71-3': ('absent', [], 'The backup cancellation and customer objections are absent from this article answer.'),
    'a71-4': ('complete', ['e4'], 'Extracted but refused by the quote check.'),
    'a71-5': ('complete', ['e5'], 'SemiAnalysis forecast, second-half data-center compute rather than full-year segment revenue.'),
    'a93-1': ('complete', ['e1'], 'The quote includes product revenue as well as cloud share; the summary omits product revenue.'),
}


def main():
    reference = json.loads((HERE / 'source-reference.json').read_text())
    ledger = json.loads((HERE / 'ledger.json').read_text())['v38']
    coverage = {r['id']: r for r in json.loads((HERE / 'coverage.json').read_text())}
    rows = []
    seen = set()
    for article in reference['articles']:
        actual = ledger[article['article_no'] - 1]
        assert article['input_id'] == actual['input_id']
        for claim in article['claims']:
            ident = claim['id']
            if ident == 'a64-3':
                continue  # Alex's explicit exclusion, not an inferred general rule.
            assert ident not in seen and claim['source_text'] in actual['source']
            seen.add(ident)
            status, ids, note = REVIEWS[ident]
            records = {r['id']: r for r in actual['records']}
            assert len(ids) == len(set(ids)) and all(i in records for i in ids)
            assert status in ('complete', 'partial', 'absent')
            assert (status == 'absent') == (not ids)
            evidence = [records[i] for i in ids]
            extra_sources = (['Cloud customers reportedly rejected it because the design was awkward and the service was expensive to run.']
                             if ident == 'a71-3' else [])
            assert all(span in actual['source'] for span in extra_sources)
            # This only measures whether the source meaning is in written
            # records. It does not decide if any destination is right.
            written_content = status == 'complete' and all(r['final_status'] == 'written' for r in evidence)
            rows.append({
                'id': ident, 'article_no': article['article_no'], 'input_id': article['input_id'],
                'publication_day': actual['day'], 'source_text': claim['source_text'], 'additional_source_text': extra_sources,
                'meaning': claim['meaning'], 'previous_model_core': claim['core'],
                'reviewed_meaning': ('NVL72x2 stopgap cancelled after the largest customers objected to operating two linked cabinets as one unit.'
                                     if ident == 'a70-3' else claim['meaning']),
                'extraction_content': status, 'analyst_note': note,
                'records': [{k: r[k] for k in ('id', 'quote', 'one_line', 'speaker', 'original_who',
                            'original_day', 'tier', 'event_time', 'status', 'drop_reason',
                            'final_status', 'stored_id', 'stored_links')} for r in evidence],
                'complete_content_written': written_content,
                'destination_correct': 'not assessed',
                'old_coverage_complete': coverage[ident]['versions']['v38']['complete'],
            })
    assert seen == set(REVIEWS) and len(rows) == 32
    count = collections.Counter(r['extraction_content'] for r in rows)
    output = {'scope': 'retrospective model-authored review of 32 provisional claims from 20 week articles; not an accepted benchmark',
              'exclusion': 'a64-3: user excluded this specific FY2028 EPS estimate',
              'counts': dict(count), 'complete_content_written': sum(r['complete_content_written'] for r in rows),
              'limitations': 'Not unique events; source repetition, significance, targets and independent blind review remain unresolved. Written content is not correct placement.',
              'rows': rows}
    path = HERE / 'week-fact-review-2026-10-29-v2.json'
    with path.open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'rows'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
