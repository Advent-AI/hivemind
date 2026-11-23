"""Tests of Step 2's three hard lines on draw new-1 (verdict-rule.json `hard_checks`; DESIGN-1.6.md §2, v6; D675; council round 8), with a
fake closed reader in place of `census_readers.run` and small real stores (a Step 1 trace, `decisions.json`, `library.json`) on a
temporary path.

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider docs/research/2026-11-17-product-comparison/stage0/test_step2_lines.py
"""
import datetime
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import step2_lines  # noqa: E402

eligibility = step2_lines.eligibility
library = step2_lines.library
FIRST_DAY = datetime.date(2026, 7, 1)
ANCHOR = 'Acme Corp signs a ten gigawatt supply agreement with NVIDIA for Rubin systems'


# ---- stores -------------------------------------------------------------------------------------------------------------------------

def step1_record(summary, party='Acme Corp', verified=True):
    """A kept Step 1 record; an unverified one has a passage Step 1 did not find in its article."""
    return {'summary': summary, 'passages': [f'{summary}, the company said.'], 'original_party': party, 'reporting_speaker': 'Reuters',
            'tier': 'fact', 'period': None, 'verified': verified}


def write_trace(path, articles):
    """A Step 1 trace as run_forward.step1_records reads it: article n published on 2026-07-01 plus n - 1 days, with its kept records
    (an article with none is in the manifest and holds no record)."""
    conn = sqlite3.connect(path)
    conn.execute('create table run (manifest text)')
    conn.execute('create table trace (sequence integer, input_id text, request text, result text, before_state text, after_state text, '
                 'status text)')
    item_ids = [f'item-{n}' for n in range(1, len(articles) + 1)]
    conn.execute('insert into run values (?)', (json.dumps({'item_ids': item_ids}),))
    for number, records in enumerate(articles, 1):
        day = (FIRST_DAY + datetime.timedelta(days=number - 1)).isoformat()
        source = {'id': item_ids[number - 1], 'title': f'Article {number}', 'publisher': 'Reuters', 'publication_date': day,
                  'text': 'Opening paragraph. ' + ' '.join(p for r in records if r['verified'] for p in r['passages']) + ' Closing paragraph.'}
        request = {'messages': [{'role': 'system', 'content': 'extract'}, {'role': 'user', 'content': json.dumps({'source_item': source})}]}
        evidence = [{'local_id': f'E{k}', 'summary': r['summary'], 'source_passages': r['passages'],
                     'verified_source_passages': r['passages'] if r['verified'] else [None] * len(r['passages']),
                     'original_party': r['original_party'], 'reporting_speaker': r['reporting_speaker'], 'tier': r['tier'],
                     'statement_date': day, 'statement_date_text': None, 'evidence_period': r['period'], 'figures': [], 'links': []}
                    for k, r in enumerate(records, 1)]
        conn.execute('insert into trace values (?, ?, ?, ?, ?, ?, ?)', (number, item_ids[number - 1], json.dumps(request),
                     json.dumps({'evidence': evidence, 'new_thesis_ids': {}}), '[]', '[]', 'complete'))
    conn.commit()
    conn.close()


def make_draw(root, articles, decisions, stored_library):
    """new-1 with its Step 1 trace and Step 2 files, and an eligibility record fingerprinting every file the §1.6 tools read."""
    folder = root / 'new-1'
    (folder / 'step1').mkdir(parents=True)
    (folder / 'step2').mkdir()
    write_trace(folder / 'step1' / 'trace.sqlite', articles)
    (folder / 'step2' / 'decisions.json').write_text(json.dumps(decisions))
    (folder / 'step2' / 'library.json').write_text(json.dumps(stored_library))
    record = {'components': {c: {'state': 'completed', 'folder': c} for c in ('step1', 'step2')}}
    (folder / 'run.json').write_text(json.dumps(record))
    return {'draws': {'new-1': {'inputs': {rel: eligibility.sha256(folder / rel) for rel in eligibility.section_inputs(root, 'new-1', record)}}}}


