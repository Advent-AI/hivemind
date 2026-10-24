"""Harvest a hand-listed set of pages found by research (transcripts of interviews, company blog posts, IR releases)
from extra-urls.json. Each entry carries the date and classification the list-maker verified. Resumable.

Writes raw/extra/<sha>.html, .txt and raw/extra/manifest.json.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, fetch, decode, html_to_text, article_paragraphs, title_of, sha256_text, read_json, write_json, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'extra')
LIST = os.path.join(os.path.dirname(__file__), 'extra-urls.json')


def run():
    os.makedirs(OUT, exist_ok=True)
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'pages': []})
    have = {p['url'] for p in manifest['pages']}
    for entry in read_json(LIST, []):
        url = entry['url']
        if url in have:
            continue
        status, final, body = fetch(url, timeout=60)
        time.sleep(1.0)
        record = dict(entry, status=status, final_url=final, retrieved_at=now_iso())
        if status == 200 and body:
            markup = decode(body)
            key = sha256_text(url)
            paragraphs, count = article_paragraphs(markup)
            text = paragraphs if count >= 4 else html_to_text(markup)
            with open(os.path.join(OUT, key + '.html'), 'wb') as handle:
                handle.write(body)
            with open(os.path.join(OUT, key + '.txt'), 'w', encoding='utf-8') as handle:
                handle.write(text)
            record.update({'file': key, 'title': title_of(markup)[:200], 'chars': len(text), 'paragraphs': count})
            log('ok', entry['date'], entry['category'], len(text), 'chars', url[:80])
        else:
            log('failed', status, url, '(not recorded; the next run tries again)')
            continue
        manifest['pages'].append(record)
        have.add(url)
        write_json(os.path.join(OUT, 'manifest.json'), manifest)
    log('done:', len(manifest['pages']))


if __name__ == '__main__':
    main_guard(run)
