# Filing exposure under literal D265 (old-2, $0; 2026-11-21)

Counted on old-2's stored reading answers (`handovers`, seq >= 148, the item that opened total revenue v14): **105** statements were
linked by the reading step to both v9 (Data Center FY2027) and v14 (total revenue FY2027). With a link "v9 reads v14" read as a
hierarchy (D265 literally, `extraction.narrowest_links`), each would keep v9 only. Among them, seq 185: "NVIDIA reported record FY2027
first-quarter revenue of $81.6 billion, up 85% year over year" and "NVIDIA management guided FY2027 Q2 revenue to approximately $91
billion": total revenue's own figure and guidance (D207: "company-wide figure questions take only their own figures, guidance and
management statements"). A first-order count: a replay under the literal rule would diverge from the archive at the first moved link,
so the exact loss is not replayable at $0. Under D694 (a) (`kind = 'reads'` skipped by `store.direct_parents`) none moves.
