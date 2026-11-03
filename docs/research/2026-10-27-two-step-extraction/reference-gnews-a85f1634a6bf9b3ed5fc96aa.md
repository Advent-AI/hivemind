# Reference statements for the fresh control article (written 2026-10-27 18:50, before any two-call send)

Article: `gnews:a85f1634a6bf9b3ed5fc96aa`, Tom's Hardware, 2026-10-20, "China's tech giants drop $35 billion on
export-compliant Nvidia RTX Pro 5500 workstation GPU orders …", cleaned text 3,471 characters, 11 paragraphs. Used by no
trial before this file. Assistant-authored (Claude), not human gold. Paragraph ids as the reading call numbers them.

An analyst reading this for NVIDIA's China revenue, product mix and export-control theses would keep these statements.
Each must be present (its paragraph read, a statement covering the span, the quantity in `one_line`) in every reading
send for the fresh-article bar in design.md §8.

| # | paragraph | statement | speaker / tier expected |
|---|---|---|---|
| 1 | p0005 | ByteDance, Alibaba and Tencent reportedly ordered more than 3 million RTX Pro 5500 GPUs for over $35 billion | sources to Reuters, retold by Tom's Hardware → rumour |
| 2 | p0005 | Nvidia told customers it cannot fill the orders; they far outstrip planned production | sources to Reuters → rumour |
| 3 | p0005 or p0006 | the RTX Pro 5500 is compliant with U.S. export restrictions on AI-capable GPUs to China | reporter → fact (a published rule) or third_party_view |
| 4 | p0006 | the card has the RTX 5090's CUDA core count with 84GB of GDDR7 | reporter → fact |
| 5 | p0006 | the H200 and B300 remain banned or heavily restricted for China | reporter → fact / third_party_view |
| 6 | p0007 | about $11,400 per card, $35 billion total | two sources → rumour |
| 7 | p0007 | Nvidia may deliver only 5% to 10% of the demand | one source → rumour |
| 8 | p0007 | Nvidia can produce only 3 million RTX Pro 5500 cards globally in 2027 | report → rumour |
| 9 | p0008 | neither Nvidia nor the three companies confirmed any of it on the record | reporter → fact |
| 10 | p0008 | an Nvidia spokesman: demand from China for these chips has seen "unprecedented growth since 2022"; U.S. firms restricted by outdated export controls and China's import limits | Nvidia spokesman to Reuters → party_statement |
| 11 | p0009 | export-restricted Nvidia AI chips continue to reach China despite the restrictions | reporter → third_party_view |

Not statements (should be skipped or absent): p0001–p0002 the headline (repeat), p0003 the byline, p0004 the standfirst
(a claim without a figure; acceptable either way), p0010 the author's bio, p0011 a reader comment (cleaning residue).

Linking expectation (for the linking bar, not a pass/fail): 1, 2, 6, 7, 8 bear on NVIDIA's China/data-center revenue and
RTX Pro demand theses; 3, 5, 10, 11 on the export-control theme; 4 and 9 are context that may link to nothing.
