"""Step 2 comparison with Jev over stored items: one request per incoming item, one `choice` question per earlier candidate.

Arms:
  J0  the existing piece question as written ("already under the same thesis"), production's state line.
  J1  the same criteria (views/jev_matching.PIECES) with the premise removed: the stored piece is earlier evidence of the same company and
      may sit under a different research question; both sides carry tier, original party, reporting speaker, statement date, period.
  J2  J0 with one change: same_statement holds only when the incoming piece adds nothing an analyst would keep; a retelling that adds a
      figure, date, party, condition or a qualification that changes the claim is a separate choice, same_with_new_fact.
Sets:
  labelled   the reference v2 pairs (incoming = later, candidate = earlier), whatever retrieval found;
  retrieved  each association's R1 top 10;
  merges     the pairs the forward simulation merged (forward-sim.json).
`--dry-run` counts requests and input characters without sending. Answers are archived in the output folder.

Usage: jev_compare.py <folder> <labelled|retrieved> <J0|J1> [--dry-run]"""
import concurrent.futures, hashlib, json, sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, jev, model  # noqa: E402
from hivemind.views import jev_matching  # noqa: E402

SETTING = config.Setting('step2-validation', 'jev-1.14.0', 'step2-validation', None, 0)


def j0_state(it):
    return (f"INCOMING PIECE [{it['tier']}; {it['reporting_speaker']}; original source {it['original_party']}, stated "
            f"{it['statement_date'] or it['statement_date_text'] or 'unknown'}] {it['summary']} | quote: {' '.join(it['passages'])[:600]}")


def j1_text(it, label):
    return (f"{label} [tier {it['tier']}; original party {it['original_party'] or 'unknown'}; reported by {it['reporting_speaker'] or 'unknown'}; "
            f"stated {it['statement_date'] or it['statement_date_text'] or 'unknown'}; period {it['evidence_period'] or 'unknown'}; "
            f"article {it['publication_date']}] {it['summary']} | quote: {' '.join(it['passages'])[:600]}")


PIECES_J2 = {
    'same_statement': ('the same evidence and nothing new: a retelling, the same number in text and in a table or another document, or the same '
                       'speaker repeating the same statement, where the incoming piece adds no fact an analyst would keep; wording, precision '
                       'and outlet may differ'),
    'same_with_new_fact': ('the same statement, but the incoming piece also carries a fact the stored piece lacks that an analyst would keep: a '
                           'figure, date, party, condition or scope, a qualification that changes what the claim means (for example sales '
                           'rather than orders, deployed rather than expected), or a further statement; background an analyst following the '
                           'company already knew and wording do not count'),
    'supersedes': jev_matching.PIECES['supersedes'],
    'different': jev_matching.PIECES['different']}


def question(arm, earlier):
    if arm == 'J2':
        return dict(jev_matching.piece_question(j0_state(earlier).replace('INCOMING PIECE', 'STORED PIECE', 1)), criteria=PIECES_J2)
    if arm == 'J0':
        return jev_matching.piece_question(j0_state(earlier).replace('INCOMING PIECE', 'STORED PIECE', 1))
    return {'type': 'choice', 'criteria': jev_matching.PIECES,
            'instructions': ('How does the INCOMING PIECE relate to the STORED PIECE below? The stored piece is earlier evidence about the same '
                             'company and may be filed under a different research question; a shared topic does not make it the same statement. '
                             'Use only the supplied text. STORED PIECE:\n' + j1_text(earlier, 'STORED PIECE'))}


def main():
    folder, which, arm = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    dry = '--dry-run' in sys.argv
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    groups = {}
    if which == 'labelled':
        for pair in json.loads((folder / 'reference-v2.json').read_text()):
            groups.setdefault(pair['later'], set()).add(pair['earlier'])
    elif which == 'merges':
        for d in json.loads((folder / 'forward-sim.json').read_text())['decisions']:
            for earlier in d['merged_into']:
                groups.setdefault(d['key'], set()).add(earlier)
    else:
        for row in json.loads((folder / 'retrieval.json').read_text()):
            groups.setdefault(row['key'], set()).update(row['R1'])
    jobs = []
    for later, earliers in groups.items():
        incoming = items[later]
        state = j0_state(incoming) if arm in ('J0', 'J2') else j1_text(incoming, 'INCOMING PIECE')
        ordered = sorted(earliers)
        questions = {f'q{i}': question(arm, items[e]) for i, e in enumerate(ordered)}
        jobs.append((later, ordered, state, questions))
    chars = sum(len(json.dumps({'state': s, 'questions': q})) for _, _, s, q in jobs)
    print(f'{arm} {which}: {len(jobs)} requests, {sum(len(o) for _, o, _, _ in jobs)} questions, about {chars // 4} input tokens, '
          f'about ${chars / 4 / 1e6 * model.PRICES[SETTING.model][0]:.4f} at the listed Jev rate')
    if dry:
        return
    archive = model.Archive(str(folder / f'jev-{arm}-{which}.sqlite'))
    cfg = SimpleNamespace(provider='jev', version=f'step2-{arm}', checksum=hashlib.sha256(arm.encode()).hexdigest()[:16])
    def ask(job):
        later, ordered, state, questions = job
        try:
            answer = jev.ask(archive, cfg, SETTING, state, questions, f'step2_{arm}_{which}')
            return [{'later': later, 'earlier': e, 'choice': answer.data[f'q{i}']['choice'], 'probabilities': answer.data[f'q{i}']['probabilities']}
                    for i, e in enumerate(ordered)]
        except Exception as error:   # recorded, never retried silently
            return [{'later': later, 'earlier': e, 'error': f'{type(error).__name__}: {error}'} for e in ordered]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows = [row for batch in pool.map(ask, jobs) for row in batch]
    (folder / f'jev-{arm}-{which}.json').write_text(json.dumps(rows, indent=1))
    print(f'answers {len(rows)}; errors {sum(1 for r in rows if "error" in r)}')


if __name__ == '__main__':
    main()
