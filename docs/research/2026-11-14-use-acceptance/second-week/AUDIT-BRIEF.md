# Independent read for a prompt audit of two classes of marks (read-only)

Repository `/Users/lchingen/hivemind`. You are an independent second reader. Do not edit files, run model calls or start runs.
You are not told what the first reader concluded; do not look for it (do not open any other file of
`docs/research/2026-11-14-use-acceptance/second-week/` than the two named below, and nothing under `reflection-2/`).

## What is audited

A step writes, for one research topic opened from one news article, the one question the topic is judged on, with its answer
choices. Its whole request, as the model reads it:
- the instructions `clean-arch/step4-2026-11-10/ladder/candidate-system.txt` (23 lines; line 5 and line 16 matter most here);
- the closing check `clean-arch/step4-2026-11-10/ladder/candidate-closing.txt`, placed after the article;
- the answer's schema `clean-arch/step4-2026-11-10/ladder/candidate-schema.json` (read the descriptions of `not_judged` and of
  `reference` with its `words`, `kind`, `value`);
- the user message: the company, a fiscal-year note, the list of themes (id and name), the topic's five fields (`description`,
  `outcome`, `period`, `opens_as`, `settled_by`) and the article.

Readers then mark each answer with the form `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md` (rows `L`, `X`, `XR`).
The owner's decisions behind the two fields: in `docs/DECISIONS-log.md` search "## D397" (one judged question a topic; every
other part of its wording listed as not judged), "## D436" (a second side of one bet stays in the topic, shown as not judged),
"## D411" (a reference's kind) and "## D547" (an earlier audit of unlisted parts: read what it found and what it left open).
How an answer is shown to the later judge: `clean-arch/step4-2026-11-10/ladder/ladder_step.py`, from the line
`reference = ladder.get('reference')` near line 327 to the end of that function.

The cases: `docs/research/2026-11-14-use-acceptance/second-week/proofs/audit-cases.json`.
- `event_reference_cases_failed_or_open`: every stored answer about an **event** whose reference mark (`XR`) failed or was left
  open by the third readers, in three readings, with the article's sentence, what each of the topic's three attempts wrote in
  `reference` (null or the quoted words) and how it was marked.
- two samples of event answers that both reader families held: with no reference, and with a quoted one.
- `unlisted_parts_new_agreed_cases`: two topics of one week where both families failed `L` on some attempts.
- `every_topic_of_the_week_with_what_each_attempt_listed`: all thirteen topics of that week, each with its `description`, its
  `outcome` and what each attempt listed in `not_judged`.

## What to return

**A. The reference of an event.** (1) Quote the words of the request that decide whether an event's reference is null or a
quotation, and the words of the reading form that decide the mark. Do the two say the same thing? (2) For each distinct
expectation in the cases (group repeated runs of one article), say whether the request, read carefully, requires quoting it,
forbids it, or leaves it open, and whether the step did the same thing in every attempt. (3) Were the same words of the same
article marked the same way in every reading? (4) Does any later reader of the answer (the judge) see an event's reference?
(5) One verdict for the class, from this closed set, with one sentence why: `contradiction` (two sentences of the request pull
opposite ways, or the request removes what the decisions keep), `missing` (no sentence decides the case), `abstract` (a clause
without an example, read differently each time), `misread` (the sentence is plain and the model does not apply it), `not the
prompt` (the readers, the form or the code). If different cases need different verdicts, give each.

**B. The unlisted parts.** (1) For every topic of the week, sort each thing the topic names beyond what its question asks by
where it sits: in the `description`, or only in the `outcome`. Count, for each place, in how many attempts the part was listed.
(2) Quote the words of the request that say what must be listed. Do they say which of the topic's fields "the topic's wording"
is? (3) Say whether D547's finding holds, fails or cannot be told on these new cases. (4) One verdict from the same closed
set, with one sentence why. (5) Is the list a later reader sees (the product shows it beside the answer)?

**C.** For each class: is a general repair of the request worth designing, judged by what a reader of the product or the judge
would gain, and what could it break? Name cases in the packet that a repair must leave as they are. Do not write the repair.

Answer in English, at most 700 words, facts first. Where the packet is not enough to decide, say so instead of guessing.
