# Evidence retriever recall@k, oracle over every piece in force (120 sampled truncated decisions of 330; $0.0537)

- decisions where the oracle finds a same-statement piece anywhere: 45
- of which the strongest lies only OUTSIDE the shown top-10 (candidate recall misses, to read): **5**
- inside and outside both ≥ 0.5: 4
- recall@k estimate on decisions with a true repeat (before reading the misses): 40/45

## Candidate misses
- gnews:9a640a26663ca36632da00cd e1→v2 (47 in force, decided new )
    IN: 24/7 Wall St. analyst Joel South reported NVIDIA Q1 FY2027 revenue of $81.62 billion, up 85.2% year over year,
    OUTSIDE e192 p_same 0.86: David Jagielski says NVIDIA has performed strongly in recent quarters; the article highlights 85% revenue grow
    best inside: e32 different 0.47
- gnews:39deea97b690ac7b56dada0b e4→v3 (76 in force, decided new )
    IN: Insider Monkey identified hyperscalers' in-house custom AI chip development as a long-term risk to NVIDIA GPU 
    OUTSIDE e114 p_same 0.52: Micah Zimmerman notes that NVIDIA relies on a small number of large customers, some designing their own chips,
    best inside: e116 different 0.01
- gnews:4bfaa1ed7017b3c1d2638b59 e1→v20 (23 in force, decided new )
    IN: The Open Secure AI Alliance, as reported by Giann Liguid, advised US policymakers that blanket restrictions on
    OUTSIDE e63 p_same 0.66: The letter's signatories said open-weight models promote competition and innovation and called for targeted le
    best inside: e163 different 0.13
- gnews:6f53d290d7aa54066ad3f160 e3→v2 (75 in force, decided new )
    IN: NVIDIA management projected FY2027 Q2 revenue of $91 billion, plus or minus 2%, and said it expected AI demand
    OUTSIDE e290 p_same 0.54: 24/7 Wall St. reported NVIDIA's Q2 revenue guidance of $91.0 billion, excluding China Data Center compute.
    best inside: e29 different 0.01
- gnews:1cf5ba5937521dce264a1445 e2→v3 (48 in force, decided new )
    IN: David Jagielski says NVIDIA has performed strongly in recent quarters; the article highlights 85% revenue grow
    OUTSIDE e32 p_same 0.86: NVIDIA CFO Colette Kress reported Q1 FY2027 revenue of $82 billion, up 85% year over year.
    best inside: e44 different 0.09
