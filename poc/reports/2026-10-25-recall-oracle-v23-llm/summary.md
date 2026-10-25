# Evidence retriever recall@k, oracle over every piece in force (120 sampled truncated decisions of 213; $0.0616)

- decisions where the oracle finds a same-statement piece anywhere: 49
- of which the strongest lies only OUTSIDE the shown top-10 (candidate recall misses, to read): **3**
- inside and outside both ≥ 0.5: 7
- recall@k estimate on decisions with a true repeat (before reading the misses): 46/49

## Candidate misses
- gnews:6825341a116bd4528557ba9d e1→v2 (54 in force, decided repeat e123)
    IN: 24/7 Wall St. reports, citing The Wall Street Journal, that NVIDIA is reportedly discussing up to $600 billion
    OUTSIDE e110 p_same 0.74: Al Jazeera reported on 2026-07-27 that the reported $250bn guarantee covers the centre lease, while Nvidia sai
    best inside: e123 different 0.13
- gnews:cf24fe6341ca980677ca786e e1→v1 (16 in force, decided new )
    IN: Bloomberg Intelligence analysts Anurag Rana and Josh Christensen said Alphabet’s capex had increased the previ
    OUTSIDE e116 p_same 0.74: Yahoo Finance reported that Alphabet raised its capital-spending outlook last week to support AI infrastructur
    best inside: e128 different 0.2
- gnews:1cf5ba5937521dce264a1445 e2→v8 (19 in force, decided new )
    IN: David Jagielski said NVIDIA’s growth rate accelerated to 85% in the most recent quarter; the article did not s
    OUTSIDE e30 p_same 0.91: NVIDIA reported Q1 FY2027 revenue of $81.6 billion, up 85% year over year.
    best inside: e153 different 0.01
