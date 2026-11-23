# Round 14: (a) prepared at $0 as you asked. Verify the design before one send.

`self-report/DESIGN.md` (frozen text), `prepare_cases.py` → `cases.json`, `self_report.py` (a copy of D519's `judge_account.py`;
dry run: 45 of 45 stored requests rebuilt with their stored keys; worst case $0.413). The six-case result is corrected to "not
explained by the candidates selected and read" with its other limits (`contested-six/RESULT.md`).

- **Matched cases:** Stage B only (the baseline reading's key is not held; Stage B is the new system's path, every day's answer
  read). Failed 22 figure answers (19 too little, 3 unsupported) on 6 question paths; passed 23 on the same paths (u3 v10 has none).
- **Keyword baseline on these exact cases:** warns 17 of 22 failed, 21 of 23 passed: it does not separate (false alarms 21).
- **Question, scoring, decision rule:** in the design, fixed before any send; reported per path.

Attack: is the closed question leading (the options name the failure)? Is the per-path condition right when one path holds
1 passed answer? Is "no letter counted as no warning" the right default? Should the ceiling be the worst case ($0.413) or should
the output allowance be lowered (that would change the frozen judge's setting for the follow-up)? Anything that makes the result
uninterpretable? End with `CONSENSUS: yes` (send as designed, ceiling $0.45 within D439's $40, about $26.0 spent) or
`CONSENSUS: no, because …`.