def anchor_corpus(repeats, misses=0):
    """Article 1 states the anchor; each later article repeats it, and Step 2 grouped every repeat with it. The last `misses` repeats did
    not have the anchor's group among their Step 2 candidates."""
    articles = [[step1_record(ANCHOR)]] + [[step1_record(f'{ANCHOR}, report {n}')] for n in range(1, repeats + 1)]
    ids = [f'{n}:E1' for n in range(1, repeats + 2)]
    decisions = [{'id': ids[0], 'candidates': [], 'answers': {}, 'outcome': {'kind': 'new'}, 'group': ids[0]}]
    decisions += [{'id': rid, 'candidates': ['0:E9'] if n > repeats - misses else [ids[0]], 'answers': {},
                   'outcome': {'kind': 'repeat', 'repeat_of': [ids[0]]}, 'group': ids[0]} for n, rid in enumerate(ids[1:], 1)]
    stored = {'order': [ids[0]], 'groups': {ids[0]: {'original': {'id': ids[0]}, 'members': [{'id': rid} for rid in ids[1:]]}},
              'placement': {rid: ids[0] for rid in ids}}
    return articles, decisions, stored


def library_record(record_id, article, summary, period=None, speaker='Reuters'):
    return {'id': record_id, 'article': article, 'publisher': 'Reuters', 'publication_date': '2026-07-0%d' % (1 + article % 9),
            'summary': summary, 'passages': [f'{summary}, the company said.'], 'original_party': f'Company {article}',
            'reporting_speaker': speaker, 'tier': 'fact', 'statement_date': '2026-07-01', 'evidence_period': period, 'thesis_ids': []}


def grouped_library(groups, period_in=(), speaker_in=(), thesis_of=None):
    """`groups` groups of an original and one later report adding a margin figure, plus two groups with no later report. The later
    reports of the groups in `period_in` or `speaker_in` carry their own period or speaker, attribution fields only the apart rendering
    shows. `thesis_of(n)` links group n to a thesis."""
    order, stored = [], {}
    for n in range(1, groups + 3):
        original = library_record(f'{n}:E1', n, f'Company {n} raises its capacity guidance')
        members = [library_record(f'{n}:E2', n, f'Company {n} raises its capacity guidance with a {n}% margin',
                                  period='FY2027' if n in period_in else None, speaker='Bloomberg' if n in speaker_in else 'Reuters')
                   ] if n <= groups else []
        links = {thesis_of(n): original['id']} if thesis_of else {}
        stored[original['id']] = {'original': original, 'members': members, 'links': links, 'revises': []}
        order.append(original['id'])
    return {'order': order, 'groups': stored, 'placement': {r['id']: g for g, v in stored.items() for r in [v['original']] + v['members']}}


# ---- the fake closed reader ---------------------------------------------------------------------------------------------------------

def packet_of(prompt):
    return json.loads(prompt.split('```json\n', 1)[1].split('\n```', 1)[0])


def excerpt_of(prompt):
    return prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0]


def states(family, detail, excerpt):
    return detail.lower() in excerpt.lower()


