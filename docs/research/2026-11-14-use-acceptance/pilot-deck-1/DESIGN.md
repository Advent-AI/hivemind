# Deck 1: a pilot of Alex's own product-level review (D560), 2026-11-15, $0

**Status: built from stored material; waits for Alex's half hour. It ranks nothing, passes nothing, replaces nothing.**
Council: `../reflection-4/council-codex-2.md` (the minimum design), `council-codex-3.md` (four adjustments, consensus).

## What it is for

Every judgement of quality since 2026-11-10 was made by two families of model readers who do not agree with each other, on
packets Alex never saw. This pilot tries one thing: can Alex himself mark a short deck of the product's actual output, with
known controls mixed in, in about half an hour, and does that give a reading the model readers can then be checked against?

## Material

The stored comparison of the fresh week, 2026-09-22 to 09-28 (235 articles, 232 not sent before; one run of each system from
an empty library): `poc/data/clean-lean-week-2026-11-14/` (old system `week/p1/prod`, new system `week-r2/c1/judge/draw-c1`); the
reading packets and marks in `../week/`; the census of kept facts that reached no answer in `../delivery-class/`. No model is
called. The two model families' marks on the same questions and answers were made on 2026-11-14 and are frozen; they are not
shown on the cards and stay in the sealed key with their scope (question worth: the whole library seen at once; answer
support: the complete request).

## The selection rule (written before the draw; seed 20261115; the draw itself is in the sealed key, outside the repository)

Sixteen distinct cards and three hidden repeats.

1. **New system, six real answers.** Its planted wrong answer is built on question v1, so v1's real answer is left out (a real
   card must not reveal a plant). That leaves exactly six: v2, v3 and v7 (the three questions of D508's confirmed pairs, which
   carry the completeness sheets) and v4, v5, v6.
2. **Old system, six real answers of fifteen.** First the planted wrong answer is drawn (rule 4) and its question left out.
   Then one independently confirmed supported control is drawn at random from those the separate reader confirmed
   (`../week/controls-B.json`, `control-confirmation.jsonl`); then five more at random from the remaining questions.
3. **Two matters with no question:** M01 (fiscal 2027 revenue: both families mark it missed by one system) and M04 (supply
   commitments: missed by the other), from `../week/matters-A2.json`. The card shows the matter and its source articles; answer
   support is not applicable.
4. **Two wrong answers, one per system:** the new system's planted answer (item 1 of the week's reading B: the rung moved),
   and one of the old system's two planted answers whose cited statements are all stored (items 22 and 24; the third plant
   cites an added statement), drawn at random. Each keeps the request and the answer choices of its original control. Both
   model families marked all four plants unsupported on 2026-11-14.
5. **Three hidden repeats:** drawn at random from the real answers among the first ten cards in the order that carry no
   completeness sheet (so a repeat is the same card as its original). *Changed before any card was seen: the first build
   failed on a repeat of a sheet card.*
6. **Order:** the sixteen shuffled; the last six positions and the three repeats shuffled together.
7. **Completeness sheets on three cards** (new system v2, v3, v7): the confirmed kept-but-undelivered fact of that question
   (D508; for v2 one fact reported by three articles) and one negative control drawn at random from the kept statements both
   first census readers, reading every statement against all seven questions, left empty for this question while naming it
   for another (a substantive fact), not linked to it and not among its candidates. *Changed before any card was seen: no
   candidate of v3 or v7 was marked not bearing by both fresh readers, so the control comes from the first readers' pass.*
   On every other card completeness is not assessed.

## A card

The question; whose it is and its due day; its answer choices with the present answer marked; the answer's stated reasons;
the statements it cites, each with its passage and a link to the stored article; and, one click away, the complete request
the answer step was shown. No system name. Blinding is imperfect in two known ways: the two systems' requests are worded a
little differently, and the two wrong answers were built on earlier days' requests (2026-09-22) while most real answers are of
the week's last day; each card shows the true day of the answer it carries.

## Alex's marks

Per card: **worth tracking** (yes / no / cannot tell); **answer supported by what is shown** (yes / no / cannot tell); a few
words. Per fact on a completeness sheet: **bears on this question** (yes / no / cannot tell), then **it would change**: the
answer / only the confidence / neither / cannot tell. Opening the complete request or an article is allowed and recorded by
the page, with the time spent.

## What is reported afterwards

Every mark. His marks on the three repeats beside their originals. His marks beside each model family's stored marks on the
same cards. Whether the two wrong answers were rejected and the confirmed supported controls accepted. His answers on the
completeness sheets beside the census readers'. The time, and where it went. The classes of what he rejects, in his words.

**Signals for redesign, not a pass line:** two repeats marked differently; both wrong answers accepted; the deck not markable
in about half an hour. Three repeats and two wrong answers are too few for an error rate; perfect marks would not prove the
method reliable.

**It cannot show:** a usable share for any system; which system is better; what the cards' selection left out; a rate for
other news; which step caused a bad card. $0 covers model calls only: Alex's time and the preparation are not priced.

## To open it

`deck-1.html` in this folder, in a browser. Marks are kept in the browser as he goes; the last box on the page holds them as
text to paste back.
