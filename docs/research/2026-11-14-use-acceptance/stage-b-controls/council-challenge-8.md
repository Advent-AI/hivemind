# Council round 8: design version 8 and its texts

Version 8 is in `review-v8/` in this folder, read-only: the design, the items brief and `templates/`. It answers your round-7 review and the
Claude family's, condensed in `council-claude-7.md`. Its change list is §15. Two probes were run since round 7:
- a knowledge probe (post-window facts and training cutoff, §4);
- Claude's system events, which include `thinking_tokens`, now allowed.

Check your round-7 findings first:
1. blind retries, with shape-only reasons;
2. the direct byte check of rendered questions against the stripped file;
3. one control or point per shown-check session, with an object parser;
4. interrupted sessions, with the process id recorded and a live process stopped.

Then check what version 8 adds:
- the D263 disclosure;
- the knowledge probe;
- the rewritten reason lists and summary.

Report only findings that would change what is built or measured. Out of scope: the ladder step's prompt, gate 1 and cost. The frozen ruler's
files must not change. End with `READY` or `NOT READY: <the smallest change>`.
