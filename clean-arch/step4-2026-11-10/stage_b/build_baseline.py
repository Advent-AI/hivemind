"""The packets of the Stage B baseline reading ($0): the 159 stored judgements of the three unseeded replays, unaltered, with
nine control judgements: six planted wrong answers (two under each UNSUPPORTED test of the form) and three unaltered repeats.

Every judgement is read alone: a packet is a shuffled handful of judgements, no two of the same question, so that nothing in
a packet's shape tells a control from a stored judgement. The key is written outside the readers' folder.

  python3 clean-arch/step4-2026-11-10/stage_b/build_baseline.py reading <new data folder> <key path>
  python3 clean-arch/step4-2026-11-10/stage_b/build_baseline.py validation <new data folder> <key path>   # the planted answers, read before the reading
"""
import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stored_judgements  # noqa: E402

SEED = 20261111
PREVIOUS_STARTS, PREVIOUS_ENDS = '[Previous conclusion, for comparison only] ', '\n\nAnswer per the JSON schema'

# (draw, view, judgement number in the view, the form's test, the planted answer's changed fields, the request's previous conclusion
# when the plant is an answer that stays). Every judgement is read alone, so nothing else in a packet can contradict a plant.
PLANTED = [
    ('d3', 'v13', 7, 1, {'rung': 3, 'changed': True, 'why_changed': 'The forecast moves from rung 5 to rung 3 on the balance of the evidence in view.'}, None),
    ('d3', 'v7', 8, 1, {'rung': 2, 'changed': True, 'why_changed': 'The forecast moves from rung 1 to rung 2 on the balance of the evidence in view.'}, None),
    ('d2', 'v4', 7, 2, {
        'rung': 5,
        'implied_outcome': 'About $840 billion in calendar 2026: the four companies’ roughly $650 billion plan plus Google’s 2026 capital-expenditure guidance of up to $190 billion.',
        'reasons': 'The reference is the roughly $650 billion 2026 plan for the four hyperscalers, which sits in rung 3. The evidence now implies about $840 billion: Google’s guidance of up to $190 billion in 2026 capital expenditure is added to the $650 billion plan, which takes the total above the $800 billion boundary for rung 5. The $765 billion estimate covers broader AI infrastructure and the trillion-dollar forecasts refer to 2027, so neither is used; the overbuild and slower-agent signals are unquantified.',
        'changed': True,
        'why_changed': 'The forecast moves from rung 3 to rung 5: Google’s $190 billion guidance is counted in addition to the four-company plan, raising the implied total from about $650 billion to about $840 billion.'}, None),
    ('d1', 'v13', 6, 2, {
        'rung': 3,
        'implied_outcome': 'About $850 billion in 2027: NVIDIA’s projection of more than $1 trillion, less the roughly $150 billion of 2027 data-center spending that Microsoft and Meta have said they will defer to 2028.',
        'reasons': 'The reference is NVIDIA’s forecast that the big four hyperscalers’ 2027 data-center capex will exceed $1 trillion, which is rung 5. Microsoft and Meta have said they will defer about $150 billion of 2027 data-center spending to 2028, which takes the implied total to about $850 billion, in rung 3. The AWS GPU deployment plan spans 2027–2028 and does not offset the deferral; rack-cost estimates and tight computing capacity lean toward higher spending but do not establish a different total. The NVIDIA revenue dependency v2 is not yet judged and supplies no input.',
        'changed': True,
        'why_changed': 'The forecast moves from rung 5 to rung 3: the deferral of about $150 billion by Microsoft and Meta takes the implied 2027 total below $900 billion.'}, None),
    ('d2', 'v7', 9, 3, {
        'rung': 2,
        'reference': 'NVIDIA’s stated plan is to begin shipping Rubin systems in fall 2026, which sits at rung 1.',
        'implied_outcome': 'First shipments after December 31, 2026: delays across the Vera Rubin lineup have been reported and no shipment has been established, so the fall 2026 plan is taken to slip past the deadline.',
        'reasons': 'The reference is NVIDIA’s stated plan to begin shipping Rubin systems in fall 2026, which sits at rung 1. The forecast stays at rung 2: delays across the Vera Rubin lineup have been reported, and the statements that systems are in full production, that the roadmap is intact and that shipments will begin this fall are plans rather than shipments. No fact in the evidence establishes that any Rubin system has shipped, so shipment before December 31, 2026 is not established. Dependency v2 has no judged conclusion and supplies no constraint.',
        'changed': False,
        'why_changed': 'The rung remains 2. The newer statements repeat NVIDIA’s plan and its denial of a delay; none establishes a shipment.'},
     'rung 2; reasons: The reference is NVIDIA’s stated plan to begin shipping Rubin systems in fall 2026, which sits at rung 1. Delays across the Vera Rubin lineup have been reported, and no shipment has been established; the company’s statements that systems are in full production and will ship this fall are plans. The forecast is therefore rung 2. Dependency v2 has no judged conclusion and supplies no constraint.'),
    ('d2', 'v4', 9, 3, {
        'rung': 1,
        'reference': 'The stated plan is around $650 billion for the four hyperscalers in 2026; that is rung 3 ($600 billion to below $700 billion).',
        'implied_outcome': 'About $520 billion in calendar 2026: the roughly $650 billion four-company plan, held about 20% lower because it is a plan rather than reported spending and overbuild concerns have been raised.',
        'reasons': 'The reference is the roughly $650 billion 2026 plan for the four hyperscalers, which sits in rung 3. The forecast stays at rung 1: the $650 billion figure is a plan rather than reported spending, overbuild concerns and slower-than-expected progress in AI agents have been raised, and so the plan is not established; the estimate remains about 20% below it, at roughly $520 billion. Google’s and Meta’s figures are company-wide capex guidance rather than data-center-only amounts and cannot be added to the aggregate. The trillion-dollar forecasts refer to 2027.',
        'changed': False,
        'why_changed': 'The implied outcome remains about $520 billion, as in the previous conclusion. The updated evidence adds signals in both directions but no quantified change to the four-company 2026 estimate.'},
     'rung 1; reasons: The reference is the roughly $650 billion 2026 plan for the four hyperscalers, which sits in rung 3. The figure is a plan rather than reported spending and overbuild concerns have been raised, so it is not established; the implied outcome is held about 20% below it, at roughly $520 billion, in rung 1. Google’s $190 billion and Meta’s $125–145 billion figures are company-wide capex guidance, not data-center-only amounts.'),
]
REPEATED = [('d1', 'v8', 4), ('d2', 'v16', 6), ('d3', 'v18', 3)]      # unaltered; each is read twice
VALIDATION_STORED = [[('d1', 'v8', 2), ('d1', 'v18', 5), ('d3', 'v9', 7)], [('d3', 'v8', 6), ('d2', 'v18', 4), ('d1', 'v9', 3)]]


