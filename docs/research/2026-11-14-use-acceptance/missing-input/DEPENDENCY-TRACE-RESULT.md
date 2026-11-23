# Would a dependency between questions have delivered the undelivered facts? A bounded trace (D532, under D439), 2026-11-15, $0

Apart from PRD 10's filing work. Read in the stored records of the trial's old-system run (`poc/data/clean-e2e-full-2026-11-13/p1/prod`)
and the trial's fact list (`../facts-C.json`, the frozen reference's facts in forty articles). Nothing was sent; nothing is built.

## The answer

**This trace found no directionally valid case in which a dependency's conclusion would supply the needed figure.** Of the 22
reference facts the old system filed under another question (three of them with no question on their matter; the trial's 19 are
the subset never delivered although a later judgement was made), one sits in the direction a dependency would serve, and it is
an unsized report (which may still be of value to a reader). Under D368's direction (the supported question reads the
conclusions of the questions that support it) most of the others sit under the broader, supported question and bear on a
narrower one. By the stop rule set for this trace it ends here. Some relations between questions were not recorded, and no
judgement was re-run. The stored run holds no dependency at all (known and decided: D368).

## The 22 facts, by the question that holds them and the question they bear on

| Held under | Bear on | Facts | Relation the comparison step recorded | Under D368's direction |
|---|---|---|---|---|
| total revenue growth, fiscal 2027 or 2028 (`v6`, `v7`) | the cloud companies' capital spending, 2026 or 2027 (`v4`, `v5`) | 9 | none recorded between these questions | **not valid**: the revenue question is the supported one; it would read the spending questions' conclusions, not the reverse |
| total revenue growth, fiscal 2027 (`v6`) | China's authorization of H200 purchases (`v11`) | 2 | "different" (0.91) when `v11` opened | **not valid**, for the same reason |
| the total of credit support (`v1`) | the Ohio lease guarantee, yes or no (`v2`) | 5 | "part of" (0.59) and "same quantity or event" (0.69) when `v2` opened | **not valid**: the part supports the total; the facts sit under the total |
| the Ohio lease guarantee (`v2`) | the total of credit support (`v1`) | 1 | as above | **valid**. The fact: NVIDIA "has also recently been negotiating to provide financial guarantees for OpenAI's lease of a large data center in Ohio" (unsized). It is present in `v2`'s conclusion as a judge would receive it ("reports negotiations ... an unsized report about a lease whose fully built-out cost could reach $500 billion"). It gives the total no figure |
| Rubin shipping (`v3`) | the Kyber rack's launch (`v9`) | 5 | "different" (0.91) when `v9` opened | unavailable: no supporting relation is recorded or evident between the two events |
| total revenue growth, fiscal 2027 (`v6`) | no question on the matter | 3 | none | unavailable |

(The trial's page counts 19 of these as "never delivered, though judged after it arrived"; the class in the fact list is 22.)

## What it shows

- Eleven of the 22 sit under a company-wide revenue question and bear on a narrower question that was open (spending, the China
  authorization); five more sit under a total and bear on its part. This is the picture PRD 10 §2 draws for the old system and
  the first run's record names as known defect 4 of D354 (the company-wide revenue question as the home of indirect evidence,
  with narrower questions losing the evidence that answers them). It is the filing work's subject, not the dependency slice's.
- A dependency in D368's direction carries conclusions from supporting questions to the supported one. Sixteen of these facts
  would have to travel the other way. This trace gives D368's slice no case of a figure it would deliver here; it does not test
  the slice, which stays decided and awaiting its build.

## What it does not show

That the 22 facts would change an answer (the trial's reading found none it could name, with no control); why each fact was filed
where it was (not traced here; D354's record and PRD 10 hold the earlier work on the fallback); anything about the new system.
