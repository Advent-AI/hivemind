"""The five-send benchmark again with the cleaned page text (D256): the stored request of the paused run (built on the whole
page) with only its [Item] text replaced by the cleaned database's text, sent N times at reasoning_effort low. Same prompt,
theses, groups and schema as the stored request; only the article text differs. A piece is the same when its quote is the
same text. Run: python3 benchmark_clean.py <run folder> <cleaned items db> <scratch archive> <N> <input_id...>"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from benchmark import send  # noqa: E402
from pinned_arm import norm  # noqa: E402
from wire_order import restore  # noqa: E402  (the archive is alphabetised; send the production order)

ITEM_HEAD = '\n\n[Item] id '
CLOSING = '\n\nReturn evidence and candidates per the JSON schema.'


def with_clean_text(request, input_id, clean_text):
    request = json.loads(json.dumps(request))
    user = request['messages'][1]['content']
    head = user.index(ITEM_HEAD + input_id + ',')
    header_end = user.index('\n\n', head + len(ITEM_HEAD))
    closing = user.rindex(CLOSING)
    assert head < header_end < closing
    request['messages'][1]['content'] = user[:header_end + 2] + clean_text + user[closing:]
    return request


def main(run, items_db, scratch, n, input_ids):
    from hivemind import model
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{items_db}?mode=ro', uri=True)
    archive = model.Archive(scratch)
    total = 0.0
    print('| article | text chars page → clean | pieces per sample | reasoning tokens | distinct pieces | pieces in every sample | seconds |')
    print('|---|---|---|---|---|---|---|')
    for input_id in input_ids:
        req, = stored.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id limit 1", (f'%[Item] id {input_id},%',)).fetchone()
        request = restore(json.loads(req))
        clean, page = items.execute('select text, coalesce(text_page, text) from items where input_id=?', (input_id,)).fetchone()
        request = with_clean_text(request, input_id, clean)
        counts, reasons, secs, sets = [], [], [], []
        for _ in range(n):
            pieces, reasoning, cost, seconds = send(archive, request, 'low')
            total += cost
            counts.append(len(pieces)); reasons.append(reasoning); secs.append(seconds)
            sets.append({norm(p['quote'])[:120] for p in pieces})
        union = set().union(*sets); common = set.intersection(*sets) if sets else set()
        print(f'| {input_id} | {len(page):,} → {len(clean):,} | {counts} | {reasons} | {len(union)} | {len(common)} | {secs} |')
    print(f'\ntotal USD {total:.4f}')


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'src'))
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5:])
