"""Blind packets for scoring probe answers against the census matter lists, which readers wrote before any candidate existed.

Usage: build_probe_packets.py <probe folder> <census key file> <arm key output path>
Each article's answers from every arm and draw are shuffled and labelled R1..Rn; the arm of each label is written only to the key file."""
import json, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / 'poc/data/clean-step1-takeover-2026-11-07'

def main():
    probe, census_key_path, key_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    results = json.loads((probe / 'results.json').read_text())
    census = {a['article']: a for part in range(1, 5) for a in json.loads((CENSUS / f'census-answer-{part}.json').read_text())}
    texts = {p['article']: p for part in range(1, 5) for p in json.loads((CENSUS / f'census-packet-{part}.json').read_text())}
    chooser = random.Random(7)
    articles = sorted({r['article'] for r in results})
    packets, key = [], {}
    for number in articles:
        answers = [r for r in results if r['article'] == number and 'answer' in r]
        chooser.shuffle(answers)
        labelled = {}
        for index, answer in enumerate(answers, 1):
            label = f'R{index}'
            key[f'{number}:{label}'] = f"{answer['arm']}:d{answer['draw']}"
            labelled[label] = [{'summary': ev['summary'], 'quotes': ev['source_passages']} for ev in answer['answer']['evidence']]
        matters = [{'id': f'M{i}', 'matter': m['matter'], 'weight': m['weight']} for i, m in enumerate(census[number]['matters'], 1)]
        packets.append({'article': number, 'title': texts[number]['title'], 'text': texts[number]['text'], 'matters': matters, 'answers': labelled})
    groups = [articles[i::4] for i in range(4)]
    for part, group in enumerate(groups, 1):
        (probe / f'score-packet-{part}.json').write_text(json.dumps([p for p in packets if p['article'] in group], ensure_ascii=False, indent=1))
    key_path.write_text(json.dumps(key, indent=1))
    print('articles', articles, 'answers labelled', len(key), 'groups', groups)

if __name__ == '__main__':
    main()
