"""The identity probe (D463): the reviewed c14 probe (`clean-arch/step1-diagnosis-2026-11-12/probe_c14.py`) unchanged except two things: the
ledger is a module-level class, and a response whose usage is missing, malformed or prices at zero settles at its reservation (council round
15; `test_probe_identity.py` proves it). Original description follows.

The small first test of Step 1 candidate c14 against c8 (D433; `DIAGNOSIS.md`, "The first test"): stored c8 requests re-sent as
production sent them, the c8 arm unchanged and the c14 arm with only its system text and closing check replaced; several sends each.

Production adapts the built request before sending (`clean-arch/step1/live.py`, `deepseek_json_mode`: the schema appended to the
system text, JSON-object mode, reasoning effort) and keeps the adapted request as `sent_request` in the stored response. Both arms
are adapted by that same function. Before anything is sent, the c8 arm's adapted request must equal the stored `sent_request`
exactly, and every stored request must carry c8's system text and closing check exactly, or the run refuses. The c14 arm is the
built request with messages[0] replaced by `arms/c14-system.txt` and the closing check at the end of messages[1] replaced by
`arms/c14-closing.txt`, then adapted the same way. Answers are handled as the runner handles them (`runner.py`, the live path): a
refusal or an unfinished answer is recorded and not resent; an answer cut at the output limit, malformed JSON, or an answer that
fails the schema check (`model.check_schema`) is a format failure and is sent once more, as the runner's format rule does; an
answer that passes the schema and fails the runner's own checks (`runner.validate`) is recorded and not resent; every response
is written to `responses.jsonl` the moment it arrives, before it is processed or resent, and each finished record to
`records.jsonl`; new theses with no kept evidence are dropped, as the runner drops them. Each attempt goes out once over the network,
as production's live transport sends it (`max_attempts=1`). A send needs `--max-usd`: each attempt reserves production's own upper
estimate (`live.py`: input at twice the request's bytes plus 4,096 tokens, and the whole output cap, at published rates); an attempt
waits while reservations in flight would pass the ceiling, and is not sent (recorded so) when the spend so far plus its own reservation
would pass it. A response settles at its usage; one with no usage, or usage that is not a pair of whole token counts, settles at its
reservation. A response whose usage costs more than its reservation stops the run: every later attempt is recorded as not sent.
With `--network-resends N`, a send that got no answer from the service is sent again, up to N more times, as `model.openai_transport`'s
default retries such failures: a `model.TransportError` with no HTTP status (a dropped, refused or truncated connection, a timeout) or
with status 429 or 5xx. A client HTTP error (400, 401, 403, 404) or a malformed or non-object response is an unusable answer and is not
sent again. Every attempt's reservation is settled whatever happens. An answer, once received, is sent again only for a format failure.

  python3 clean-arch/step1-diagnosis-2026-11-12/probe_c14.py <cases.json> <output folder> --cases capex-open --sends 3 [--send]
"""
import argparse
import concurrent.futures
import copy
import threading
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARMS = ROOT / 'clean-arch/step1-unfiled-2026-11-08/arms'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
from hivemind import model  # noqa: E402
import live  # noqa: E402
import runner  # noqa: E402

REASONING_EFFORT = 'high'          # the stored runs' setting (settings.json), sent by production's adapter


def arm_text(arm):
    return (ARMS / f'{arm}-system.txt').read_text(encoding='utf-8'), (ARMS / f'{arm}-closing.txt').read_text(encoding='utf-8')


def arm_schema(arm):
    return json.loads((ARMS / f'{arm}-schema.json').read_text(encoding='utf-8'))


def build(case, arm):
    """(request as sent, payload): production's adaptation of the stored built request (c8), or of it with the two texts replaced (c14).
    The c8 arm must equal the stored sent_request exactly."""
    conn = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
    stored_text, raw = conn.execute("select request, raw_response from trace where sequence = ? and status = 'complete'", (case['sequence'],)).fetchone()
    stored = json.loads(stored_text)
    sent = json.loads(raw).get('sent_request')
    adapted_c8 = live.deepseek_json_mode(stored, REASONING_EFFORT)
    if sent is None or adapted_c8 != sent or json.dumps(adapted_c8) != json.dumps(sent):
        raise SystemExit(f"{case['case']}: production's adapter does not rebuild the stored sent request")
    c8_system, c8_closing = arm_text('c8')
    user = stored['messages'][1]['content']
    if stored['messages'][0]['content'] != c8_system or not user.endswith('\n\n' + c8_closing):
        raise SystemExit(f"{case['case']}: the stored request does not carry c8's system text and closing check exactly")
    payload, _ = json.JSONDecoder().raw_decode(user)
    if arm == 'c8':
        return adapted_c8, payload
    if stored['response_format']['json_schema']['schema'] != arm_schema('c8'):
        raise SystemExit(f"{case['case']}: the stored request does not carry c8's schema exactly")
    system, closing = arm_text(arm)
    request = copy.deepcopy(stored)
    request['messages'][0]['content'] = system
    request['messages'][1]['content'] = user[: len(user) - len(c8_closing)] + closing
    request['response_format']['json_schema']['schema'] = arm_schema(arm)     # an arm may change a field's description
    return live.deepseek_json_mode(request, REASONING_EFFORT), payload


