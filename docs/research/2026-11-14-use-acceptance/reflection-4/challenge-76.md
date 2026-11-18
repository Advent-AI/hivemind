# Round 77: G settled as a separate diagnostic, as gate 1's accounting treats it. Go or no-go.

DESIGN-A2 v4: "correct" means no failed gate-accounted mark (the marks gate 1's accounting settles), W and H included; G is reported
apart, as gate 1's accounting reports it; each recovery topic is printed with the sends whose G both first readers mark failing
(`probe_score.py`, the new report line after the decisions, read from the raw rows of both families); a recovery counted correct is not
called wholly sound when its G fails. Tests 10 + 17 pass. End with `CONSENSUS: yes` (send; read as designed) or `CONSENSUS: no, because …`.
