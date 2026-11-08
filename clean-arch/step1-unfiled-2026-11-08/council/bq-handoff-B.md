You are a senior hedge-fund analyst reading blind for a measurement (read-only; do not open any other file of the repository, and do
not look for which system proposed what). Read `clean-arch/step1-unfiled-2026-11-08/council/bq-packet-B.md`. It quotes a standard
(section 3 of an extraction prompt and decision D388), then gives articles, each with the questions open before it and questions
proposed after reading it.

For every proposed question (labels like fresh-9/T3), judge it against the standard and the article only:
- open: a separate bet a senior analyst covering the company would hold, that fits one of the four reasons, has a date, and that no
  open question or other listed question already asks;
- small: by its own scale it does not change the company's revenue, profit, cash or credit risk enough for a separate bet;
- off_topic: not a bet on this company an analyst would hold;
- duplicate: an open question already asks it (name which);
- fragment: a part, period or wording of another bet;
- wrong_fact: it misstates what the article says (for example, calls signed what the article says is agreed, or the reverse).

Several proposed questions in one article may be wordings of the same matter: judge each on its own. Where the scale of an obligation
or stake matters, say what you compare it with. Write one line per question, every label in the packet, in this form:
`<label> | <verdict> | <the article sentence it rests on, short> | <one-sentence reason>`
End with the count of labels judged.
