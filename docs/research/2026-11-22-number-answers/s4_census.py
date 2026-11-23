"""Census: every stored v13s first reply (both blind tests) through the current checker and the rate-stop copy; print any change."""
import importlib.util, json, sys
from pathlib import Path
R = Path('/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers')
sys.path.insert(0, str(R)); sys.path.insert(0, '/Users/lchingen/hivemind/src')
import calc_small as cur
spec = importlib.util.spec_from_file_location('calc_fix', sys.argv[1]); fix = importlib.util.module_from_spec(spec); spec.loader.exec_module(fix)
import blind_test as bt
from hivemind import model
judged = changed = 0
for folder in ('judging-v13s-blind-2026-11-22', 'judging-v13s-blind2-2026-11-22'):
    out = Path('/Users/lchingen/hivemind/poc/data') / folder
    for name in bt.CASES:
        it = json.loads((out / name / 'item.json').read_text())
        for w in bt.WRITERS:
            data = bt.first_json((out / name / 'answers' / f'{w}.json').read_text())
            if model.check_schema(data, it['schema']):
                print(folder, name, w, 'schema error'); continue
            res = {}
            for label, mod in (('cur', cur), ('fix', fix)):
                calc = mod.from_answer(data, it['family'])
                r = mod.check(it['family'], it['passages'], calc)
                res[label] = (sorted(map(tuple, r['errors'])), mod.publish_decision(it['family'], calc, r))
            judged += 1
            s4 = [e for e in res['cur'][0] if e[0] == 'S4']
            flag = 'CHANGED' if res['cur'] != res['fix'] else 'same'
            changed += flag == 'CHANGED'
            print(f'{folder[-13:]:13} {name:5} {w:7} {flag:7} cur={res["cur"][1]} fix={res["fix"][1]} S4cur={s4} errs_fix={res["fix"][0]}'[:400])
print(f'judged {judged}, changed {changed}')
