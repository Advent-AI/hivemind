# Gold v3 evidence entries checked against standard version 4 (D248), 2026-10-30

The standard page went to version 4 on 2026-10-30 (D248). Its section 8 says the version-3 gold is a historical record until it is
re-derived: the opening part re-judged entry by entry, and the evidence part checked entry by entry for whether D248 touches it, the result
recorded as a correction (D243 item 11: a separate dated record, never an overwrite).

This record covers the evidence part only. The opening part (must-open, may-open, must-not) is not re-derived here; no question score is
reported against gold v3 until it is (the opening work is the next step, after the noise class).

## Which D248 items can touch an evidence entry

| D248 item | What it changes | Touches the keep or weight of an evidence entry? |
|---|---|---|
| 1 one plan, several wordings | question identity | no |
| 2 one event, several deadlines | question identity, succession | no |
| 3 one product generation, several milestones | which question opens; launch and sampling are its evidence | no (the statements stay evidence) |
| 4 a company's own quantity by fiscal and calendar year | only the fiscal year opens; a calendar-year estimate is evidence to the fiscal question, weighed lower when the two years differ much | **possibly**, for calendar-year estimates of a company's own annual quantity |
| 5 a model-written period start | matching identity | no |
| 6 small matters opened as questions | no question opens; "whether its statement is kept follows the evidence rule (standard §5)" | no |
| 7 one statement carried by several outlets | how the judge sees repeats; every piece is still stored | no |

## Item 4, entry by entry

A code scan of every gold item (dev 348, test 51) for a calendar year or "calendar" beside a quantity word found 38 dev and 7 test entries
(`scan` below). Read one by one, they fall into:

- fiscal-period figures (fiscal quarters, fiscal 2027/2028): not calendar-year estimates; 16 entries.
- one NVIDIA quarter the author labels "the first quarter of calendar 2026" (optional): a quarter, not an annual quantity; unchanged.
- other companies' own figures (Intel, Samsung and SK Hynix, Sharon AI, Huawei twice, Micron, Alphabet, Broadcom, Nebius, SpaceX): item 4
  concerns the company whose question it is; unchanged; 10 entries.
- shared quantities by calendar year (hyperscaler capex, AI infrastructure capex, memory share of data-center spend): the shared-quantity
  class is calendar-year by design (§3 D); unchanged; 7 entries.
- events, programmes, appointments, financing (AI Compute Partnership twice, the profit-sharing programme, an executive's start date,
  SpaceX financing): no annual quantity; unchanged; 5 entries.
- valuation multiples (a P/E of 30.6, a forward P/E below 20): no annual quantity; unchanged; 2 entries.
- a multi-year cumulative forecast (Blackwell and Rubin sales from March 2026 to the end of 2027): not an annual quantity; unchanged; 1.
- calendar-year estimates of NVIDIA's own annual quantity, 3 entries: gnews:92c7e54d38dc2916aa185568 ("82% revenue growth for this year and 41% next
  year", core), gnews:71df54965281684cc500960f ("For the rest of this year ... 82% growth. For 2027 ... 41%", core),
  gnews:3df0bbc8aff2c1d008bc0a32 ("12X its forecasted 2028 earnings", optional). NVIDIA's fiscal year ends in late January, one month from
  the calendar year (FY2027 runs February 2026 to January 2027), so calendar 2026 and FY2027 share eleven months: the two years do not
  "differ much", and the weight stays.

Result: **no evidence entry changes weight or verdict under version 4.** Evidence scores against `golden-v3/golden-v3-signed.json` (sha256
78844bc3…) and `test-set/golden-test-signed.json` are read as version-4 evidence scores with this record named beside them.

## scan

`python3` over both gold files: an entry is listed when its span or meaning holds `calendar`, `日历`, `自然年`, `CY20xx` or `2026`–`2028`
together with a quantity word (revenue, sales, margin, EPS, earnings, capex, spend, 收入, 利润, 毛利, 支出, 营收). The listing was read in full
on 2026-10-30; the categories above account for all 45 entries (16 + 1 + 10 + 7 + 5 + 2 + 1 + 3).