def as_item(view, judgement, answer=None, request=None):
    return {'question': view['question'], 'day': judgement['day'], 'request_as_sent': request or judgement['request_as_sent'],
            'answer': answer or judgement['answer'], 'not_shown': judgement['not_shown']}


def entry_of(kind, views, draw, view_id, number, answer=None, request=None):
    view = views[(draw, view_id)]
    return {'kind': kind, 'draw': draw, 'view': view_id, 'number': number, 'request_altered': request is not None,
            'item': as_item(view, view['judgements'][number - 1], answer, request)}


def planted_entries(views):
    out = []
    for draw, view_id, number, test, changes, previous in PLANTED:
        view = views[(draw, view_id)]
        judgement = view['judgements'][number - 1]
        answer = copy.deepcopy(judgement['answer'])
        answer.update(changes)
        answer['rung_label'] = next(rung['label'] for rung in view['rungs'] if rung['position'] == answer['rung'])
        if answer['rung'] == judgement['answer']['rung']:
            raise SystemExit('a planted answer keeps the stored rung')
        request = None
        if previous is not None:
            stored_request = judgement['request_as_sent']
            if stored_request.count(PREVIOUS_STARTS) != 1 or stored_request.count(PREVIOUS_ENDS) != 1:
                raise SystemExit('the request has no single previous-conclusion block to replace')
            head, rest = stored_request.split(PREVIOUS_STARTS)
            request = head + PREVIOUS_STARTS + previous + PREVIOUS_ENDS + rest.split(PREVIOUS_ENDS)[1]
        out.append(entry_of(f'planted test {test}', views, draw, view_id, number, answer, request))
    return out


