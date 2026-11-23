"""Mutants of calc_small.py (AGENTS §4): each disables one rule on a scratch copy; small_cases.py must fail on every mutant while the
unmutated control passes. Usage: python3 small_mutants.py <scratch folder>"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
M = [
    ('S1 value', "            ok = _same(f.get('value'), parsed['value'])\n", "            ok = True\n"),
    ('S1 qualifier', "        if q not in written:\n", "        if False:\n"),
    ('S1 estimated qualifier [D745]', "'below', 'under', 'near', 'estimated'], key=len", "'below', 'under', 'near'], key=len"),
    ('S1 whole expression', "        starts = [(s, e) for s, e in spans if text[s:e] == qn]", "        starts = [(m.start(), m.end()) for m in re.finditer(re.escape(qn), text)]"),
    ('S1 sign kept', "            return {'unit': '%', 'value': (-1.0 if g[0] else 1.0) * _num(g[1])}", "            return {'unit': '%', 'value': _num(g[1])}"),
    ('S1 passage', "            errors.append(('S1', f'{fid}: \"{qn}\" is part of the longer expression", "            (lambda *args: None)(('S1', f'{fid}: \"{qn}\" is part of the longer expression"),
    ('S2 arithmetic', "        if not ok:\n            declared =", "        if False:\n            declared ="),
    ('S2 money times percent', "        if money + pct > 1:", "        if money > 1 or pct > 1:"),
    ('S2 zero divisor', "            if denominator[0] <= 0 <= denominator[1]:", "            if False:"),
    ('S2 share range', "        if op == 'share' and not (0 <= got[ins[1]][0] and got[ins[1]][1] <= 100):", "        if False:"),
    ('S2 one value on every path', "            return _apply(f['operation'], [self.point(i, assign) for i in f['inputs']])",
     "            return _apply(f['operation'], [self.point(i, {}) if self.figs[i].get('kind') == 'computed' else self.point(i, assign) for i in f['inputs']])"),
    ('S2 zero inside a straddling range', "        return sorted({lo, hi} | ({0.0} if lo < 0 < hi else set()))", "        return sorted({lo, hi})"),
    ('S3 part above whole', "            if not calc.fits(part, whole):", "            if False:"),
    ('S3 linked ranges', "        shared = lp & lw\n", "        shared = set()\n"),
    ('S4 two forecasts', "        if len(ids) > 1:\n            errors.append(('S4'", "        if False:\n            errors.append(('S4'"),
    ('S4 adopted only', "        if k not in keys:\n            tops.add(fid)", "        if True:\n            tops.add(fid)"),
    ('S4 bypass', "            if bypass:\n", "            if False:\n"),
    ('S4 bypass walks inputs only [D742]', "                stack.extend(f.get('inputs') or [])", "                stack.extend((f.get('inputs') or []) + (f.get('rests_on') or []))"),
    ('S5 estimate under reference', "            if any(figs[g]['kind'] == 'estimate' for g in chain):", "            if False:"),
    ('S5 forecast under reference', "            elif any(figs[g]['basis'] == 'forecast' for g in chain):", "            elif False:"),
    ('S5 outside source', "            elif not any(figs[g]['kind'] == 'source' and figs[g]['basis'] in EXTERNAL for g in chain):", "            elif False:"),
    ('S5 one choice', "            else:\n                errors.append(('S5', f'{v}: needs exactly one", "            elif False:\n                errors.append(('S5', f'{v}: needs exactly one"),
    ('S6 rung holds outcome', "        if interval is not None and not _overlaps_band(", "        if False and not _overlaps_band("),
    ('S6 own forecast', "        if out['kind'] not in ('computed', 'estimate') or out['basis'] != 'forecast':", "        if False:"),
    ('S6 one outcome marker', "                errors.append(('S6', f'{v}: {len(outs)} figures are marked", "                (lambda *args: None)(('S6', f'{v}: {len(outs)} figures are marked"),
    ('S6 outcome key', "        if _key(out['what']) != _key(member['what']):", "        if False:"),
    ('S7 cycle', "    if any(cyclic(fid) for fid in figs):", "    if False:"),
    ('S7 value or range', "            errors.append(('S7', f'{fid}: a figure has value, or low and high", "            (lambda *args: None)(('S7', f'{fid}: a figure has value, or low and high"),
    ('S7 source basis', "            if f['basis'] == 'forecast':\n                errors.append(('S7', f'{fid}: a source cannot", "            if False:\n                errors.append(('S7', f'{fid}: a source cannot"),
    ('S7 unresolved shape', "            if outs or refs or reason or a.get('rung') is not None or not _text(a.get('why')):", "            if False:"),
    ('S7 rests_on estimates only', "        if kind != 'estimate' and f.get('rests_on'):", "        if False:"),
    ('S7 inputs computed only', "        if kind != 'computed' and (f.get('inputs') or f.get('operation')):", "        if False:"),
    ('S7 finite numbers', "        if any(not math.isfinite(n) or abs(n) > LIMIT for n in numbers):", "        if False:"),
    ('S8 part into whole', "                if any(_overlap(p['what']['period'], w['what']['period']) for p in parts for w in wholes):", "                if False:"),
    ('S8 overlap only', "                if any(_overlap(p['what']['period'], w['what']['period']) for p in parts for w in wholes):", "                if True:"),
    ('S8 remainder same period', "                      and ins[0]['what']['period'] == ins[1]['what']['period'] == f['what']['period']\n", "\n"),
    ('S8 one period once', "        if f['operation'] == 'sum' and len(set(inputs_periods)) < len(inputs_periods):", "        if False:"),
    ('S8 periods', "        if not ok:\n            sign =", "        if False:\n            sign ="),
    ('S8 period spelling', "            errors.append(('S8', f'{fid}: when periods of one quantity", "            (lambda *args: None)(('S8', f'{fid}: when periods of one quantity"),
    ('D740 from-to is a change', "                if before.endswith('from') and not re.search(", "                if False and not re.search("),
    ('D741 carried share', "                if carried:\n", "                if False:\n"),
    ('recorded conversion', "            if any(_quantity(i['what']) != _quantity(f['what']) for i in money) and f['operation'] != 'share':", "            if False:"),
]


def run(folder):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(REPO / 'src'), CALC_SMALL_DIR=str(folder))
    r = subprocess.run([sys.executable, '-B', str(HERE / 'small_cases.py')], capture_output=True, text=True, env=env)
    out = r.stdout + r.stderr
    if 'calc_small' in out and str(folder) not in subprocess.run([sys.executable, '-B', '-c', 'import calc_small, sys; print(calc_small.__file__)'],
                                                                  capture_output=True, text=True, env=dict(env, PYTHONPATH=f'{folder}:{REPO / "src"}')).stdout:
        raise SystemExit('the scratch calc_small.py was not the one imported')
    return r.returncode, out


def main(scratch):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    source = (HERE / 'calc_small.py').read_text()
    results = []
    for name, old, new in [('control', None, None)] + M:
        folder = scratch / name.replace(' ', '-')
        folder.mkdir(parents=True)
        shutil.copy(HERE / 'calc_small.py', folder / 'calc_small.py')
        if old is not None:
            if source.count(old) != 1:
                raise SystemExit(f'mutant {name}: the site occurs {source.count(old)} times')
            (folder / 'calc_small.py').write_text(source.replace(old, new))
        code, out = run(folder)
        (folder / 'output.txt').write_text(out)
        crashed = 'Traceback' in out
        caught = code != 0 and not crashed                 # a crash is not a catch until its traceback is read (AGENTS §4)
        ok = (code == 0 and not crashed) if old is None else caught      # [54] a crashing control is a failure
        first = next((l for l in out.splitlines() if l.startswith('FAIL') or 'Traceback' in l), '')
        results.append(ok)
        print(f'{"PASS" if ok else "FAIL"}  {name}: ' + ('control passes' if old is None and ok else
              ('caught: ' + first[:160] if caught else ('CRASHED (read output.txt)' if crashed else 'NOT CAUGHT'))))
    print(f'{sum(results)} of {len(results)} as expected (control + {len(M)} mutants)')
    return 0 if all(results) else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
