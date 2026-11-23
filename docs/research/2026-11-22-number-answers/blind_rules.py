"""The one source of the defect definitions and the writer's format material for judging-v13s blind readers and adjudicators (D744).

Readers and adjudicators get the same text: the writer's system text, every schema description, and these definitions, so that what
the format rules permit is never marked as a defect by one and cleared by the other.
"""
import json
from pathlib import Path

DEFINITIONS = """Definitions (judge each against the passages and the format rules the writer was given, shown below; what the format rules permit is
not a defect):
- supported: the forecast follows from the shown passages and the answer's stated assumptions; a reader could check it against them.
  For a forecast, the assumption that decides the band must rest on the passages in one of three ways: its size, a bound that
  justifies the rung, or, when the passages do not give the asked quantity, a related figure that the answer explains. An explained
  related figure satisfies this requirement even though the other side of the line remains possible. It is explained when the
  answer says why the comparison applies to the companies, the period and the quantity asked, and why, under the answer's own stated
  assumptions, the chosen side of the line is more likely; an answer that does not explain this is not supported (a ruling). For an unresolved
  member, supported means its reason holds: after the strongest relevant passages, a gap remains that keeps the rung unsettled (a
  ruling).
- number misread: a source figure's number, scale, sign or qualifier differs from what its passage's quote writes, allowing what the
  format rules permit.
- wrong arithmetic: a computed figure does not equal its operation on its inputs, within the tolerance the format rules state.
- part above or added into its whole: a segment is larger than the total it belongs to, or is added again into a total that already
  includes it (directly or through an intermediate figure or an estimate).
- two forecasts of one quarter: two different figures are used as the value of one quantity and period. A growth rate computed from
  guidance and used only as a stated benchmark for an estimate is not a second value, when one figure supplies the quarter in the
  calculation (a ruling). Look through any rate or multiple, including inside a stated assumption, for a second dollar value of the
  quarter.
- own estimate passed off as the market's reference: a figure marked as the market's reference is, or rests on, the writer's own
  estimate or forecast. A reference that applies a past period's reported share or multiple to another period (a quarter's mix
  applied to the year) is our comparison estimate, not the market's (a ruling).
- broken structure: a link that does not resolve, a figure that depends on itself, a missing or doubled answer, an outcome that is not
  the question's quantity, or a rung whose band does not hold the outcome. For a range outcome, the format allows "a band it overlaps,
  with the reason in reasons": such a rung is not broken structure; a band the range does not reach is. A total used for a narrower
  quantity (total capital expenditure for data-center spending) without a stated deduction or a supported bound is an outcome not of
  the question's quantity (a ruling)."""


def descriptions(schema, path=''):
    """Every description in the schema, keyed by its field path."""
    found = {}
    if isinstance(schema, dict):
        if isinstance(schema.get('description'), str):
            found[path.strip('/') or 'answer'] = schema['description']
        for key, value in schema.items():
            if key != 'description':
                step = '' if key in ('properties', 'items', 'anyOf') else key
                found.update(descriptions(value, f'{path}/{step}' if step else path))
    elif isinstance(schema, list):
        for value in schema:
            found.update(descriptions(value, path))
    return found


def allowed_qualifiers(schema):
    """The qualifier values the writer's own schema allowed (D747: an older run's schema, not today's list)."""
    options = schema['properties']['figures']['items']['properties']['qualifier']['anyOf']
    found = [o['enum'] for o in options if isinstance(o, dict) and 'enum' in o]
    if len(found) != 1:
        raise SystemExit('the schema does not hold exactly one qualifier list')
    return found[0]


def format_material(case_folder):
    """The writer's system text and every schema description, as shown to readers and adjudicators."""
    case_folder = Path(case_folder)
    schema = json.loads((case_folder / 'schema.json').read_text())
    return '\n'.join(['# The system text the writer was given', (case_folder / 'system.txt').read_text(), '',
                      '# The format rules the writer was given (schema descriptions)',
                      json.dumps(descriptions(schema), indent=1, ensure_ascii=False), '',
                      'The qualifier values the format allows (a qualifier not in this list cannot be recorded): '
                      + ', '.join(allowed_qualifiers(schema)) + '.'])
