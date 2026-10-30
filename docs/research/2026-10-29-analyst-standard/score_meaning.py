"""Content layer of the standard's ruler (standard.md §11): reads the hand labels in labels-<set>.txt and structure.json and
adds them up. No judgement is made here; a cell without a label is refused (never defaulted), except an omitted item, which is
'absent' unless a label says otherwise.

Label file, one block per article (the reading sheet's order); a block may repeat (Luna first, Haiku later) and its lines merge:
  @ <call id or input id>
  <item id>  L1:<l> L2:<l> L3:<l> H1:<l> H2:<l> H3:<l>
      <l> = c correct | p partial | w wrong | - absent | k kept (optional items: no meaning judged) | x retained (exclude items)
      a trailing ! marks a material record issue (date invented, period or certainty changed); (text) is the reason
  + <draw>: <record id>><item id> ...   another cut of the item; the item's label on its line covers it
  + <draw>: <record id>:<u|r|o|j> ...    u material statement the reference lacks | r repeat of a kept item | o background a
                                         reader may keep | j junk;  rest:<u|r|o|j> labels every remaining unmatched record
  ? <n> L1:y L2:n ...                    must_propose number n (1-based) proposed in a form §6 accepts (y) or not (n)
  ! <draw>: <text>                       a candidate §6 rules out
Draws: L = gpt-6-luna, H = claude-haiku-5-5, 1..3 the draw.
"""
import collections
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
DRAWS = {'L1': 'luna-1', 'L2': 'luna-2', 'L3': 'luna-3', 'H1': 'haiku-1', 'H2': 'haiku-2', 'H3': 'haiku-3'}
MODELS = {'luna': ['L1', 'L2', 'L3'], 'haiku': ['H1', 'H2', 'H3']}
CELL = re.compile(r'([LH][123]):([cpwkx-])(!?)(?:\(([^)]*)\))?')


def parse(path):
    blocks, current = {}, None
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            current = blocks.setdefault(line[1:].strip(), {'items': {}, 'unmatched': collections.defaultdict(dict), 'rest': {},
                                                           'propose': {}, 'propose_dropped': {}, 'ruled_out': collections.defaultdict(list)})
        elif line.startswith('+'):
            draw, _, body = line[1:].strip().partition(':')
            for token in body.split():
                if token.startswith('rest:'):
                    current['rest'][draw.strip()] = token[5:]
                elif '>' in token:
                    rid, item = token.split('>')
                    current['unmatched'][draw.strip()][rid] = '>' + item
                else:
                    rid, kind = token.split(':')
                    current['unmatched'][draw.strip()][rid] = kind
        elif line.startswith('?d'):   # proposed in the raw answer, dropped by the production sift
            parts = line[2:].split()
            current['propose_dropped'].setdefault(int(parts[0]), {}).update(dict(p.split(':') for p in parts[1:]))
        elif line.startswith('?'):
            parts = line[1:].split()
            current['propose'].setdefault(int(parts[0]), {}).update(dict(p.split(':') for p in parts[1:]))
        elif line.startswith('!'):
            draw, _, text = line[1:].strip().partition(':')
            current['ruled_out'][draw.strip()].append(text.strip())
        else:
            item, _, cells = line.partition(' ')
            current['items'].setdefault(item, {}).update({m.group(1): {'label': m.group(2), 'material': bool(m.group(3)), 'why': m.group(4) or ''}
                                                          for m in CELL.finditer(cells)})
    return blocks


