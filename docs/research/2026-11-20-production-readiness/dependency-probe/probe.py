"""Alex's A (2026-11-20): does a Data Center question answer consistently with the total-revenue question once it reads that
question's conclusion through a dependency? Probe on the three finished poc-v118 draws (release comparison old-1..3).

  python3 probe.py check <scratch>          # $0: rebuild each Data Center question's last stored request through production code,
                                            #     prove it byte-equal to the stored one, build the changed request, print both sizes
  python3 probe.py send <scratch> <out>     # paid: old-2 only (council round 3): control (as stored) and changed, three samples each

The finished stores are opened read-only. Each draw's scratch copy is rolled back to the moment before the Data Center question's
last judgement (that row and every later judgement removed); the control request must then reproduce the stored request's sha256.
The changed copy adds one dependency row (Data Center reads total revenue, `first_is_bullish`); production code renders it.
Every sample goes to its own new archive (an existing path refuses the send), so no answer is a cached replay. A refused answer is
retried once with production's note, and both attempts are kept. Each call makes one transport attempt; before it, the worst case (one
token per character of the serialized request plus the full output allowance) is reserved against the cap, and stays charged when
the call fails with its usage unknown. A cap stop before both arms have three samples is reported as inconclusive.
"""
import json, sqlite3, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import config, model                     # noqa: E402
from hivemind.views import judging                     # noqa: E402

RUNS = REPO / 'poc/data/comparison-2026-11-17/run'
PAIRS = {'old-1': ('v8', 'v4'), 'old-2': ('v9', 'v14'), 'old-3': ('v35', 'v3')}   # (Data Center FY2027, total revenue FY2027)
SEND_DRAWS = ('old-2',)                                # council round 3: the only draw whose shown total carries both FY and Q4
SAMPLES = 3
CAP_USD = 0.15                                         # 6 sends (about $0.006 each) and their retries; each call reserves about $0.017


def one_attempt(provider, request):
    """Production's transport with a single attempt, so every possible charge is reserved before it is made."""
    return model.openai_transport(provider, request, max_attempts=1)


def prepared(scratch, draw, with_dependency):
    data_center, total = PAIRS[draw]
    source = sqlite3.connect(f'file:{RUNS / draw}/prod/views.sqlite?mode=ro', uri=True)
    path = scratch / f'{draw}-{"changed" if with_dependency else "control"}.sqlite'
    path.unlink(missing_ok=True)
    copy = sqlite3.connect(path)
    source.backup(copy)
    source.close()
    copy.row_factory = sqlite3.Row
    last = copy.execute('select judgement_id, seq, request_sha256, publication_day from judgements where view_id=? order by judgement_id desc limit 1',
                        (data_center,)).fetchone()
    copy.execute('drop trigger judgements_no_delete')
    copy.execute('delete from judgements where judgement_id=? or seq>?', (last['judgement_id'], last['seq']))
    if with_dependency:
        copy.execute("insert into dependencies(view_id, depends_on, wait_chain_view_id, wait_year, direction, seq) values (?, ?, '', '', 'first_is_bullish', ?)",
                     (data_center, total, last['seq']))
    copy.commit()
    return copy, dict(last)


def requests(scratch):
    cfg = config.load(str(REPO / 'poc/config/poc-v118.json'))
    version = cfg.rejudging.prompt_version
    schema = judging.schema_for(version)
    out = {}
    for draw, (data_center, total) in PAIRS.items():
        for arm in ('control', 'changed'):
            conn, last = prepared(scratch, draw, arm == 'changed')
            system, user = judging.build_prompt(conn, data_center, version)
            request = model.build_request(cfg.rejudging, system, user, schema, 'judgement', cfg.provider)
            _, sha = model.request_identity(request)
            out[(draw, arm)] = {'conn': conn, 'system': system, 'user': user, 'sha': sha, 'stored_sha': last['request_sha256'],
                                'day': last['publication_day'], 'seq': last['seq']}
    return cfg, schema, out


