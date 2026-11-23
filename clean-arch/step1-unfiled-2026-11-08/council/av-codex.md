c8 is adopted and passed its agreed checks on one fresh, narrow article sequence; the clean system’s ability to help an analyst reach the right conclusion remains untested.

For example, it kept 132 of 139 useful matters, but it never opened the specific Ohio guarantee question in three development runs.

### 1. Summary

The day began with K6b keeping 32 of 42 useful test matters, with seven of the ten misses extracted but discarded because no question took them.  
Alex decided to keep useful unlinked material, treat financial figures as conditions, and open questions only for large matters under the agreed boundaries.  
After several attempts and a retrospective council, c8 was frozen and tested on 50 previously unused articles: it kept 132 of 139 useful matters, opened one wrongly judged question, found 141 of 143 available repeat pairs, and made one clear wrong merge in 57.  
The three development runs kept 214, 211 and 212 of 234 useful matters, while all three missed the specific Ohio guarantee question.  
Alex adopted c8 for clean Step 1, and a subsequent investigation of weak links stopped before any new prompt was sent. ([Log §§43–46](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1603))

Two corrections to Claude’s reflection: development search was **98.9%–100%**, not 99%–100%; and the log supports **$0.66 for the fresh Step 1 run**, but does not substantiate its claimed $4.20 total for that run plus the three development runs. The log also says Alex authorized finding the cause of weak links, not designing a new check. ([Reflection](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/council/au-claude.md:15), [log](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1696))

### 2. What worked and what failed

The decisive improvement was a product decision: useful material could survive without an existing question. That removed the need to invent a question merely to save a fact. Separating a report from another party’s denial also addressed a grouping cascade in which one bundled record caused six wrong merges.

Claude’s lessons are too confident in three places:

- **“Council catches errors before they cost a run”** is only true when the review actually happens before the send. Several changes bypassed it, and a council itself initially miscounted merges. Reading the underlying prompt corrected that mistake.
- **“Read-back is the strongest lever”** is not established. The model’s later explanation identifies a possible cause; it does not show that a closing check will fix it. The proposed check could discard the very evidence that founded a question.
- **“The cause is found”** overstates the evidence. The model reported topic overlap and inference chains, but no intervention has isolated or fixed their contribution.

The missing lesson is that a passing total can hide the wrong question or an unusable grouping. Another is that single-draw differences and disagreeing readers cannot reliably identify an improvement: calibration agreed on only 17 of 52 disputed cases. The test set was then used across configurations, making a new fresh set necessary. ([Log §§8–10](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:230), [§39](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1440))

### 3. Where the work stands

**Accepted:** Alex adopted c8 as the clean Step 1 configuration. The fresh run met the declared checks under their agreed definitions.

**Measured, with limits:** the fresh set was one holiday-weekend draw with no NVIDIA posts. One repeated story supplied 55 search pairs; revisions were barely exercised. The detail result establishes that grouped records retain text, not that an analyst or a later step can use it. Search was 141/143 among available pairs and **141/145 across the whole system**, including two pairs lost when an item was not kept. ([Log §44](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1645))

The PRD and D387 state the results correctly, but their compact presentation can imply broader acceptance than this evidence supports. In particular, “about one link in five” and “2% wrong” are estimates from one fresh sequence and a recheck of the 34 disputed links plus ten controls; the other 49 links were not independently rechecked in that exercise. ([PRD](/Users/lchingen/hivemind/clean-arch/PRD.md:547), [D387](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4142))

### 4. Open issues, ranked by product impact

1. **Ohio guarantee coverage.** The specific yes/no question was missed in all three development draws; a broader credit-support amount question appeared instead. That can leave an analyst without the answer to a distinct risk. Its frequency and cause beyond this case are not established.
2. **Wrongly opened revenue-share question.** One of ten fresh-set questions merely tracked Vera Rubin’s revenue share, contrary to Alex’s decision. It adds a misleading question, but this is one observed case.
3. **Weak links.** The recheck found 19 weak and two wrong among 34 disputed links; weak links add reading clutter, while wrong links can mislead. The product cost and prevalence outside this sequence remain unknown. I would not yet rank clutter above a repeatedly missing material question.
4. **Passage fidelity.** Two of 288 stored items had unverified passages, including an inserted word. They were marked, but incorrect quotations can undermine trust.

**Step 4 is a larger end-to-end capability gap**, but its contract is still open and outside the modules taken up for this review. It means none of these results establishes that the clean system can judge an investment view; it is not a defect to assign to this slice.

### 5. Check-in readiness

I would correct these documents before a commit:

- [CURRENT_STATE.md:3](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:3) leads with the older K5 status, and [line 24](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:24) says Steps 2–4 are not built. The later c8 status shows Steps 2–3 have since been exercised; mark the earlier account as historical and lead with the current state.
- [CURRENT_STATE.md:133](/Users/lchingen/hivemind/docs/CURRENT_STATE.md:133) calls the link cause “found.” State that the model supplied plausible explanations, with no fix proven.
- [au-claude.md:17](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/council/au-claude.md:17) incorrectly claims approval to design the check; also correct its search range and unsupported cost total.
- [PRD.md:550](/Users/lchingen/hivemind/clean-arch/PRD.md:550) and [D387](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4147) should carry the whole-system search denominator and the narrow fresh-set and storage-test limits alongside the headline numbers.

**KEEP DOING:** Read source and answers directly; challenge proposed changes before sends.

**STOP DOING:** Generalizing one ruling, treating model explanations as proof, or selecting versions using the exposed test set.

**START DOING:** Put the repeated Ohio miss through a source-backed trace and establish what distinct answer the broader question fails to provide before choosing the next change.