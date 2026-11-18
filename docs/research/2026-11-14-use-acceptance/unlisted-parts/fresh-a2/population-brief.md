# Classing fresh topics against the matters used in development

The packet holds `fresh_topics`, each with its description, outcome and opening article. It also holds `development_matters`, 110
topics that were read while a change to the system was being developed.

For each fresh topic, decide whether it is about the same underlying matter as any development matter:
- the same deal, decision, proceeding, product or programme;
- or the same quantity of the same company or theme.

This holds whatever the wording or the period. Two years of the same spending figure are the same matter.

| Class | When |
|---|---|
| `development matter` | it tracks the same underlying matter as at least one development matter; name the nearest one |
| `different matter` | no development matter tracks the same underlying matter |
| `uncertain` | the texts do not let you decide |

Answer with one JSON line per fresh topic, in packet order:

`{"id": "<fresh topic id>", "class": "<class>", "nearest": "<development matter id, or null>", "why": "<one sentence>"}`
