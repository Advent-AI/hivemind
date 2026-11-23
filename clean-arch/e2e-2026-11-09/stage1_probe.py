"""Stage 1 of the seeded end-to-end diagnostic (D392): does c8, unchanged, link the facts the ruler's questions need when the 22 seed
questions are its open theses? For each case the control is the stored dev-d1 request re-sent the same day exactly as it was sent
(`sent_request` from the trace); the treatment is that same sent request with only the open-theses list in the user message replaced by
the 22 seeds, shown by a frozen rule. Every answer goes through the runner's checks; a gold fact counts as delivered to a question when a
kept evidence item quotes the gold item's passage and links to that question's seed.

Usage: stage1_probe.py <output folder> [--draws 3] [--send]"""
import argparse, concurrent.futures, json, re, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
from hivemind import model, testdb  # noqa: E402
import runner  # noqa: E402
from live import deepseek_json_mode  # noqa: E402

TRACE = ROOT / 'poc/data/clean-step1-c8-dev-d1-2026-11-09/trace.sqlite'
SOURCE = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEEDS = ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'
PACKET = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json'
PRD = ROOT / 'clean-arch/PRD.md'


def dump(obj):
    """The runner's payload serialisation (runner.run: json.dumps with ensure_ascii=False)."""
    return json.dumps(obj, ensure_ascii=False)


def seed_theses():
    """The frozen rule for showing a seed as a c8 thesis: description = the question, outcome = what it looks at, period = its year and
    due day."""
    seeds = json.loads(SEEDS.read_text())['questions']
    return [{'id': q['view_id'], 'description': q['question'], 'outcome': q['looks_at'], 'period': f"{q['year']}, due {q['due_day']}"}
            for q in seeds]


def normalise(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^0-9a-z.%$ ]', ' ', text.lower())).strip()


def quotes_gold(evidence, gold_passage):
    """Identity only: after normalising case, punctuation and spaces, one of the kept item's passages contains the whole gold passage,
    or is contained in it and covers at least 60% of its length. A fragment of a gold passage does not count as the fact."""
    gold = normalise(gold_passage)
    for passage in evidence.get('verified_source_passages') or evidence['source_passages']:
        mine = normalise(passage or '')
        if gold in mine or (mine in gold and len(mine) >= 0.6 * len(gold)):
            return True
    return False


def gold_questions():
    """Which questions the frozen judgement gold cites each item for (reference and implied-outcome items)."""
    gold = json.loads((ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json').read_text())
    cited = {}
    for entry in gold['entries']:
        target = entry['seed_view_id'] or entry['question_id']
        for part in ('reference', 'implied_outcome'):
            for item in (entry.get(part) or {}).get('items', []):
                cited.setdefault(item, set()).add(target)
    return cited


def build_jobs(cases, draws):
    conn = sqlite3.connect(f'file:{TRACE}?mode=ro', uri=True)
    rows = {iid: (seq, req, raw, before) for seq, iid, req, raw, before in
            conn.execute("select sequence, input_id, request, raw_response, before_state from trace where status='complete'")}
    seeds = seed_theses()
    _, schema = runner.draft(PRD)
    jobs = []
    for case in cases:
        seq, req, raw, before = rows[case['input_id']]
        sent = json.loads(raw)['sent_request']
        stored_user = json.loads(req)['messages'][1]['content']
        stored = json.loads(req)
        if sent != deepseek_json_mode(stored, sent.get('reasoning_effort')):
            raise SystemExit(f"{case['case']}: the sent request is not the live transport's form of the stored request")
        payload, end = json.JSONDecoder().raw_decode(stored_user)
        if payload['open_theses'] != [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in json.loads(before)]:
            raise SystemExit(f"{case['case']}: the stored payload does not show the stored before-state")
        treated_payload = dict(payload, open_theses=seeds)
        treated_user = dump(treated_payload) + stored_user[end:]
        if stored_user != dump(payload) + stored_user[end:]:
            raise SystemExit(f"{case['case']}: the payload does not re-serialise byte for byte")
        treated = json.loads(json.dumps(sent))
        treated['messages'][1]['content'] = treated_user
        item = {'text': payload['source_item']['text']}
        jobs.append((case, 'control', 1, sent, item, payload['open_theses'], schema))
        for draw in range(1, draws + 1):
            jobs.append((case, 'seeded', draw, treated, item, seeds, schema))
    return jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output'); parser.add_argument('--draws', type=int, default=3, choices=[1, 2, 3]); parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    cases = json.loads((HERE / 'stage1_cases.json').read_text())
    jobs = build_jobs(cases, args.draws)
    price_in, price_out = model.PRICES['deepseek-flash']
    chars = sum(len(json.dumps(j[3])) for j in jobs)
    print(f'{len(jobs)} requests over {len(cases)} articles; about {chars // 4} input tokens; about '
          f'${chars / 4 / 1e6 * price_in + len(jobs) * 6000 / 1e6 * price_out:.2f} at published rates (6k output tokens each assumed); '
          f'about ${chars / 4 / 1e6 * price_in + len(jobs) * jobs[0][3]["max_tokens"] / 1e6 * price_out:.2f} if every answer used the '
          f'{jobs[0][3]["max_tokens"]}-token cap (input tokens estimated; up to three transport attempts could triple it)')
    if not args.send:
        return
    gold = {i['id']: i for i in json.loads(PACKET.read_text())['items']}
    out = Path(args.output); out.mkdir(parents=True, exist_ok=False)
    def send(job):
        case, arm, draw, request, item, shown, schema = job
        record = {'case': case['case'], 'arm': arm, 'draw': draw}
        try:
            response = model.openai_transport('deepseek', request)
        except Exception as error:   # recorded with its reason, never retried silently
            record['error'] = f'{type(error).__name__}: {error}'
            return record
        usage = response.get('usage') or {}
        record.update(input_tokens=usage.get('prompt_tokens'), output_tokens=usage.get('completion_tokens'))
        try:
            record['raw'] = response['choices'][0]['message']['content']
            answer = json.loads(record['raw'])
            checked = runner.validate(answer, schema, item, shown)
        except Exception as error:
            record['contract_error'] = f'{type(error).__name__}: {error}'
            return record
        record['kept'] = checked['evidence']
        record['new_theses'] = answer['new_theses']
        record['delivered'] = {g: sorted({l['target_id'] for e in checked['evidence'] if quotes_gold(e, gold[g]['passage']) for l in e['links']
                                          if l['target_type'] == 'existing'})
                               for g in case['gold']}
        record['matched'] = {g: [p for e in checked['evidence'] if quotes_gold(e, gold[g]['passage'])
                                 for p in (e.get('verified_source_passages') or e['source_passages'])] for g in case['gold']}
        record['written'] = {g: any(quotes_gold(e, gold[g]['passage']) for e in checked['evidence']) for g in case['gold']}
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(send, jobs))
    (out / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    tokens_in = sum(r.get('input_tokens') or 0 for r in records); tokens_out = sum(r.get('output_tokens') or 0 for r in records)
    print(f"{len(records)} records; errors {sum('error' in r for r in records)}; contract errors {sum('contract_error' in r for r in records)}; "
          f'${tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out:.2f} at published rates')


if __name__ == '__main__':
    main()