class Reader:
    """Answers each kind of closed session from its prompt alone, by fixed rules; records every (family, prompt)."""

    def __init__(self, void=lambda family, prompt, attempt: False, render=states, key_extra=None):
        self.calls, self.void, self.render, self.attempts, self.key_extra = [], void, render, {}, key_extra or {}

    def __call__(self, family, prompt):
        self.calls.append((family, prompt))
        attempt = self.attempts[(family, prompt)] = self.attempts.get((family, prompt), 0) + 1
        if self.void(family, prompt, attempt):
            return None, 'a tool use'
        if 'Question 1, the relation' in prompt:
            rows = [{'id': p['id'], 'relation': 'same_statement' if all('gigawatt' in p[s]['summary'] for s in ('earlier', 'later')) else 'different',
                     'why': 'rule'} for p in packet_of(prompt)]
        elif 'one incoming evidence record' in prompt:
            rows = [{'incoming_key': p['incoming_key'], 'possible_earlier': []} for p in packet_of(prompt)]
        elif 'has just placed' in prompt:
            rows = [{'id': p['id'], 'relation': 'same_statement', 'merge_acceptable': not re.search('WRONG|OVERLAP', p['later']['summary']),
                     'why': 'rule'} for p in packet_of(prompt)]
        elif 'independent senior reader' in prompt:
            rows = [{'id': p['id'], 'merge_acceptable': False, 'verdict': 'wrong' if 'WRONG' in p['later']['summary'] else 'overlap',
                     'why': 'rule'} for p in packet_of(prompt)]
        elif 'building an answer key' in prompt:
            rows = [{'id': m['id'], 'details': re.findall(r'\d+% margin', m['summary']) + self.key_extra.get(family, [])}
                    for g in packet_of(prompt) for m in g['later']]
        elif 'third reader settling an answer key' in prompt:
            rows = [{'id': m, 'details': sorted(set(d['A']) & set(d['B'])), 'dropped': sorted(set(d['A']) ^ set(d['B']))}
                    for g in packet_of(prompt) for m, d in g['drafts'].items()]
        elif 'The excerpt:' in prompt:
            rows = [{'id': d['id'], 'stated': self.render(family, d['detail'], excerpt_of(prompt))} for d in packet_of(prompt)]
        else:
            raise AssertionError('a session the tests do not expect')
        return json.dumps(rows), None


@pytest.fixture
def reader(monkeypatch):
    def install(**options):
        fake = Reader(**options)
        monkeypatch.setattr(step2_lines.census_readers, 'run', fake)
        return fake
    return install


def packet_entries_sent(fake, marker):
    """Every record entry ('earlier', 'later' or 'incoming') of the packets sent in sessions whose prompt holds `marker`."""
    return [p[side] for _f, prompt in fake.calls if marker in prompt for p in packet_of(prompt)
            for side in ('earlier', 'later', 'incoming') if side in p]


# ---- line 1 -------------------------------------------------------------------------------------------------------------------------

def test_line1_passes_with_90_of_100_labelled_records_found_and_fails_with_89(tmp_path, reader):
    """Hard check: Step 2 line 1 needs >= 90% recall on 100 labelled records, decided on the point estimate (DESIGN-1.6.md §2)."""
    reader()
    for misses, expected in ((10, 'passed'), (11, 'failed')):
        root = tmp_path / f'misses-{misses}'
        result = step2_lines.line1(root, make_draw(root, *anchor_corpus(100, misses)), root / 'out', root / 'keys')
        assert (result['status'], result['labelled records'], result['found']) == (expected, 100, 100 - misses)


def test_line1_short_of_100_labelled_records_is_not_measured(tmp_path, reader):
    """Hard check: a line short of its sample is not measured and cannot clear release (verdict-rule.json; D675)."""
    reader()
    result = step2_lines.line1(tmp_path, make_draw(tmp_path, *anchor_corpus(99)), tmp_path / 'out', tmp_path / 'keys')
    assert (result['status'], result['labelled records']) == ('not measured', 99)
    assert json.loads((tmp_path / 'out' / 'step2-lines.json').read_text())['release'][0] == 'release not cleared: Step 2 line 1 not measured'


def test_line1_labels_are_frozen_before_step2_candidates_are_read(tmp_path, reader, monkeypatch):
    """DESIGN-1.6.md §2 line 1: the labels are frozen (file and sha256) before Step 2's candidates are read."""
    reader()
    real = eligibility.verified
    frozen = tmp_path / 'out' / 'line-1' / 'labels.json'
    frozen_when_read = []

    def watching(record, run_root, draw, relative):
        if relative.startswith('step2/'):
            sha = Path(f'{frozen}.sha256')
            frozen_when_read.append(sha.exists() and sha.read_text().split()[0] == eligibility.sha256(frozen))
        return real(record, run_root, draw, relative)
    monkeypatch.setattr(eligibility, 'verified', watching)
    step2_lines.line1(tmp_path, make_draw(tmp_path, *anchor_corpus(12)), tmp_path / 'out', tmp_path / 'keys')
    assert frozen_when_read == [True, True]


