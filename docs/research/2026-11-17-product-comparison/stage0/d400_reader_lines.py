"""D400's reader lines 1–5 on each new-system draw (DESIGN-1.6.md §1, "Reader lines 1–5"; RUN-PLAN-v12.md §1.6, row "D400 accounting").

Stage A's reading, run per draw with Stage A's own tools unchanged:
- `clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py`, its second form with one run, writes the packets and the key;
- every packet is read by two closed sessions, one per family (`census/census_readers.run`), with the form
  `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md` and the packet inline, since a closed session opens no file; the words are
  those of `stage-a-reader-handoff-template.md`, with the file paths replaced by the material;
- `collect_readings.py disputes` writes the third readers' packets; each is read by two third readers, one per family, with
  `stage-a-third-reader-brief.md`, the form and the packet inline (the words of `stage-a-third-reader-handoff-template.md`);
- `collect_readings.py report` gives the lines.

Line 5 is recomputed from the report's counts with D452's scaling (`clean-arch/e2e-comparison-2026-11-13/READING-PLAN.md` §2, "Line 5, a
council-set diagnostic line"): "right ≥ ceil(35·N/44) and right by a ladder ≥ ceil(28·N/44) for the N fresh theses. Alex's D400 wording
(35 and 28 of 44) is printed beside it with the actual N and the result; it is not reported as Alex's line. N = 0 reads NOT MEASURED
(zero thresholds would pass vacuously)." `accounting.py` hard-codes 35 and 28, so its own line-5 verdict is never read. The reader lines are
printed beside the verdict (verdict-rule.json `printed_beside`); they clear or block no release.

    python3 d400_reader_lines.py packets <run root> <eligibility.json> <out> [--keys <folder>]
    python3 d400_reader_lines.py read <out>
    python3 d400_reader_lines.py third <out>
    python3 d400_reader_lines.py report <out>

`packets` reads each draw's ladder and cases folders from its `run.json` (`components[...]['folder']`, a redo's folder after a redo). A
ladder component not completed (skipped: the draw opened no question) is not measured. Every file is read only through
`eligibility.verified` and its bytes are checked against the fingerprint; one refusal stops the command before anything is written. Each
draw with a completed ladder gets a reading folder `<out>/<draw>/`, the folder `collect_readings.py` reads: byte copies of `send-1..3/outcomes.jsonl` and
of `cases.json`, then `readers/`, `readers-answers/`, `third-reader/`, `stage-a-report.json` and `report.txt`. Sessions' raw answers and
`launches.jsonl` sit in `<out>/<draw>/attempts/`. The key from item number to case and pass is written to `<keys>/<out name>/<draw>.json`
(default `~/.hivemind-keys/comparison-2026-11-17/`), outside `<out>` and outside the repository; `<out>/reading.json` records where.

A session is void when `census_readers.run` voids it (a closed-session breach, or no answer within its 3600 s), or when the collector
would read its answer otherwise than as a complete one (`rows_problem`, `rulings_problem`): a line it would not read, an item or point
given twice or outside the packet, or an item without a valid row (Stage A's own rule, `accounting.row_problem`) or a point without a
valid ruling. A void session is retried once; a still-void one writes no answer file and is reported missing, recorded by a marker
beside its answer file (`<answer>.missing`, which no glob of the collector reads). Exhaustion is terminal: `read` and `third` skip a
session whose answer file or marker exists. A draw with any session missing (reported missing, or not run yet) has every reader line
1–5 not measured, and the collector's lines are not read for it. There is no ask-again round (Stage A's item-by-item `-again-<k>` step):
the council left it out, since the reader lines are printed beside the verdict only.
"""
import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE_A = ROOT / 'clean-arch' / 'step4-2026-11-10' / 'stage_a'
LADDER = ROOT / 'clean-arch' / 'step4-2026-11-10' / 'ladder'
sys.path[:0] = [str(STAGE_A), str(HERE), str(HERE / 'census'), str(ROOT / 'src')]
import accounting  # noqa: E402
import census_readers  # noqa: E402
import collect_readings  # noqa: E402
import eligibility as eligibility_tool  # noqa: E402
from hivemind import universe  # noqa: E402