def rendered(packets, views):
    """(the text of each packet file in order, the key) for packets given as lists of entries, under one numbering."""
    texts, key, number_in_all = [], {}, 0
    for packet_number, packet in enumerate(packets, start=1):
        rows = []
        for entry in packet:
            number_in_all += 1
            rows.append({'judgement': number_in_all, **entry['item']})
            view = views[(entry['draw'], entry['view'])]
            stored = view['judgements'][entry['number'] - 1]
            key[str(number_in_all)] = {'packet': packet_number, 'kind': entry['kind'], 'draw': entry['draw'], 'view': entry['view'], 'number_in_view': entry['number'],
                                       'judgement_id': stored['judgement_id'], 'day': stored['day'], 'shape': view['shape'], 'rung_count': len(view['rungs']),
                                       'stored_rung': stored['answer']['rung'], 'shown_rung': entry['item']['answer']['rung'], 'request_altered': entry['request_altered'],
                                       'last_of_view': entry['number'] == len(view['judgements'])}
        texts.append(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    return texts, key


def reading_packets(views, in_use):
    """The reading's packets, the same every time for the same stored runs and planted answers in use: every stored judgement,
    the planted answers that passed the trial and the three repeats, each read alone, no two of one question in a packet."""
    planted = [entry for entry in planted_entries(views) if (entry['draw'], entry['view'], entry['number']) in in_use]
    if len(planted) != len(in_use):
        raise SystemExit('planted-in-use.json names a planted answer the builder does not have')
    chooser = random.Random(SEED)
    entries = [entry_of('stored', views, draw, view_id, index + 1) for (draw, view_id), view in views.items() for index in range(len(view['judgements']))]
    entries += planted + [entry_of('repeated', views, *name) for name in REPEATED]
    by_question = {}
    for entry in entries:
        by_question.setdefault(entry['item']['question'], []).append(entry)
    packets = [[] for _ in range(max(len(members) for members in by_question.values()))]
    sizes = [0] * len(packets)
    chooser.shuffle(entries)
    for entry in sorted(entries, key=lambda entry: -len(entry['item']['request_as_sent'])):     # the longest first, each into the lightest packet without its question
        open_packets = [index for index, packet in enumerate(packets) if all(other['item']['question'] != entry['item']['question'] for other in packet)]
        lightest = min(open_packets, key=lambda index: (sizes[index], index))
        packets[lightest].append(entry)
        sizes[lightest] += len(entry['item']['request_as_sent'])
    for packet in packets:
        chooser.shuffle(packet)
    chooser.shuffle(packets)
    return packets


def validation_packets(views):
    """The six planted answers among six stored judgements of other questions, in two packets, read before the reading."""
    planted = planted_entries(views)
    chooser = random.Random(SEED)
    packets = [planted[0:3] + [entry_of('stored', views, *name) for name in VALIDATION_STORED[0]],
               planted[3:6] + [entry_of('stored', views, *name) for name in VALIDATION_STORED[1]]]
    for packet in packets:
        questions = [entry['item']['question'] for entry in packet]
        if len(set(questions)) != len(questions):
            raise SystemExit('a validation packet holds two judgements of one question')
        chooser.shuffle(packet)
    return packets


def main():
    mode, folder, key_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if key_path.resolve().is_relative_to(folder.resolve()):
        raise SystemExit('the key must sit outside the readers\' folder')
    views = {(view['draw'], view['view']): view for draw in stored_judgements.DRAWS for view in stored_judgements.views_of(draw)}
    if mode == 'validation':
        folder_name, packets = 'validation', validation_packets(views)
    elif mode == 'reading':
        in_use = {tuple(name) for name in json.loads((folder / 'planted-in-use.json').read_text())}      # written by plant_trial.py
        folder_name, packets = 'readers', reading_packets(views, in_use)
    else:
        raise SystemExit('the first argument is "reading" or "validation"')
    texts, key = rendered(packets, views)
    (folder / folder_name).mkdir(parents=True, exist_ok=False)
    for packet_number, text in enumerate(texts, start=1):
        (folder / folder_name / f'packet-{packet_number}.json').write_text(text)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    kinds = {}
    for entry in key.values():
        kinds[entry['kind']] = kinds.get(entry['kind'], 0) + 1
    characters = sorted(len(text) for text in texts)
    print(f'{len(packets)} packets, {len(key)} judgements: {kinds}; a packet holds {min(len(packet) for packet in packets)} to {max(len(packet) for packet in packets)} '
          f'judgements, no two of one question, and {characters[0] // 1000} to {characters[-1] // 1000} thousand characters (median {characters[len(characters) // 2] // 1000})')


if __name__ == '__main__':
    main()
