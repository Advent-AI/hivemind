"""Blind thesis reading for a probe (AGENTS §7.1: meaning is judged by a reader who did not write the change). For each named case,
every thesis any arm opened is listed under a shuffled label, beside the article and the theses open before it; the arm key is written
outside the repository. The standard given to the reader is c8's section 3 and D388's decided paragraph, quoted verbatim.

Usage: build_thesis_reading.py <key.json> <packet prefix> <batch>:<case>,<case>... [<batch>:...] --records <records.json>..."""
import argparse, json, random, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import probe_unfiled  # noqa: E402

system = (HERE / 'arms/c8-system.txt').read_text(encoding='utf-8')
SECTION_3 = system[system.index('3. WHEN TO PROPOSE A NEW THESIS'):system.index('If the two cannot move apart')]
log = (ROOT / 'docs/DECISIONS-log.md').read_text(encoding='utf-8')
D388 = re.search(r'- \*\*Decided\.\*\*(.*?)\n- \*\*Why', log[log.index('## D388'):], re.S).group(1).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('key'); parser.add_argument('prefix'); parser.add_argument('batches', nargs='+')
    parser.add_argument('--records', nargs='+', required=True)
    args = parser.parse_args()
    records = [r for path in args.records for r in json.loads(Path(path).read_text()) if 'new_theses' in r]
    cases = {c['case']: c for c in json.loads((HERE / 'cases-c9.json').read_text())}
    shuffle = random.Random(20261109)
    key = {}
    for batch in args.batches:
        name, names = batch.split(':')
        parts = []
        for case_name in names.split(','):
            _, _, _, payload = probe_unfiled.build(cases[case_name], 'c8')
            opened = [(r['arm'], r['draw'], t) for r in records if r['case'] == case_name for t in r['new_theses']
                      if t['local_id'] not in r.get('unlinked_new_theses', [])]
            shuffle.shuffle(opened)
            item = payload['source_item']
            lines = [f"## Article {case_name}", f"Published: {item.get('published_at') or item.get('date')}; title: {item.get('title')}", '',
                     item['text'], '', 'Theses open before this article:']
            lines += [f"- {t['id']}: {t['description']}" for t in payload['open_theses']] or ['- none']
            lines += ['', 'Theses proposed after reading this article (judge each):']
            for number, (arm, draw, thesis) in enumerate(opened, 1):
                label = f'{case_name}/T{number}'
                key[label] = {'arm': arm, 'draw': draw, 'description': thesis['description']}
                lines.append(f"- {label} [{thesis.get('opens_as')}]: {thesis['description']} (period: {thesis.get('period')})")
            parts.append('\n'.join(lines))
        Path(f'{args.prefix}-{name}.md').write_text(
            '# The standard (verbatim)\n\n' + SECTION_3.strip() + '\n\nDecision D388: ' + D388 + '\n\n# Articles\n\n' + '\n\n'.join(parts) + '\n',
            encoding='utf-8')
        print(name, 'theses:', sum(1 for label in key if label.split('/')[0] in names.split(',')))
    Path(args.key).write_text(json.dumps(key, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
