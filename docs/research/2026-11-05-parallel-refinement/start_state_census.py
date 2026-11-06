"""Audit the saved 8/28 start ledger against its recorded source items; do not certify publisher history."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'poc/data/parallel-thesis-evidence-input-2026-11-05'
OUT = Path(__file__).with_name('start-state-census-2026-11-05.json')

def read(name):
    conn = sqlite3.connect((DATA / name).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn

def norm(value):
    return re.sub(r'\s+', ' ', value or '').strip().casefold()

def main():
    views, items = read('views.sqlite'), read('items.sqlite')
    end = views.execute("select seq from days_completed where day='2026-08-28' order by id desc limit 1").fetchone()
    if not end or end['seq'] != 1204:
        raise ValueError('expected 8/28 completed sequence missing')
    questions = views.execute('select view_id,created_seq,created_from_input,question from views where created_seq <= ? order by created_seq, rowid', (end['seq'],)).fetchall()
    if len(questions) != 68 or questions[0]['view_id'] != 'v1':
        raise ValueError('start state population or positive control changed')
    result=[]
    for q in questions:
        item = items.execute('select input_id,publication_day,published_at,title,source_uri,text from items where input_id=?', (q['created_from_input'],)).fetchone()
        if item is None:
            result.append(dict(q,source_missing=True)); continue
        evidence = views.execute('''select e.evidence_id,e.quote,e.created_seq from evidence e join evidence_links l on l.evidence_id=e.evidence_id where l.view_id=? and e.created_from_input=? and e.created_seq<=? order by e.evidence_id''',(q['view_id'],q['created_from_input'],end['seq'])).fetchall()
        anchored = [e['evidence_id'] for e in evidence if norm(e['quote']) and norm(e['quote']) in norm(item['text'])]
        result.append(dict(q,source_missing=False,source_day=item['publication_day'],source_published_at=item['published_at'],source_title=item['title'],source_uri=item['source_uri'],source_text_sha256=hashlib.sha256((item['text'] or '').encode()).hexdigest(),recorded_before_start=bool(item['publication_day'] and item['publication_day']<'2026-08-29'),source_quote_count=len(evidence),quote_matches_saved_body=anchored))
    meta={'scope':'68 recorded questions through 2026-08-28, checked against saved item bodies only. Neither publisher publication timestamps nor body versions are certified.', 'questions':len(result),'unique_source_items':len({r['created_from_input'] for r in result}),'source_missing':sum(r['source_missing'] for r in result),'recorded_not_before_start':sum(not r.get('recorded_before_start',False) for r in result),'no_linked_origin_quote_found_in_saved_body':sum(not r.get('quote_matches_saved_body',[]) for r in result),'rows':result}
    if OUT.exists():
        raise ValueError('refusing to overwrite census')
    OUT.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in meta.items() if k!='rows'})
    print('questions without matching source quote:',[r['view_id'] for r in result if not r.get('quote_matches_saved_body')])
if __name__=='__main__':main()
