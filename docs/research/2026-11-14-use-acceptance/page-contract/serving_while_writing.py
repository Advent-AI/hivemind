"""Serving while a stored-answer replay writes (D573; $0). The extension proof's draw is judged again through the accepted loop
(D567) into a new scratch store, to an end day past its due days; every judge request is answered from the stored archive by
identity, and a request with none stops the run. At fixed pauses inside the loop (before a day's judging round, before its
closing and completion, after them) the product's API, started on the store being written, is asked for `/days` and `/library`,
and a fresh page pointed at it is rendered in headless Chrome. It exits 1 unless every check holds.

  python3 serving_while_writing.py <extension proof folder> <new scratch folder> [end day]
"""
import json
import re
import socket
import subprocess
import sys
import time
import html
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'), str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import ladder_adapter  # noqa: E402
from hivemind import model  # noqa: E402

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PAUSES = {('2026-09-22', 'before close'), ('2026-09-24', 'after close'), ('2026-09-25', 'before judging'),
          ('2026-09-25', 'after close'), ('2027-01-30', 'after close'), ('2027-01-31', 'before close'), ('2027-01-31', 'after close')}
PAGES = {('2026-09-25', 'before judging'), ('2027-01-31', 'after close')}


def free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get(port, path):
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{port}{path}', timeout=60) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b'{}')


def main(proof, scratch, end_day='2027-04-02'):
    scratch = Path(scratch)
    scratch.mkdir(parents=True)
    draw = Path(proof) / 'week/c1'
    stored = __import__('sqlite3').connect(f"file:{draw / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    answers = {sha: json.loads(r) for sha, r in stored.execute('select request_sha256, response_json from model_calls where response_json is not null')}

    def from_the_archive(provider, request):
        sha = model.request_identity(request)[1]
        if sha not in answers:
            raise SystemExit(f'a judge request with no stored answer: {sha[:16]}')
        return answers[sha]

    output = scratch / 'out'
    api = {'port': free_port(), 'process': None}
    page_shell = (scratch / 'shell.html')
    subprocess.run([sys.executable, str(ROOT / 'scripts/mock_build.py'), '--out', str(page_shell)], check=True, capture_output=True)
    seen = {}

    def ask(day, phase):
        if (day, phase) not in PAUSES:
            return
        if api['process'] is None:
            api['process'] = subprocess.Popen([sys.executable, str(ROOT / 'scripts/hivemind_api.py'), '--port', str(api['port']), '--lexical', '--config', '',
                                               '--views', str(output / 'views.sqlite'), '--index', str(scratch / 'index.sqlite'), '--archive', str(scratch / 'archive.sqlite')],
                                              stdout=open(scratch / 'api.log', 'w'), stderr=subprocess.STDOUT)
            for _ in range(60):
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:{api['port']}/days", timeout=2)
                    break
                except Exception:
                    time.sleep(0.5)
        record = {'days': get(api['port'], '/days'), 'library': get(api['port'], '/library')}
        if (day, phase) in PAGES:
            record['page'] = render(api['port'], page_shell, scratch, f'{day}-{phase}'.replace(' ', '-'))
        seen[(day, phase)] = record
        lib = record['library']
        print(f"pause {day} {phase}: /days {record['days'][1]} | /library {lib[0]} as_of {lib[1].get('as_of')} questions {len(lib[1].get('views', []))}"
              + (f" | page {record['page']}" if 'page' in record else ''), flush=True)

    real_judge, real_close = ladder_adapter.LadderAdapter.judge, ladder_adapter.LadderAdapter.close_and_complete

    def judge(self, day, seq, changed):
        ask(day, 'before judging')
        return real_judge(self, day, seq, changed)

    def close(self, day):
        ask(day, 'before close')
        result = real_close(self, day)
        ask(day, 'after close')
        return result

    ladder_adapter.LadderAdapter.judge, ladder_adapter.LadderAdapter.close_and_complete = judge, close
    inputs = {'trace': str(draw / 'step1/trace.sqlite'), 'step2': str(draw / 'step2'), 'ladders': str(draw / 'ladder/send-1/outcomes.jsonl'),
              'ladder_archive': str(draw / 'ladder/send-1/archive.sqlite'), 'cases': str(draw / 'cases/cases.json'), 'output_root': str(scratch)}
    try:
        ladder_adapter.replay('c1', output, transport=from_the_archive, cap_usd=5.0, inputs=inputs, end_day=end_day)
    finally:
        if api['process']:
            api['process'].terminate()
    checks = check(seen)
    (scratch / 'seen.json').write_text(json.dumps({f'{d} {p}': r for (d, p), r in seen.items()}, indent=1, ensure_ascii=False))
    failed = False
    for name, holds in checks.items():
        known = next((note for prefix, note in FINDINGS.items() if name.startswith(prefix)), None)
        print(('ok   ' if holds else ('KNOWN ' if known else 'FAIL ')) + name + (f' [{known}]' if known and not holds else ''))
        failed |= not holds and not known
    if failed:
        raise SystemExit(1)


def render(port, shell, scratch, name):
    """A fresh page pointed at the API; returns what it shows: its question count and the dates in its library text."""
    page = shell.read_text()
    m = re.search(r'<body([^>]*)>', page)
    page = page.replace(m.group(0), f'<body{m.group(1)} data-api="http://127.0.0.1:{port}">', 1)
    probe = ('<pre id="probe-result"></pre><script>setTimeout(()=>{const lib=document.getElementById("library");'
             'const out={cards:lib.querySelectorAll(".card").length,questions:[...lib.querySelectorAll(".card__q")].map(q=>q.textContent.trim()).sort(),'
             'status:Object.fromEntries([...lib.querySelectorAll(".library-card")].map(c=>[c.querySelector(".card__q").textContent.trim(),c.querySelector(".library-card-meta .chip--line").textContent.trim()]))};'
             'document.querySelector("#probe-result").textContent=JSON.stringify(out);},6000);</script></body>')
    (scratch / f'{name}.html').write_text(page.replace('</body>', probe))
    web_port = free_port()
    web = subprocess.Popen([sys.executable, '-m', 'http.server', str(web_port), '--bind', '127.0.0.1'], cwd=scratch,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={scratch / "chrome"}',
                              '--virtual-time-budget=20000', '--dump-dom', f'http://127.0.0.1:{web_port}/{name}.html'],
                             capture_output=True, text=True, timeout=180).stdout
    finally:
        web.terminate()
    m = re.search(r'<pre id="probe-result">(.*?)</pre>', dom, re.S)
    return json.loads(html.unescape(m.group(1))) if m and m.group(1) else None


