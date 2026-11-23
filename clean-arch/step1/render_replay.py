#!/usr/bin/env python3
"""Render a local Step 1 SQLite trace as a self-contained, read-only replay."""
import argparse
import html
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit


def esc(value):
    return html.escape(str(value if value is not None else ''), quote=True)


def load_trace(path):
    conn = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    try:
        run = conn.execute('select * from run').fetchone()
        if run is None:
            raise ValueError('run record is missing')
        items = {item['input_id']: item for item in json.loads(run['source_items'])}
        rows = [dict(row) for row in conn.execute('select * from trace order by sequence')]
        if not rows:
            raise ValueError('run has no trace rows')
        return items, rows
    finally:
        conn.close()


def display_passages(evidence):
    raw = evidence.get('source_passages')
    if raw is None:
        raw = [evidence['source_passage']] if evidence.get('source_passage') else []
    verified = evidence.get('verified_source_passages')
    if verified is None:
        verified = [evidence['source_passage_verified']] if evidence.get('source_passage_verified') else []
    flags = evidence.get('source_passages_repaired')
    if flags is None:
        flags = [bool(evidence.get('source_passage_repaired'))] if verified else []
    output = []
    for n in range(max(len(raw), len(verified))):
        original = raw[n] if n < len(raw) else None
        source = verified[n] if n < len(verified) else None
        repaired = flags[n] if n < len(flags) else False
        label = f'Source passage {n + 1}'
        if source:
            output.append(f'<div class="source"><div class="source-label">{label} · located in input{" · repaired" if repaired else ""}</div><blockquote>{esc(source)}</blockquote></div>')
        else:
            output.append(f'<div class="source warning"><div class="source-label">{label} · unverified model passage</div><blockquote>{esc(original)}</blockquote></div>')
        if source and original is not None and (repaired or original != source):
            output.append(f'<details class="raw-passage"><summary>Show the passage Luna returned</summary><blockquote>{esc(original)}</blockquote></details>')
    if not output:
        return '<p class="muted">No source passage recorded.</p>'
    return ''.join(output)


def evidence_card(evidence, link, note):
    data = [('Tier', evidence.get('tier')), ('Original party', evidence.get('original_party')),
            ('Reported by', evidence.get('reporting_speaker')), ('Statement date', evidence.get('statement_date')),
            ('Date text', evidence.get('statement_date_text')),
            ('Period', evidence.get('evidence_period'))]
    metadata = ''.join(f'<span><b>{esc(k)}</b> {esc(v)}</span>' for k, v in data if v)
    note_html = f'<div class="alert"><b>Review note</b><br>{esc(note)}</div>' if note else ''
    relevance = f'<p class="relevance"><b>Why it links:</b> {esc(link["relevance"])}</p>' if link.get('relevance') else ''
    return (f'<article class="evidence"><div class="evidence-head"><span class="chip">Evidence {esc(evidence.get("local_id", ""))}</span>'
            f'<span class="muted">Model proposal</span></div><p class="statement">{esc(evidence.get("summary", ""))}</p>'
            f'<div class="meta">{metadata}</div>{relevance}{note_html}{display_passages(evidence)}</article>')


def source_preparation_detail(item):
    """Show the experimental model-selected source and the archived material."""
    raw = item.get('source_preparation')
    if not raw:
        return ''
    try:
        preparation = json.loads(raw) if isinstance(raw, str) else raw
        if preparation.get('version') != 1:
            raise ValueError('unknown source preparation version')
        roles = preparation['roles']
        overlap = preparation.get('article_generated_overlap', [])
        conflict = (f'<p class="alert">The same source lines were selected as article text and as a generated summary: {esc(overlap)}. '
                    'The role assignment needs review.</p>') if overlap else ''
        return (f'<details class="source-article"><summary>Review experimental source preparation</summary>'
                f'<p>These are model-selected page lines, not verified article boundaries or authors. '
                f'Source selection: {esc(preparation.get("source_role_arm"))}, draw {esc(preparation.get("source_role_draw"))}. '
                f'Selected line IDs: {esc(preparation.get("selected_line_ids"))}.</p>{conflict}'
                f'<details><summary>Show all source roles and line IDs</summary><pre>{esc(json.dumps(roles, ensure_ascii=False, indent=2))}</pre></details>'
                f'<details><summary>Show the earlier cleaned source</summary><div class="article-text">{esc(preparation.get("original_cleaned_text"))}</div></details>'
                f'<details><summary>Show the archived full page</summary><div class="article-text">{esc(item.get("text_page"))}</div></details>'
                f'<details><summary>Show the source-selection request and answer</summary>'
                f'<pre>{esc(json.dumps({"request": preparation.get("source_role_request"), "response": preparation.get("source_role_response")}, ensure_ascii=False, indent=2))}</pre></details>'
                f'</details>')
    except (AttributeError, KeyError, TypeError, ValueError):
        return '<p class="alert">The source-preparation record could not be displayed; review the original trace.</p>'


