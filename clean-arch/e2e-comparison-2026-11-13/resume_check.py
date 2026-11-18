"""The no-cost recovery check of the three stopped production draws (council round ml-7): each draw's views, archive and day
manifests are copied to a scratch folder, and production's own replay (`hivemind.replay.run`, with the parallel day the draw used)
resumes the copy to 2026-07-14 through a fake transport: no network, no credential. The fake answers extraction with no evidence and
a judgement with that view's last archived judgement answer (a valid answer for its own ladder, citing evidence it was shown before),
and refuses any other request, so the resume path itself is exercised: the stopped day's remaining items in order, the later days,
day-end judging, the archive serving any request it already holds.

Checks per draw: (a) the copy completes every day to 2026-07-14; (b) no input gets a second handover; (c) dispatch sequence numbers
stay strictly increasing in input order across the resume; (d) every request the fake received was absent from the archive before the
resume (an archived request is served, not sent); (e) the item that failed is processed on the resume; (f) the fake received only
extraction and judgement requests, each judgement for exactly one known view.

  python3 resume_check.py <scratch folder> <draw folder> ...
"""
import json
import os
import shutil
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model, parallel_day, replay, universe  # noqa: E402

TESTDB = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
CONFIG = ROOT / 'poc/config/poc-v118.json'
EMPTY_EXTRACTION = {'evidence': [], 'candidates': [], 'new_groups': []}


class FakeTransport:
    def __init__(self, archived_keys, last_answer_by_question):
        self.archived_keys, self.sent, self.unexpected, self.repeated = archived_keys, [], [], 0
        self.last_answer_by_question = last_answer_by_question

    def __call__(self, *args):
        request = args[-1]
        _, key = model.request_identity(request)
        if key in self.archived_keys:
            self.repeated += 1
        if len(args) == 1:
            self.unexpected.append('jev')
            raise model.TransportError('fake: Jev not expected with no evidence')
        name = request['response_format']['json_schema']['name']
        self.sent.append(name)
        if name.startswith('extract'):
            content = json.dumps(EMPTY_EXTRACTION)
        elif name.startswith('judg'):
            user = request['messages'][-1]['content']
            hits = [answer for question, answer in self.last_answer_by_question.items() if question in user]
            if len(hits) != 1:
                self.unexpected.append(f'{name}: {len(hits)} archived answers match')
                raise model.TransportError('fake: no single archived judgement for this view')
            content = hits[0]
        else:
            self.unexpected.append(name)
            raise model.TransportError(f'fake: {name} not expected')
        return {'choices': [{'finish_reason': 'stop', 'message': {'content': content}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}


def check(scratch, draw):
    draw = Path(draw)
    copy = Path(scratch) / draw.name
    if copy.exists():
        shutil.rmtree(copy)
    copy.mkdir(parents=True)
    for name in ('views.sqlite', 'archive.sqlite'):
        shutil.copy(draw / name, copy / name)
    shutil.copytree(draw / 'manifests', copy / 'manifests')
    before = sqlite3.connect(copy / 'views.sqlite')
    days_before = [d for (d,) in before.execute('select day from days_completed order by day')]
    handovers_before = before.execute('select count(*) from handovers').fetchone()[0]
    before.close()
    failed_line = next((l for l in (draw / 'run.out').read_text().splitlines() if l.strip().startswith('! ')), '')
    failed_input = failed_line.strip()[2:].split(':', 2)[:2]
    failed_input = ':'.join(failed_input) if len(failed_input) == 2 else None
    archive = model.Archive(str(copy / 'archive.sqlite'))
    archived_keys = {k for (k,) in sqlite3.connect(copy / 'archive.sqlite').execute('select request_sha256 from model_calls')}
    views_db = sqlite3.connect(copy / 'views.sqlite')
    archive_db = sqlite3.connect(copy / 'archive.sqlite')
    last_answer_by_question = {}
    for view_id, question in views_db.execute('select view_id, question from views'):
        row = views_db.execute('select call_id from judgements where view_id=? order by judgement_id desc limit 1', (view_id,)).fetchone()
        if row:
            answer = archive_db.execute('select answer_json from model_calls where call_id=?', (row[0],)).fetchone()
            if answer and answer[0]:
                last_answer_by_question[question] = answer[0]
    views_db.close(); archive_db.close()
    fake = FakeTransport(archived_keys, last_answer_by_question)
    cfg, uni = config.load(str(CONFIG)), universe.load(str(ROOT / 'poc/universe.json'))
    day_runner = parallel_day.ParallelDay(str(TESTDB), str(copy / 'manifests'), extraction_workers=16, jev_workers=8)
    replay.run(testdb_path=str(TESTDB), views_path=str(copy / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni,
               from_day='2026-07-01', until_day='2026-07-14', transport=fake, log=lambda *a: None, only_objects={'NVDA'},
               day_runner=day_runner)
    after = sqlite3.connect(copy / 'views.sqlite')
    days_after = [d for (d,) in after.execute('select day from days_completed order by day')]
    per_input = after.execute('select input_id, count(*) from handovers group by input_id having count(*) > 1').fetchall()
    steps = after.execute("select input_id, min(sequence_no) from processing_steps group by input_id order by min(sequence_no)").fetchall()
    sequences = [s for _, s in steps]
    processed_failed = failed_input is not None and after.execute('select count(*) from handovers where input_id=?', (failed_input,)).fetchone()[0] == 1
    results = {
        'a completes to 2026-07-14': days_after[-1:] == ['2026-07-14'],
        'b no second handover': not per_input,
        'c sequence strictly increasing': all(x < y for x, y in zip(sequences, sequences[1:])),
        'd no archived request sent': fake.repeated == 0,
        'e failed item processed': processed_failed,
        'f only extraction and judgement sent, each judgement matched to one view': not fake.unexpected,
    }
    print(f'{draw.name}: days {days_before[-1] if days_before else None} -> {days_after[-1]}; handovers {handovers_before} -> '
          f'{after.execute("select count(*) from handovers").fetchone()[0]}; fake received {len(fake.sent)} requests; failed item {failed_input}')
    for label, ok in results.items():
        print(f'   {"ok " if ok else "FAIL"} {label}')
    return all(results.values())


if __name__ == '__main__':
    scratch, draws = sys.argv[1], sys.argv[2:]
    outcomes = [check(scratch, d) for d in draws]
    print(f'{sum(outcomes)} of {len(outcomes)} draws resume cleanly on copies')
    sys.exit(0 if all(outcomes) and outcomes else 1)
