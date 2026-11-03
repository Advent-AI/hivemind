"""The model's own account of a core gold entry the reshaped role (SEQ-v67) left out: rebuild the arm request (role override, fields, the
run's own ledger snapshot), check its hash against the stored one, continue the conversation with one question.
    python3 probe_v67.py "<input_id>|<words of the gold span>" ..."""
import copy, json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sequential_arm as sa, score_ref as sr, score_seq as ss, reference_arm as ra  # noqa: E402

sa.ROLE_FILE = str(HERE / 'role-v67-draft.txt'); sa.EXTRA_FIELDS = sa.FIELD_NOTES_V67
Q = ('Your answer did not include this statement from the item: "{span}". Which of the three questions (new or in force; which question '
     'it moves; a row that rejects it) made you leave it out, or was it an oversight? Quote the sentence of the request you applied and '
     'answer in two sentences.')
for pair in sys.argv[1:]:
    iid, words = pair.split('|', 1)
    a = ss.articles[iid]; item = next(i for i in a['items'] if words in i['span'])
    for d in (1, 2, 3):
        db = sqlite3.connect(f'file:{ra.LOOP / "loop-2026-10-29" / f"SEQ-v67-d{d}" / "answers.sqlite"}?mode=ro', uri=True)
        sha, content, response = db.execute('select request_sha256, content, response_json from answers where input_id=?', (iid,)).fetchone()
        data = json.loads(content)
        if any(sr.sg.same_matter(item, e) for e in data.get('evidence', [])):
            continue
        it, uni, setting, schema, request, cfg = ra.bench.build(iid, ra.CONFIG)
        shown = ss.shown_for('SEQ-v67', d, iid)
        before = max([x['opened_day'] for x in shown], default=a['publication_day'])
        prev = max([q['opened_day'] for q in ss.ledger('SEQ-v67', d)['questions'] if q['opened_day'] < a['publication_day']] + [None], key=lambda x: x or '')
        body = sa.arm_request(request, shown, prev or a['publication_day'])
        if ra.model.request_identity(body)[1] != sha:
            # the day label is the previous day with articles, not the last opening day: try the day before in the run's calendar
            days = sorted({x['publication_day'] for x in sr.articles}); i = days.index(a['publication_day'])
            body = sa.arm_request(request, shown, days[i - 1] if i else a['publication_day'])
        if ra.model.request_identity(body)[1] != sha:
            print(iid[:30], 'REQUEST MISMATCH'); break
        full = json.loads(response)['choices'][0]['message']['content']
        body.pop('response_format', None)
        body['messages'] += [{'role': 'assistant', 'content': full}, {'role': 'user', 'content': Q.format(span=item['span'][:220])}]
        reply = ra.model.openai_transport(cfg.provider, body)['choices'][0]['message'].get('content') or ''
        (HERE / 'probes').mkdir(exist_ok=True)
        (HERE / 'probes' / f'v67-drop-{iid.split(":")[-1][:10]}.txt').write_text(f'{iid} d{d}\ngold: {item["span"]}\n\n{reply}\n')
        print(iid[:30], f'd{d} ok'); break
    else:
        print(iid[:30], 'kept in every draw')