def page_source_detail(item):
    """Display the captured-page candidate's provenance and historical cleaned text."""
    raw = item.get('page_source_audit')
    if not raw:
        return ''
    try:
        audit = json.loads(raw) if isinstance(raw, str) else raw
        if audit['representation'] not in ('captured_page', 'historical_clean'):
            raise ValueError('unknown source representation')
        identity = audit['source_identity']
        completeness = audit['source_completeness']
        previous = audit['original_cleaned_text']
        return (f'<details class="source-article"><summary>Compare the saved source versions</summary>'
                f'<p>Sent representation: {esc(audit["representation"])}. '
                f'Target-article identity: {esc(identity)}. Source completeness: {esc(completeness)}. '
                'A saved page can include other articles or later material.</p>'
                f'<p>Article date: {esc(item.get("publication_day") or "unknown")}. '
                f'Captured at: {esc(item.get("retrieved_at") or "unknown")}. '
                f'Upstream feed: {esc(audit.get("upstream_feed"))}; '
                f'previous cleaned feed: {esc(audit.get("cleaned_feed"))}.</p>'
                f'<details><summary>Show the previously cleaned input</summary>'
                f'<div class="article-text">{esc(previous if previous else "No cleaned text was retained.")}</div></details>'
                '</details>')
    except (AttributeError, KeyError, TypeError, ValueError):
        return '<p class="alert">The saved source comparison could not be displayed; review the original trace.</p>'


