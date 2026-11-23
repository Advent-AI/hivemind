"""The paired test's send and reading paths at $0 (council round 4: "then check and a dry run"): the real check, all six arm-draws through
the real runner and spend limit with a fake transport answering each topic's stored astra answer, and the blind reading and source-review
packets built from that run."""
import glob
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paired_probe as probe  # noqa: E402

USAGE = {'prompt_tokens': 5200, 'completion_tokens': 200, 'prompt_tokens_details': {'cached_tokens': 2300}}   # the stored astra means on these topics (38 requests: input 5,187, output 196); the system text cached, as the diagnostic's $0.034 a send shows
STORED = ['poc/data/clean-ladder-stage-a-astra-2026-11-17/run-1/send-*/outcomes.jsonl',
          'poc/data/clean-second-side-probe-2026-11-17/run-1/*/outcomes.jsonl']


def transport():
    """Answers each request with a stored astra answer for its topic: a written ladder in the edited arm and a decline in the frozen arm
    when both are stored, else whichever is stored."""
    by_name = {}
    for pattern in STORED:
        for path in glob.glob(str(probe.ROOT / pattern)):
            for row in map(json.loads, Path(path).read_text().splitlines()):
                if row['status'] in ('ladder', 'no ladder'):
                    by_name.setdefault(row['case'].split('|')[-1], {}).setdefault(row['status'], row['requests'][-1]['answer_text'])
    descriptions = {case['thesis']['description']: name for name, case in probe.population().items()}
    edited_system = probe.edited_texts()['system']
    sent = []

    def send(provider, request):
        system, user = request['messages'][0]['content'], request['messages'][1]['content']
        name = next(name for description, name in descriptions.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        arm = 'edited' if system == edited_system else 'frozen'
        stored = by_name[name]
        text = stored.get('ladder' if arm == 'edited' else 'no ladder') or next(iter(stored.values()))
        sent.append((arm, name, request))
        return {'choices': [{'message': {'content': text}}], 'usage': USAGE}
    send.sent = sent
    return send


@pytest.fixture(scope='module')
def run(tmp_path_factory):
    folder = tmp_path_factory.mktemp('paired')
    original, probe.RECORD = probe.RECORD, folder / 'check-passed.json'
    try:
        probe.check()
        fake = transport()
        probe.send(folder / 'run', transport=fake)
        probe.reading(folder / 'run', folder / 'keys')
        yield folder, fake
    finally:
        probe.RECORD = original


def test_every_planned_send_is_made_once_with_its_arms_texts(run):
    _, fake = run
    first = {}
    for arm, name, request in fake.sent:
        first.setdefault((arm, name), []).append(request)
    planned = {(arm, name) for arm, draw in probe.ORDER for name in probe.topics_of(draw)}
    assert set(first) == planned
    texts = {arm: probe.TEXTS[arm]() for arm in probe.ARMS}
    for (arm, _), requests in first.items():
        for request in requests:
            assert request['messages'][0]['content'] == texts[arm]['system']
            assert request['messages'][1]['content'].split('\n\n')[1].startswith(texts[arm]['closing'])
            no_ladder = request['response_format']['json_schema']['schema']['properties']['no_ladder']['description']
            assert no_ladder == texts[arm]['schema']['properties']['no_ladder']['description']
    assert sum(len(probe.topics_of(draw)) for _, draw in probe.ORDER) == 52


def test_the_reading_holds_every_send_and_the_review_holds_only_written_targets_share_and_capacity_topic(run):
    folder, _ = run
    key = json.loads((folder / 'keys' / 'key.json').read_text())
    sends = {case for case, _ in key.values() if '|' in case and case.split('|')[0] in {f'{a}-d{d}' for a, d in probe.ORDER}}
    outcomes = [json.loads(line) for arm, draw in probe.ORDER
                for line in (folder / 'run' / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()]
    assert sends == {row['case'] for row in outcomes if row['status'] in ('ladder', 'no ladder')}
    review_key = json.loads((folder / 'keys' / 'review-key.json').read_text())
    allowed = set(probe.TARGETS + probe.SHARE + ('u3/clean-10',))
    assert review_key and all(case.split('|', 1)[1] in allowed for case in review_key.values())
    written = {row['case'] for row in outcomes if row['status'] == 'ladder' and row['case'].split('|', 1)[1] in allowed}
    assert set(review_key.values()) == written
