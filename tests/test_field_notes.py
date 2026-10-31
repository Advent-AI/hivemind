"""Record-field class (open defect 1): from role-v53 the evidence fields' definitions travel in the schema beside their fields;
v54 rewrites the attribution notes and v55 alone adds the source tier's; each version's schema, hence every stored request, stays as it
was sent."""
from hivemind import extraction


def evidence_fields(version):
    return extraction.schema_for(version)['properties']['evidence']['items']['properties']


def notes(version):
    return {name: field['description'] for name, field in evidence_fields(version).items() if 'description' in field}


def test_v53_carries_the_attribution_notes_it_was_sent_with():
    assert notes('v53') == extraction.FIELD_NOTES
    assert evidence_fields('v53')['original_day']['type'] == 'string'


def test_v54_carries_the_rewritten_attribution_notes_and_no_tier_note():
    assert notes('v54') == extraction.FIELD_NOTES_V54


def test_only_v55_carries_the_tier_note():
    assert notes('v55') == {**extraction.FIELD_NOTES_V54, 'tier': extraction.TIER_NOTE}
    assert evidence_fields('v55')['tier']['enum'] == evidence_fields('v51')['tier']['enum']
    assert notes('v56') == extraction.FIELD_NOTES_V54


def test_from_v57_the_schema_carries_v53s_adopted_notes_not_v54s():
    """D247 adopted v53's notes; the noise arm (role-v57, role-v58) changes only the keep rule, so its schema carries v53's notes."""
    assert notes('v57') == extraction.FIELD_NOTES
    assert notes('v58') == extraction.FIELD_NOTES


def test_before_v53_the_schema_carries_no_field_definitions():
    for version in ('v51', 'v52'):
        assert notes(version) == {}
