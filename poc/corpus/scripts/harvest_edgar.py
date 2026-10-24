"""Harvest NVIDIA's SEC filings from EDGAR for 2026-02-25..2026-10-22: every 8-K, 10-Q, 10-K with its primary
document and every exhibit, as fetched HTML plus a text conversion. Public, no credentials; SEC asks for a
descriptive User-Agent and at most 10 requests per second (we do about 2).

Writes raw/edgar/<accession>/index.json, <name>.htm, <name>.txt and raw/edgar/manifest.json.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from common import (RAW, SEC_USER_AGENT, BOOTSTRAP_START, WINDOW_END, fetch, decode, html_to_text, write_json,
                    read_json, now_iso, log, main_guard)  # noqa: E402

CIK = '0001045810'
CIK_SHORT = '1045810'
OUT = os.path.join(RAW, 'edgar')
FORMS = {'8-K', '8-K/A', '10-Q', '10-Q/A', '10-K', '10-K/A'}


def sec_get(url, accept=None):
    status, final, body = fetch(url, user_agent=SEC_USER_AGENT, accept=accept, timeout=60)
    time.sleep(0.5)
    return status, body


def filings_in_window():
    status, body = sec_get(f'https://data.sec.gov/submissions/CIK{CIK}.json', accept='application/json')
    if status != 200:
        raise SystemExit(f'submissions index failed: {status}')
    recent = json.loads(decode(body))['filings']['recent']
    rows = []
    for form, date, accession, primary, description, accepted, items in zip(
            recent['form'], recent['filingDate'], recent['accessionNumber'], recent['primaryDocument'],
            recent['primaryDocDescription'], recent['acceptanceDateTime'], recent['items']):
        if form in FORMS and BOOTSTRAP_START <= date <= WINDOW_END:
            rows.append({'form': form, 'filing_date': date, 'accession': accession, 'primary_document': primary,
                         'description': description, 'acceptance_datetime': accepted, 'items': items})
    return rows


def exhibit_list(accession):
    folder = accession.replace('-', '')
    status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{CIK_SHORT}/{folder}/index.json',
                           accept='application/json')
    if status != 200:
        return folder, []
    items = json.loads(decode(body))['directory']['item']
    documents = [it['name'] for it in items
                 if it['name'].lower().endswith(('.htm', '.html', '.txt'))
                 and not it['name'].startswith('R')
                 and 'index' not in it['name'].lower()
                 and not it['name'].endswith('_htm.xml')]
    return folder, documents


def exhibit_roles(accession, folder):
    """Which document is which exhibit, from the filing's index page (EX-99.1 and the like)."""
    status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{CIK_SHORT}/{folder}/{accession}-index.html')
    roles = {}
    if status == 200:
        page = decode(body)
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', page, re.S | re.I):
            cells = [re.sub(r'<[^>]+>', ' ', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S | re.I)]
            link = re.search(r'href="[^"]*/([^"/]+\.(?:htm|html|txt))"', row, re.I)
            if link and len(cells) >= 4:
                roles[link.group(1)] = {'description': cells[1], 'type': cells[3]}
    return roles


def run():
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'filings': []})
    done = {f['accession'] for f in manifest['filings']}
    for filing in filings_in_window():
        accession = filing['accession']
        if accession in done:
            continue
        folder, documents = exhibit_list(accession)
        roles = exhibit_roles(accession, folder)
        saved = []
        failed = False
        for name in documents:
            target = os.path.join(OUT, accession, name)
            if not os.path.exists(target):
                status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{CIK_SHORT}/{folder}/{name}')
                if status != 200 or not body:
                    log('failed', accession, name, status)
                    failed = True
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, 'wb') as handle:
                    handle.write(body)
                text = html_to_text(decode(body)) if name.lower().endswith(('.htm', '.html')) else decode(body)
                with open(target + '.txt', 'w', encoding='utf-8') as handle:
                    handle.write(text)
            with open(target + '.txt', encoding='utf-8') as handle:
                chars = len(handle.read())
            saved.append({'name': name, 'chars': chars, 'role': roles.get(name)})
        if failed or not documents:
            log('filing left for a later run (a document failed or the index was empty):', accession)
            continue   # not recorded as done, so the next run fetches what is missing
        record = dict(filing, folder=folder, documents=saved, retrieved_at=now_iso())
        write_json(os.path.join(OUT, accession, 'index.json'), record)
        manifest['filings'].append(record)
        write_json(os.path.join(OUT, 'manifest.json'), manifest)
        log(filing['filing_date'], filing['form'], accession, [(d['name'], d['chars']) for d in saved])
    log('done:', len(manifest['filings']), 'filings')


if __name__ == '__main__':
    main_guard(run)
