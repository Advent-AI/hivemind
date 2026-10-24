"""The test database: the corpus items.sqlite built by poc/corpus/scripts/assemble.py, read as a stream in
publication order. This is "the team's own database" of D7: the system keeps no copy of the material, only the
processing record; an item's text is read from here when it is processed.

Order inside a day (the arrival order upstream would give): company documents (filings, transcripts, releases),
official material, then news by published_at. Only items with feed = 1 (an original, whole) or a copy of one are
streamed; the rest stay in the database for the review.
"""
import json
import sqlite3

KIND_RANK = {'公司材料': 0, '官方材料': 1, '新闻': 2}


def open_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def feed(conn, from_day, until_day):
    """Yield items with from_day <= publication_day <= until_day in processing order."""
    rows = conn.execute(
        "select * from items where publication_day >= ? and publication_day <= ? and (feed = 1 or copy_of is not null) "
        "order by publication_day, case klass when '公司材料' then 0 when '官方材料' then 1 else 2 end, "
        "coalesce(published_at, ''), rowid", (from_day, until_day))
    for row in rows:
        item = dict(row)
        item['object_identifiers'] = json.loads(item.get('object_identifiers') or '[]')
        yield item


def days_with_items(conn, from_day, until_day):
    return [r[0] for r in conn.execute("select distinct publication_day from items where publication_day >= ? and publication_day <= ? and feed = 1 order by 1", (from_day, until_day))]


def count(conn, from_day, until_day):
    return conn.execute("select count(*) from items where publication_day >= ? and publication_day <= ? and feed = 1", (from_day, until_day)).fetchone()[0]