def main(label_set, version='', structure_path=None, labels_path=None, out_path=None):
    suffix = f'-{version}' if version else ''
    structure = json.loads(Path(structure_path or HERE / f'structure{suffix}.json').read_text())
    refs = json.loads((HERE / f'reference-{label_set}{suffix}.json').read_text())['articles']
    labels = parse(Path(labels_path or HERE / f'labels-{label_set}.txt'))
    problems = []
    tally = {m: collections.Counter() for m in MODELS}
    per_item_core = collections.defaultdict(dict)
    per_item_support = collections.defaultdict(dict)
    per_item_exclude = collections.defaultdict(dict)
    per_propose = collections.defaultdict(dict)
    per_propose_raw = collections.defaultdict(dict)
    junk_per_article = {m: collections.defaultdict(list) for m in MODELS}
    propose = {m: collections.Counter() for m in MODELS}
    ruled_out = collections.Counter()
    for art in refs:
        key = str(art.get('call_id', art['input_id']))
        block = labels.get(key)
        if block is None:
            problems.append(f'{key}: no label block')
            continue
        items = art.get('statements', []) + [dict(x, weight='exclude') for x in art.get('exclude', [])]
        for item in items:
            given = block['items'].get(item['id'], {})
            for model, draws in MODELS.items():
                for d in draws:
                    cell = structure['per_item'][f"{art['input_id']}|{item['id']}"][DRAWS[d]]
                    reassigned = any(v == '>' + item['id'] for v in block['unmatched'].get(d, {}).values())
                    if d in given:
                        lab = given[d]
                    elif cell['state'] == 'omitted' and not reassigned:
                        lab = {'label': '-', 'material': False, 'why': ''}
                    else:
                        problems.append(f"{key} {item['id']} {d}: {cell['state']} but no label")
                        continue
                    w = item['weight']
                    if w == 'optional' and lab['label'] == 'x':   # an exclude item made optional (v2, D231): retained means kept
                        lab = dict(lab, label='k')
                    tally[model][f'{w}:{lab["label"]}'] += 1
                    if lab['material']:
                        tally[model][f'{w}:material_issue'] += 1
                    if w == 'core':
                        per_item_core[(key, item['id'])][d] = lab['label'] == 'c' and not lab['material']
                    if w == 'supporting':
                        per_item_support[(key, item['id'])][d] = lab['label'] in ('c', 'p')
                    if w == 'exclude':
                        per_item_exclude[(key, item['id'])][d] = lab['label'] == 'x'
        for model, draws in MODELS.items():
            for d in draws:
                rest_rows = structure['unmatched'][art['input_id']][DRAWS[d]]
                named = block['unmatched'].get(d, {})
                junk = 0
                for r in rest_rows:
                    kind = named.get(r['id']) or block['rest'].get(d)
                    if kind is None:
                        problems.append(f"{key} {d} {r['id']}: unmatched record not labelled")
                        continue
                    if kind.startswith('>'):
                        kind = 'cut'
                    tally[model][f'unmatched:{kind}'] += 1
                    junk += kind == 'j'
                junk_per_article[model][key].append(junk)
        for n in range(1, len(art.get('must_propose', [])) + 1):
            if n not in block['propose']:
                problems.append(f'{key} propose {n}: no marks')
        for n, marks in block['propose'].items():
            if n > len(art.get('must_propose', [])):   # a must_propose the reference version no longer holds (v2)
                continue
            for model, draws in MODELS.items():
                for d in draws:
                    if d not in marks:
                        problems.append(f'{key} propose {n} {d}: no mark')
                    else:
                        propose[model][f'must_propose:{marks[d]}'] += 1
                        per_propose[(key, n)][d] = marks[d] == 'y'
                        per_propose_raw[(key, n)][d] = marks[d] == 'y' or block['propose_dropped'].get(n, {}).get(d) == 'y'
        for d, texts in block['ruled_out'].items():
            ruled_out[d] += len(texts)
    if problems:
        print('\n'.join(problems[:60]))
        print(f'{len(problems)} problems; nothing summed')
        sys.exit(1)
    summary = {}
    for model, draws in MODELS.items():
        core_pass = sum(all(v.get(d, False) for d in draws) for v in per_item_core.values())
        support_pass = sum(sum(v.get(d, False) for d in draws) >= 2 for v in per_item_support.values())
        art_junk = {k: sorted(v)[1] for k, v in junk_per_article[model].items()}
        failing_core = [f'{k}:{i}' for (k, i), v in per_item_core.items() if not all(v.get(d, False) for d in draws)]
        failing_support = [f'{k}:{i}' for (k, i), v in per_item_support.items() if sum(v.get(d, False) for d in draws) < 2]
        exclude_retained = {f'{k}:{i}': sum(v.get(d, False) for d in draws) for (k, i), v in per_item_exclude.items()}
        propose_every_draw = sum(all(v.get(d, False) for d in draws) for v in per_propose.values())
        propose_raw = sum(v.get(d, False) for v in per_propose_raw.values() for d in draws)
        propose_raw_every_draw = sum(all(v.get(d, False) for d in draws) for v in per_propose_raw.values())
        summary[model] = {'tally': dict(tally[model]), 'core_items': len(per_item_core), 'core_every_draw_correct': core_pass,
                          'supporting_items': len(per_item_support), 'supporting_two_of_three': support_pass,
                          'junk_median_per_article_sum': sum(art_junk.values()), 'propose': dict(propose[model]),
                          'ruled_out_candidates': sum(ruled_out[d] for d in draws),
                          'failing_core': failing_core, 'failing_supporting': failing_support,
                          'exclude_retained_draws': exclude_retained,
                          'must_propose_items': len(per_propose), 'must_propose_every_draw': propose_every_draw,
                          'must_propose_raw_marks_y': propose_raw, 'must_propose_raw_every_draw': propose_raw_every_draw}
    junk_cmp = {'haiku_articles_above_luna_median': sum(
        1 for k in junk_per_article['haiku'] if sorted(junk_per_article['haiku'][k])[1] > sorted(junk_per_article['luna'][k])[1])}
    out = {'set': label_set, 'summary': summary, 'junk_comparison': junk_cmp}
    Path(out_path or HERE / f'scores-{label_set}{suffix}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '')
