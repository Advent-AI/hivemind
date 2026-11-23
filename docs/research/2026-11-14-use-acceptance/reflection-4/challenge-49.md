# Round 50: both round-49 points fixed. Accept or not.

1. The page check now also compares each card's status at the page's day with the served status (`serving_while_writing.py`; rerun,
   `serving-while-writing.txt`, exit 0): on 2027-01-31 after its closing, the three due questions' cards read "Closed" and the other
   four "Open", as served as of 2027-01-31 (on 2027-01-30 the three would read "Open"), and on 2026-09-25 mid-day the five cards' statuses
   equal those served as of 2026-09-24; the question identities still compared. First day reported as the known defect B.
2. `LIVE-READ-DESIGN.md`: the per-read guard section is marked "Rejected proposal, not built", above the status section.

End with `CONSENSUS: yes` (accept A; B recorded; the next step is the $0 live-service design) or `CONSENSUS: no, because …`.
