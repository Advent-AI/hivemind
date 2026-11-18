# Council mt: the reflection after the full run (read-only, cold)

You are reading the record cold, as an independent council member, after a same-day end-to-end measurement of two systems. Read:
- `docs/prd/10-filing-phase.md` (the current phase PRD: §0 checklist, §1 goal, §2 blocker, §3 out of scope, §4 constraints);
- `clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md`, `STAGE-A-FULL-RESULT.md`, `SLICE-RESULT.md`;
- `docs/DECISIONS-log.md`: D395, D427, D441, D447, D451–D455 (search "## D4");
- `clean-arch/e2e-comparison-2026-11-13/TRACE.md` (the earlier census's opening-loss trace) and `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§81–85;
- `AGENTS.md` ("Authority and scope", D439; §6 prompt principles; §7.3 iterating).
Only then read Claude's reflection: `clean-arch/step1-unfiled-2026-11-08/council/mt-claude.md`.

Answer, each with the file evidence:
1. The lessons at mechanism level from the full run (what it showed that the earlier measurements did not).
2. The conclusions that are weaker than they look.
3. The remaining problems by their effect on the PRD's goal (the final judgement), largest first.
4. The single next angle, with its falsifier, and how it fits the PRD's scope: is "opening" (out of phase 10's scope, §3) the next phase to
   open by council decision under D439, or does the evidence point elsewhere (for example production's unlinked facts, phase 10's own
   blocker, or the clean path's acceptance under D427)? Name what must be written before any send.
5. Anything in Claude's reflection you disagree with.

Out of scope: changing the frozen ruler or gold; any push, deploy or commit; spending decisions beyond naming what a test would cost.

End with: "Council position: <...>".
