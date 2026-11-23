# Toolkit: reference implementations from the Step 1 run

All of these live in `clean-arch/takeover-2026-11-07/`. Copy and adapt them for another step; keep their contracts:
- outputs blinded under shuffled labels, with the key kept outside the repo;
- the frozen scorer's matching functions imported, never reimplemented;
- the gold sha256 printed;
- every failed send recorded with its reason, never retried silently.

| Script | What it does |
|---|---|
| `build_census_packets.py`, `tally_census.py` | The blind census: the current system against the reference on identical inputs |
| `model_account.py` | Continues stored conversations with one question; records the model's own account |
| `probe.py` | The fixed-state probe. Arms are files: `<arm>-system.txt`, `<arm>-closing.txt`, optional `<arm>-schema.json`, and `<arm>@<variant>-settings.json` with model, effort, provider and `json_mode`. It checks the control's bytes, uses one archive per (arm, draw), and has a DeepSeek and JSON-mode path |
| `build_probe_packets.py`, `tally_probe.py` | Blind coverage scoring of probe answers against a census matter list |
| `score_round.py` | Probe answers on golden-v5 (kept evidence only), plus the blind thesis and unfiled packet |
| `score_gold_runs.py` | Forward runs on golden-v5 (joins continuation segments with `+`), with production's draws for reference |
| `build_forward_packets.py`, `tally_forward.py` | Blind whole-run coverage, extras and link scoring across several runs |
| `build_library_packet.py` | The final thesis libraries of several runs, shuffled to letters, for a library verdict |
| `build_field_audit.py` | Blind per-field audit: random items from two systems in one shape |

The Step 1 runner (`clean-arch/step1/runner.py`, `run_live.py`, `live.py`) runs a forward pass. It accepts a candidate system text,
closing check and schema; it supports Luna and DeepSeek in JSON mode; and it records unfiled evidence and the exact sent request.