def check(scratch):
    _, _, built = requests(scratch)
    ok = True
    for (draw, arm), r in built.items():
        same = r['sha'] == r['stored_sha']
        if arm == 'control' and not same:
            ok = False
        added = len(r['user']) - len(built[(draw, 'control')]['user'])
        print(f'{draw} {arm}: day {r["day"]} seq {r["seq"]} chars {len(r["user"])} (+{added}) sha {"== stored" if same else "differs"}')
    print('control requests byte-equal to the stored ones:', ok)
    return ok


def send(scratch, out_dir):
    cfg, schema, built = requests(scratch)
    if not all(r['sha'] == r['stored_sha'] for (draw, arm), r in built.items() if arm == 'control'):
        raise SystemExit('a control request differs from the stored one: nothing sent')
    out_dir.mkdir(parents=True, exist_ok=True)
    spent, rows = 0.0, []
    price_in, price_out = model.PRICES[cfg.rejudging.model]
    for sample in range(1, SAMPLES + 1):
        for (draw, arm), r in built.items():
            if draw not in SEND_DRAWS:
                continue
            data_center = PAIRS[draw][0]
            archive_path = scratch / f'archive-{draw}-{arm}-{sample}.sqlite'
            if archive_path.exists():
                raise SystemExit(f'{archive_path} exists: a sample needs a new archive')
            archive = model.Archive(str(archive_path))
            attempts, note = [], ''
            for attempt in (1, 2):
                # hard bound (council round 5): one transport attempt per call, reserved at one token per character of the full
                # serialized request plus the full output allowance; when usage is unknown (an exception) the reservation stays charged
                request = model.build_request(cfg.rejudging, r['system'], r['user'] + note, schema, 'judgement', cfg.provider)
                worst = len(json.dumps(request)) / 1e6 * price_in + cfg.rejudging.max_output_tokens / 1e6 * price_out
                if spent + worst > CAP_USD:
                    raise SystemExit(f'cap: spent ${spent:.4f} + worst ${worst:.4f} > ${CAP_USD}; stopped before {draw} {arm} {sample}: inconclusive')
                try:
                    answer = model.call(archive, cfg, cfg.rejudging, r['system'], r['user'] + note, schema, 'judgement', 'judge',
                                        transport=one_attempt)
                except Exception as error:                     # transport failure or malformed answer: usage unknown
                    spent += worst
                    attempts.append({'attempt': attempt, 'errors': [f'{type(error).__name__}: {error}'[:300]], 'cost': worst, 'answer': None})
                    note = ''
                    continue
                charged = answer.cost_usd if (answer.input_tokens or answer.output_tokens) else worst   # a reply without usage keeps its reservation (round 6)
                spent += charged
                errors = judging.check_answer(r['conn'], data_center, answer.data, r['user'])
                attempts.append({'attempt': attempt, 'errors': errors, 'cost': answer.cost_usd, 'answer': answer.data,
                                 'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens})
                if not errors:
                    break
                note = judging.retry_note(errors)
            row = {'draw': draw, 'arm': arm, 'sample': sample, 'view_id': data_center, 'attempts': attempts}
            rows.append(row)
            with open(out_dir / 'answers.jsonl', 'a', encoding='utf-8') as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')
            final = attempts[-1]['answer'] or {}
            print(f'{draw} {arm} {sample}: rung {final.get("rung")} refused {bool(attempts[-1]["errors"])} spent ${spent:.4f}', flush=True)
    print(f'total spent ${spent:.4f}')


if __name__ == '__main__':
    mode, scratch = sys.argv[1], Path(sys.argv[2])
    scratch.mkdir(parents=True, exist_ok=True)
    if mode == 'check':
        sys.exit(0 if check(scratch) else 1)
    send(scratch, Path(sys.argv[3]))