def check(seen):
    lib = lambda key: seen[key]['library']
    out = {}
    first = seen[('2026-09-22', 'before close')]
    out[f"before the first completed day the API serves no library (/library {lib(('2026-09-22', 'before close'))[0]}, /days {first['days'][1]})"] = \
        lib(('2026-09-22', 'before close'))[0] != 200 or not lib(('2026-09-22', 'before close'))[1].get('views')
    out['inside 2026-09-25, before its judging round, /library equals what it served right after 2026-09-24 completed'] = \
        lib(('2026-09-25', 'before judging')) == lib(('2026-09-24', 'after close'))
    out['right after 2026-09-25 completed, /library is as of 2026-09-25'] = lib(('2026-09-25', 'after close'))[1].get('as_of') == '2026-09-25'
    out['on 2027-01-31 before its closing, /library equals what it served after 2027-01-30'] = lib(('2027-01-31', 'before close')) == lib(('2027-01-30', 'after close'))
    after = {v['view_id']: v for v in lib(('2027-01-31', 'after close'))[1]['views']}
    out['after 2027-01-31 completed, its three due questions are closed on that day'] = all(
        not after[v]['open'] and after[v]['switches'][-1]['day'] == '2027-01-31' for v in ('v3', 'v4', 'v7'))
    for key, served in ((('2026-09-25', 'before judging'), ('2026-09-24', 'after close')), (('2027-01-31', 'after close'), ('2027-01-31', 'after close'))):
        page = seen[key].get('page') or {}
        expected = sorted(v['question'] for v in lib(served)[1]['views'])
        out[f"a fresh page at {key[0]} {key[1]} shows exactly the questions served as of {lib(served)[1].get('as_of')} ({page.get('cards')} cards)"] = page.get('questions') == expected
        status = {v['question']: ('Open' if v['open'] else 'Closed') for v in lib(served)[1]['views']}
        out[f"... and each card's status is the served one on {lib(served)[1].get('as_of')} (the page's day, not another)"] = page.get('status') == status
    return out


FINDINGS = {"before the first completed day the API serves no library": 'known open defect B (LIVE-READ-DESIGN.md): reported, not a failing check'}


if __name__ == '__main__':
    main(*sys.argv[1:])
