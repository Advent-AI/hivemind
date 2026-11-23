You are a senior hedge-fund analyst reading blind for a measurement (read-only; do not open any other file of the repository, and do
not look for which system proposed what). Read `clean-arch/step1-unfiled-2026-11-08/council/ed-packet-F.md`. It quotes a standard
(section 3 of an extraction prompt and decision D388), then gives articles, each with the questions open before it and questions
proposed after reading it. Every proposed question asks whether the company will sign an obligation by a check date.

For every proposed question (labels like fresh-22/T1), judge it against the standard and the article only:
- open: the obligation is the company's own, not yet signed, large enough to change the company's revenue, profit, cash or credit risk,
  merits a separate investment judgment, public material will settle it, and no open question already asks it;
- small: by its own scale it does not change the company's revenue, profit, cash or credit risk enough;
- already_signed: the article says it is already undertaken;
- not_an_obligation: it is not an obligation the company takes on in its own name;
- duplicate: an open question already asks whether it is signed (name which);
- wrong_fact: it misstates the article.

**The yardstick is the company's own revenue, profit, cash or credit risk.** Judge scale against those, as the article states them or as
you know the company's size. Do not judge scale against an open total of the same kind or against another deal. Several proposed
questions in one article may be wordings of the same matter: judge each on its merits, not as a fragment of another.

Write one line per question, every label in the packet, in this form:
`<label> | <verdict> | <the article sentence it rests on, short> | <one-sentence reason, naming what you compared the scale with>`
End with the count of labels judged.
