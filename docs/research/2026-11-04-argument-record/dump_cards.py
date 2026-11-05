"""The reader's packet for H6 (log.md): for the questions judged most often in a finished judging-v8 run, the question, its final card,
and for every ref the piece it cites (quote, one-line summary, speaker, original party and day, source) or the dependency or theme
conclusion it cites, in the version the card's read record names (the judgement the card read, never a later one), plus the evidence in
force the final card does not cite (one line each), so a reader can judge what the card left out.

usage: python3 dump_cards.py <run folder> <output.md> [questions=10]
"""
import json
import sqlite3
import sys


def main():
    run, out = sys.argv[1], sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    busiest = [r[0] for r in conn.execute('select view_id from judgements group by view_id order by count(*) desc, view_id limit ?', (count,))]
    lines = ['# Argument cards for an independent reader', '',
             'For each question: its final card, every piece or conclusion the card cites, and the evidence in force the card does not cite.', '']
    for vid in busiest:
        view = conn.execute('select * from views where view_id=?', (vid,)).fetchone()
        card_row = conn.execute('select * from arguments where view_id=? order by id desc limit 1', (vid,)).fetchone()
        versions = conn.execute('select count(*) from arguments where view_id=?', (vid,)).fetchone()[0]
        state = conn.execute('select rung, reference, implied_outcome, reasons from judgements where view_id=? order by judgement_id desc limit 1', (vid,)).fetchone()
        lines += [f'## {vid}: {view["question"]}', f'Due {view["due_day"]}; {versions} card versions; last rung {state["rung"]}; reference: {state["reference"]}; implied: {state["implied_outcome"]}', '']
        if not card_row:
            lines += ['(no card)', '']
            continue
        card = json.loads(card_row['card_json'])
        cited = set()
        for side in ('for', 'against'):
            lines.append(f'**{side}**')
            for c in card[side]:
                lines.append(f'- {c["id"]} [refs {", ".join(c["refs"])}; relays {", ".join(c["relays"]) or "none"}; {c["independent_sources"]} independent] {c["text"]}')
                cited.update(c['refs'])
        lines += [f'**would move it**: {"; ".join(card["watch"]) or "none"}', f'**not known**: {"; ".join(card["gaps"]) or "none"}',
                  f'**removed in this version**: {"; ".join(r["id"] + " — " + r["reason"] for r in card["removed"]) or "none"}', '', '**cited**']
        for ref in sorted(cited, key=lambda x: (x[0], int(x[1:]))):
            if ref.startswith('e'):
                e = conn.execute('select * from evidence where evidence_id=?', (ref,)).fetchone()
                src = conn.execute('select input_id, publication_day from evidence_sources where evidence_id=? order by rowid limit 1', (ref,)).fetchone()
                lines.append(f'- {ref} [{e["tier"]}; {e["speaker"]}; original {e["original_who"]} {e["original_day"]}; from {src["input_id"] if src else ""} {src["publication_day"] if src else ""}] '
                             f'{e["one_line"]}\n    Quote: {e["quote"][:500]}')
            else:
                v = conn.execute('select question from views where view_id=?', (ref,)).fetchone()
                read_id = (card.get('read') or {}).get(ref)
                if read_id is None:
                    raise SystemExit(f'{vid}: the card cites {ref} but its read record names no judgement of it')
                s = conn.execute('select rung, reasons, publication_day from judgements where judgement_id=?', (read_id,)).fetchone()
                lines.append(f'- {ref} (a dependency or theme, its judgement {read_id} of {s["publication_day"]}, the one this card read) {v["question"] if v else ""}: '
                             f'rung {s["rung"]}; {s["reasons"][:300]}')
        uncited = [r[0] for r in conn.execute('select l.evidence_id from evidence_links l where l.view_id=? order by l.id', (vid,)) if r[0] not in cited]
        lines += ['', f'**in force but not cited by the final card ({len(uncited)})**']
        for ref in uncited:
            e = conn.execute('select evidence_id, tier, original_who, original_day, one_line from evidence where evidence_id=?', (ref,)).fetchone()
            lines.append(f'- {ref} [{e["tier"]}; {e["original_who"]} {e["original_day"]}] {e["one_line"]}')
        lines.append('')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'wrote {out}: {len(busiest)} questions')


if __name__ == '__main__':
    main()
