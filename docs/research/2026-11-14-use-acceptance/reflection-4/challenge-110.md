# Round 111: the live-service operating contract, version 1 (`live-service/OPERATING-CONTRACT.md`). Review it against D575's rows and its falsifier

- **The shortfall record** is corrected as you said: "an unchanged re-send cannot exercise the line"; the two-step course could be
  reviewed under D439; a diagnostic on another population need not replace the ruler. D592 is recorded.
- **What I searched for the reader table:**
  - `scripts/hivemind_api.py`: `Connections`, one read-only connection per request.
  - `scripts/hivemind_mcp.py`: one connection at start, and its object list computed once.
  - `scripts/mock_build.py` → `bundle.library`, the Idea scripts, the research scripts, and `snapshot.sh` (the backup API).
  - The writer `ladder_adapter.py` commits several times within a day.
- **The contract's seven rows:**
  1. WAL mode, side files on local disk, no bind mount or network share, `mode=ro`, never `immutable`, backup-API copies only.
  2. One explicit read transaction per request or tool call. Python's default otherwise runs each `SELECT` alone.
  3. Passive checkpoints; no transaction held between MCP calls; the object list per call.
  4. The first day refused everywhere, including the streamed Idea route.
  5. An explicit future `as_of` refused, naming the last completed day.
  6. Crash recovery.
  7. AGENTS §9 kept for everything but the product's own service readers. Any text change is decided at acceptance.
- **A state × event table** and an 8-test proof plan, one test per required case.

**Asked of you:** a case from D575's list, or one you find, that this contract cannot serve consistently without blocking the writer
or exposing partial work. Also any reader or copy path missing from the table, and any row that overreaches what the code and
SQLite's documented behaviour support.

End with `CONSENSUS: yes` (the contract is ready for its $0 proof build, which comes back to you) or `CONSENSUS: no, because …`.
