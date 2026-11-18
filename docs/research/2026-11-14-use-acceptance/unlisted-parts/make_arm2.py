"""Writes arm A2 of DESIGN-A2.md into arm-a2/: arm A's three request files (make_arm.py) with one clause added to system line 5,
before "Never fold two things into one ladder". The clause's examples are D436's own three; every replaced or anchored string must
occur exactly once. The frozen files are read, never written."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_arm  # noqa: E402

OUT = HERE / 'arm-a2'
ANCHOR = 'one sentence on why it is not the one tracked. Never fold two things into one ladder'
CLAUSE = ('A second side of the same bet, for example a market\'s tightness beside the volume shipped, a share beside the total it is part '
          'of, or capacity beside the demand it serves, stays in the one question as context: list it in not_judged. A second side is '
          'not by itself a reason to decline; decline only when no part is the main one, or when the main part itself meets a case '
          'below. ')
REPLACEMENTS = dict(make_arm.REPLACEMENTS)
REPLACEMENTS['candidate-system.txt'] = make_arm.REPLACEMENTS['candidate-system.txt'] + [
    (ANCHOR, 'one sentence on why it is not the one tracked. ' + CLAUSE + 'Never fold two things into one ladder')]


def main():
    OUT.mkdir(exist_ok=True)
    for name, pairs in REPLACEMENTS.items():
        text = (make_arm.FROZEN / name).read_text()
        before = len(text)
        for old, new in pairs:
            if text.count(old) != 1:
                raise SystemExit(f'{name}: {old!r} occurs {text.count(old)} times, not once')
            text = text.replace(old, new)
        if 'wording' in text:
            raise SystemExit(f'{name}: "wording" remains')
        (OUT / name).write_text(text)
        print(f'{name}: {before} -> {len(text)} characters, {len(pairs)} replacements')
    return 0


if __name__ == '__main__':
    sys.exit(main())