def test_line1_candidates_are_records_of_earlier_articles_only(tmp_path, reader):
    """DESIGN-1.6.md §2 line 1: candidates are earlier records only; a record of the same article or a later one is never paired."""
    reader()
    articles, decisions, stored = anchor_corpus(12)
    articles[4].append(step1_record(f'{ANCHOR}, second report in article 5'))   # same article, same party, same words
    decisions.append({'id': '5:E2', 'candidates': ['1:E1'], 'answers': {}, 'outcome': {'kind': 'repeat', 'repeat_of': ['1:E1']}, 'group': '1:E1'})
    stored['placement']['5:E2'] = '1:E1'
    step2_lines.line1(tmp_path, make_draw(tmp_path, articles, decisions, stored), tmp_path / 'out', tmp_path / 'keys')
    labels = json.loads((tmp_path / 'out' / 'line-1' / 'labels.json').read_text())
    pairs = [(p['earlier'], r['record']) for r in labels['records'] for p in r['pairs']]
    article = lambda record_id: int(record_id.split(':')[0])
    assert pairs and all(article(earlier) < article(later) for earlier, later in pairs)
    assert {'5:E1', '5:E2'} <= {r['record'] for r in labels['records']}


def test_line1_strata_are_thirds_of_the_manifest_by_forward_position(tmp_path, reader):
    """Council round 8 (Codex): three equal strata by the article's forward position in the run's manifest, articles that hold no record
    included."""
    reader()
    holding = {1, 2, 5, 9, 12}                                   # 12 manifest articles; the others hold no record
    articles = [[step1_record(f'Statement of article {n}')] if n in holding else [] for n in range(1, 13)]
    ids = [f'{n}:E1' for n in sorted(holding)]
    decisions = [{'id': rid, 'candidates': [], 'answers': {}, 'outcome': {'kind': 'new'}, 'group': rid} for rid in ids]
    stored = {'order': ids, 'groups': {rid: {'original': {'id': rid}, 'members': []} for rid in ids}, 'placement': {rid: rid for rid in ids}}
    step2_lines.line1(tmp_path, make_draw(tmp_path, articles, decisions, stored), tmp_path / 'out', tmp_path / 'keys')
    labels = json.loads((tmp_path / 'out' / 'line-1' / 'labels.json').read_text())
    assert {r['record']: r['stratum'] for r in labels['records']} == {'2:E1': 0, '5:E1': 1, '9:E1': 2, '12:E1': 2}


def test_line1_and_line2_packets_flag_an_unverified_quote_and_give_it_no_source_context(tmp_path, reader):
    """Council round 8 (Codex): a passage Step 1 did not find in the source is shown as "Unverified quote" and never as source context."""
    unverified = f'{ANCHOR}, report 2'
    for line, corpus, marker in ((step2_lines.line1, anchor_corpus(12), 'Question 1, the relation'),
                                 (step2_lines.line2, anchor_corpus(200), 'has just placed')):
        fake = reader()
        corpus[0][2][0] = step1_record(unverified, verified=False)
        root = tmp_path / line.__name__
        line(root, make_draw(root, *corpus), root / 'out', root / 'keys')
        entries = packet_entries_sent(fake, marker)
        flagged = [e for e in entries if e['summary'] == unverified]
        control = [e for e in entries if e['summary'] == f'{ANCHOR}, report 3']
        assert flagged and all(e['passages'] == [f'Unverified quote: {unverified}, the company said.'] and e['source_context'] == []
                               for e in flagged)
        assert control and all(e['passages'] == [f'{ANCHOR}, report 3, the company said.'] and e['source_context'] for e in control)