def render(items, rows, annotations, independent=False):
    tabs, panels = [], []
    provisional_so_far = False
    for index, row in enumerate(rows):
        item = items.get(row['input_id'], {})
        before = json.loads(row['before_state'])
        after = json.loads(row['after_state']) if row['after_state'] else None
        result = json.loads(row['result']) if row['result'] else None
        provisional = False
        if result is None and row.get('status') == 'failed' and row.get('raw_response'):
            try:
                response = json.loads(row['raw_response'])
                candidate = json.loads(response['choices'][0]['message']['content'])
                if isinstance(candidate, dict) and isinstance(candidate.get('new_theses'), list) and isinstance(candidate.get('evidence'), list):
                    result, provisional = candidate, True
            except (KeyError, IndexError, TypeError, ValueError):
                pass
        seq, input_id = row['sequence'], row['input_id']
        item_notes = annotations.get('items', {}).get(input_id, {})
        title = item.get('title') or input_id
        day = item.get('publication_day') or 'Date unavailable'
        tabs.append(f'<a class="article-tab" href="#article-{seq}"><span>ARTICLE {seq}</span><b>{esc(day)}</b><small>{esc(title)}</small></a>')
        note = item_notes.get('note')
        note_html = f'<div class="alert"><b>Source note</b><br>{esc(note)}</div>' if note else ''
        header = (f'<section id="article-{seq}" class="article-section"><div class="article-heading"><div><div class="eyebrow">Article {seq} · {esc(row["status"])}</div>'
                  f'<h2>{esc(title)}</h2><p class="muted">{esc(day)} · {esc(item.get("publisher") or "Publisher unavailable")}</p></div></div>{note_html}')
        uri = item.get('source_uri') or ''
        external = f' <a href="{esc(uri)}" target="_blank" rel="noopener noreferrer">Open original ↗</a>' if urlsplit(uri).scheme in ('http', 'https') else ''
        header += (f'<details class="source-article"><summary>Read the supplied source text{external}</summary>'
                   f'<div class="article-text">{esc(item.get("text") or "Source text unavailable.")}</div></details>')
        header += source_preparation_detail(item)
        header += page_source_detail(item)
        state_before = {entry['id']: entry for entry in before}
        content = []
        lookup_errors = result.get('quote_lookup_errors', []) if result else []
        unverified = bool(result and (lookup_errors or result.get('unresolved_links') or result.get('unlinked_new_thesis_ids') or any(any(p is None for p in ev.get('verified_source_passages', [])) for ev in result.get('evidence', []))))
        if unverified:
            provisional_so_far = True
            message = ('This independent proposal needs review.' if independent else
                       'This exploratory state and later states are provisional.')
            content.append('<div class="alert"><b>Review needed.</b> Unverified passages, source lookup errors or unresolved thesis links are retained below. ' + message + '</div>')
            for error in lookup_errors:
                content.append(f'<div class="alert"><b>Source lookup error.</b> Evidence {esc(error.get("evidence_id"))}, passage {esc(error.get("passage_number"))}: {esc(error.get("error_type"))}: {esc(error.get("message"))}</div>')
        elif provisional_so_far and not independent:
            content.append('<div class="alert"><b>Provisional state.</b> An earlier article needs review.</div>')
        if provisional:
            content.append(f'<div class="alert"><b>Failed extraction: unaccepted model output.</b> {esc(row.get("error"))} The proposals below were not saved or added to the thesis state; source passages have not been verified.</div>')
        if result is None:
            content.append(f'<div class="alert"><b>No completed extraction.</b> {esc(row.get("error") or "The item is incomplete or in flight.")}</div>')
        else:
            proposed = {entry['local_id']: entry for entry in result.get('new_theses', [])}
            allocated = result.get('new_thesis_ids', {})
            evidence = result.get('evidence', [])
            groups = {}
            for ev in evidence:
                for link in ev.get('links', []):
                    key = (link.get('target_type'), link.get('target_id'))
                    groups.setdefault(key, []).append((ev, link))
            for local_id, thesis in proposed.items():
                groups.setdefault(('new', local_id), [])
            valid_groups = sum(1 for kind, target in groups if (kind == 'new' and target in proposed) or (kind == 'existing' and target in state_before))
            content.append(f'<div class="run-summary"><span><strong>{len(proposed)}</strong> new thesis proposals</span><span><strong>{len(evidence)}</strong> evidence items</span><span><strong>{valid_groups}</strong> defined theses shown</span></div>')
            if not groups:
                content.append('<p class="muted">No thesis–evidence pairs were returned for this article.</p>')
            for (kind, target_id), pairs in groups.items():
                if kind == 'new':
                    thesis = proposed.get(target_id, {})
                    persistent = allocated.get(target_id)
                    marker = (f'New thesis · {persistent}' if persistent else
                              'New thesis proposal · not added to state' if thesis else
                              f'Unresolved new thesis reference · {target_id}')
                elif kind == 'existing':
                    thesis = state_before.get(target_id, {})
                    marker = f'Existing thesis · {target_id}' if thesis else f'Unresolved existing thesis · {target_id}'
                else:
                    thesis, marker = {}, f'Unresolved target · {target_id}'
                question = thesis.get('description') or 'Thesis reference not available in the recorded context'
                outcome = f'<p class="outcome"><b>Tracking:</b> {esc(thesis["outcome"])}</p>' if thesis.get('outcome') else ''
                content.append(f'<div class="thesis"><div class="thesis-label">{esc(marker)}</div><h3>{esc(question)}</h3>{outcome}<div class="evidence-list">')
                for ev, link in pairs:
                    ev_note = item_notes.get('evidence', {}).get(ev.get('local_id', ''), '')
                    content.append(evidence_card(ev, link, ev_note))
                if not pairs:
                    content.append('<p class="muted">No evidence link recorded for this proposed thesis.</p>')
                content.append('</div></div>')
        state = lambda value: esc(json.dumps(value, ensure_ascii=False, indent=2))
        footer = f'<details class="technical"><summary>Inspect thesis state before and after</summary><h4>Before</h4><pre>{state(before)}</pre><h4>After</h4><pre>{state(after) if after is not None else "Not recorded"}</pre></details>'
        if row.get('raw_response'):
            footer += f'<details class="technical"><summary>Inspect full provider response</summary><pre>{state(json.loads(row["raw_response"]))}</pre></details>'
        panels.append(header + ''.join(content) + footer + '</section>')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Step 1 · Article replay</title><style>