BUILD_READER_PACKETS = STAGE_A / 'build_reader_packets.py'
COLLECT_READINGS = STAGE_A / 'collect_readings.py'
READER_BRIEF = LADDER / 'stage-a-reader-brief.md'
THIRD_READER_BRIEF = LADDER / 'stage-a-third-reader-brief.md'
UNIVERSE = ROOT / 'poc' / 'universe.json'
DEFAULT_KEYS = Path.home() / '.hivemind-keys' / 'comparison-2026-11-17'
NEW_DRAWS = ('new-1', 'new-2', 'new-3')
PASSES = (1, 2, 3)
FAMILIES = census_readers.FAMILIES
SESSIONS_AT_ONCE = 6
D400_THESES, D400_RIGHT, D400_RIGHT_BY_A_LADDER = 44, 35, 28
D400_LIMIT = ('D400\'s limit: Stage A measures the step against the lines and its own three sends; it does not establish that the step '
              'writes better ladders than production, nor any comparison with production.')
TWO_COUNTINGS = ('every unresolved point counted for the answer', 'every unresolved point counted against it')
NO_ASK_AGAIN = ('not measured for a missing session: there is no ask-again round, by the council\'s choice (round 8), since the reader '
                'lines are printed beside the verdict only')
LOG_LOCK = threading.Lock()

READER_PROMPT = """Follow the brief below exactly. It is your whole task.
The packet it speaks of is given after the brief ({count} items). The company in every item is NVIDIA (ticker NVDA); each
item carries its fiscal-year note. The listed themes are: {themes}.

You are read-only: do not edit files, run model calls or start runs. You have no files and no tools: the brief and the packet below are
your whole material.

You cannot write files: return your answer as your final message, exactly {count} lines, one JSON object per line, in item order, each
with the `item` number the packet gives and the fields the brief lists, and nothing else: no prose before or after, no code fence.

## The brief

{brief}

## The packet

{packet}"""

THIRD_READER_PROMPT = """Follow the third reader's brief below exactly; it sends you to the form, which is given in full after it and which you
read first. It is your whole task. The packet is given last ({items} items, {points} points to rule on). The company in every item is NVIDIA
(ticker NVDA); each item carries its fiscal-year note. The listed themes are: {themes}.

You are read-only: do not edit files, run model calls or start runs. You have no files and no tools: the two briefs and the packet below
are your whole material.

You cannot write files: return your answer as your final message, exactly {points} lines, one JSON object per line, in the order
the packet gives the points, and nothing else: no prose before or after, no code fence.

## The third reader's brief

{third_brief}

## The form

{brief}

## The packet

{packet}"""


def sha256_of_bytes(data):
    return hashlib.sha256(data).hexdigest()


