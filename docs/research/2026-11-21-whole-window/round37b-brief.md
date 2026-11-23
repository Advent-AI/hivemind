# Council round 37, challenge: linked-1 finished (read-only)

Same scope and limits as before. linked-1 is finished; read its copy at
`/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/linked-1-copy/` (read-only).

## New facts (verify each)

1. linked-1 completed 07-01..09-20; every acceptance check true (summary.json). Spend for both sequences $1.70 of $2.50. Links
   committed: v14 reads v8 ("stand-alone CPU sales FY2027"), v9 reads v14, v16 reads v14, v21 reads v16.
2. **H1 as registered, now:** on the 200 matched reader-days, linked-1 has 5 reader refusals (8777, 8848, 8855, 8888, 8909), control-1
   has 1 (8807): excess 4, the harm line. If control-1 were resumed, (v21, 09-08) would become a matched day (linked judged v21 that
   day) and control's 8938/8941 would count, bringing the excess to 2 or 3. So option C would move H1 across its line through the
   very refusals that invalidated the control. I now agree with your A: C cannot be a registered reading.
3. **linked-1's refusals:** 11 refused rows: 4 old-2 refusals given back to non-readers (e88, e3955, e3998, theme ids), and 7 reader
   refusals, all corrected on retry: 8777 v16 `e693` (one-edit id); 8822 and 8855 v16 pushed on `v14` (its dependency) as an evidence
   id; 8848, 8909 v14 and 8888 v9 and 9021 v21 put theme ids (v5, v6) in `cites_views` beside their dependency. Across the four stored
   v118 runs and both pilot arms, every refused judge answer is an id-membership error (an id not in the list the field allows). The
   prompt (judging-v7 = judging-v8, line 7) says themes are not cited in `cites`; nothing says they are not `cites_views`; the schema
   gives `cites_views` no description and no closed set.
4. **P, read by hand on a sample (exploratory, not the registered reading):** contradictions.py on 07-10..09-07: linked-1 3 definite of
   60, control-1 28 of 60 (whole window linked-1 3 of 73). I read linked-1's 3 definite dates (07-22, 08-03, 08-09) and its one overlap
   (08-21): all four are parser artefacts: the Data Center text is "About $352 billion: v14's approximately $387.3 billion … multiplied
   by 91%" and the parser took the total's amount. In linked-1, Data Center is computed as a share of v14's total on every date I read.
   Five random control-1 definite dates (07-15, 08-19, 08-23, 08-25, 09-06) are real (Data Center $400-439B against a total of
   $387-407B).
5. **H4, read by me on all 71 post-link v14 forecasts of linked-1:** four answers add v8's CPU forecast on top of a total built from the
   company's total-revenue guidance: 07-15 (judgement 118) "Adding the dependency's approximately $19.5 billion stand-alone CPU forecast
   gives about $407 billion", 07-16 (134), 07-17 (150, "as incremental"), 07-18 (153); in force 07-15..07-19. 07-20 (174) reverses it
   ("included within, not added to"); 07-10, 07-11, 08-20, 08-22 say the CPU figure is part of the total; 63 do not mention it. By
   §4 and §8, any double count is harm: with a valid control the pilot would still have stopped (H4). Please read the 71 v14
   judgements yourself, blind to my list (`judgements` where view_id='v14' and publication_day>='2026-07-10', implied_outcome and
   reasons), and list every double count you find before comparing with mine.

## Questions

1. Consensus on A: pair 1 closed as inconclusive (control double refusal), C and B not run. Agreed?
2. The exploratory findings to report beside the verdict, labelled one pair, one draw, not blind-read: (a) the part reading its whole
   (Data Center reads total) removed the contradiction class in this draw; (b) the whole reading its part (total reads stand-alone CPU)
   produced CPU double counting on four answers; (c) the links raised id-membership refusals (6 of 7 reader refusals involve the new
   block). Is each stated correctly, and is anything missing (for example H1's own numbers)?
3. The next step for Alex, as one recommendation and one test. My candidate: open one new version that (i) gives every id field of the
   judge a closed list built from the exact request (cites and push ids = the evidence ids shown; cites_views = its dependencies;
   theme_pushes ids = the themes shown), which removes the whole refused-answer class seen in about 7,700 stored judge calls, in both
   arms; and (ii) links a part and its whole only in one direction, the part reading the whole (part and whole known from the typed keys:
   same company and period, a component revenue against total revenue), so no whole reads its own part. Test: $0 checks on stored data
   (every stored accepted answer fits its closed lists; every stored refused answer is outside them; the new link plan on the three probe
   draws), then one fresh pre-registered pair with a resume-once rule for a double refusal, about $2. Challenge: is (ii) case-fitted to
   CPU/total revenue? Is it identity (code) or judgement (model)? Should (i) and (ii) be one version or two? Does changing the control's
   judge (i) break the comparison with the frozen product, and is that acceptable? Or is the right recommendation to stop the link line?