def test_line1_prompts_name_only_their_chunk_and_no_folder(tmp_path, reader):
    """Council round 8 wording: the scan session sees one chunk of the earlier records' summaries; a closed label session opens no folder."""
    fake = reader()
    step2_lines.line1(tmp_path, make_draw(tmp_path, *anchor_corpus(12)), tmp_path / 'out', tmp_path / 'keys')
    scans = [p for _f, p in fake.calls if 'one incoming evidence record' in p]
    labels = [p for _f, p in fake.calls if 'Question 1, the relation' in p]
    assert scans and all('one chunk of the evidence records stored before it' in p and 'every evidence record stored before it' not in p
                         for p in scans)
    assert labels and not any('Do not open any other file in that folder' in p for p in labels)


# ---- line 2 -------------------------------------------------------------------------------------------------------------------------

def merge_corpus(repeats, wrong, refused=0):
    """`repeats` repeats of article 1's record, the first `wrong` of them a different statement both readers reject and the third
    reader calls wrong, and `refused` further repeats the library refused."""
    articles = [[step1_record(ANCHOR)]] + [[step1_record(f'{ANCHOR}, report {n}' + (' WRONG figure' if n <= wrong else ''))]
                                           for n in range(1, repeats + refused + 1)]
    decisions = [{'id': '1:E1', 'candidates': [], 'answers': {}, 'outcome': {'kind': 'new'}, 'group': '1:E1'}]
    for n in range(2, repeats + refused + 2):
        decision = {'id': f'{n}:E1', 'candidates': ['1:E1'], 'answers': {}, 'outcome': {'kind': 'repeat', 'repeat_of': ['1:E1']}}
        decision.update({'refused': 'Refused: test'} if n > repeats + 1 else {'group': '1:E1'})
        decisions.append(decision)
    return articles, decisions, {'order': ['1:E1'], 'groups': {}, 'placement': {}}


def test_line2_passes_at_4_clear_wrong_merges_of_200_fails_at_5_and_is_not_measured_below_200(tmp_path, reader):
    """Hard check: Step 2 line 2, <= 2% clearly wrong merges on 200 (at most 4), the third reader's `wrong`; refused repeats are not in
    the population, and fewer than 200 repeats is not measured (DESIGN-1.6.md §2)."""
    reader()
    for name, corpus, expected in (('four', merge_corpus(200, 4), ('passed', 4)), ('five', merge_corpus(200, 5), ('failed', 5)),
                                   ('short', merge_corpus(199, 0, refused=1), ('not measured', None))):
        root = tmp_path / name
        result = step2_lines.line2(root, make_draw(root, *corpus), root / 'out', root / 'keys')
        assert (result['status'], result.get('wrong')) == expected


def test_a_session_void_twice_leaves_its_line_not_measured_and_one_void_attempt_is_retried(tmp_path, reader):
    """DESIGN-1.6.md, state x event: a reader session that voids is retried once, then reported missing; a line with a missing mark is
    not measured."""
    first_packet = lambda family, prompt: family == 'codex' and '"id": "X1"' in prompt and 'has just placed' in prompt
    for name, void, expected in (('twice', lambda f, p, attempt: first_packet(f, p), 'not measured'),
                                 ('once', lambda f, p, attempt: first_packet(f, p) and attempt == 1, 'passed')):
        reader(void=void)
        root = tmp_path / name
        result = step2_lines.line2(root, make_draw(root, *merge_corpus(200, 0)), root / 'out', root / 'keys')
        assert result['status'] == expected and len(result['sessions']['missing']) == (name == 'twice')


def test_an_input_the_eligibility_check_did_not_fingerprint_is_refused(tmp_path, reader):
    """DESIGN-1.6.md §0: every tool reads a draw's stores only through `eligibility.verified`, and refuses a file not fingerprinted."""
    fake = reader()
    record = make_draw(tmp_path, *merge_corpus(200, 0))
    del record['draws']['new-1']['inputs']['step2/decisions.json']
    with pytest.raises(SystemExit, match='refused: new-1/step2/decisions.json is not fingerprinted'):
        step2_lines.line2(tmp_path, record, tmp_path / 'out', tmp_path / 'keys')
    assert fake.calls == []


