"""Tabulate saved human-readable model judgments; never grade answer text."""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from statistics import mean, median

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--readings', default='blind-readings.json')
    parser.add_argument('--output', default='measurements.json')
    args = parser.parse_args()
    readings = read(args.readings)
    mapping = read('blind-map.json')
    assert len(readings['rows']) == len(mapping) == 60
    assert len(set(mapping.values())) == 60
    assert readings['scoring_sha256'] == hashlib.sha256((HERE / 'scoring.md').read_bytes()).hexdigest()
    rows = []
    for judgment in readings['rows']:
        blind = HERE / 'blind' / (judgment['id'] + '.json')
        assert hashlib.sha256(blind.read_bytes()).hexdigest() == judgment['answer_sha256']
        ident = mapping[judgment['id']]
        case, model, prompt, draw = ident.split('-')
        result = read(ident + '-answer.json')
        assert json.loads(blind.read_text())['answer'] == result['answer']
        assert result['completed'] and result['errors'] == []
        usage = result['response']['usage']
        if model == 'haiku':
            inputs, outputs = usage['input_tokens'], usage['output_tokens']
            cache = usage['cache_read_input_tokens']
        else:
            inputs, outputs = usage['prompt_tokens'], usage['completion_tokens']
            cache = usage['prompt_tokens_details']['cached_tokens']
        rows.append(dict(judgment, answer_id=ident, model=model, prompt=prompt,
                         draw=int(draw), seconds=result['seconds'], input_tokens=inputs,
                         output_tokens=outputs, cached_input_tokens=cache,
                         visible_answer_characters=len(json.dumps(result['answer'], ensure_ascii=False)),
                         note_characters=len(result['answer']['note']),
                         rate_assumption_estimate_usd=(inputs * .1 + outputs * .5) / 1e6))
        assert case == judgment['case']

    def summarize(group):
        assert group
        positive = [r for r in group if r['case'] != 'singapore']
        negative = [r for r in group if r['case'] == 'singapore']
        return dict(
            responses=len(group), positive_units=len(positive),
            core_content=dict(Counter(r['content'] for r in positive)),
            exclusion_units=len(negative), exclusions=dict(Counter(r['exclusion'] for r in negative)),
            definite_fact_error_responses=sum(bool(r['definite_fact_errors']) for r in group),
            inference=dict(Counter(r['inference'] for r in group)),
            actions=dict(Counter(r['action'] for r in group)),
            seconds_mean=mean(r['seconds'] for r in group),
            seconds_median=median(r['seconds'] for r in group),
            seconds_min=min(r['seconds'] for r in group), seconds_max=max(r['seconds'] for r in group),
            note_characters_mean=mean(r['note_characters'] for r in group),
            input_tokens=sum(r['input_tokens'] for r in group),
            output_tokens=sum(r['output_tokens'] for r in group),
            cached_input_tokens=sum(r['cached_input_tokens'] for r in group),
            rate_assumption_estimate_usd=sum(r['rate_assumption_estimate_usd'] for r in group))

    summary = dict(
        judgment_file_sha256=hashlib.sha256((HERE / args.readings).read_bytes()).hexdigest(),
        limitations='Five known development sources, four positive units, three repeats each. No whole-week retention rate, no independent test set, no population accuracy or billing claim.',
        totals=summarize(rows),
        cells={f'{m}-{p}': summarize([r for r in rows if r['model'] == m and r['prompt'] == p])
               for m in ('haiku', 'luna') for p in ('base', 'check')},
        models={m: summarize([r for r in rows if r['model'] == m]) for m in ('haiku', 'luna')},
        per_case={f'{c}-{m}-{p}': summarize([r for r in rows if r['case'] == c and r['model'] == m and r['prompt'] == p])
                  for c in ('nvidia', 'nn', 'cloud', 'signed', 'singapore')
                  for m in ('haiku', 'luna') for p in ('base', 'check')},
        rows=rows)
    target = HERE / args.output
    if target.exists():
        assert read(args.output) == summary
    else:
        with target.open('x') as stream:
            json.dump(summary, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k: summary[k] for k in ('totals', 'cells', 'models')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
