"""Census of the record-field class (open defect 1) over what production keeps from stored answers, at no cost.

Two code-countable signals, checked against the cases Claude verified in quality-2026-10-30/adjudication.py:
  outlet_as_original  on a media, analyst or individual item, tier fact or party_statement, and original_who names the item's
                      own publisher (or "the article", "the reporter"): the outlet is written as the original speaker of
                      another party's action or statement. A company's or official's own page names itself rightly.
  earlier_day_known   on a media, analyst or individual item, original_day is the publication day while event_time or the
                      quote dates the action to an earlier month or day: the answer itself knows the earlier day and writes
                      the report day. (A filing or a company page is the original; its quarter is not an earlier statement.)
Neither signal catches every member of the class (an undated earlier announcement written as the report day, a wrong tier);
they count the class's two code-visible forms across every draw.

    python3 census_fields.py P-v51-d1 P-v51-d2 P-v51-d3
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402
import haiku_week as hw  # noqa: E402  (on the path through score_gold)

MONTHS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                                          'september', 'october', 'november', 'december'])}
GENERIC = {'news', 'the', 'article', 'reporter', 'report', 'reported', 'media', 'finance', 'times', 'daily', 'com', 'www',
           'newsletter', 'as', 'by', 'of', 'and', 'inc', 'group', 'online', 'post'}
SELF_WORDS = ('the article', "article's", 'the reporter', "reporter's", 'the author', 'the item', 'the outlet', 'the newsletter')


def tokens(text):
    return {t for t in re.findall(r'[a-z0-9]+', (text or '').lower()) if len(t) >= 4 and t not in GENERIC}


def outlet_names(publisher):
    """'newsletter.semianalysis.com' -> {'semianalysis'}; 'finance.yahoo.com' -> {'yahoo'}."""
    return tokens(re.sub(r'\.(com|net|org|co|io|asia|sg|uk|au|in|vn)\b', ' ', publisher or ''))


def names_outlet(who, publisher):
    low = (who or '').lower()
    if any(w in low for w in SELF_WORDS):
        return True
    squashed = re.sub(r'[^a-z0-9]', '', low)
    return any(name in squashed for name in outlet_names(publisher))


def earlier_dates(text, pub):
    """(year, month, day-or-0) dates written in text that fall before the publication day (month granularity when no day)."""
    py, pm, pd = (int(x) for x in pub.split('-'))
    found = []
    for y, m, d in re.findall(r'\b(20\d\d)-(\d\d)(?:-(\d\d))?\b', text or ''):
        found.append((int(y), int(m), int(d or 0)))
    for name, d, y in re.findall(r'\b(' + '|'.join(MONTHS) + r')\b\.?(?:\s+(\d{1,2})(?!\d)(?:st|nd|rd|th)?)?\s*,?\s*(20\d\d)?', (text or '').lower()):
        if name == 'may' and not d and not y:
            continue      # the verb
        found.append((int(y) if y else py, MONTHS[name], int(d) if d else 0))
    out = []
    for y, m, d in found:
        if (y, m) < (py, pm) or ((y, m) == (py, pm) and d and d < pd):
            out.append((y, m, d))
    return out


def main(tags):
    db = sqlite3.connect(f'file:{hw.ITEMS}?mode=ro', uri=True)
    meta = {i: (p, ptype, day) for i, p, ptype, day in db.execute('select input_id, publisher, publisher_type, publication_day from items')}
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    ids = [a['input_id'] for a in dev + test]
    counts = collections.Counter()
    per_article = collections.Counter()
    hits = collections.defaultdict(list)
    for tag in tags:
        runs = sg.answers(tag)
        for iid in ids:
            s = sg.kept(runs.get(iid), iid)
            if s is None:
                counts['unusable answers'] += 1
                continue
            publisher, publisher_type, pub = meta[iid]
            relayed = publisher_type in ('media', 'analyst', 'individual')
            for e in s['evidence']:
                counts['statements'] += 1
                outlet = relayed and e.get('tier') in ('fact', 'party_statement') and names_outlet(e.get('original_who'), publisher)
                day = e.get('original_day') or ''
                earlier = relayed and day == pub and (earlier_dates(e.get('event_time'), pub) or earlier_dates(e.get('quote'), pub))
                if outlet:
                    counts['outlet_as_original'] += 1
                    hits['outlet_as_original'].append((tag, iid, e['id'], e.get('original_who'), e['tier'], e['quote'][:100]))
                if earlier:
                    counts['earlier_day_known'] += 1
                    hits['earlier_day_known'].append((tag, iid, e['id'], day, e.get('event_time'), e['quote'][:100]))
                if outlet or earlier:
                    counts['either'] += 1
                    per_article[iid] += 1
    out = {'tags': tags, 'articles': len(ids), 'counts': dict(counts),
           'articles with a hit in any draw': len(per_article),
           'top articles': per_article.most_common(12)}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    (HERE / f'census-{"-".join(tags)}.json').write_text(json.dumps({'summary': out, 'hits': hits}, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
