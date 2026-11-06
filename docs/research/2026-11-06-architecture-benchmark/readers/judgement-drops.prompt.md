You are an independent reader. You built neither system. Read-only: do not edit any file.

The agreed benchmark design (docs/research/2026-11-06-architecture-benchmark/benchmark-design.md, "When the line stops") says a judgement question
whose agreements drop by two or more between the arms is read: its last judgement and the evidence it cites in each draw. Two questions dropped:
v9 (agreements: split 1 of 3, control 3 of 3) and v10 (split 0 of 3, control 2 of 3). The frozen judgement gold (reader B) puts v9's outcome at
$25–60 billion and v10's at 65–69%.

Input: docs/research/2026-11-06-architecture-benchmark/results/judgement-drops-packet.json. For each question: its text and ladder, and for each of
the six draws (three split, three control) the final judgement at 2026-07-14 (rung, reference, implied outcome, reasons), the evidence it cites in
full, and every record filed under the question.

For each question and each draw that disagrees with the gold, say exactly one of:
- MISSING_EVIDENCE: a record the agreeing draws used is absent from this draw's question (name the record and the agreeing draw's use of it);
- SAME_EVIDENCE_OTHER_REASONING: the draw had comparable evidence and reasoned to another rung (quote the step where the reasoning parts);
- BOTH: name each part.
Then say, per question, what the split's losses rest on, in two sentences, and whether one missing record alone would have changed the answer
(say "unknown" if the packet cannot show it). Return your answer as the final message.
