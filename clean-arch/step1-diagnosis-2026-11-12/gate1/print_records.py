"""Prints every gate-1 record for reading by hand: the final outcome, each retained new thesis whole, and the kept or unlinked evidence
that quotes a given phrase, with its links. It decides nothing.

  python3 clean-arch/step1-diagnosis-2026-11-12/gate1/print_records.py <records.jsonl> [phrase ...]
  python3 clean-arch/step1-diagnosis-2026-11-12/gate1/print_records.py <records.jsonl> --full   # every evidence item whole
"""
import json, sys
records = [json.loads(line) for line in open(sys.argv[1])]
full = '--full' in sys.argv[2:]
phrases = [a for a in sys.argv[2:] if a != '--full']
for record in sorted(records, key=lambda r: (r['case'], r['arm'], r['send'])):
    last = record['attempts'][-1] if record['attempts'] else {}
    print(f"== {record['case']} | {record['arm']} | send {record['send']} | attempts {len(record['attempts'])} | "
          f"{last.get('outcome') or last.get('error')} | kept {record.get('kept')} unlinked {record.get('unfiled')} dropped {record.get('dropped_unlinked')}")
    for thesis in record.get('new_theses') or []:
        print(f"   NEW {thesis.get('local_id')}: {thesis.get('description')}\n       outcome: {thesis.get('outcome')}\n       period: {thesis.get('period')}")
    for item in record.get('links') or []:
        if full:
            print(f"   EVIDENCE {item.get('local_id')}: links {[link.get('target_id') for link in item.get('links') or []]}\n"
                  f"       summary: {item.get('summary')}\n       passages: {item.get('source_passages')}")
            continue
        text = json.dumps(item, ensure_ascii=False)
        if any(p.lower() in text.lower() for p in phrases):
            print(f"   EVIDENCE quoting {[p for p in phrases if p.lower() in text.lower()]}: links {[link.get('target_id') for link in item.get('links') or []]} | "
                  f"{(item.get('summary') or '')[:200]}")
