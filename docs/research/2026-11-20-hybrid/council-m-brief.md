# Council M: after D687, is any opening test worth sending?

**New since council L.** Alex answered D382 for the hybrid: "单独开题吧". Recorded as D687 (`docs/DECISIONS-log.md`, last entry): in
the hybrid, a company's own material, separately answerable figure keeps its own question, as old's opening does. D382 stays for the
clean path.

**Read:** `docs/research/2026-11-20-hybrid/OPENING-CENSUS.md`, the new last section "After D687: the attainable check". Its data
sources are:
- `poc/data/comparison-2026-11-17/reading-diagnostic/deck/readings.json` and `mapping-out/mapping.json`, with the PRD's served rule in
  `clean-arch/PRD.md` lines 135–146;
- `poc/data/hybrid-2026-11-20/opening-census.json`;
- the frozen prompt `src/hivemind/prompts/role-v74i.txt` (line 1, and lines 13–15 on `binding_obligation` and on same versus
  another question).

**Out of scope:**
- the frozen ruler and the frozen 32-matter list (D671; a concern about them is recorded, never an edit);
- the clean path;
- D198's judge line (paused, D685).

## Claude's position (written before reading yours)
1. **Per-draw served counts for old:**
   - 3 of 3: M11, M13, M15, M18, M31 (and M04 under counting 2);
   - 2 of 3: M04 under counting 1, M06, M10, M17, M19;
   - 1 of 3: M05, M09, M25 (and M30 under counting 2).

   With old's opening, noise alone costs about 1.3 of the five 2-of-3 matters and gains about 0.8–1 of the 1-of-3 ones.
2. **The only mechanism within the standing rules that a new extraction version could fix is the obligation form.** It covers 3
   matters:
   - **M12:** the Ohio guarantee is reported as agreed ("agreed last month to provide a guarantee of up to $105 billion"). By the prompt's
     own `binding_obligation` rule, its amount at the next annual filing is the question. Old keeps linking to "will NVIDIA sign it" and
     to the aggregate credit-support question.
   - **M27:** the Hugging Face acquisition is agreed at $12.9B. Old holds only its completion.
   - **M20:** "may put up as much as $125 billion" is not signed, which calls for a yes/no question. Old links it to the aggregate.

   Add M05, a theme quantity proposed once under a free name and refused by the research-list check. M09, M30 and M25 are 1-of-3 coin
   flips; steadying M09 and M30 widens "not every reported or guided line". M07, M16, the five-company capex matters, the review
   stages, M32 and the five other-company matters need a rule of Alex's to change: D248, the four opening reasons, or the library
   subject.
3. **Arithmetic:**
   - **Best case:** 7 gross gains with no loss. That passes D665 only if every one converts in 2 of 3 draws.
   - **Expected:** a ≈ 3.4, b ≈ 1.4 plus any regression from a new extraction version, net about +2. So "no practical winner".

   **An opening test within the standing rules cannot decide release, so it is not sent as a release test.**
4. **What I would do next. Challenge it:**
   - **(a) Diagnosis only, a few cents.** Get the model's own account on the obligation-form cases: M12's and M27's agreed-deal
     articles, and M20's article, in old-1..3. Ask which instruction led it to link and not propose, and what it would propose. If it
     is a misread of the prompt's own rule, it is a real defect, since an analyst tracks how much of a $105B guarantee is outstanding.
     Its fix is a quality change for the hybrid, not a release lever.
   - **(b) To Alex, as the binding question:** the library subject. Should the research also open questions on key figures of
     research-list companies other than NVIDIA that articles about NVIDIA carry (Alphabet's capex, Broadcom's AI revenue, CoreWeave's
     revenue), under that company as D187 says? My lean is yes for companies already on the research list. It is the largest lever,
     up to +4 (+5 with Marvell added), and it is a scope choice only Alex makes.
   - With (a) and (b) together, the best case is +11 and the expected value is perhaps +5. Only then would an opening test against
     old be worth its cost.

## Questions to you
1. **Check each mechanism** against the stored trace and the prompt:
   - Is M12/M27/M20 really a misread of the `binding_obligation` rule?
   - Or does "as one deal or as a programme" let the aggregate credit-support question legitimately take M12 and M20?
   - Does an agreed acquisition fall under `binding_obligation` ("an equity stake whose size is stated and is not yet completed")?
2. **Check the arithmetic and the per-draw counts.** Is the expected-value argument sound enough to skip a paid opening test?
3. **One next step.** Is it (a), (b), both, or something else? If (b), is library scope the right question for Alex, or is the binding
   constraint really the matter list's granularity against D248, which is a ruler concern and not his product choice?
4. **Falsifiers.** What result of (a) would change the plan?

End with one line: CONSENSUS (you agree with the position as written or with named edits) or DISAGREE (with the alternative).
