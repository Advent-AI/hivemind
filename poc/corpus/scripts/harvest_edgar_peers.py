"""Harvest the SEC filings of the peer, supplier and customer companies in companies.json for the window
(2026-07-24..2026-10-22): the forms each company lists, primary document and every exhibit, HTML kept and the
whole document converted to text. CIKs come from SEC's company_tickers.json. Public, no credentials.

Writes raw/edgar-peers/<TICKER>/<accession>/… and raw/edgar-peers/manifest.json. Resumable.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from common import RAW, SEC_USER_AGENT, WINDOW_START, WINDOW_END, fetch, decode, page_text, write_json, read_json, now_iso, log, main_guard  # noqa: E402

OUT = os.path.join(RAW, 'edgar-peers')
COMPANIES = read_json(os.path.join(os.path.dirname(__file__), 'companies.json'))['companies']


def sec_get(url, accept=None):
    status, final, body = fetch(url, user_agent=SEC_USER_AGENT, accept=accept, timeout=60)
    time.sleep(0.4)
    return status, body


def ciks():
    status, body = sec_get('https://www.sec.gov/files/company_tickers.json', accept='application/json')
    if status != 200:
        raise SystemExit(f'company_tickers failed: {status}')
    table = json.loads(decode(body))
    return {row['ticker'].upper(): str(row['cik_str']).zfill(10) for row in table.values()}


def filings_in_window(cik, forms):
    status, body = sec_get(f'https://data.sec.gov/submissions/CIK{cik}.json', accept='application/json')
    if status != 200:
        log('submissions failed', cik, status)
        return []
    recent = json.loads(decode(body))['filings']['recent']
    rows = []
    for form, date, accession, primary, description, accepted, items in zip(
            recent['form'], recent['filingDate'], recent['accessionNumber'], recent['primaryDocument'],
            recent['primaryDocDescription'], recent['acceptanceDateTime'], recent['items']):
        if form in forms and WINDOW_START <= date <= WINDOW_END:
            rows.append({'form': form, 'filing_date': date, 'accession': accession, 'primary_document': primary,
                         'description': description, 'acceptance_datetime': accepted, 'items': items})
    return rows


def documents_of(cik_short, accession):
    folder = accession.replace('-', '')
    status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{cik_short}/{folder}/index.json', accept='application/json')
    names = []
    if status == 200:
        for it in json.loads(decode(body))['directory']['item']:
            name = it['name']
            if (name.lower().endswith(('.htm', '.html')) and not name.startswith('R') and 'index' not in name.lower()
                    and not name.endswith('_htm.xml')):
                names.append(name)
    roles = {}
    status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{cik_short}/{folder}/{accession}-index.html')
    if status == 200:
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', decode(body), re.S | re.I):
            cells = [re.sub(r'<[^>]+>', ' ', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S | re.I)]
            link = re.search(r'href="[^"]*/([^"/]+\.(?:htm|html|txt))"', row, re.I)
            if link and len(cells) >= 4:
                roles[link.group(1)] = {'description': cells[1], 'type': cells[3]}
    return folder, names, roles


def run():
    manifest = read_json(os.path.join(OUT, 'manifest.json'), {'filings': []})
    done = {f['accession'] for f in manifest['filings']}
    table = ciks()
    for company in COMPANIES:
        ticker = company['ticker']
        cik = table.get(ticker)
        if not cik:
            log('no CIK for', ticker)
            continue
        cik_short = cik.lstrip('0')
        for filing in filings_in_window(cik, set(company['forms'])):
            accession = filing['accession']
            if accession in done:
                continue
            folder, names, roles = documents_of(cik_short, accession)
            saved = []
            failed = False
            for name in names:
                target = os.path.join(OUT, ticker, accession, name)
                if not os.path.exists(target):
                    status, body = sec_get(f'https://www.sec.gov/Archives/edgar/data/{cik_short}/{folder}/{name}')
                    if status != 200 or not body:
                        log('failed', ticker, accession, name, status)
                        failed = True
                        continue
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    with open(target, 'wb') as handle:
                        handle.write(body)
                    with open(target + '.full.txt', 'w', encoding='utf-8') as handle:
                        handle.write(page_text(decode(body)))
                with open(target + '.full.txt', encoding='utf-8') as handle:
                    chars = len(handle.read())
                saved.append({'name': name, 'chars': chars, 'role': roles.get(name)})
            if failed or not names:
                log('filing left for a later run (a document failed or the index was empty):', ticker, accession)
                continue
            record = dict(filing, ticker=ticker, cik=cik, folder=folder, documents=saved, themes=company['themes'],
                          company_name=company['name'], retrieved_at=now_iso())
            write_json(os.path.join(OUT, ticker, accession, 'index.json'), record)
            manifest['filings'].append(record)
            done.add(accession)
            write_json(os.path.join(OUT, 'manifest.json'), manifest)
            log(ticker, filing['filing_date'], filing['form'], accession, len(saved), 'documents')
    log('done:', len(manifest['filings']), 'filings')


if __name__ == '__main__':
    main_guard(run)
