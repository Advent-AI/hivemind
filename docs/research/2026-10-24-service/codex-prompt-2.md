# Second read-only review: the fixes after the first review

Read-only: modify nothing, run nothing that writes, call no model API.

The first review is `docs/research/2026-10-24-service/codex-review.md`; what was done about each finding is
`disposition.md` in the same folder. The design is `docs/poc/service.md` (rewritten). Files under review are the same:
`src/hivemind/service.py`, `src/hivemind/search.py`, `scripts/hivemind_api.py`, `scripts/hivemind_mcp.py`,
`scripts/search_eval.py`, `tests/test_service.py`, `tests/test_search.py`. The sealed ledger is
`poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite` (read-only); the index `poc/data/search-index.sqlite`.

Deliver, ranked by what it breaks for a caller, each with a concrete input and the wrong output:
1. For each of the eight findings: is it fixed, and does the test named in `disposition.md` fail on the old
   behaviour (read the test; say which assertion is the decisive one)?
2. The new band parser (`service.band`, `ladder_bands`, `verdict_for`): read every money ladder of the sealed ledger
   against its conditions once more; any band still wrong, any ladder accepted as a partition that is not one, any
   refused that should not be; any verdict wrong for a threshold on a shared boundary.
3. `fresh_vectors` and `search`: any way a stale or missing vector still ranks as semantic; cost of the freshness
   check per query; whether `ensure_index` at start can leave the fronts in a state the answers do not report.
4. Anything the fixes introduced.
Out of scope: everything else in the repository. A style remark is not a finding.
