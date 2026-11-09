Alex chose "加在最后复查里再试一次" (D393). Council A for arm c13 before its send. Read-only, under 300 words.

**Read:**
- `clean-arch/q12-capex-2026-11-09/probe-c13-frozen.md` (with its sha256 file);
- the diff between `clean-arch/step1-unfiled-2026-11-08/arms/c8-closing.txt` and `c13-closing.txt`, and between `c8-system.txt` and
  `c13-system.txt`;
- `q12_probe.py`, which now takes `--arm` and `--no-control`. The dry run passes the byte checks on all 14 cases.

**Check:**
1. **Is the new closing-check step general, and does it require "can change the thesis's answer"?** Or could it link every derivable
   figure, or revive Alex's ruled-out cash figures? In his library no open thesis asks about a figure that follows from them.
2. **Is reusing the c12 probe's same-day c8 arm as the control sound?** The requests are byte-identical and were sent today.
3. **Are the lines decidable?** Line 3 now reads kept items against the gold sentence by hand, because the matcher misses rewordings.
   Is that acceptable, or does it need a blind reader?
4. Anything else before the send (about $0.44 estimated)?

End with SEND or BLOCKER.