# ---- line 3 -------------------------------------------------------------------------------------------------------------------------

def misses(family_and_rendering):
    """A rendering reader that does not see one group's detail in the named (family, rendering) sessions."""
    def render(family, detail, excerpt):
        rendering = 'grouped' if 'Later reports of the same statement' in excerpt else 'apart'
        return states(family, detail, excerpt) and family_and_rendering.get((family, rendering)) != detail
    return render


def test_line3_passes_on_pooled_totals_no_fewer_grouped_and_is_not_measured_below_30(tmp_path, reader):
    """Hard check: Step 2 line 3, no fewer later details grouped than apart on 30 groups, the totals summed over both readers as the
    recorded reader test summed them (council round 8); each family's totals beside; fewer than 30 groups is not measured."""
    cases = (('equal', 30, states, 'passed', {'codex': (30, 30), 'claude': (30, 30)}),
             ('one-fewer', 30, misses({('claude', 'grouped'): '3% margin'}), 'failed', {'codex': (30, 30), 'claude': (29, 30)}),
             ('offsetting', 30, misses({('claude', 'grouped'): '3% margin', ('codex', 'apart'): '5% margin'}), 'passed',
              {'codex': (30, 29), 'claude': (29, 30)}),
             ('short', 29, states, 'not measured', None))
    for name, groups, render, expected, totals in cases:
        fake = reader(render=render)
        root = tmp_path / name
        result = step2_lines.line3(root, make_draw(root, *anchor_corpus(1)[:2], grouped_library(groups)), root / 'out', root / 'keys')
        assert result['status'] == expected
        if totals:
            assert {f: (t['grouped'], t['apart']) for f, t in result['totals by family'].items()} == totals
        else:
            assert fake.calls == []


def test_line3_key_readers_see_content_only_and_attribution_differences_are_counted_beside(tmp_path, reader):
    """Council round 8 (D675): the key holds content only, so the key readers never see a record's tier, stated day, period or speaker;
    code counts the later reports whose attribution fields differ, printed beside line 3 and not in its rule."""
    fake = reader()
    stored = grouped_library(30, period_in={3}, speaker_in={5})
    result = step2_lines.line3(tmp_path, make_draw(tmp_path, *anchor_corpus(1)[:2], stored), tmp_path / 'out', tmp_path / 'keys')
    keys = [p for _f, p in fake.calls if 'building an answer key' in p]
    assert keys and not any(word in p for p in keys for word in ('"tier"', '"statement_date"', '"period"', '"reporting_speaker"',
                                                                  'FY2027', 'Bloomberg', 'statement date, period and speaker'))
    for counted in ('attribution differences, sampled groups', 'attribution differences, all groups with a later report'):
        assert result[counted]['later reports that differ'] == 2
        assert result[counted]['by field'] == {'tier': 0, 'statement_date': 0, 'evidence_period': 1, 'reporting_speaker': 1}
    assert result['status'] == 'passed'


def test_line3_key_prompts_count_only_what_the_statement_adds(tmp_path, reader):
    """Council round 9 (Codex): the key readers and the key tie-break count only facts the later report's statement adds (its summary and
    quotes), and use its visible publisher and publication date only as context, never as details."""
    fake = reader(key_extra={'claude': ['published by Reuters']})        # the drafts differ, so every group goes to a tie-break session
    result = step2_lines.line3(tmp_path, make_draw(tmp_path, *anchor_corpus(1)[:2], grouped_library(30)), tmp_path / 'out', tmp_path / 'keys')
    keys = [p for _f, p in fake.calls if 'building an answer key' in p]
    thirds = [p for _f, p in fake.calls if 'third reader settling an answer key' in p]
    sentences = ("Count only facts the later record's statement itself adds: its summary and quotes.",
                 'Use its publisher and publication date only as context for reading; never list them as details.')
    assert keys and thirds and all(sentence in p for p in keys + thirds for sentence in sentences)
    assert result['key details'] == 30 and result['status'] == 'passed'


