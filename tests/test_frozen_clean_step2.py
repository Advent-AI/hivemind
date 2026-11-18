"""The clean path's Step 2 is frozen (D427, Alex, 2026-11-11: "好jev 收尾冻结"): the search, the Jev comparison and its request text, the
choice of the group a repeat joins, the forward runner, and Step 3's grouping library stay as accepted at D381 and measured through
the Step 2 log §17. This test holds their sha256 and fails the suite when any of them moves; the positive control flips one byte of a
copy and shows the check catches it. A change is a new version that only Alex opens, measured against this one."""
import hashlib
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZEN = {
    'clean-arch/step2/compare.py': 'c7fcf0903d7df58a12f29c8a74171bf51968c68cb3cfcbcae54fd449935ffabe',
    'clean-arch/step2/run_forward.py': 'ca2a49f85e58283737e06457b0875c28e56294802148b9b443f7447f5cb4a96d',
    'clean-arch/step2/test_compare.py': '6f1cc0ba2d4cc5c9177aa40a181a82e8fcf28df686330216daf4cf8ecd13ee3f',
    'clean-arch/step2/test_run_forward.py': '8f4d8779fd248a22b3a57fea6d9d08c6a1d374cda14c57ef88ffbcdc15e5ffca',
    'clean-arch/step3/library.py': 'e091095d3034791d6d59a0ddce0be190aa468e8539abbb941eaeca228d089885',
    'clean-arch/step3/test_library.py': 'b3d20fb9dd05e818039febbcbf6b026cf47e93bc88e645ee404a7b407fa74b7c',
}


def sha256_of(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def moved(expected, actual):
    return [path for path, digest in expected.items() if actual.get(path) != digest]


def test_every_frozen_step2_file_still_has_its_recorded_hash():
    actual = {path: sha256_of(os.path.join(ROOT, path)) for path in FROZEN}
    assert moved(FROZEN, actual) == [], 'a frozen clean Step 2 file changed: a change is a new version Alex opens (D427)'


def test_the_check_catches_a_one_byte_change(tmp_path):
    key = 'clean-arch/step2/compare.py'
    with open(os.path.join(ROOT, key), 'rb') as handle:
        data = bytearray(handle.read())
    data[len(data) // 2] ^= 0x01
    mutant = tmp_path / 'compare.py'
    mutant.write_bytes(bytes(data))
    assert moved({key: FROZEN[key]}, {key: sha256_of(str(mutant))}) == [key]
