You are a blind second reader for a prompt audit, read-only. Do not run model calls, start runs, or write files. Do not read any
file named PROMPT-AUDIT*, DIAGNOSIS*, or any council file other than this hand-off. Cite files and lines.

The request: Step 1 of a research pipeline reads one news item for a company and returns evidence and, when warranted, new
theses. Its candidate version c15 is three files: `clean-arch/step1-unfiled-2026-11-08/arms/c15-system.txt` (system text),
`c15-closing.txt` (the closing check appended after the item), `c15-schema.json` (the answer schema; production states it at the
end of the system text). The previous version is `c8-*` in the same folder; c15 changes four sentences and one schema field description (diff all three files).

The standard it must carry: `docs/prd/05-extraction-standard.html` (frozen, version 5; mostly Chinese), in particular §3 (the
reasons a thesis opens, the table rows A–E, the periods "今年和明年") and §4 (the opening standard and when two questions are one).

Task (the prompt-audit procedure, both directions): read the whole c14 request (system, closing, schema descriptions) against the
standard clause by clause, giving priority to every clause on periods, years, the same question, merging and opening. For each
relevant clause say: consistent / contradicts / keeps wider / keeps narrower / has no source. Then answer: do the two changed
sentences carry the standard or add a rule? Does either changed sentence create a conflict with another clause of the request or
of the standard (including events under another deadline, a company's own fiscal and calendar years, another population or
wording of an aggregate, a year after next)? Is anything in the whole request on these topics wrong that the change does not touch?

End with one line: the changed request is fit to send for a small test (yes / yes with changes / no).