def test_line3_no_session_sees_both_renderings_of_a_group(tmp_path, reader):
    """DESIGN-1.6.md §2 line 3: each rendering of a group goes to its own closed session in each family, four per group; none sees both."""
    fake = reader()
    stored = grouped_library(30)
    step2_lines.line3(tmp_path, make_draw(tmp_path, *anchor_corpus(1)[:2], stored), tmp_path / 'out', tmp_path / 'keys')
    store = library.Library()
    store.groups, store.order = stored['groups'], stored['order']
    renderings = [p for _f, p in fake.calls if 'The excerpt:' in p]
    assert len(renderings) == 4 * 30
    for group_id in stored['order'][:30]:
        group = stored['groups'][group_id]
        grouped = library.group_text(store, group_id, 'E1', {group_id: 'E1'}, member_text=True)
        apart = library.record_text(group['original'], 'E1') + '\n\n' + library.record_text(group['members'][0], 'E2')
        assert sorted(f for f, p in fake.calls if grouped in p) == sorted(f for f, p in fake.calls if apart in p) == ['claude', 'codex']
        assert not any(grouped in p and apart in p for p in renderings)


def test_line3_both_renderings_follow_the_same_surrounding_dossier(tmp_path, reader):
    """DESIGN-1.6.md §2 line 3 ("the group's other context is the same in both renderings"; council round 8): each rendering session
    sees every other group linked to the group's first thesis, as its original's record_text, identical in both renderings."""
    reader()
    stored = grouped_library(30, thesis_of=lambda n: f'T{n % 2}')
    step2_lines.line3(tmp_path, make_draw(tmp_path, *anchor_corpus(1)[:2], stored), tmp_path / 'out', tmp_path / 'keys')
    code_key = json.loads((tmp_path / 'keys' / 'step2-line3-key.json').read_text())
    prompts = tmp_path / 'out' / 'line-3' / 'prompts'
    seen = {}
    for code, entry in code_key.items():
        for family in step2_lines.FAMILIES:
            seen[(entry['group'], entry['rendering'], family)] = excerpt_of((prompts / f'render-{code}-{family}.md').read_text())
    assert len(seen) == 4 * 30
    for group_id in stored['order'][:30]:
        thesis = next(iter(stored['groups'][group_id]['links']))
        others = [g for g in stored['order'] if g != group_id and thesis in stored['groups'][g]['links']]
        context = '\n\n'.join(library.record_text(stored['groups'][g]['original'], f'E{n}') for n, g in enumerate(others, 1)) + '\n\n'
        excerpts = [seen[(group_id, rendering, family)] for rendering in ('grouped', 'apart') for family in step2_lines.FAMILIES]
        assert len(others) == 15 and all(excerpt.startswith(context) for excerpt in excerpts)
        assert excerpts[0][len(context):] != excerpts[2][len(context):]


# ---- report -------------------------------------------------------------------------------------------------------------------------

def test_the_report_puts_a_failed_line_ahead_of_one_not_measured_and_clears_only_when_all_pass(tmp_path):
    """D675 (DESIGN-1.6.md §0): a failed hard check prints "release blocked"; one only not measured prints "release not cleared"; a line
    not run is not measured; three passed lines print "hard checks clear"."""
    for line, status in ((1, 'failed'), (3, 'passed')):
        (tmp_path / f'line-{line}').mkdir()
        (tmp_path / f'line-{line}' / 'result.json').write_text(json.dumps({'line': line, 'status': status}))
    summary = step2_lines.report(tmp_path)
    assert summary['status'] == 'failed'
    assert summary['release'] == ['release blocked: Step 2 line 1 failed', 'release not cleared: Step 2 line 2 not measured']
    for line in (1, 2, 3):
        (tmp_path / f'line-{line}').mkdir(exist_ok=True)
        (tmp_path / f'line-{line}' / 'result.json').write_text(json.dumps({'line': line, 'status': 'passed'}))
    assert step2_lines.report(tmp_path)['release'] == ['hard checks clear']
