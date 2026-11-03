"""Every reader flag (field errors, duplicates, noise) beside the article sentences it rests on, for Claude to adjudicate one by
one (2026-10-30, Alex: "那你找到的这些问题验证是真的问题吗？"). Writes flags-for-reading.md."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE_WORDS = re.compile(r"[^.]*\b(?:January|February|March|April|May|June|July|August|September|October|November|December|yesterday|today|last (?:week|month|year)|earlier this|this week|on (?:Monday|Tuesday|Wednesday|Thursday|Friday))\b[^.]*\.", re.I)


def context(text, quote):
    key = quote[:40]
    i = text.find(key)
    if i < 0:
        key = quote[:20]
        i = text.find(key)
    if i < 0:
        return '(quote start not found)'
    return text[max(0, i - 250):i + len(quote) + 150].replace('\n', ' ')


out = []
for f in sorted((HERE / 'verdicts').glob('*.json')):
    v = json.loads(f.read_text())
    p = json.loads((HERE / 'packets' / f.name).read_text())
    by_id = {e['id']: e for e in p['output']['statements']}
    flagged = [s for s in v['statements'] if any(s.get(k) is False for k in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok')) or s.get('duplicate_of') or s['worth'] == 'noise']
    if not flagged:
        continue
    out.append(f'\n######## {f.name} | {p["publication_day"]} | {p["title"]}')
    out.append('DATE SENTENCES: ' + ' || '.join(m.group(0).strip()[:160] for m in DATE_WORDS.finditer(p['text']))[:1500])
    for s in flagged:
        e = by_id[s['id']]
        flags = [k for k in ('one_line_ok', 'who_ok', 'day_ok', 'tier_ok') if s.get(k) is False] + (['dup:' + s['duplicate_of']] if s.get('duplicate_of') else []) + (['NOISE'] if s['worth'] == 'noise' else [])
        out.append(f'\n[{s["id"]}] FLAGS {flags}')
        out.append(f'  record: who={e.get("original_who")!r} day={e.get("original_day")!r} event={e.get("event_time")!r} tier={e.get("tier")} speaker={e.get("speaker")!r}')
        out.append(f'  quote: {e["quote"][:300]}')
        out.append(f'  line : {e["one_line"][:300]}')
        out.append(f'  reader: worth={s["worth"]}: {s.get("worth_reason", "")[:200]}')
        for k, note in (('one_line_problem', 'line'), ('day_note', 'day'), ('tier_note', 'tier')):
            if s.get(k):
                out.append(f'  reader {note}: {s[k][:260]}')
        out.append(f'  article: …{context(p["text"], e["quote"])[:700]}…')
(HERE / 'flags-for-reading.md').write_text('\n'.join(out) + '\n')
print(sum(1 for l in out if l.startswith('\n[')), 'flagged records')
