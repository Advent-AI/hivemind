"""Record-field class (open defect 1, D247): the evidence fields' definitions travel in the schema beside their fields: the three
attribution fields carry the adopted notes, and the links field carries the filing rule (D256, D274); the source tier carries none."""
from hivemind import extraction, placement


def test_the_schema_carries_the_attribution_notes_and_the_filing_rule_beside_their_fields():
    fields = extraction.schema_for('v74i')['properties']['evidence']['items']['properties']
    notes = {name: field['description'] for name, field in fields.items() if 'description' in field}
    assert notes == dict(extraction.FIELD_NOTES, links=placement.FILING_RULE_ROOT_FALLBACK)
    assert fields['original_day']['type'] == 'string' and 'description' not in fields['tier']
