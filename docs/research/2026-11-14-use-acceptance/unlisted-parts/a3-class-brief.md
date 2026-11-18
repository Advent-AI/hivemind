# Classing the entries of an event question's not-judged list

Each entry in the packet is one item from an answer's list of parts it does **not** judge. The answer judges one event, and the
judge sees three choices: Yes, Ruled out and Still open. For each entry you get:
- `topic`: the topic's description and outcome;
- `choices_as_shown`: the choices as the judge sees them, word for word, including any text a choice adds about what else makes it
  hold;
- `entry` and its `why`: the listed text and its reason;
- `matters`: the matters this topic can raise.

Split the entry into its parts, one for each distinct thing it names. Most entries have one part. "Whether the merger is renegotiated,
delayed or cancelled" has three.

Give each part one `kind`:

| Kind | When |
|---|---|
| `restates happening` | it says only that the event itself happens, the Yes choice, in other words |
| `restates ruled out unnamed` | it says only that the event is ruled out, decided against or abandoned, and does not name by whom or how |
| `restates still awaited` | it says only that the event has not happened on the due day, for example a delay past it or still pending, and names no decision to defer |
| `named way` | it names a particular way the event could be ruled out: who decides, or which decision. Examples: a termination by the parties, a regulator's rejection, an abandonment without a finding. A formal decision to defer is a named way |
| `other` | anything else: a figure, a condition, a separate matter, a second event, a source of information, or a finer case inside a choice such as an approval with a cap |
| `cannot tell` | the text does not let you choose between the kinds above |

Give each part the one `matter` from the entry's `matters` that it names, or `other`.

Answer with one JSON line per entry, in packet order:

`{"id": "<the entry's id>", "parts": [{"text": "<the part, in the entry's own words>", "kind": "<kind>", "matter": "<matter>"}]}`
