"""Reader A of the judgement ruler (ruler-v1.md §1): Codex, read-only, ephemeral, no repository context beyond the brief, the packet and
the questions, which are put inline in the prompt (one batch of questions per call, four calls in parallel). The raw answers are kept as
written in reader-A/batchN.txt; reader-A.json is the parsed list, one object per question.

    python3 run_reader_codex.py           # writes reader-A/ and reader-A.json
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BATCHES = 4


def packet_text(packet):
    return '\n'.join(f"{i['id']} | {i['day']} | {i['tier']} | who: {i['who']} | article: {i['title']}\n   passage: {i['passage']}\n   meaning: {i['meaning']}"
                     for i in packet['items'])


def prompt_for(brief, packet, questions):
    qs = '\n\n'.join(json.dumps({k: q[k] for k in ('id', 'kind', 'question', 'due_day', 'unit', 'rungs')}, ensure_ascii=False) for q in questions)
    return (brief + '\n\n# The packet (every item an analyst following the company noted, 2026-07-01 to 2026-07-14)\n\n' + packet_text(packet)
            + '\n\n# The questions you answer in this batch\n\n' + qs
            + '\n\n# Output\n\nReturn one JSON array containing exactly one object per question above, in the shape the brief gives, nothing else. '
              'Do not read any file or run any command: everything you may use is in this message.')


def run_batch(n, text):
    out = HERE / 'reader-A' / f'batch{n}.txt'
    cmd = ['codex', 'exec', '-s', 'read-only', '-C', str(ROOT), '--skip-git-repo-check', '--ephemeral', '-o', str(out), '-']
    result = subprocess.run(cmd, input=text, text=True, capture_output=True, timeout=3600)
    (HERE / 'reader-A' / f'batch{n}.log').write_text(result.stdout[-4000:] + '\n--- stderr ---\n' + result.stderr[-4000:], encoding='utf-8')
    return n, result.returncode, out


def parse(text):
    start = text.find('[')
    depth = 0
    for k in range(start, len(text)):
        depth += {'[': 1, ']': -1}.get(text[k], 0)
        if depth == 0:
            return json.loads(text[start:k + 1])
    raise ValueError('no JSON array in the answer')


def main():
    brief = (HERE / 'reader-brief.md').read_text(encoding='utf-8')
    packet = json.loads((HERE / 'packet-v1.json').read_text(encoding='utf-8'))
    questions = json.loads((HERE / 'questions-v1.json').read_text(encoding='utf-8'))['questions']
    (HERE / 'reader-A').mkdir(exist_ok=True)
    batches = [questions[k::BATCHES] for k in range(BATCHES)]
    print(f'{len(questions)} questions in {BATCHES} batches; prompt ≈ {len(prompt_for(brief, packet, batches[0])):,} chars each', flush=True)
    answers = []
    with ThreadPoolExecutor(BATCHES) as pool:
        for n, code, out in pool.map(lambda nb: run_batch(nb[0], prompt_for(brief, packet, nb[1])), enumerate(batches)):
            text = out.read_text(encoding='utf-8') if out.exists() else ''
            try:
                parsed = parse(text)
            except Exception as error:   # the raw text stays; a batch that cannot be parsed is reported, not patched
                print(f'batch {n}: exit {code}, {len(text)} chars, NOT PARSED: {error}', flush=True); continue
            print(f'batch {n}: exit {code}, {len(parsed)} answers', flush=True)
            answers.extend(parsed)
    answers.sort(key=lambda a: a.get('question_id', ''))
    (HERE / 'reader-A.json').write_text(json.dumps({'reader': 'A: Codex (codex exec, read-only, ephemeral), model-authored', 'ruler_version': 1, 'answers': answers},
                                                   ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'reader-A.json: {len(answers)} answers; ids {[a.get("question_id") for a in answers]}')


if __name__ == '__main__':
    sys.exit(main())
