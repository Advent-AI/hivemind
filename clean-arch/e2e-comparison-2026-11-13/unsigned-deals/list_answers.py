"""The unsigned-deal probe's answers, for reading by hand (D474): per case, arm and send, every new thesis (reason, question, period) and
every kept statement with the theses it is linked to. Counting is done by reading this listing beside the articles, never by pattern.

  python3 list_answers.py <records.jsonl> > answers-listing.txt
"""
import collections
import json
import sys


def main():
    records = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
    by_case = collections.defaultdict(list)
    for record in records:
        by_case[record['case']].append(record)
    for case in sorted(by_case, key=lambda name: (not name.startswith('u'), name)):
        print(f'\n######## {case}')
        for record in sorted(by_case[case], key=lambda r: (r['arm'], r['send'])):
            outcomes = '; '.join(a.get('outcome') or a.get('error', '?') for a in record['attempts'])
            print(f"  [{record['arm']} send {record['send']}] {outcomes[:90]}")
            for thesis in record.get('new_theses') or []:
                print(f"     NEW ({thesis.get('opens_as')}): {thesis.get('description', '')[:230]}")
                print(f"         period: {str(thesis.get('period'))[:150]}")
            for link in record.get('links') or []:
                targets = link.get('thesis_ids') or link.get('links') or link.get('theses') or link.get('linked')
                print(f"     ev -> {targets}: {str(link.get('summary', ''))[:170]}")


if __name__ == '__main__':
    main()
