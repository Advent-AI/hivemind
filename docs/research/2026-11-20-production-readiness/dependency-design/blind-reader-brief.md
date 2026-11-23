# Blind reader: score six sequences against a frozen reading rule

You are an independent reader. Read `docs/research/2026-11-20-production-readiness/dependency-design/reading-rule.md` (the rule, frozen
before the answers existed) and `poc/data/july-link-test-2026-11-21/reader-packet.md` (six sequences under shuffled labels; each gives
two questions' answers on 2026-07-10..07-12, and at the end the material the questions were shown). Do not read any other file in that
folder or in `docs/research/2026-11-20-production-readiness/dependency-design/` (other readers' marks are there). Reference points from
the material: Q1 FY2027 total revenue $81.6B, Q1 Data Center $75.25B, Q2 total-revenue guide about $91B.

For each sequence, apply A, B and C to the 07-12 answers of v9 (Data Center) and v14 (total revenue), and D where v9's answers show it
read v14 (a sequence where v9 never cites v14 is one where D does not apply). Score each line as written; give the figures and the
arithmetic you checked; where a line is a judgement call, say which way you read it and why. Then the harm checks over the whole window
(first-attempt refusals; material grounding errors as the rule defines them), and the verdict of the pass line, stating which sequences
you counted as linked (from the answers alone) and which as controls. Write Markdown.
