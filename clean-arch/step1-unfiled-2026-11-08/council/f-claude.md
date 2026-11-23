# Claude's reflection (written before reading Codex's)

## Lessons

1. **The account located a contradiction, but the fix did not move behaviour measurably.** The model's account named "one quarter's
   figures … or unfiled" (a real D371 contradiction), yet removing it (u1k) changed nothing the instrument can see. Accounts locate a
   stated reason; they can be post-hoc. What did move behaviour in probe 1 was cutting two general sentences: the role paragraph's
   restatement of the unfiled rule, and "a number … alone is not enough to open". Instruction salience matters more than the specific
   wording.
2. **The instrument is weaker than the effect.**
   - The two reader families disagree 15 against 6 on the same control answers.
   - The dev ruler cannot see D371 items.
   - Unfiling varies by draw (dev d1 15, d2 34).
   - 16 cases × 3 draws cannot separate arms that differ by 3 items.
3. **The test-set miss is partly protocol and chance.** K6b at the empty state opens revenue and margin theses for article 57 in 3 of 3
   draws. The test run began from an empty library over sparse articles. 32 against 35 is one draw on 42 entries.

## Conclusions weaker than they look

- Probe 1's "only the combination works": retracted.
- "The D371 sentence causes the test miss": located, not shown by intervention.
- "u1k opens good theses": true for the theses it opened, but at +14 theses over 48 answers, whether that density holds over a forward
  run is unknown.

## Remaining problems, by product impact

1. **Unfiling variance** makes recall unstable run to run (8 helpful matters between dev draws). It affects every run.
2. **Bootstrap:** a new entity's first results can be dropped when no home exists yet. That is at most a short window per entity, with
   core information at stake.
3. **The gold–standard mismatch on small matters (D373):** a measurement issue, not a product one.

## Next angle: one recommendation

**Stop prompt iteration on this class.** Two rounds moved nothing the instrument can see, and a third arm would be tuning inside
noise (a trap already paid for). Record the defect.

Take one product question to Alex, the structural lever the evidence points to: **what happens to an unfiled statement.**
- Now, by D209 (his words), it is dropped.
- The census shows unfiled items carry about 2.4 helpful matters per not-kept span, and some get a home a day later (Dell RTX Spark,
  Oct 9 against Oct 10).
- A product option: keep unfiled statements for a short window, so that a thesis opened later can pick them up. That is the bootstrap
  case.
- This reverses D209 in part, so it is his call, with the census as evidence.

**Instrument improvement**, if he wants more prompt work: a separately versioned D371 evaluation (D371 itself calls for one). A new
evaluation piece needs his decision (AGENTS §7.1).
