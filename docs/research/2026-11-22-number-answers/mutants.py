"""Mutants of calc_check.py: each disables one rule on a scratch copy; the gate must miss the item that exercises it, and the
unmutated control must pass. Harness-only. Usage: python3 mutants.py <scratch dir>  (writes the table to stdout)."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTANTS = [
    ('control (unmutated)', None, None, None),
    ('C4 path rule off', "bypass = [f for f in reachable(outcomes[view_id], stop=stop) if f not in stop and _key(figs[f]['what']) == want]",
     "bypass = []", 'R1b'),
    ('C5 one-choice rule off', "        if ('figure' in ref) == ('unavailable' in ref):", "        if False:", 'P3d'),
    ('scenario borrowing allowed', "            borrowed = sorted(r for r in upstream if r in stop and figs[r].get('scenario', 'base') != sc)", "            borrowed = []", 'R1bx4'),
    ('range summary not validated', "        if f['kind'] != 'estimate' or 'low' not in f or 'high' not in f or f['id'] not in outcome_ids or readers:", "        if False:", 'R1bx3'),
    ('prior status from label only', "        earlier = fig['kind'] == 'prior' or fig.get('basis') == 'prior_forecast' or 'pointer' in fig", "        earlier = fig['kind'] == 'prior'", 'P3e2'),
    ('prior as outcome allowed', "        if owners:                                    # [46h.2] nor the current outcome", "        if False:", 'P3e'),
    ('derived scenario rule off', "        other = derived(f['id']) - {sc}", "        other = set()", 'G2x2'),
    ('member scenario coverage off', "            if sp != sw:", "            if False:", 'R1sc'),
    ('changed ignores the rung', "    if answer['rung'] != previous['rung']:", "    if False:", 'CH2'),
    ('C9 per-scenario block off', "            if sc == 'range' or _key(figs[f]['what']) != later_key or figs[f]['basis'] != 'forecast':", "            if True:", 'G24c'),
    ('C9 scenario coverage off', "        if len(by_scenario) > 1 and later_scen != set(by_scenario):", "        if False:", 'G24d'),
    ('changed compares midpoints', "    if cur[2] != prev[2] or not near(cur[0], prev[0]) or not near(cur[1], prev[1]):",
     "    mids = lambda t: None if None in t[:2] else (t[0] + t[1]) / 2\n    if cur[2] != prev[2] or not near(mids(cur), mids(prev)):", 'CH4'),
    ('changed counts sibling sources', "    own = set()\n    for start in (answer.get('outcome'), (answer.get('reference') or {}).get('figure')):",
     "    own = set(figs)\n    for start in (answer.get('outcome'), (answer.get('reference') or {}).get('figure')):", 'CH3'),
    ('operand count unchecked', "            if not lo_n <= len(fig.get('inputs', [])) <= hi_n:", "            if False:", 'G24c3'),
    ('single-scenario citation allowed', "        if earlier_nodes and not later_scen:", "        if False:", 'G4c'),
    ('signs unchecked', "            if signs is not None and (fig['operation'] not in ('sum', 'roll_forward') or len(signs) != len(fig.get('inputs', []))", "            if False and (fig['operation'] not in ('sum', 'roll_forward') or len(signs) != len(fig.get('inputs', []))", 'G24s0'),
    ('C9 sensitivity off', "                if abs(after - before) <= 1e-9 * max(1.0, abs(before)):", "                if False:", 'G24x'),
    ('C9 sensitivity on intervals (46o code)', "                if abs(after - before) <= 1e-9 * max(1.0, abs(before)):",
     "                b2, a2 = _evaluate(figs, refs, {})[f], _evaluate(figs, refs, {target: tuple(x * 1.1 for x in _interval(figs[target]))})[f]\n"
     "                if abs(a2[0] - b2[0]) <= 1e-9 * max(1.0, abs(b2[0])) and abs(a2[1] - b2[1]) <= 1e-9 * max(1.0, abs(b2[1])):", 'G4x2'),
    ('numbers unchecked', "        if has_value == has_range or (has_range and fig['low'] > fig['high']):", "        if False:", 'G24nv'),
    ('rung range unchecked', "        if not isinstance(rung, int) or isinstance(rung, bool) or not 1 <= rung <= len(member['bands']):", "        if rung is None:", 'R1rneg'),
    ('C6 ignores bounds', "        shown = _outcome_set(out)", "        shown = (_interval(out)[0], True, _interval(out)[1], True)", 'R4b2'),
    ('minus sign ignored in bounds', "        dirs = [FLIP[d] if k < 0 else d for d, k in zip(dirs, signs)]", "        dirs = dirs", 'R2b2b'),
    ('overlap alternate drops bounds', "            side = _bound_direction(fig['operation'], [figs[i] for i in keep], signs)      # [46u.1] the retained operands' bounds",
     "            side = None", 'R2b1'),
    ('opposing bounds merged', "    if 'mixed' in found or {'lower', 'upper'} <= found:     # [46v] opposing bounds leave the result unbounded", "    if False:", 'R2m'),
    ('repeated operands not netted', "    kept = [i for i in dict.fromkeys(ids) if net[i] != 0]\n    return kept, [net[i] for i in kept]",
     "    return ids, fig.get('signs')", 'R2rev'),
    ('C3 ambiguity allowed', "                    if len(hits) > 1:                 # [46x.1] one forecast per member quantity, period and scenario", "                    if False:", 'R1amb'),
    ('difference x - x not netted', "    if fig.get('operation') == 'difference' and len(ids) == 2 and ids[0] == ids[1]:", "    if False:", 'R2rev2'),
    ('algebraic zero tolerant', "        if not ins and (lo != 0 or hi != 0):              # [46y.2] an algebraic zero is exactly zero", "        if False:", 'R2z'),
    ('C9 accepts any earlier node', "            by_scenario = {figs[e_out].get('scenario', 'base'): [e_out]}", "            by_scenario = {figs[e_out].get('scenario', 'base'): sorted(earlier_nodes)}", 'G4b2'),
    ('declared values kept after checks', "        if fig['kind'] == 'computed' and fig.get('operation') in OPERATIONS:\n            (lo_r, hi_r), b_r = recomputed[fid]",
     "        if False:\n            (lo_r, hi_r), b_r = recomputed[fid]", 'R1canon'),
    ('changed reads the declared outcome', "    if out['kind'] == 'computed':                     # [46aa] the same recomputed outcome publication uses", "    if False:", 'CH5'),
    ('changed ignores the bound', "    if cur[2] != prev[2] or not near(cur[0], prev[0]) or not near(cur[1], prev[1]):", "    if not near(cur[1], prev[1]) and cur[1] is not None:", 'CH6'),
    ('source identity drops the component', "    return sorted(f'{figs[f][\"evidence\"]}|{figs[f][\"expression\"]}|{figs[f].get(\"component\", \"value\")}' for f in own if figs[f]['kind'] == 'source')",
     "    return sorted(f'{figs[f][\"evidence\"]}|{figs[f][\"expression\"]}' for f in own if figs[f]['kind'] == 'source')", 'CH7'),
    ('unresolved not routed first', "    if answer.get('shape') == 'unresolved' or was_unresolved:          # [46ac.2] an unresolved answer is routed before any number", "    if False:", 'CH8'),
    ('C3 off', "                if p and w and _exceeds(_outcome_set(p), _outcome_set(w)):          # [46s] open and closed ends kept", "                if False:", 'R1a'),
    ('crossings ignore open ends', "    return hi < edge or (hi == edge and not hi_c)", "    return hi < edge", 'R4b3'),
    ('C3 bounds use paired ends', "    if inf in (abs(plo), abs(phi), abs(wlo), abs(whi)):", "    if False:", 'R1qc'),
    ('C3 impossibility ignores open ends', "        return plo > whi + 1e-9 or (abs(plo - whi) <= 1e-9 and not (plc and whc))", "        return plo > whi + 1e-9", 'R1qb'),
    ('bounds dropped in recomputation', "            values[fid] = (interval, bound)", "            values[fid] = (interval, None)", 'R4one'),
    ('C1 accepts any substring (alone)', "matches = [e for e in extract(passage['text']) if e['text'] == fig.get('expression')]",
     "matches = [e for e in extract(passage['text']) if fig.get('expression') in e['text']]", 'T9'),
    ('C5 allows estimates', "if any(n['kind'] in ('estimate', 'prior') or n['basis'] in ('forecast', 'prior_forecast') for n in nodes):",
     "if any(n['kind'] == 'prior' for n in nodes):", 'P3b'),
    ('per-unit identity ignores scope', "same = all((i['what']['population'], i['what']['scope']) == (out['population'], out['scope']) for i in ins)",
     "same = True", 'P4'),
    ('per-unit inverse loses its scale', "            lo, hi = lo / 1e9, hi / 1e9", "            pass", 'G3inv'),
    ('C2 tolerance 50%', "return abs(declared - expected) <= max(0.005 * abs(expected), floor)",
     "return abs(declared - expected) <= max(0.5 * abs(expected), floor)", 'P2'),
    ('bound direction ignored', "        elif want is not None and have != want:", "        elif want is not None and have is None:", 'R4m'),
    ('C9 same base off (both clauses)', "        if rel['type'] != 'same_base' or rel['later'] not in outcomes", "        if True or rel['later'] not in outcomes", 'G4m'),
    ('C10 prior not authenticated', "        if ans_prior.get('day') != ptr.get('day') or not any(_same(fig.get('value'), v) for v in ans_prior.get('values', [])):",
     "        if False:", 'P3c'),
]


NOTE = "All rules have a mutant; none is left unexercised."


def main(scratch):
    scratch = Path(scratch)
    src = (HERE / 'calc_check.py').read_text()
    gate = (HERE / 'gate.py').read_text().replace('REPO = HERE.parents[2]', f"REPO = Path('{HERE.parents[2]}')")
    print('mutant | expected miss | result')
    failed = 0
    for name, old, new, target in MUTANTS:
        if old is not None and src.count(old) != 1:
            print(f'{name} | {target} | MUTATION SITE NOT FOUND ONCE')
            failed += 1
            continue
        folder = scratch / name.replace(' ', '_').replace('(', '').replace(')', '')
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'calc_check.py').write_text(src if old is None else src.replace(old, new))
        (folder / 'gate.py').write_text(gate.replace('HERE = Path(__file__).resolve().parent', f"HERE = Path('{folder}')"))
        run = subprocess.run([sys.executable, 'gate.py'], cwd=folder, capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        misses = run.stdout.split('misses:')[-1].strip().splitlines()[0] if 'misses:' in run.stdout else f'no output: {run.stderr.strip()[-200:]}'
        if target is None:
            ok = run.returncode == 0
            print(f'{name} | none | {"PASS" if ok else "BROKEN"} ({misses})')
        else:
            ok = run.returncode == 1 and f"'{target}'" in misses
            print(f'{name} | {target} | {"CAUGHT" if ok else "NOT CAUGHT"} ({misses})')
        failed += not ok
    print(NOTE)
    shutil.rmtree(scratch, ignore_errors=True)
    return 1 if failed else 0


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        raise SystemExit('usage: mutants.py <scratch dir>')
    raise SystemExit(main(sys.argv[1]))