def is_network_loss(error):
    """True when the service gave no answer: a transport failure with no HTTP status, or a 429 or 5xx status."""
    if not isinstance(error, model.TransportError):
        return False
    status = getattr(error, 'http_status', None)
    return status is None or status == 429 or status >= 500


def capex_theses(new_theses):
    """The new theses on hyperscalers' combined data-centre capital spending, with the calendar years each names."""
    out = []
    for thesis in new_theses or []:
        text = ' '.join(str(thesis.get(key) or '') for key in ('description', 'outcome', 'period')).lower()
        if 'capital expenditure' in text or 'capex' in text or 'capital-expenditure' in text:
            out.append({'description': thesis.get('description'), 'years': sorted({year for year in ('2026', '2027', '2028') if year in text})})
    return out


class Ledger:
    """One run's spending ledger: reserve an upper estimate before an attempt, settle it at its usage. Usage that is missing, not a pair of
    whole nonnegative token counts, or that prices at zero settles at the reservation; a settlement above its reservation stops the run."""

    def __init__(self, ceiling, price_in, price_out):
        self.ceiling, self.price_in, self.price_out = ceiling, price_in, price_out
        self.spent = self.reserved = 0.0
        self.overrun = False
        self.changed = threading.Condition()

    def estimate(self, request):
        return ((2 * len(json.dumps(request).encode('utf-8')) + 4096) * self.price_in + request['max_tokens'] * self.price_out) / 1e6

    def reserve(self, request, wait=True):
        amount = self.estimate(request)
        with self.changed:
            while self.spent + self.reserved + amount > self.ceiling or self.overrun:
                if self.overrun or self.spent + amount > self.ceiling or not wait:
                    return None
                self.changed.wait()
            self.reserved += amount
        return amount

    def cost_of(self, usage):
        if isinstance(usage, dict):
            counts = (usage.get('prompt_tokens'), usage.get('completion_tokens'))
            if all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in counts):
                return (counts[0] * self.price_in + counts[1] * self.price_out) / 1e6
        return None

    def settle(self, amount, usage):
        cost = self.cost_of(usage)
        if cost is None or cost <= 0:
            cost = amount
        with self.changed:
            self.reserved -= amount
            self.spent += cost
            if cost > amount:
                self.overrun = True
            self.changed.notify_all()
        return cost


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cases')
    parser.add_argument('output')
    parser.add_argument('--cases', dest='names', required=True, help='comma-separated case kinds, e.g. capex-open')
    parser.add_argument('--arms', default='c8,c14')
    parser.add_argument('--sends', type=int, default=3)
    parser.add_argument('--send', action='store_true')
    parser.add_argument('--max-usd', type=float, help='spending ceiling for this run, required with --send')
    parser.add_argument('--network-resends', type=int, default=0, help='resends of a network failure before any answer arrives')
    parser.add_argument('--only', help='send only these jobs, as comma-separated case:arm:send (e.g. d3-memory:c15yc:17), keeping their numbers')
    args = parser.parse_args()
    if args.send and not (args.max_usd and args.max_usd > 0):
        raise SystemExit('--send needs a positive --max-usd')
    kinds = set(args.names.split(','))
    cases = [case for case in json.loads(Path(args.cases).read_text()) if case['case'].split('-', 1)[1] in kinds]
    wanted = None
    if args.only:
        wanted = {tuple(item.split(':')[:2]) + (int(item.split(':')[2]),) for item in args.only.split(',')}
    jobs = [(case, arm, send, *build(case, arm)) for case in cases for arm in args.arms.split(',') for send in range(1, args.sends + 1)
            if wanted is None or (case['case'], arm, send) in wanted]
    if wanted is not None and len(jobs) != len(wanted):
        raise SystemExit(f'--only names {len(wanted)} jobs but {len(jobs)} match the cases, arms and sends given')
    price_in, price_out = model.PRICES['deepseek-flash']
    chars = sum(len(json.dumps(job[3], ensure_ascii=False)) for job in jobs)
    print(f'{len(jobs)} requests over {len(cases)} stored states; every stored request carries c8 exactly; about {chars // 4} input tokens; '
          f'about ${(chars / 4 * price_in + len(jobs) * 9500 * price_out) / 1e6:.2f} at published rates (9,500 output tokens each, the stored mean)')
    if not args.send:
        return
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)

    schema_of = {arm: arm_schema(arm) for arm in args.arms.split(',')}

    lock = threading.Lock()
    ledger = Ledger(args.max_usd, price_in, price_out)
    reserve = ledger.reserve
    settle = ledger.settle

    def keep(name, row):
        with lock, (out / name).open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')

    def send(job):
        case, arm, number, request, payload = job
        record = {'case': case['case'], 'sequence': case['sequence'], 'arm': arm, 'send': number, 'attempts': []}
        network_resends_left = args.network_resends
        attempt = 0
        while attempt < 2:                     # the runner's format rule: a cut or malformed answer is sent once more
            attempt += 1
            entry = {}
            record['attempts'].append(entry)
            estimate = reserve(request)
            if estimate is None:
                entry['outcome'] = f'not sent: the ceiling of ${args.max_usd} would be passed'
                return record
            try:
                response = model.openai_transport('deepseek', request, max_attempts=1)
            except Exception as error:   # recorded with its reason
                settle(estimate, None)
                entry['error'] = f'{type(error).__name__}: {error}'
                entry['network_loss'] = is_network_loss(error)
                if entry['network_loss'] and network_resends_left > 0:
                    network_resends_left -= 1
                    attempt -= 1               # no answer arrived: the same attempt goes out again
                    continue
                return record
            settle(estimate, response.get('usage') if isinstance(response, dict) else None)
            if not isinstance(response, dict):
                entry['outcome'] = f'unusable: the response is a {type(response).__name__}, not an object'
                return record
            entry['response'] = response
            keep('responses.jsonl', {'case': case['case'], 'arm': arm, 'send': number, 'attempt': attempt, 'response': response})
            usage = response.get('usage') if isinstance(response.get('usage'), dict) else {}
            entry.update(input_tokens=usage.get('prompt_tokens'), output_tokens=usage.get('completion_tokens'))
            choice = response['choices'][0]
            if choice['message'].get('refusal'):
                entry['outcome'] = 'refused'
                return record
            if choice.get('finish_reason') == 'length':
                entry['outcome'] = 'cut at the output limit'
                continue
            if choice.get('finish_reason') != 'stop':
                entry['outcome'] = f"unfinished: {choice.get('finish_reason')}"
                return record
            try:
                answer = json.loads(choice['message']['content'])
            except ValueError as error:
                entry['outcome'] = f'format failure: malformed answer: {error}'
                continue
            errors = model.check_schema(answer, schema_of[arm])
            if errors:
                entry['outcome'] = 'format failure: ' + '; '.join(errors[:5])
                continue
            try:
                checked = runner.validate(answer, schema_of[arm], {'text': payload['source_item']['text']}, payload['open_theses'])
            except runner.ContractError as error:      # the runner records this and does not resend
                entry['outcome'] = f'refused by the runner checks: {error}'
                return record
            retained = [t for t in answer['new_theses'] if t['local_id'] not in checked['unlinked_new_thesis_ids']]
            entry['outcome'] = 'valid'
            record.update(new_theses=retained, dropped_unlinked=checked['unlinked_new_thesis_ids'], capex_theses=capex_theses(retained),
                          kept=len(checked['evidence']), unfiled=len(checked['unfiled_evidence']), links=checked['evidence'])
            return record
        return record
    def send_and_keep(job):
        try:
            record = send(job)
        except Exception as error:     # an error while processing an answer is recorded, never lost
            case, arm, number = job[0], job[1], job[2]
            record = {'case': case['case'], 'sequence': case['sequence'], 'arm': arm, 'send': number,
                      'attempts': [{'outcome': f'error while processing: {type(error).__name__}: {error}'}]}
        keep('records.jsonl', record)
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(send_and_keep, jobs))
    tokens_in = sum(entry.get('input_tokens') or 0 for record in records for entry in record['attempts'])
    tokens_out = sum(entry.get('output_tokens') or 0 for record in records for entry in record['attempts'])
    print(f"{len(records)} records; valid {sum('new_theses' in r for r in records)}; attempts {sum(len(r['attempts']) for r in records)}; "
          f"tokens {tokens_in} in, {tokens_out} out: ${(tokens_in * price_in + tokens_out * price_out) / 1e6:.2f} at published rates; "
          f"ledger spent ${ledger.spent:.2f} of the ${args.max_usd} ceiling")
    for arm in args.arms.split(','):
        both = sum(1 for r in records if r['arm'] == arm and {'2026', '2027'} <= {y for t in r.get('capex_theses') or [] for y in t['years']}
                   and len(r.get('capex_theses') or []) >= 2)
        print(f"{arm}: (a lead, read by hand) both years among two or more retained capex theses in {both} of {sum(1 for r in records if r['arm'] == arm)} sends")


if __name__ == '__main__':
    main()
