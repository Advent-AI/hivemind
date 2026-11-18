"""The H-only diagnostic at $0 (council round 33): the packet built from the stored run with four controls, made-up rows, the VOID
rule and the bound fixed before."""
import json
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'astra'), str(HERE.parent / 'due-day')]
import h_reading  # noqa: E402

RUN = Path('/Users/lchingen/hivemind/poc/data/clean-astra-a2-2026-11-16')


@pytest.fixture()
def prepared(tmp_path):
    run = tmp_path / 'run'
    for arm, draw in h_reading.a2_probe.ORDER:
        shutil.copytree(RUN / f'{arm}-d{draw}', run / f'{arm}-d{draw}', ignore=shutil.ignore_patterns('archive.sqlite'))
    h_reading.prep(run, tmp_path / 'keys')
    return run, tmp_path / 'keys'


def rows(run, keys, harm=(), miss=None):
    """Two readers: every entry `part`, the controls as expected, `already_judged` on the first entry of the sends in `harm` (both
    readers), and the Codex reader missing the control named in `miss`."""
    key = json.loads((keys / 'key.json').read_text())
    expected = json.loads((keys / 'controls-expected.json').read_text())
    packet = {item['item']: item for item in json.loads((run / 'h-reading' / 'packet.json').read_text())}
    paths = []
    for reader in ('codex', 'claude'):
        lines = []
        for item, send in key.items():
            values = ['part'] * len(packet[int(item)]['other_fields']['not_judged'])
            if send in expected:
                values = [want or 'part' for want in expected[send]]
                if reader == 'codex' and send == miss:
                    values = ['part'] * len(values)
            if send in harm:
                values[0] = 'already_judged'
            lines.append(json.dumps({'item': int(item), 'H': values, 'why': f'made up ({reader})'}))
        path = run / f'h-{reader}.jsonl'
        path.write_text('\n'.join(lines) + '\n')
        paths.append(path)
    return paths


def test_equal_listings_are_within_the_bound(prepared):
    run, keys = prepared
    assert h_reading.score(run, keys, *rows(run, keys))[0] == 'within the bound'


def test_two_more_harmful_listings_in_a2_exceed_the_bound(prepared):
    run, keys = prepared
    a2 = [send for send in json.loads((keys / 'key.json').read_text()).values() if send.startswith('a2-')][:2]
    assert h_reading.score(run, keys, *rows(run, keys, harm=a2))[0] == 'exceeds the bound'


def test_a_reader_who_misses_a_planted_listing_voids_the_reading(prepared):
    run, keys = prepared
    with pytest.raises(SystemExit, match='VOID: codex misses the control\\|planted-outcome'):
        h_reading.score(run, keys, *rows(run, keys, miss='control|planted-outcome'))