:root{--ink:#24343a;--muted:#647575;--green:#275b4c;--line:#dce8e1;--paper:#fff;--bg:#f4f8f5}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1050px;margin:auto;padding:32px 28px 70px}h1,h2,h3,p{margin:0}h1{font-size:31px;letter-spacing:-.03em;line-height:1.2}h2{font-size:23px;line-height:1.3;margin:6px 0 7px}h3{font-size:19px;line-height:1.35;margin:8px 0}.eyebrow,.thesis-label{color:var(--green);font-size:11px;letter-spacing:.09em;text-transform:uppercase;font-weight:750}.lead{max-width:800px;margin-top:10px;color:var(--muted)}.banner{margin:20px 0 18px;padding:14px 17px;border:1px solid #e9d9b7;background:#fff9ec;border-radius:10px;color:#614d2a;font-size:13px}.tabs{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.article-tab{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--ink);background:white;border:1px solid var(--line);border-radius:10px;padding:13px 15px}.article-tab:hover,.article-tab:focus{border-color:#72a995;box-shadow:0 2px 10px #174d2d15}.article-tab span{font-size:10px;letter-spacing:.09em;color:var(--green);font-weight:750}.article-tab small{color:var(--muted);line-height:1.35}.article-section{scroll-margin-top:12px;margin-top:32px;padding:24px;background:white;border:1px solid var(--line);border-radius:14px}.muted{color:var(--muted);font-size:13px}.article-heading{display:flex;justify-content:space-between}.source-article,.technical{margin:16px 0;color:var(--green)}summary{cursor:pointer;font-weight:650}a{color:#176b58}.article-text,pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f7f4;color:#344941;padding:15px;border-radius:8px;margin:10px 0;font-size:13px}.run-summary{display:flex;gap:20px;flex-wrap:wrap;background:#eef6f1;border-radius:9px;padding:12px 15px;margin:17px 0;color:#557066;font-size:13px}.run-summary strong{font-size:18px;color:#244f41}.thesis{border:1px solid #cfdfd5;border-radius:12px;padding:20px;margin-top:14px}.outcome{font-size:13px;color:#5d716a;margin-bottom:12px}.evidence-list{display:grid;gap:12px;margin-top:17px}.evidence{background:#f9fbfa;border:1px solid #e0eae3;border-radius:10px;padding:17px}.evidence-head{display:flex;justify-content:space-between;gap:10px}.chip{font-size:11px;letter-spacing:.04em;font-weight:700;color:#3d665b}.statement{font-size:15px;font-weight:600;margin:9px 0 10px}.meta{display:flex;gap:8px 16px;flex-wrap:wrap;font-size:12px;color:#60766e}.meta b{color:#425a51}.relevance{font-size:13px;margin:10px 0;color:#536c62}.source{margin-top:13px;padding-left:13px;border-left:3px solid #b1d1bf}.source-label{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#557669;font-weight:700}blockquote{margin:6px 0;white-space:pre-wrap;color:#465b53;font-size:13px}.raw-passage{font-size:12px;color:#557669;margin-top:10px}.alert{background:#fff4df;border:1px solid #eed6a7;border-radius:8px;padding:12px 14px;margin:12px 0;color:#6d5127;font-size:13px}.warning{color:#805424}.technical{font-size:13px}@media(max-width:600px){main{padding:20px 14px 50px}.article-section{padding:18px}.thesis{padding:15px}.run-summary{gap:10px 17px}}
</style></head><body><main><div class="eyebrow">Hivemind · Step 1</div><h1>Article replay</h1><p class="lead">Follow what Luna proposed for each article, which thesis each piece of evidence informs, and the source passages it returned.</p><div class="banner">''' + esc(annotations.get('run_note', 'This is an exploratory local run, not a production record or a quality measurement.')) + '</div><nav class="tabs" aria-label="Jump to an article">' + ''.join(tabs) + '</nav>' + ''.join(panels) + '</main></body></html>\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='Existing run SQLite file, opened read-only')
    parser.add_argument('--output', required=True, help='Generated replay HTML path')
    parser.add_argument('--annotations', help='Optional review notes JSON')
    args = parser.parse_args()
    source, output = Path(args.source).resolve(), Path(args.output).resolve()
    if output == source:
        raise ValueError('output must not overwrite the source database')
    annotations = json.loads(Path(args.annotations).read_text(encoding='utf-8')) if args.annotations else {}
    items, rows = load_trace(source)
    output.write_text(render(items, rows, annotations), encoding='utf-8')
    print(f'Wrote {output}: {len(rows)} article traces')


if __name__ == '__main__':
    main()
