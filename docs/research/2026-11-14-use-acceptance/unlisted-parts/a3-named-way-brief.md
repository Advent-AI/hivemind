# Ruling on parts of entries that name a way an event could be ruled out

Each point is one part of an entry listed as **not judged** beside an event question. Another reader found that the entry names a
particular way the event could be ruled out (or the point is another part of such an entry). For each point you get:
- `part`: the part to rule on;
- `entry`: the whole listed entry;
- `topic`;
- `choices_as_shown`: the choices as the judge sees them, word for word.

Rule each point with one of the four values in `h-brief.md` (`part`, `already_judged`, `settlement`, `cannot_tell`). Apply its test
exactly: "a rung decides a part only when holding that rung says whether the part happened". Read each choice in full, including any
text it adds about what else makes it hold. Give your reason in `why`.

Answer with one JSON line per point, in packet order:

`{"id": "<the point's id>", "ruling": "<value>", "why": "<one sentence>"}`
