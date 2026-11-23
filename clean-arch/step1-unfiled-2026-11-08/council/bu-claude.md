# Arm c11: a required company-impact field (Claude, before the council; 2026-11-09)

**Alex's word.** "继续，逼它跟公司比 (Recommended)" (LOG §51). When the model opens a signing question, it must write what the
obligation could change in the company's revenue, cash or credit risk, or say the amount is unknown.

**Mechanism it answers** (LOG §51, `thesis-account.json`). Under c10a the model sized $2–3bn stakes against clean-7's $25bn total and
the $12.9bn Hugging Face deal, never against the company (4 of 4 answers). The signed standard's test is the company's own revenue,
profit, cash or credit risk (D248 boundary 6, carried in c8 §3).

**The change** (one lever on c10a; system text unchanged):
- **Schema:** a required `company_impact` on each new thesis, placed after `opens_as`, string or null: "For a binding_obligation
  thesis: what the obligation could change in the company's own revenue, profit, cash or credit risk, judged against the company's
  size (from the item, the open theses or the company's known scale), not only against a total of its kind or another deal; when the
  item states no amount for the obligation itself, say so and judge from what it does state (the cost of a project or asset is not
  the obligation's amount). For any other opens_as, null."
- **The read-back,** the closing's last paragraph:
  - "when its scale meets section 3" becomes "write the company_impact of its signing question first; when that shows it can change
    the company's own revenue, profit, cash or credit risk (section 3)";
  - the last sentence becomes "When its company_impact shows it cannot change those, or it is not a separate bet, drop that question
    and link the statement to the theses it informs".

**Sources:**
- c8 §3 binding_obligation, "large enough to change its revenue, profit, cash or credit risk";
- D248 boundary 6;
- D388, "material … merits a separate investment judgment";
- the council's limits (`bt-codex.md`): comparisons with a total or another deal stay as context, not banned ("not only against");
  the asset cost is not the exposure; null for non-obligation theses, so no figure is forced on a product, policy or shared-quantity
  question.

**Decision it takes from the model:** none. The model still judges importance; code checks only the shape (the field is present, a
string or null). Whether it is non-null exactly for obligation theses is counted after the probe, not enforced.

**$0 checks:**
- a synthetic Ohio answer passes every check;
- null for a shared-quantity thesis passes;
- an answer without the field is refused;
- stored answers cannot be replayed, since they lack the required field.

Size: +1,871 characters against c8 (+405 tokens on Ohio, +4.8%; an estimate from c8's measured ratio).

**Probe:** the same 32 cases (`cases-c9.json`) plus Ohio ×3, c11 only; the c8 control from `probe-r13-c9` and c10a from
`probe-r14-c10` as references. One draw per case. About 35 sends, about $0.55.

**Falsifiers** (any one stops the line):
- Ohio's signing question in fewer than 2 of 3 draws, or an Ohio `company_impact` that presents the $500bn asset cost as the
  guarantee amount;
- fresh-47 or fresh-50 opens a thesis;
- any thesis new against c8 that a blind reader judges wrong. The reader sees c11's theses only, one packet per arm, so a same-matter
  wording from another arm cannot read as a fragment;
- fresh-9 opens a signing question for the guarantee the article says was agreed;
- fresh-8 loses its thesis, or dev-1's aggregate is recast;
- links per item move more than 10% against c8;
- an empty answer on an article c8 keeps items from;
- a thesis c8 opens on these cases lost because no comparison figure exists (read each lost thesis's article).

**Weaker than it looks:** one draw per case; the 32 cases hold only two small stakes; no material unsigned obligation outside the
cloud programme exists in the stored NVDA set.
