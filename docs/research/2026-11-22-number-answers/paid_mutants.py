"""Mutants of the paid-gate harness's round 47b defences: each mutant breaks one defence on a scratch copy, and the rehearsal check named
beside it must fail while the unmutated control passes. Usage: python3 paid_mutants.py <scratch folder>."""
import concurrent.futures
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTANTS = [
    ('equivalence is exact equality', "return all(abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y)) for x, y in zip(a[0], b[0]))",
     'return a[0] == b[0]', 'separate-agree-float'),
    ('a transport failure counts as finished', "if d not in ('publish', 'held', 'refused')]", "if d not in ('publish', 'held', 'refused', 'transport')]",
     'a unit failed in transport'),
    ('an attempt in flight is not seen', 'if len(done) < len(started):', 'if False:', 'interrupt:'),
    ('results only on a clean exit', "        finally:                                          # [47b.2] the results come from the attempt records, written even after an abort\n            summary",
     '        except BaseException:\n            raise\n        if True:\n            summary', 'interrupt:'),
    ('a first refusal with no retry counts as unresolved', "decision = 'unresolved' if len(done) >= 2 else 'retry not sent'", "decision = 'unresolved'",
     'retry was never sent'),
    ('any text is a ground', " and any(re.search(rf'\\b{re.escape(g)}\\b', ground) for g in grounds)", '', 'ground naming nothing'),
    ('the key is not bound to the run', "problems = [] if frozen.get('run_digest') == run_digest(out) else ['the packet key does not belong to this run']",
     'problems = []', 'a run changed after'),
    ('the readings are not bound to the packets', "if submitted.get('packets_sha256') != sha:", 'if False:', 'readings made on other packets'),
    ('the packets can be remade', "if (key_dir / 'packet-key.json').exists():", 'if False:', 'a second packets run is refused',
     [("open(out / 'packets.md', 'x')", "open(out / 'packets.md', 'w')"), ("open(key_dir / 'packet-key.json', 'x')", "open(key_dir / 'packet-key.json', 'w')"),
      ("open(out / 'attempts.md', 'x')", "open(out / 'attempts.md', 'w')")]),
    ('a card shows the whole calculation', "sub = {'figures': [f for f in calc['figures'] if f['id'] in own], 'answers': [ans]}",
     "sub = {'figures': list(calc['figures']), 'answers': [ans]}", 'card view'),
    ('assumption records keep their raw ids', "mapped.append({k: rename[v] if k in ('figure', 'bridge') else v for k, v in r.items()})",
     'mapped.append(dict(r))', 'card view'),
    ('a reconciled card shows the merged calculation', "per_card = {a.split('-', 1)[1]: first_attempt(results['finals'].get(f'{unit}|{a}|{draw}', {})) for",
     "per_card = {a.split('-', 1)[1]: dict(first_attempt(results['finals'].get(f'{unit}|{a}|{draw}', {})), data=entry.get('calc')) for",
     'own original derivation'),
    ('a several-candidate first call is unified', """        if len(by_call) == 2 and all(len(ids) == 1 for ids in by_call.values()):
            (a,), (b,) = (by_call[v] for v, _ in parts)""", """        if len(by_call) == 2 and len(by_call[parts[1][0]]) == 1:
            a, b = by_call[parts[0][0]][0], by_call[parts[1][0]][0]""", 'within one call'),
    ('a several-candidate second call is unified', """        if len(by_call) == 2 and all(len(ids) == 1 for ids in by_call.values()):
            (a,), (b,) = (by_call[v] for v, _ in parts)
            if units[a] == units[b] and _same_value(recomputed.get(a), recomputed.get(b)):   # [47b.1] equal values, [47e.2] in one unit
                alias[b] = a""", """        if len(by_call) == 2 and len(by_call[parts[0][0]]) == 1:
            a = by_call[parts[0][0]][0]
            for b in by_call[parts[1][0]]:
                if _same_value(recomputed.get(a), recomputed.get(b)):
                    alias[b] = a""", 'separate-within-dup-second'),
    ('the commitment is not checked', "    if not written.startswith(f'Key commitment: {key_commitment(frozen)}\\n'):", "    if False:", 'identical text'),
    ('an interrupted card reads as never sent', "'interrupted': 'The request was started; no answer was recorded.'", "'interrupted': 'No request was sent for this card.'",
     'request was started'),
    ('a card is not a ground', "        grounds.add(token)\n", "", 'abstain'),
    ('a torn journal line stops the summary', "            except json.JSONDecodeError:\n                if damaged is not None:", "            except KeyError:\n                if damaged is not None:",
     'torn journal'),
    ('a damaged line does not make the verdict incomplete',
     "    problems += [f'answers.jsonl line {d[\"line\"]} is damaged' for d in results.get('damaged', [])\n                 if d.get('journal') == 'answers.jsonl']",
     "", 'damaged journal line'),
    ('the last attempt is scored', "    return attempts[0] if attempts else {'attempt': 1", "    return attempts[-1] if attempts else {'attempt': 1", 'joint-retry-fix'),
    ('units are not compared', "if units[a] == units[b] and _same_value(", "if _same_value(", 'separate-unit'),
    ('a returned text is dropped', "        if a.get('status') == 'format invalid':\n            returned", "        if False:\n            returned", 'format: the scoring packet'),
    ('format failures are not listed', "if a['attempt'] >= 2 or a.get('status') == 'format invalid'", "if a['attempt'] >= 2", 'format: the scoring packet'),
    ('a run takes several verdicts', "    if (out / 'verdict.json').exists() or (out / 'readings.json').exists():", "    if False:", 'one verdict',
     [("open(out / 'readings.json', 'xb')", "open(out / 'readings.json', 'wb')"), ("open(out / 'verdict.json', 'x')", "open(out / 'verdict.json', 'w')")]),
    ('replay does not compare', "    matches = same and summary == record['summary']", "    matches = True", 'one verdict'),
    ('a retry is sent before later first attempts', """                        if first['decision'] == 'refused':
                            refused.append((it, draw, first))""", """                        if first['decision'] == 'refused':
                            self.attempt(it, draw, it['user'] + RETRY_MARK + 'x', 2)""", 'before any retry'),
    ('completeness from the final attempts', "    scored = {k: first_attempt(v)['decision'] for k, v in results['finals'].items()}",
     "    scored = {k: v.get('decision') for k, v in results['finals'].items()}", 'leaves the scored test complete'),
    ('the returned text is cut', "raw=row[0] if row and row[0] else None)", "raw=row[0][:20000] if row and row[0] else None)", 'kept whole'),
    ('a null content is passed on', "    if isinstance(message.get('content'), str):\n        return message['content']", "    if True:\n        return message['content']",
     'null content'),
    ('a file is written before both render', "    attempts_text = render_attempts(out, key['attempts'])          # [47f.2] both rendered before anything is written",
     "    attempts_text = None", 'written only after both files render', [("        handle.write(attempts_text)", "        handle.write(render_attempts(out, key['attempts']))")]),
    ('records split on any line break', "        for number, line in enumerate(text.split('\\n'), 1):", "        for number, line in enumerate(text.splitlines(), 1):",
     'Unicode line separators'),
    ('retries share the scored journal', "        name = 'answers.jsonl' if line['attempt'] == 1 else 'retries.jsonl'", "        name = 'answers.jsonl'", 'damaged retry record'),
    ('a damaged retry makes the verdict incomplete', "                 if d.get('journal') == 'answers.jsonl']", "                 ]", 'damaged retry record'),
]


