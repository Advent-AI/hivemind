"""The main-numbers probe's answers, for reading by hand (D490): per case, arm and send, every new thesis (reason, question, period,
settling material, the closest open thesis and why it is a separate bet) and every kept statement with the theses it is linked to. Counting
is done by reading this listing beside the articles, never by a pattern.

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
    for case in sorted(by_case):
        print(f'\n######## {case} (step {by_case[case][0]["sequence"]})')
        for record in sorted(by_case[case], key=lambda row: (row['arm'], row['send'])):
            outcomes = '; '.join(attempt.get('outcome') or attempt.get('error', '?') for attempt in record['attempts'])
            print(f"\n  [{record['arm']} send {record['send']}] {outcomes[:110]} | kept {record.get('kept')} | new theses dropped for no link: "
                  f"{record.get('dropped_unlinked')}")
            for thesis in record.get('new_theses') or []:
                print(f"     NEW {thesis.get('local_id')} ({thesis.get('opens_as')}): {thesis.get('description', '')}")
                print(f"         outcome: {str(thesis.get('outcome'))[:260]}")
                print(f"         period: {str(thesis.get('period'))[:260]}")
                print(f"         settled_by: {str(thesis.get('settled_by'))[:200]}")
                print(f"         closest: {thesis.get('closest_open_thesis')} | separate because: {str(thesis.get('why_a_separate_bet'))[:260]}")
            for statement in record.get('links') or []:
                targets = [f"{link.get('target_type')}:{link.get('target_id')}" for link in statement.get('links') or []]
                figures = len(statement.get('figures') or [])
                print(f"     ev {statement.get('local_id')} -> {targets or 'no link'} | figures {figures} | {str(statement.get('summary', ''))[:230]}")


if __name__ == '__main__':
    main()
