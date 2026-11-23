"""The packets of Stage B's reading ($0; `STAGE_B_READING.md`): every judgement the frozen judge made in Stage B's three draws, six
planted answers written on Stage B's own judgements (two under each of the form's tests, of Stage B's shapes and wording, used
only after a trial shows both families call them UNSUPPORTED with the stored rung), and three repeats of Stage B judgements drawn
with a fixed seed. Every judgement is read alone, in shuffled packets with no two judgements
of one question, as in the baseline (`build_baseline.py`, whose functions this reuses); here a packet holds one draw's judgements. The key is written outside the readers'
folder.

  python3 clean-arch/step4-2026-11-10/stage_b/build_stage_b.py validation <new data folder> <key path>   # the trial of the planted answers
  python3 clean-arch/step4-2026-11-10/stage_b/build_stage_b.py reading <data folder> <key path> <trial key path>   # only after the trial passed
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_baseline  # noqa: E402
import stored_judgements  # noqa: E402

SEED = 20261112
REPEATS = 3
MOST_CHARACTERS_A_PACKET = 110_000          # of requests, about the baseline's packet

# (draw, view, judgement number, the form's test, the changed fields, and for an answer that stays the previous judgement's reasons,
# which the request shows as the judge shows them: "rung N; reasons: " and the first 800 characters, src/hivemind/views/judging.py)
PLANTED = [
    ('u2', 'v2', 10, 1, {
        'rung': 3, 'changed': True,
        'why_changed': 'The forecast moves to rung 3: the stand-alone CPU forecast and the Perplexity adoption add support, but no item confirms that a first Vera Rubin shipment has been made, so the shipment is treated as unconfirmed at the deadline.'}, None),
    ('u1', 'v4', 6, 1, {
        'rung': 1, 'changed': True,
        'why_changed': 'The forecast moves to rung 1: the AWS plan for 2 million additional GPUs spans 2027 and 2028 with no annual split, and the delayed-project and resale risks weigh on the 2027 total.'}, None),
    ('u2', 'v4', 7, 2, {
        'rung': 5,
        'implied_outcome': 'About $840 billion for calendar 2026: the roughly $650 billion four-company plan plus Google’s up-to-$190 billion 2026 capital-expenditure guidance.',
        'reasons': 'The market reference is the reported plan of around $650 billion for 2026, which sits in rung 3. The evidence now implies about $840 billion: Google’s guidance of up to $190 billion of 2026 capital expenditure is added to the $650 billion plan, which takes the total above the $800 billion floor of rung 5. The $765 billion estimate covers broader AI infrastructure and the trillion-dollar forecasts refer to 2027, so neither is used; cost and demand indicators lean upward, while project delays lean downward, without a quantified adjustment.',
        'changed': True,
        'why_changed': 'The forecast moves from rung 3 to rung 5: Google’s up-to-$190 billion guidance is counted in addition to the four-company plan.'}, None),
    ('u1', 'v7', 6, 2, {
        'rung': 1,
        'implied_outcome': 'About $74 billion at FY2027 year-end: the $119 billion of commitments in Q1 FY2027 less the roughly $45 billion of supply commitments NVIDIA has said it will cancel before the fiscal year ends.',
        'reasons': 'The reference is the cited $119 billion supply-commitment amount, which is in rung 3 ($100 billion to below $140 billion). NVIDIA has said it will cancel roughly $45 billion of its supply commitments before the fiscal year ends, which brings the outstanding total to about $74 billion, below the $80 billion floor of rung 2. The named multi-gigawatt customers support continuing demand, but no item adds new commitments to offset the cancellation.',
        'changed': True,
        'why_changed': 'The forecast moves from rung 3 to rung 1: the stated cancellation of about $45 billion of commitments takes the total below $80 billion.'}, None),
    ('u3', 'v3', 9, 3, {
        'rung': 3,
        'implied_outcome': 'No confirmation of a first shipment is expected to be on record by December 31, 2026: the fall-2026 plan and Morgan Stanley’s Q3 schedule are forecasts, and no item confirms that any Vera Rubin system has shipped.',
        'reasons': 'The reference is NVIDIA’s fall-2026 shipment schedule, which sits at rung 1. The forecast stays at rung 3: rung 1 requires a confirmation that first shipments have begun, and the evidence holds only plans and schedules (the fall-2026 plan, Morgan Stanley’s Q3 schedule, the full-production statements), none of which confirms a shipment. Until such a confirmation is in the evidence, rung 1 is not established, and no post-July 2 decision deferring the platform supports rung 2, so neither rung holds.',
        'changed': False,
        'why_changed': 'The rung remains 3. The Vera CPU and Perplexity adoption items and the repeated roadmap statements add no confirmation of a first shipment.'},
     'The reference is NVIDIA’s plan for Rubin systems to begin shipping in fall 2026, which sits at rung 1; Morgan Stanley’s Q3 first-shipment schedule with a Q4 volume ramp points the same way. The systems are reported in full production and scheduled to ship to eight cloud partners, and NVIDIA says its roadmap is intact, with the delay report concerning Rubin Ultra/Kyber rather than the initial 2026 Rubin systems. But these are schedules, not confirmation that shipments have begun, and rung 1 holds only on a confirmation of first shipments. Until a confirmation is in the evidence, rung 1 is not established; with no post-July 2 decision deferring the first Vera Rubin shipments as a whole, rung 2 does not hold either, so the forecast is rung 3.'),
    ('u2', 'v4', 3, 3, {
        'rung': 2,
        'implied_outcome': 'About $555 billion for calendar 2026: the roughly $650 billion four-company plan reduced by about 15%, since spending plans of this size are seldom met in full.',
        'reasons': 'The reference is the reported plan of around $650 billion for 2026, which sits in rung 3. The forecast stays at rung 2: plans of this size are seldom spent in full within the year, so the plan is taken about 15% lower, at roughly $555 billion. The new Google figure is guidance for total capital expenditure, not a data-center-only amount, and NVIDIA’s more-than-$1-trillion projection is for 2027; neither changes the 2026 total.',
        'changed': False,
        'why_changed': 'The rung remains 2. Google’s up-to-$190 billion guidance is total capital expenditure and does not change the four-company data-center estimate.'},
     'The reference is around $650 billion, which sits in rung 3. The specific 2026 plan and NVIDIA’s projected 2026 figure both remain around $650 billion; NVIDIA’s projection of more than $1 trillion is for 2027, so it does not quantify a 2026 increase. Plans of this size are seldom spent in full within the year, so the forecast takes the plan about 15% lower, near $555 billion, in rung 2. Higher projected rack costs and reports of delayed projects give opposing directional risks, but neither establishes a further change large enough to cross a rung boundary.'),
]
# The trial's two packets: three planted answers and three stored judgements each, no two of one matter in a packet (the three
# draws word one matter differently, so this is set by hand: packet 1 holds Vera Rubin, 2026 capital expenditure, supply
# commitments, China's H200 imports, the French inquiry and custom silicon; packet 2 holds Vera Rubin, 2026 and 2027 capital
# expenditure, the French inquiry, China's H200 sales and HBM capacity).
TRIAL_PACKETS = [[('planted', 'u2', 'v2', 10), ('planted', 'u2', 'v4', 7), ('planted', 'u1', 'v7', 6),
                  ('stored', 'u1', 'v11', 3), ('stored', 'u2', 'v9', 2), ('stored', 'u1', 'v8', 5)],
                 [('planted', 'u3', 'v3', 9), ('planted', 'u2', 'v4', 3), ('planted', 'u1', 'v4', 6),
                  ('stored', 'u3', 'v9', 3), ('stored', 'u3', 'v5', 6), ('stored', 'u3', 'v10', 2)]]


def planted_entries(views):
    """The planted answers as packet entries: the stored judgement with its answer changed, and its request's previous conclusion
    rewritten when the plant is an answer that stays (the same mechanics as the baseline's, build_baseline.planted_entries)."""
    import copy
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
            if stored_request.count(build_baseline.PREVIOUS_STARTS) != 1 or stored_request.count(build_baseline.PREVIOUS_ENDS) != 1:
                raise SystemExit('the request has no single previous-conclusion block to replace')
            head, rest = stored_request.split(build_baseline.PREVIOUS_STARTS)
            block = f"rung {answer['rung']}; reasons: {previous[:800]}"            # as the frozen judge renders it
            request = head + build_baseline.PREVIOUS_STARTS + block + build_baseline.PREVIOUS_ENDS + rest.split(build_baseline.PREVIOUS_ENDS)[1]
        out.append(build_baseline.entry_of(f'planted test {test}', views, draw, view_id, number, answer, request))
    return out


def all_views():
    """Stage B's views keyed (u1, v3) …"""
    return {(view['draw'], view['view']): view for draw, folder in stored_judgements.stage_b_folders().items()
            for view in stored_judgements.views_of(draw, folder)}


def validation_packets(views):
    planted = {(entry['draw'], entry['view'], entry['number']): entry for entry in planted_entries(views)}
    chooser = random.Random(SEED)
    packets = [[planted[(draw, view_id, number)] if kind == 'planted' else build_baseline.entry_of('stored', views, draw, view_id, number)
                for kind, draw, view_id, number in members] for members in TRIAL_PACKETS]
    if sorted(tuple(key) for members in TRIAL_PACKETS for kind, *key in members if kind == 'planted') != sorted(planted):
        raise SystemExit('the trial packets do not hold each planted answer once')
    for packet in packets:
        chooser.shuffle(packet)
    return packets


def stage_b_packets(views, in_use):
    stored = [build_baseline.entry_of('stored', views, draw, view_id, index + 1) for (draw, view_id), view in views.items()
              if draw.startswith('u') for index in range(len(view['judgements']))]
    chooser = random.Random(SEED)
    repeats = [build_baseline.entry_of('repeated', views, entry['draw'], entry['view'], entry['number'])
               for entry in chooser.sample(sorted(stored, key=lambda e: (e['draw'], int(e['view'][1:]), e['number'])), REPEATS)]
    planted = [entry for entry in planted_entries(views) if (entry['draw'], entry['view'], entry['number']) in in_use]
    if len(planted) != len(in_use):
        raise SystemExit('planted-in-use.json names a planted answer the builder does not have')
    entries = stored + planted + repeats
    chooser.shuffle(entries)
    packets = []
    for draw in sorted({entry['draw'] for entry in entries}):
        # A packet holds one draw's judgements, at most one of each of its views: the three draws word one matter differently,
        # so packets that mixed draws could hold two versions of one matter, which an exact-text rule would not see.
        members = [entry for entry in entries if entry['draw'] == draw]
        by_view = {}
        for entry in members:
            by_view.setdefault(entry['view'], []).append(entry)
        total = sum(len(entry['item']['request_as_sent']) for entry in members)
        count = max(max(len(group) for group in by_view.values()), -(-total // MOST_CHARACTERS_A_PACKET))
        draw_packets, sizes = [[] for _ in range(count)], [0] * count
        for entry in sorted(members, key=lambda entry: -len(entry['item']['request_as_sent'])):
            open_packets = [index for index, packet in enumerate(draw_packets) if all(other['view'] != entry['view'] for other in packet)]
            lightest = min(open_packets, key=lambda index: (sizes[index], index))
            draw_packets[lightest].append(entry)
            sizes[lightest] += len(entry['item']['request_as_sent'])
        packets += draw_packets
    for packet in packets:
        chooser.shuffle(packet)
    chooser.shuffle(packets)
    return packets


def main():
    mode, folder, key_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if key_path.resolve().is_relative_to(folder.resolve()):
        raise SystemExit('the key must sit outside the readers\' folder')
    views = all_views()
    if mode == 'validation':
        name, packets = 'validation', validation_packets(views)
    elif mode == 'reading':
        import stage_b_trial
        derived, problems = stage_b_trial.trial_result(folder, json.loads(Path(sys.argv[4]).read_text()))
        if problems:
            raise SystemExit('the trial has not passed, so the reading packets are not built: ' + '; '.join(problems[:5]))
        if json.loads((folder / 'planted-in-use.json').read_text()) != derived:
            raise SystemExit('planted-in-use.json is not the trial\'s result, so the reading packets are not built')
        name, packets = 'readers', stage_b_packets(views, {tuple(entry) for entry in derived})
    else:
        raise SystemExit('the first argument is "validation" or "reading"')
    texts, key = build_baseline.rendered(packets, views)
    (folder / name).mkdir(parents=True, exist_ok=False)
    for number, text in enumerate(texts, start=1):
        (folder / name / f'packet-{number}.json').write_text(text)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    kinds = {}
    for entry in key.values():
        kinds[entry['kind']] = kinds.get(entry['kind'], 0) + 1
    sizes = sorted(len(text) for text in texts)
    print(f'{len(texts)} packets, {len(key)} judgements: {kinds}; {sizes[0] // 1000} to {sizes[-1] // 1000} thousand characters a packet')


if __name__ == '__main__':
    main()