def build(folder, mutant):
    folder.mkdir(parents=True)
    gate = (HERE / 'paid_gate.py').read_text()
    gate = gate.replace('HERE = Path(__file__).resolve().parent', f'HERE = Path({str(HERE)!r})')
    if mutant:
        pairs = [(mutant[1], mutant[2])] + (mutant[4] if len(mutant) > 4 else [])
        for old, new in pairs:
            if gate.count(old) != 1:
                raise SystemExit(f'{mutant[0]}: the site occurs {gate.count(old)} times')
            gate = gate.replace(old, new)
    (folder / 'paid_gate.py').write_text(gate)
    rehearsal = (HERE / 'paid_rehearsal.py').read_text().replace(
        'HERE = Path(__file__).resolve().parent\nsys.path.insert(0, str(HERE))',
        f'HERE = Path({str(HERE)!r})\nsys.path.insert(0, str(HERE))\nsys.path.insert(0, {str(folder)!r})')
    (folder / 'paid_rehearsal.py').write_text(rehearsal)


def run(scratch, n, mutant):
    folder = scratch / f'm{n:02d}'
    build(folder, mutant)
    result = subprocess.run([sys.executable, str(folder / 'paid_rehearsal.py'), str(folder / 'work')], capture_output=True, text=True,
                            env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin', 'HOME': str(Path.home())})
    out = result.stdout + result.stderr
    (folder / 'output.txt').write_text(out)
    if mutant is None:
        return n, 'control', result.returncode == 0 and 'FAIL' not in out, out.strip().splitlines()[-1]
    failed = [l for l in out.splitlines() if l.startswith('FAIL') and mutant[3] in l]
    crash = 'Traceback' in out
    aborted = result.returncode != 0 and 'checks pass' not in out and not crash     # a scenario guard stopped the rehearsal
    last = out.strip().splitlines()[-1][:200]
    detail = failed[0][:110] if failed else (last if crash or aborted else 'not caught')
    prefix = '' if failed else ('crash: ' if crash else ('aborted: ' if aborted else ''))
    return n, mutant[0], bool(failed) or crash or aborted, prefix + detail


if __name__ == '__main__':
    scratch = Path(sys.argv[1])
    jobs = [(0, None)] + list(enumerate(MUTANTS, 1))
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = sorted(pool.map(lambda job: run(scratch, *job), jobs))
    for n, name, ok, detail in results:
        print(f'{"CAUGHT" if ok and n else ("PASS" if ok else "MISSED" if n else "CONTROL FAILS")}  {n:02d} {name}  {detail}')
    print(f'{sum(1 for n, _, ok, _ in results if n and ok)} of {len(MUTANTS)} mutants caught; control {"passes" if results[0][2] else "FAILS"}')
