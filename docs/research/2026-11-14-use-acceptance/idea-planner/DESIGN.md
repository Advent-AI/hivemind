# An event as an Idea driver: design for the council (D580), 2026-11-16, version 1, nothing built

**The defect** (`RESULT.md`): the Idea planner (`idea-summary-v8`, endpoints only) shows a three-choice event as "Yes" and "Still
open". Ruled out, the opposite of Yes, is left out, and the binder can record Still open as the end that raises the Idea's outcome.

**Where it matters:** only on a new-system store; the running product's events have two choices, Yes and No. So it is integration
work for when the new system is adopted. It changes no quality gate.

## The two options

| | Option 1: context only | Option 2: an honest driver |
|---|---|---|
| What the planner is shown for a three-choice event | its three outcomes, as context | its three outcomes |
| What it may do with it | keep it as context with a reason; it cannot be a scored driver | adopt it as a driver, naming **Yes or Ruled out** as the outcome that raises the Idea's outcome; Still open cannot be named |
| What the plan records | the event among `excluded`, weight 0, with its reason | `supporting_position`, the position of the outcome that supports the claim, instead of `supporting_end` |
| The page's composite | unchanged: it never sees the event as a driver | unchanged: it refuses any event driver before reading the end (D570), with its note |
| What a reader of the card loses or gains | the event no longer appears among the drivers and their impact percentages | the event stays a driver, with an outcome that is true to its choices |
| Change to the planner contract | the schema offers no position for a three-choice event; the binder refuses one | the schema's positions for a three-choice event are Yes's and Ruled out's; the binder records the position; docs and API field added |

**My lean: option 2.** An event is often the matter an analyst's Idea turns on (an approval, a launch). Keeping it as a driver with a
true outcome serves the reader. Option 1 is simpler but hides the event's role.

## Every shape × the claim's direction (option 2)

| Shape | Planner shown | Raising outcome the model may name | Claim higher | Claim lower | Page composite |
|---|---|---|---|---|---|
| event, three outcomes (new system) | Yes, Ruled out, Still open | Yes or Ruled out | `supporting_position` = the named one | the other decided outcome (Yes ↔ Ruled out) | refused (D570) |
| event, two outcomes (Yes/No, both systems) | Yes, No (the two ends, as today) | either | `supporting_end` as today | flipped as today | as today: scored in the running product; refused for a new-system event (D570) |
| figure with a favourable end (both systems) | the two end ranges, as today | either end | as today | as today | as today |
| range with no favourable end (new system) | the two end ranges, as today | either end | as today | as today | refused (D570); its scale is Alex's question (page, choice 5) |
| unrecorded shape (new system, no ladder row) | the two ends, as today | either | as today | as today | refused (D570); this design does not change it |

`claim_direction: unclear` keeps its rule: no scored drivers.

## Consumers to review, and their checks

- **`idea_composite.py`.**
  - `add_ladders` keeps all choices for a three-choice event even when endpoints only.
  - The schemas give that event the positions of Yes and Ruled out.
  - `bind_adoption` and `bind_endpoints` record `supporting_position` for it, and refuse Still open.
- **`idea.py`:** nothing beyond the binder's output.
- **The page** (`composite.js`): refuses an event driver before reading `supporting_end`. A test is needed to show that a plan with
  `supporting_position` and no `supporting_end` gives the note, not a TypeError.
- **`docs/poc/idea-card.md`:** the `reading.composite` row names the new field.
- **API clients:** see the new field on an event driver. No MCP tool plans Ideas.
- **Tests:** a three-choice event through the planner's schema and binder; Still open refused; both claim directions; a two-choice
  event and a figure unchanged; the page's note for an event driver.
- **Mutants:**
  - a binder that maps Ruled out to `last`;
  - a schema that offers Still open.

## Prior decisions

- **D570/D571:** neutral treatment of undirected questions and the page's refusal stay.
- **D397:** an event's outcomes as written.
- **The planner** is not one of the frozen pieces (AGENTS, "The production configuration is frozen" names extraction, opening,
  matching and judging), but it is the product's Idea step, so this change is decided here under D439 and reversible.
