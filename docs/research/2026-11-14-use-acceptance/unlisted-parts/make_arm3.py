"""Writes arm A3 of DESIGN-A3.md v11 into arm-a3/: arm A2's three request files (make_arm2.py) with one sentence added to the closing
check, right after "...listed in not_judged?". Every replaced or anchored string must occur exactly once; the frozen files are read,
never written."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_arm  # noqa: E402
import make_arm2  # noqa: E402

OUT = HERE / 'arm-a3'
ANCHOR = "listed in not_judged? For a figure"
SENTENCE = ('For an event, an entry that only restates one of its outcomes, the event itself happening, its being ruled out without naming '
            'how, or its still being awaited on the due day, is not a part the question leaves out: remove it. Keep every other entry, '
            'including a named way the event could be ruled out, a separate matter that would follow from an outcome, and a finer case '
            'inside one.')
REPLACEMENTS = dict(make_arm2.REPLACEMENTS)
REPLACEMENTS['candidate-closing.txt'] = make_arm2.REPLACEMENTS['candidate-closing.txt'] + [
    (ANCHOR, 'listed in not_judged? ' + SENTENCE + ' For a figure')]


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
    for name in ('candidate-system.txt', 'candidate-schema.json'):
        if (OUT / name).read_text() != (make_arm2.OUT / name).read_text():
            raise SystemExit(f'{name} differs from arm A2')
    return 0


if __name__ == '__main__':
    sys.exit(main())
