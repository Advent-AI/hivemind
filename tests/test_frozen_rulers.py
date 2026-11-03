"""The frozen ruler (AGENTS §7.1, D261, D262): the extraction gold, the seeds and the judgement gold never change. This test holds
their sha256 as recorded on 2026-11-02 and fails the suite when any of them moves; the positive control flips one byte of a copy and
shows the check catches it. A new ruler version is a new file set recorded by a decision, never an edit of these."""
import hashlib
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZEN = {
    'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json': '6f9476bb6a81ea590af273a71565e7c3c0f49908d26274b8482d52cfdee31a21',
    'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json': 'af2145cdc60c34ec1ded0bebcb809800e187d616992ea325919c3ad771da61e3',
    'poc/seeds/nvda-2026-07-01-v2.json': 'fca16f42dd7153e852c42527883552b86567f33d7e1ed3c11ef600c8a37037d6',
    'docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json': '53d1e8b40f1a970c944d30fc2add917c7b2f838ce5b64850d00f2b84099c15bf',
    'docs/research/2026-11-01-e2e-loop/judgement-gold/questions-v1.json': '3085418000d5939756971e3cbd59a94a2c7a9615cde5f43ed8ef52333ad2362c',
    'docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json': '636c056d1e4252fa759660803067e6ccd67a81067b012905e918aa9dec4005f2',
}


def sha256_of(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def moved(expected, actual):
    return [path for path, digest in expected.items() if actual.get(path) != digest]


def test_every_frozen_file_still_has_its_recorded_hash():
    actual = {path: sha256_of(os.path.join(ROOT, path)) for path in FROZEN}
    assert moved(FROZEN, actual) == [], 'a frozen ruler file changed: a defect is a dated correction record, a new version is a decision (D261)'


def test_the_recorded_hash_files_and_the_scorer_agree_with_the_gold():
    gold_dir = os.path.join(ROOT, 'docs/research/2026-11-01-e2e-loop/judgement-gold')
    with open(os.path.join(gold_dir, 'gold-v1.sha256')) as handle:
        assert handle.read().split()[0] == FROZEN['docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json']
    with open(os.path.join(gold_dir, 'score_judgement.py')) as handle:
        assert f"GOLD_SHA256 = '{FROZEN['docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json']}'" in handle.read()
    with open(os.path.join(ROOT, 'docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5.sha256')) as handle:
        recorded = dict(line.split()[::-1] for line in handle if line.strip())
    assert recorded['golden-v5-dev.json'] == FROZEN['docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json']
    assert recorded['golden-v5-test.json'] == FROZEN['docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json']


def test_the_check_catches_a_one_byte_change(tmp_path):
    original = os.path.join(ROOT, 'docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json')
    with open(original, 'rb') as handle:
        data = bytearray(handle.read())
    data[len(data) // 2] ^= 0x01
    mutant = tmp_path / 'gold-v1.json'
    mutant.write_bytes(bytes(data))
    key = 'docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json'
    assert moved({key: FROZEN[key]}, {key: sha256_of(str(mutant))}) == [key]
