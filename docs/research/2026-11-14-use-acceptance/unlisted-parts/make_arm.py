"""Writes arm A of DESIGN.md into arm-a/: the frozen ladder step's three request files with every "the topic's wording" replaced by
the topic's description and outcome. Each replaced string must occur exactly once and no "wording" may remain; the frozen files
are read, never written."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FROZEN = ROOT / 'clean-arch/step4-2026-11-10/ladder'
OUT = Path(__file__).resolve().parent / 'arm-a'
REPLACEMENTS = {
    'candidate-system.txt': [
        ("A topic's wording may ask about more than one thing.", "A topic's description and outcome together may ask about more than one thing."),
        ("List every other part of the topic's wording that the question leaves out",
         "List every other part of the topic's description and outcome that the question leaves out"),
        ("when the topic's wording names it, list it in not_judged", "when the topic's description or outcome names it, list it in not_judged"),
    ],
    'candidate-closing.txt': [
        ("is every other part of the topic's wording listed in not_judged?", "is every other part of the topic's description and outcome listed in not_judged?"),
    ],
    'candidate-schema.json': [
        ("Every other part of the topic's wording that the question leaves out", "Every other part of the topic's description and outcome that the question leaves out"),
        ("nothing of the wording out", "nothing of either out"),
    ],
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, pairs in REPLACEMENTS.items():
        text = (FROZEN / name).read_text()
        before = len(text)
        for old, new in pairs:
            if text.count(old) != 1:
                raise SystemExit(f'{name}: {old!r} occurs {text.count(old)} times, not once')
            text = text.replace(old, new)
        if 'wording' in text:
            raise SystemExit(f'{name}: "wording" remains')
        if name.endswith('.json'):
            json.loads(text)
        (OUT / name).write_text(text)
        print(f'{name}: {before} -> {len(text)} characters, {len(pairs)} replacements')
    return 0


if __name__ == '__main__':
    sys.exit(main())
