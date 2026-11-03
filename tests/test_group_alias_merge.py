"""D166, the alias half (2026-11-01): a declaration whose names hit a stored group is that group, and the names it carries that the
group lacks join the group, so every later reader of the group (the placer's takes line, membership by alias, search) sees the
matter under all the names the press has used. Found in arm 3 of the e2e loop: 23 of 35 declarations that folded into a stored
group carried names it lacked (the Kyber rack group never learnt NVL72x2 or Oberon), and the placer dropped the statements that
used those names in every draw. Real storage on a temporary path."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import placement  # noqa: E402
from hivemind.views import groups, store  # noqa: E402


def test_a_declaration_that_is_a_stored_group_gives_it_its_other_names(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.add_group(conn, group_id='g3', name='Kyber rack rollout', scope='Launch timing of the Kyber rack-scale architecture.', seq=5,
                    input_id='gnews:a', aliases=['Kyber rack rollout', 'Kyber', 'NVL576'])
    declared = [{'id': 'n1', 'name': 'Rubin Ultra rack-scale rollout', 'scope': 'The same rollout under another name.',
                 'aliases': ['Rubin Ultra', 'Kyber', 'NVL72x2', 'Oberon', 'kyber']}]
    creations, memberships, notes, extensions = groups.plan(declared, groups.stored_groups(conn), [], {}, lambda c: True)
    assert creations == [] and memberships == []
    assert extensions == [('g3', ['Rubin Ultra rack-scale rollout', 'Rubin Ultra', 'NVL72x2', 'Oberon'])]       # not Kyber, not kyber: known
    assert any('its other names join it' in n for n in notes)

    added = store.add_group_aliases(conn, 'g3', extensions[0][1], seq=9, input_id='gnews:b')
    assert added == ['Rubin Ultra rack-scale rollout', 'Rubin Ultra', 'NVL72x2', 'Oberon']
    assert store.group(conn, 'g3')['aliases'] == ['Kyber rack rollout', 'Kyber', 'NVL576', 'Rubin Ultra rack-scale rollout', 'Rubin Ultra', 'NVL72x2', 'Oberon']
    assert groups.stored_groups(conn)[0]['aliases'][-1] == 'Oberon'
    assert store.add_group_aliases(conn, 'g3', ['oberon', 'NVL72x2'], seq=10, input_id='gnews:c') == []        # appended once each

    # the placer's takes line, the reader the names were missing from, now carries every name
    view = {'key': {'measure': 'event', 'event_type': 'launch'}, 'looks_at': 'Kyber', 'groups': [store.group(conn, 'g3')]}
    assert 'NVL72x2, Oberon' in placement.takes(view)

    # a second declaration folds by one of the added names
    later = [{'id': 'n1', 'name': 'Oberon rack plan', 'scope': 'The scrapped alternative design.', 'aliases': ['Oberon', 'back-to-back racks']}]
    _, _, _, extensions2 = groups.plan(later, groups.stored_groups(conn), [], {}, lambda c: True)
    assert extensions2 == [('g3', ['Oberon rack plan', 'back-to-back racks'])]