def scaled_line_5(right, right_by_a_ladder, theses):
    """Line 5 under D452's scaling: (verdict, details). Met when right >= ceil(35N/44) and right by a ladder >= ceil(28N/44); N = 0 is
    NOT MEASURED, since zero minimums would pass vacuously."""
    details = {'right': right, 'right by a ladder': right_by_a_ladder, 'of': theses}
    if theses == 0:
        return accounting.NOT_MEASURED, {**details, 'reason': 'no thesis (N = 0): zero minimums would pass vacuously (D452)'}
    minimum_right = -(-D400_RIGHT * theses // D400_THESES)
    minimum_right_by_a_ladder = -(-D400_RIGHT_BY_A_LADDER * theses // D400_THESES)
    met = right >= minimum_right and right_by_a_ladder >= minimum_right_by_a_ladder
    return ('met' if met else 'missed'), {**details, 'minimum right': minimum_right, 'minimum right by a ladder': minimum_right_by_a_ladder}


def line_5_of(stored_line):
    """The scaled line 5 from the accounting's stored line 5: its counts are read, its own verdict (35/28 hard-coded) is not."""
    if isinstance(stored_line, str):
        return accounting.NOT_MEASURED, {'reason': f'the accounting reads {stored_line!r}'}
    counts = stored_line[1]
    return scaled_line_5(counts['right'], counts['right by a ladder'], counts['of'])


def verdict_under_both(verdicts):
    """One line under the two countings, as `collect_readings.py report` prints it: met only when met under both, missed when missed
    under both, else it depends on the unresolved points."""
    distinct = sorted(set(verdicts))
    return distinct[0] if len(distinct) == 1 else 'depends on the unresolved points: ' + ' / '.join(distinct)


def theme_list_text():
    research_list = universe.load(str(UNIVERSE))
    return ', '.join(f'{theme_id} ({name})' for theme_id, name in research_list.theme_list())


class LookupCountingKey(dict):
    """The key from item number to send, counting every item the collector finds in it, so that two rows for one item are seen."""

    def __init__(self, key):
        super().__init__(key)
        self.found = collections.Counter()

    def __getitem__(self, item):
        send = super().__getitem__(item)
        self.found[item] += 1
        return send


def rows_problem(answer, family, packet_sends, key, outcomes):
    """Why a reader's answer to a packet is void, or None. The answer is read by the collector's own `collect_readings.rows_of`, so the
    wrapper accepts only what the collector keeps: every line it reads is read as a row (an item written `1.0` is not), each item has
    one row, no row names a send outside the packet (the collector merges a family's files by item), and every send of the packet has a
    valid row (accounting.row_problem). `packet_sends` is {item: (case, pass)}; `outcomes` is {(case, pass): outcome}."""
    counting_key = LookupCountingKey(key)
    with tempfile.TemporaryDirectory(prefix='d400-reader-answer-') as folder:
        (Path(folder) / 'readers-answers').mkdir()
        (Path(folder) / 'readers-answers' / f'reader-{family}-packet-1.jsonl').write_text(answer)
        rows, unreadable = collect_readings.rows_of(folder, counting_key, family)
    if unreadable:
        return f'{len(unreadable)} lines the collector would not read as a row: ' + '; '.join(
            f'line {number}: {text}' for _, number, text in unreadable[:5])
    repeated = sorted(item for item, count in counting_key.found.items() if count > 1)
    if repeated:
        return f'more than one row for items {repeated[:10]}'
    outside = sorted(set(rows) - set(packet_sends.values()))
    if outside:
        return f'rows for sends outside the packet: {outside[:10]}'
    problems = [(item, accounting.row_problem(rows.get(send), outcomes[send])) for item, send in packet_sends.items()]
    problems = [(item, problem) for item, problem in problems if problem]
    if problems:
        return f'{len(problems)} items without a valid row: ' + '; '.join(f'item {item}: {problem}' for item, problem in problems[:5])
    return None


def rulings_problem(answer, mark_of_point):
    """Why a third reader's answer to a ruling packet is void, or None. Each line is read as `collect_readings.read_rulings` reads a
    rulings file (collect_readings.py:166-175: blank lines and code fences skipped, a line kept by its `id`); a line it would skip, a point
    ruled twice, a point outside the packet, or a point without a ruling of the form (`holds` or `fails` on a mark, `upheld` true or false
    on a fault named under W, as `read_rulings` takes them) makes the answer void."""
    rulings, unreadable, repeated = {}, [], []
    for line in answer.splitlines():
        line = line.strip()
        if not line or line.startswith('```'):
            continue
        try:
            ruling = json.loads(line)
            point = ruling['id']
            if point in rulings:
                repeated.append(point)
            rulings[point] = ruling
        except (ValueError, KeyError, TypeError):
            unreadable.append(line[:80])
    if unreadable:
        return f'{len(unreadable)} lines the collector would not read as a ruling: {unreadable[:5]}'
    if repeated:
        return f'more than one ruling for points {repeated[:10]}'
    outside = sorted(str(point) for point in set(rulings) - set(mark_of_point))
    if outside:
        return f'rulings for points outside the packet: {outside[:10]}'
    missing = [point for point, mark in mark_of_point.items()
               if not (rulings.get(point, {}).get('upheld') in (True, False) if mark == 'W'
                       else rulings.get(point, {}).get('ruling') in accounting.VERDICTS)]
    if missing:
        return f'{len(missing)} points without a valid ruling: {missing[:10]}'
    return None


def session(draw_folder, name, family, prompt, problem_of):
    """One closed session, retried once when void. Every attempt's raw answer and outcome are logged in `attempts/`. Returns (answer, None)
    or (None, the last void reason)."""
    attempts_folder = draw_folder / 'attempts'
    void = None
    for attempt in (1, 2):
        answer, void = census_readers.run(family, prompt)
        if answer is not None and void is None:
            void = problem_of(answer)
        with LOG_LOCK:
            attempts_folder.mkdir(exist_ok=True)
            if answer is not None:
                (attempts_folder / f'{name}-attempt-{attempt}.txt').write_text(answer)
            with open(attempts_folder / 'launches.jsonl', 'a') as log:
                log.write(json.dumps({'session': name, 'family': family, 'attempt': attempt, 'void': void,
                                      'prompt sha256': sha256_of_bytes(prompt.encode()),
                                      'at': datetime.datetime.now().isoformat(timespec='seconds')}) + '\n')
        if void is None:
            return answer, None
    return None, void


def load_manifest(out):
    path = Path(out) / 'reading.json'
    if not path.exists():
        raise SystemExit(f'refused: {path} missing; run `packets` first')
    return json.loads(path.read_text())


def draws_to_read(out, manifest):
    """The draws with a reading folder, each copy checked against the fingerprint it was copied under."""
    for draw, entry in manifest['draws'].items():
        if entry['status'] != 'read':
            continue
        folder = Path(out) / draw
        for copy_name, source in entry['inputs'].items():
            if sha256_of_bytes((folder / copy_name).read_bytes()) != source['sha256']:
                raise SystemExit(f'refused: {draw}/{copy_name} changed since it was copied from {source["path"]}')
        yield draw, folder, Path(entry['key'])


def number_of(packet_file):
    return int(packet_file.stem.rsplit('-', 1)[1])


def run_stage_a_tool(arguments, cwd):
    return subprocess.run([sys.executable, *map(str, arguments)], capture_output=True, text=True, cwd=str(cwd))


def verified_bytes(eligibility, run_root, draw, relative):
    """A file's bytes, read only through eligibility.verified and checked again on the bytes read."""
    data = eligibility_tool.verified(eligibility, run_root, draw, relative).read_bytes()
    if sha256_of_bytes(data) != eligibility['draws'][draw]['inputs'][relative]:
        raise SystemExit(f'refused: {draw}/{relative} changed while it was read')
    return data


def build_packets(run_root, eligibility, out, keys_folder=DEFAULT_KEYS):
    """Every new draw's reading folder, packets and key; returns the manifest written to `<out>/reading.json`."""
    run_root, out = Path(run_root).resolve(), Path(out).resolve()
    keys_folder = Path(keys_folder).expanduser().resolve()
    if out.exists():
        raise SystemExit(f'refused: {out} exists')
    if keys_folder.is_relative_to(out) or keys_folder.is_relative_to(ROOT):
        raise SystemExit(f'refused: the keys folder {keys_folder} must lie outside {out} and outside the repository')
    plans = {}
    for draw in NEW_DRAWS:                                     # every file is checked before anything is written
        record = json.loads((run_root / draw / 'run.json').read_text())
        ladder = record['components'].get('ladder', {})
        if ladder.get('state') != 'completed':
            plans[draw] = {'status': f"not measured: the ladder component is {ladder.get('state')!r}"}
            continue
        cases_folder = record['components'].get('cases', {}).get('folder')
        sources = {f'send-{number}/outcomes.jsonl': f"{ladder['folder']}/send-{number}/outcomes.jsonl" for number in PASSES}
        sources['cases.json'] = f'{cases_folder}/cases.json'
        copies = {copy_name: verified_bytes(eligibility, run_root, draw, relative) for copy_name, relative in sources.items()}
        key_path = keys_folder / out.name / f'{draw}.json'
        if key_path.exists():
            raise SystemExit(f'refused: {key_path} exists; a key is never overwritten')
        plans[draw] = {'status': 'read', 'copies': copies, 'key': key_path,
                       'inputs': {copy_name: {'path': f'{draw}/{relative}', 'sha256': sha256_of_bytes(copies[copy_name])}
                                  for copy_name, relative in sources.items()}}
    out.mkdir(parents=True)
    manifest = {'run root': str(run_root), 'eligible': eligibility.get('eligible'), 'eligibility problems': eligibility.get('problems'),
                'briefs': {str(path.relative_to(ROOT)): sha256_of_bytes(path.read_bytes()) for path in (READER_BRIEF, THIRD_READER_BRIEF)},
                'draws': {}}
    for draw, plan in plans.items():
        if plan['status'] != 'read':
            manifest['draws'][draw] = {'status': plan['status']}
            print(f'{draw}: {plan["status"]}')
            continue
        folder = out / draw
        for copy_name, data in plan['copies'].items():
            (folder / copy_name).parent.mkdir(parents=True, exist_ok=True)
            (folder / copy_name).write_bytes(data)
        plan['key'].parent.mkdir(parents=True, exist_ok=True)
        built = run_stage_a_tool([BUILD_READER_PACKETS, plan['key'], '--run', f'{folder}={folder / "cases.json"}',
                                  '--readers', folder / 'readers'], cwd=out)
        if built.returncode != 0:
            raise SystemExit(f'{draw}: build_reader_packets.py failed: {built.stderr.strip() or built.stdout.strip()}')
        packets = len(list((folder / 'readers').glob('packet-*.json')))
        manifest['draws'][draw] = {'status': 'read', 'inputs': plan['inputs'], 'key': str(plan['key']), 'packets': packets}
        print(f'{draw}: {built.stdout.strip()}')
    (out / 'reading.json').write_text(json.dumps(manifest, indent=1) + '\n')
    return manifest


def read_packets(out):
    """Every packet of every draw with a reading folder read by one closed session of each family; returns [(draw, session, void or None)]."""
    out = Path(out)
    manifest = load_manifest(out)
    brief, themes = READER_BRIEF.read_text(), theme_list_text()
    jobs, exhausted = [], []
    for draw, folder, key_path in draws_to_read(out, manifest):
        key = json.loads(key_path.read_text())
        outcomes = {(outcome['case'], outcome['pass']): outcome for outcome in collect_readings.outcomes_of(folder)}
        (folder / 'readers-answers').mkdir(exist_ok=True)
        for packet_file in sorted((folder / 'readers').glob('packet-*.json'), key=number_of):
            packet_text = packet_file.read_text()
            packet_sends = {item['item']: tuple(key[str(item['item'])]) for item in json.loads(packet_text)}
            prompt = READER_PROMPT.format(count=len(packet_sends), themes=themes, brief=brief, packet=packet_text)
            for family in FAMILIES:
                answer_file = folder / 'readers-answers' / f'reader-{family}-packet-{number_of(packet_file)}.jsonl'
                if still_to_run(answer_file):
                    jobs.append((draw, folder, answer_file, family, prompt,
                                 lambda answer, family=family, packet_sends=packet_sends, key=key, outcomes=outcomes:
                                 rows_problem(answer, family, packet_sends, key, outcomes)))
                elif missing_marker(answer_file).exists():
                    exhausted.append(f'{draw} {answer_file.stem}')
    return run_sessions(jobs, exhausted)


def read_disputes(out):
    """Every ruling packet `collect_readings.py disputes` writes, read by one third reader of each family; returns [(draw, session, void
    or None)]. A draw whose rows are missing or not valid gets no ruling packet: `disputes` refuses it, and the refusal is printed."""
    out = Path(out)
    manifest = load_manifest(out)
    brief, third_brief, themes = READER_BRIEF.read_text(), THIRD_READER_BRIEF.read_text(), theme_list_text()
    jobs, exhausted = [], []
    for draw, folder, key_path in draws_to_read(out, manifest):
        if not (folder / 'third-reader').exists():
            disputes = run_stage_a_tool([COLLECT_READINGS, 'disputes', folder, key_path], cwd=out)
            print(f"{draw}: {disputes.stdout.strip() if disputes.returncode == 0 else 'disputes refused: ' + disputes.stderr.strip()}")
            if disputes.returncode != 0:
                continue
        for packet_file in sorted((folder / 'third-reader').glob('ruling-packet-*.json'), key=number_of):
            packet_text = packet_file.read_text()
            packet = json.loads(packet_text)
            mark_of_point = {point['id']: point['mark'] for entry in packet for point in entry['to_rule']}
            prompt = THIRD_READER_PROMPT.format(items=len(packet), points=len(mark_of_point), themes=themes, third_brief=third_brief,
                                                brief=brief, packet=packet_text)
            for family in FAMILIES:
                answer_file = folder / 'third-reader' / f'rulings-{family}-{number_of(packet_file)}.jsonl'
                if still_to_run(answer_file):
                    jobs.append((draw, folder, answer_file, family, prompt,
                                 lambda answer, mark_of_point=mark_of_point: rulings_problem(answer, mark_of_point)))
                elif missing_marker(answer_file).exists():
                    exhausted.append(f'{draw} {answer_file.stem}')
    return run_sessions(jobs, exhausted)


def missing_marker(answer_file):
    """Where a session reported missing is recorded: beside its answer file, named so that no glob of the collector reads it."""
    return answer_file.with_suffix('.missing')


def still_to_run(answer_file):
    """A session runs only when it has neither an answer nor a record that it was reported missing: exhaustion is terminal."""
    return not answer_file.exists() and not missing_marker(answer_file).exists()


def run_sessions(jobs, exhausted):
    def one(job):
        draw, folder, answer_file, family, prompt, problem_of = job
        answer, void = session(folder, answer_file.stem, family, prompt, problem_of)
        if answer is not None:
            answer_file.write_text(answer)
        else:
            missing_marker(answer_file).write_text(json.dumps({'void after two attempts': void}) + '\n')
        return draw, answer_file.stem, void
    print(f'{len(jobs)} sessions to run; {len(exhausted)} reported missing earlier, not run again: {exhausted}', flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=SESSIONS_AT_ONCE) as pool:
        for draw, name, void in pool.map(one, jobs):
            print(f'{draw} {name}: {"VOID after two attempts, reported missing: " + void if void else "answered"}', flush=True)
            results.append((draw, name, void))
    return results


def missing_sessions(folder):
    """The answer files `collect_readings.py` expects and does not find, each with why: reported missing (with its last void), or not
    run yet."""
    expected = [folder / 'readers-answers' / f'reader-{family}-packet-{number_of(packet_file)}.jsonl'
                for packet_file in sorted((folder / 'readers').glob('packet-*.json'), key=number_of) for family in FAMILIES]
    expected += [folder / 'third-reader' / f'rulings-{family}-{number_of(packet_file)}.jsonl'
                 for packet_file in sorted((folder / 'third-reader').glob('ruling-packet-*.json'), key=number_of) for family in FAMILIES]
    missing = []
    for answer_file in expected:
        if answer_file.exists():
            continue
        marker = missing_marker(answer_file)
        why = (f"reported missing: {json.loads(marker.read_text())['void after two attempts']}" if marker.exists() else 'not run yet')
        missing.append(f'{answer_file.stem} ({why})')
    return missing


def report(out):
    """`collect_readings.py report` on every draw with a reading folder and no session missing, with line 5 recomputed under D452's
    scaling; a draw with a session missing has lines 1–5 not measured and the no-ask-again note. Written to `<out>/d400-reader-lines.json`
    and printed."""
    out = Path(out)
    manifest = load_manifest(out)
    result = {'eligible': manifest['eligible'], 'draws': {}}
    to_read = {draw: (folder, key_path) for draw, folder, key_path in draws_to_read(out, manifest)}
    for draw, entry in manifest['draws'].items():
        if draw not in to_read:
            result['draws'][draw] = {'status': entry['status'], **{f'line {number}': accounting.NOT_MEASURED for number in (1, 2, 3, 4, 5)}}
            continue
        folder, key_path = to_read[draw]
        stored_path = folder / 'stage-a-report.json'
        for earlier in (stored_path, folder / 'report.txt'):    # an earlier report must not be read as this one
            earlier.unlink(missing_ok=True)
        missing = missing_sessions(folder)
        if missing:                                             # none of the collector's lines is kept for this draw
            result['draws'][draw] = {'status': 'not measured: a session is missing', 'missing sessions': missing, 'note': NO_ASK_AGAIN,
                                     **{f'line {number}': accounting.NOT_MEASURED for number in (1, 2, 3, 4, 5)}}
            continue
        collected = run_stage_a_tool([COLLECT_READINGS, 'report', folder, key_path], cwd=out)
        (folder / 'report.txt').write_text(collected.stdout + (f'\n[exit {collected.returncode}] {collected.stderr}' if collected.returncode else ''))
        if collected.returncode != 0:
            reason = collected.stderr.strip().splitlines()[-1] if collected.stderr.strip() else f'exit {collected.returncode}'
            result['draws'][draw] = {'status': f'not measured: collect_readings.py report refused: {reason}',
                                     **{f'line {number}': accounting.NOT_MEASURED for number in (1, 2, 3, 4, 5)}}
            continue
        stored = json.loads(stored_path.read_text())
        countings = {'one counting (no rulings of two third readers)': stored} if 'lines' in stored else {label: stored[label] for label in TWO_COUNTINGS}
        entry_out = {'status': 'read',
                     'reading': {label: counting['reading'] for label, counting in countings.items()},
                     'dispute share': next(iter(countings.values()))['dispute share'],
                     'unresolved points': len(stored.get('unresolved', []))}
        for number in ('1', '2', '3', '4'):
            entry_out[f'line {number}'] = verdict_under_both(
                [line if isinstance(line, str) else line[0] for line in (counting['lines'][number] for counting in countings.values())])
        line_5 = {label: line_5_of(counting['lines']['5']) for label, counting in countings.items()}
        entry_out['line 5'] = verdict_under_both([verdict for verdict, _ in line_5.values()])
        entry_out['line 5 by counting'] = {label: {'verdict': verdict, **details} for label, (verdict, details) in line_5.items()}
        result['draws'][draw] = entry_out
    (out / 'd400-reader-lines.json').write_text(json.dumps(result, indent=1, ensure_ascii=False) + '\n')
    print_report(result)
    return result


def print_report(result):
    print('D400 reader lines 1–5, per new draw (printed beside the verdict; they clear or block no release)')
    print('eligibility:', {True: 'the draws are eligible', False: 'the draws are NOT eligible: a diagnostic only'}.get(result['eligible'], 'not stated'))
    names = {'1': 'no ladder fails Q', '2': 'no ladder fails L', '3': 'no ladder fails R', '4': 'no refusal fails N'}
    for draw, entry in result['draws'].items():
        print(f'== {draw}: {entry["status"]}')
        if entry['status'] == 'read':
            print(f"   reading: {entry['reading']}; dispute share {entry['dispute share']}; unresolved points {entry['unresolved points']}")
        if entry.get('missing sessions'):
            print(f"   sessions missing: {entry['missing sessions']}")
        if entry.get('note'):
            print(f"   {entry['note']}")
        for number, name in names.items():
            print(f'   line {number} ({name}): {entry[f"line {number}"]}')
        print(f"   line 5 (council-set diagnostic line, D452; never Alex's line): {entry['line 5']}")
        for label, details in entry.get('line 5 by counting', {}).items():
            minimums = (f"; minimums ceil(35N/44) = {details['minimum right']} and ceil(28N/44) = {details['minimum right by a ladder']}"
                        if 'minimum right' in details else f"; {details.get('reason', '')}")
            counts = (f"right {details['right']}, right by a ladder {details['right by a ladder']}, of N = {details['of']}"
                      if 'of' in details else 'no counts')
            print(f"      {label}: {counts}{minimums} -> {details['verdict']}")
        theses = next((details['of'] for details in entry.get('line 5 by counting', {}).values() if 'of' in details), 'not counted')
        print(f'      beside: D400\'s wording, at least {D400_RIGHT} right and {D400_RIGHT_BY_A_LADDER} right by a ladder of '
              f'{D400_THESES} theses; this draw has N = {theses}')
    print(D400_LIMIT)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    commands = parser.add_subparsers(dest='command', required=True)
    packets = commands.add_parser('packets')
    packets.add_argument('run_root')
    packets.add_argument('eligibility')
    packets.add_argument('out')
    packets.add_argument('--keys', default=str(DEFAULT_KEYS))
    for name in ('read', 'third', 'report'):
        commands.add_parser(name).add_argument('out')
    arguments = parser.parse_args(argv)
    if arguments.command == 'packets':
        build_packets(arguments.run_root, json.loads(Path(arguments.eligibility).read_text()), arguments.out, arguments.keys)
    elif arguments.command == 'read':
        read_packets(arguments.out)
        for draw, folder, key_path in draws_to_read(Path(arguments.out), load_manifest(arguments.out)):
            rows = run_stage_a_tool([COLLECT_READINGS, 'rows', folder, key_path], cwd=arguments.out)
            print(f'{draw}, collect_readings.py rows:\n{rows.stdout.rstrip()}')
    elif arguments.command == 'third':
        read_disputes(arguments.out)
    else:
        report(arguments.out)


if __name__ == '__main__':
    main()
