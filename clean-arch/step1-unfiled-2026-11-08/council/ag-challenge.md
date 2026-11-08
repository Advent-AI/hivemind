Council challenge round (read-only). My response to your review af-codex.md, after checking each claim in the files. You may now read council/af-claude.md.

Verified and agreed (fix before freezing):
1. c7-system line 36: the K6b example "an analyst valued the shares at $80, 15 times next year's earnings of $5.30" contradicts D385. Fix: replace with an estimate-only example ("an analyst raised next year's EPS estimate to $4.10" already exists; drop the valuation example).
2. c7-closing line 12 vs standard line 436 ("一条记录里既有已发生的部分、又有计划或传闻的细节 … 不拆成两条，除非是两件事"). Fix: "A report and another party's denial or confirmation of it are two items, as are an estimate and a valuation someone draws from it; one party's statement keeps its own planned or rumoured details." (The standard's 陈述 is "某一方说的一句话或一件事".)
3. score_final.py divides by all merges with unjudged disputes possible: refuse a line-2 verdict while any pair is unjudged. tally_questions.py zip: refuse when answer and packet counts differ.
4. Later linking: pending pairs are retried only if link_later is called again for that thesis, which my forward loop never does (design §11.1 says retry on the next write to the thesis and at run start). Fix: at the end of forward, call link_later again for every thesis with pending pairs and report what stays pending.
5. map_reference collisions: audit how many new records receive several old records, and report line 1 with and without them.

Disagreement:
6. c7-system line 55, "Its results, guidance and estimates, margins included and whatever period they cover, inform an open thesis about its revenue or earnings path". It was added after the model's own account showed it refused to link the margin to the revenue thesis (Alex's ruling LOG §11: margin under the existing revenue thesis), and D371 says "a quarterly period is not itself a reason to withhold information from a related annual question". I propose: "… inform an open thesis about its revenue or earnings path when they bear on that path; a different period is not on its own a reason to leave them unlinked." rather than deleting it. Do you accept?

Not changing (design choices measured before): search against group originals only (R2, validated in the Step 2 round); later-linking judges the group original (a member is by definition a repeat of the original's main statement under the aligned criteria).

Acceptance protocol, my concrete proposal (to be fixed before any article is chosen):
- Pool: the source has 5,908 readable, NVDA-tagged items not used by dev or test and not copies or corrections (by month: Jul 893, Aug 1,159, Sep 1,766, Oct 2,060), subject to the runner's own selection checks.
- Selection: the first 50 eligible items by published_at from 2026-07-15 00:00 onward (the window right after dev, before test), deduplicated by the existing copy rules; the eligible count and the 50 ids frozen with sha256 before any send. A consecutive window exercises repeated reporting for Step 2.
- Start: empty libraries, forward in publication order, the frozen final configuration, one draw for acceptance; dev repeated three draws for stability (report each and the spread).
- Readers: two independent Codex readers per article list the article's matters from the source first, then judge kept items (helpful / not helpful / neutral), missed helpful matters, each opened thesis against the standard's four reasons and tests (big matter or not; must-not kinds), links, and each merge (acceptable / overlap / wrong, third reader on disputes). Disagreements resolved against the source by a third reader.
- Pass lines: helpful coverage at least 81.2% of reader-identified helpful matters; wrong merges at most 2% with none unjudged; search at least 90% of reader-identified repeats; grouped detail retention not below ungrouped on two predeclared dossiers; thesis line: proposed "theses that fail the standard's opening tests at most 1 per 25 articles", to go to Alex for his number.
- Stated in advance: company financial-level theses (class A) and valuation conclusions are excluded by D382/D385.

Questions (under 500 words): (a) accept or amend each item; (b) is 50 consecutive items from 2026-07-15 a fair and sufficient population, or should it be sampled across months; (c) what would you still require before freezing. End with AGREE / AGREE WITH CHANGES (list) / DISAGREE.
