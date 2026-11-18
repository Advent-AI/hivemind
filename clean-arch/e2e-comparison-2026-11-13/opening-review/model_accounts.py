"""D459's bounded diagnostic: the model's own account (AGENTS §1) of seven opening choices left unresolved by the opening review — the
Ohio guarantee linked only to the credit-support amount (clean c1, c2, c3; production p2, p3) and calendar 2027's capex left as the 2026
question's reference (clean c2, c3). Each stored conversation is continued exactly: the stored request's messages, the stored answer as the
assistant turn, then one user turn that restates the response schema the model answered with (the free-text follow-up cannot carry
`response_format`, and the schema's field descriptions are instructions the model saw) and asks the question. A reply is a lead, read
against the original answer, the whole request and the standard; it proves nothing alone.

Clean requests are the trace's stored request (as sent). Production's stored request is the archive's key-sorted copy; its identity hash
is checked against `request_sha256`, and only key order differs from what was sent (message strings are identical).

  python3 model_accounts.py <output.json>        # refuses an existing output; ceiling $0.50 estimated before any send
"""
import concurrent.futures
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

DATA = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
TRACES = {'c1': DATA / 'c1/step1/trace.sqlite', 'c2': DATA / 'c2/step1-redo/trace.sqlite', 'c3': DATA / 'c3/step1/trace.sqlite'}
OHIO_ARTICLE = 'gnews:4d1677af37befd53ca3e7b45'
CEILING_USD = 0.50
TAIL = (' Quote the instruction or instructions of this request that led you there, and name the statements of the request you weighed '
        'against them. Then say what an experienced analyst covering the company would have done with this article. Answer in at most '
        '170 words.')
OHIO_CLEAN = ('Your answer linked the report that NVIDIA has been negotiating to guarantee OpenAI\'s lease of a large Ohio data center to the '
              'open thesis on the amount of credit support NVIDIA has extended. Why did you not open a thesis on whether NVIDIA signs that '
              'guarantee by a check date?')
OHIO_PROD = ('Your answer linked the report that NVIDIA has been negotiating to guarantee OpenAI\'s lease of a large Ohio data center to your '
             'candidate c1, on the amount of guarantees and credit support NVIDIA commits, and proposed no candidate on whether NVIDIA signs '
             'that guarantee by a check date. Why?')
YEAR = ('Your answer opened one thesis on the big four hyperscalers\' combined data-center capital expenditure for calendar 2026, and used '
        'the article\'s figure for calendar 2027 only as its reference. Why did you not open calendar 2027\'s combined spending as a thesis '
        'of its own?')
CASES = [('c1', 8, OHIO_CLEAN), ('c2', 8, OHIO_CLEAN), ('c3', 8, OHIO_CLEAN), ('c2', 42, YEAR), ('c3', 42, YEAR),
         ('p2', OHIO_ARTICLE, OHIO_PROD), ('p3', OHIO_ARTICLE, OHIO_PROD)]


def schema_turn(request, question):
    schema = request.get('response_format')
    reminder = ('For reference, this is the response schema you answered with, field descriptions included:\n'
                + json.dumps(schema, ensure_ascii=False) + '\n\n') if schema else ''
    return {'role': 'user', 'content': reminder + question + TAIL}


def clean_follow_up(draw, sequence, question):
    conn = sqlite3.connect(f'file:{TRACES[draw]}?mode=ro', uri=True)
    request, raw = conn.execute("select request, raw_response from trace where sequence = ? and status = 'complete'", (sequence,)).fetchone()
    conn.close()
    request, raw = json.loads(request), json.loads(raw)
    stored_answer = raw['choices'][0]['message']['content']
    follow = dict(request, messages=request['messages'] + [{'role': 'assistant', 'content': stored_answer}, schema_turn(request, question)])
    follow.pop('response_format', None)
    return 'deepseek', follow


def production_follow_up(draw, article, question):
    conn = sqlite3.connect(f"file:{DATA / draw / 'prod' / 'archive.sqlite'}?mode=ro", uri=True)
    rows = conn.execute("select request_json, request_sha256, response_json from model_calls where purpose = 'extract' and request_json like ?",
                        (f'%{article}%',)).fetchall()
    conn.close()
    if len(rows) != 1:
        raise SystemExit(f'{draw}: expected one extraction call for {article}, found {len(rows)}')
    stored, identity, response = rows[0]
    request = json.loads(stored)
    if hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode()).hexdigest() != identity:
        raise SystemExit(f'{draw}: the stored request does not match its archived identity')
    stored_answer = json.loads(response)['choices'][0]['message']['content']
    follow = dict(request, messages=request['messages'] + [{'role': 'assistant', 'content': stored_answer}, schema_turn(request, question)])
    follow.pop('response_format', None)
    return 'openai', follow


def build(case):
    draw, where, question = case
    return clean_follow_up(draw, where, question) if draw.startswith('c') else production_follow_up(draw, where, question)


def estimate(provider, request):
    prices = model.PRICES[request['model']]
    tokens_in = len(json.dumps(request, ensure_ascii=False)) / 3         # a generous character-to-token ratio
    return tokens_in * prices[0] / 1e6 + 4000 * prices[1] / 1e6          # reasoning and a 170-word reply


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise SystemExit(f'{out} exists')
    built = [(case, *build(case)) for case in CASES]
    estimated = sum(estimate(provider, request) for _, provider, request in built)
    print(f'{len(built)} follow-ups built; estimated ${estimated:.3f} against a ceiling of ${CEILING_USD:.2f}')
    if estimated > CEILING_USD:
        raise SystemExit('estimate above the ceiling: nothing sent')

    def ask(item):
        (draw, where, question), provider, request = item
        response = model.openai_transport(provider, request)
        usage = response.get('usage') or {}
        tokens_in, tokens_out = usage.get('prompt_tokens') or 0, usage.get('completion_tokens') or 0
        prices = model.PRICES[request['model']]
        return {'draw': draw, 'where': where, 'model': request['model'], 'question': question,
                'reply': response['choices'][0]['message']['content'], 'input_tokens': tokens_in, 'output_tokens': tokens_out,
                'cost_usd_from_tokens': round(tokens_in * prices[0] / 1e6 + tokens_out * prices[1] / 1e6, 6)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        replies = list(pool.map(ask, built))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(replies)} replies; ${sum(r["cost_usd_from_tokens"] for r in replies):.4f} from tokens at the published rates (no cache credit)')


if __name__ == '__main__':
    main()
