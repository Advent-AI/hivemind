"""D144 requirements, exercised on real article text and real SQLite storage."""
import copy
import json

import pytest

import ingestion_threads as threads
import ingestion_groups as base
import study
from test_ingestion_groups import fixture
from hivemind import universe
from hivemind.views import matching, store, writing


def thread(ident="t1", name="Vera Rubin rollout"):
    return {"id": ident, "name": name, "scope": "Product readiness, shipments and customer deployments of Vera Rubin."}


def fixtures():
    item, raw = fixture()
    raw["threads"] = [thread()]
    raw["candidates"][0]["thread_ids"] = ["t1"]
    corpus, sealed = study.read_only(base.CORPUS), study.read_only(base.SEALED)
    items = [item]
    for ident in base.ITEM_IDS[1:]:
        value = dict(corpus.execute("select * from items where input_id=?", (ident,)).fetchone())
        value["object_identifiers"] = json.loads(value["object_identifiers"])
        items.append(value)
    second = copy.deepcopy(raw)
    candidate = second["candidates"][0]
    candidate.update(looks_at="SK AI factory deployment", question="Will the first SK AI factory using Vera Rubin come online in 2027?",
                     due_day="2027-12-31", year="2027", rungs=[{"label":"yes", "condition":"Online by 2027-12-31."},
                     {"label":"no", "condition":"Not online by 2027-12-31."}])
    second["threads"] = [thread(name="Vera Rubin customer adoption")]
    second["evidence"][0].update(quote=sealed.execute("select quote from evidence where evidence_id='e55'").fetchone()[0],
        one_line="SK plans its first Vera Rubin AI factory online in 2027.", original_who="SK Group", speaker="SK Group",
        original_day="2026-07-24", event_time="2027")
    risk = copy.deepcopy(raw["evidence"][0])
    risk.update(quote=sealed.execute("select quote from evidence where evidence_id='e724'").fetchone()[0],
        one_line="Vera Rubin shipments may face supply delays.", original_who="Network World", speaker="Network World",
        original_day="2026-04-06", tier="third_party_view", links=["v1"])
    third = {"candidates":[], "threads":[], "evidence":[risk]}
    corpus.close(); sealed.close()
    return items, [raw, second, third]


class Answers:
    """Hand-authored external model responses prove plumbing, not model quality."""
    def __init__(self, raw):
        self.raw = raw
        self.cfg = study.config.load(str(study.ROOT / "poc/config/poc-v7.json"))
        self.names = []

    def stage(self, name, prompt, payload, schema, setting):
        self.names.append(name)
        index = int(name[4]) - 1
        if name.endswith("extract"):
            return copy.deepcopy(self.raw[index])
        if index == 1:
            assert payload["thread_candidates"]["t1"][0]["thread_id"] == "g1"
        if index == 2:
            return {"candidates":[], "thread_matches":[], "evidence":[{"id":"e1", "view_id":"v1",
                "outcome":"new", "target_evidence_id":"", "said_day":"", "reason":"New supply risk."}]}
        return {"candidates":[{"id":"c1", "outcome":"new", "target_view_id":"", "reason":"Distinct dated outcome.", "dependencies":[]}],
                "evidence":[], "thread_matches":[{"id":"t1", "target_thread_id":"g1" if index else "", "reason":"Same product rollout."}]}


def run_first(path):
    items, raw = fixtures()
    calls = Answers(raw)
    conn = threads.open_db(path)
    uni = universe.load(str(study.ROOT / "poc/universe.json"))
    first = threads.process(conn, calls, uni, items[0], 1)
    return conn, calls, uni, items, first


def test_d144_full_ingestion_reuses_subject_and_routes_later_risk(tmp_path):
    """State table: first subject, separate milestone, evidence-only update, dated read and resend."""
    conn, calls, uni, items, first = run_first(tmp_path / "views.sqlite")
    second = threads.process(conn, calls, uni, items[1], 2)
    third = threads.process(conn, calls, uni, items[2], 3)
    assert [r["thread_id"] for r in third["threads"]] == ["g1"]
    assert {r["view_id"] for r in third["memberships"]} == {"v1", "v2"}
    assert second["new_views"] == {"c1":"v2"} and third["affected_threads"] == ["g1"]
    assert [len(m["evidence"]) for m in threads.thread_detail(conn, "g1", 2)["members"]] == [1, 1]
    assert [len(m["evidence"]) for m in threads.thread_detail(conn, "g1", 3)["members"]] == [2, 1]
    before = len(calls.names)
    assert threads.process(conn, calls, uni, items[2], 3)["route"] == "skipped"
    assert len(calls.names) == before == 6
    assert conn.execute("pragma foreign_key_check").fetchall() == []
    conn.close()


@pytest.mark.parametrize("broken", ["missing", "empty", "unknown", "bad_id", "duplicate"])
def test_d144_required_local_references_are_closed(broken):
    """Closed shape: every candidate has unique, nonempty references to valid local identities."""
    _, raws = fixtures(); raw = raws[0]
    if broken == "missing": del raw["candidates"][0]["thread_ids"]
    if broken == "empty": raw["candidates"][0]["thread_ids"] = []
    if broken == "unknown": raw["candidates"][0]["thread_ids"] = ["t9"]
    if broken == "bad_id":
        raw["threads"][0]["id"] = "g1"; raw["candidates"][0]["thread_ids"] = ["g1"]
    if broken == "duplicate": raw["candidates"][0]["thread_ids"] = ["t1", "t1"]
    with pytest.raises(ValueError): threads.validate_extraction(raw)


def test_d144_same_batch_aliases_and_closed_search_targets():
    """Identity table: same-batch descriptions share a root; loops and unseen targets refuse."""
    local = [thread("t1"), thread("t2")]
    answer = {"candidates":[], "evidence":[], "thread_matches":[
        {"id":"t1", "target_thread_id":"t2", "reason":"Same development."},
        {"id":"t2", "target_thread_id":"g8", "reason":"Existing development."}]}
    offered = {"t1":[], "t2":[{"thread_id":"g8"}]}
    assert threads.resolve_threads(answer, local, offered) == {"t1":"g8", "t2":"g8"}
    answer["thread_matches"][1]["target_thread_id"] = ""
    assert threads.resolve_threads(answer, local, offered) == {"t1":"t2", "t2":"t2"}
    answer["thread_matches"][1]["target_thread_id"] = "t1"
    with pytest.raises(ValueError, match="cycle"): threads.resolve_threads(answer, local, offered)
    answer["thread_matches"][1]["target_thread_id"] = "g9"
    with pytest.raises(ValueError, match="not offered"): threads.resolve_threads(answer, local, offered)


def test_d144_failure_after_writes_rolls_back_all_new_records(tmp_path, monkeypatch):
    """Transaction table: original thesis and subject writes share the same commit boundary."""
    conn, calls, uni, items, first = run_first(tmp_path / "views.sqlite")
    original = threads.write_threads
    def fail(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError("Simulated failure after membership insert")
    monkeypatch.setattr(threads, "write_threads", fail)
    with pytest.raises(RuntimeError), conn:
        threads.process(conn, calls, uni, items[1], 2)
    assert conn.execute("select count(*) from views").fetchone()[0] == 1
    assert conn.execute("select count(*) from thread_members").fetchone()[0] == 1
    assert conn.execute("select count(*) from ingestion_events").fetchone()[0] == 1
    conn.close()


def test_d144_original_quote_rejection_cannot_create_subject(tmp_path):
    """Old checks still own acceptance: a removed candidate leaves no thread or membership."""
    items, raws = fixtures()
    raws[0]["evidence"][0]["quote"] = "This sentence is absent from the source article."
    calls = Answers(raws)
    original = calls.stage
    def answer(name, *args):
        if name.endswith("match"): return {"candidates":[], "evidence":[], "thread_matches":[]}
        return original(name, *args)
    calls.stage = answer
    conn = threads.open_db(tmp_path / "views.sqlite")
    result = threads.process(conn, calls, universe.load(str(study.ROOT / "poc/universe.json")), items[0], 1)
    assert result["threads"] == [] and result["views"] == []
    conn.close()


def test_d144_reader_uses_actual_links_and_excludes_replaced_evidence(tmp_path):
    """Provenance table: membership is no source claim; only dated, current evidence links count."""
    conn, calls, uni, items, first = run_first(tmp_path / "views.sqlite")
    threads.process(conn, calls, uni, items[1], 2)
    threads.process(conn, calls, uni, items[2], 3)
    conn.execute("insert into replacements(old_evidence_id,new_evidence_id,said_day,seq) values('e1','e3','2026-08-12',4)")
    assert [e["evidence_id"] for e in threads.thread_detail(conn, "g1", 4)["members"][0]["evidence"]] == ["e3"]
    source = calls.raw[0]["candidates"][0]
    store.create_view(conn, view_id="v3", object_id="NVDA", object_kind="company", kind="company",
        looks_at=source["looks_at"], question=source["question"], due_day=source["due_day"], year=source["year"],
        rungs=source["rungs"], seq=4, input_id=items[2]["input_id"], created_at="2026-08-12T12:00:00")
    conn.execute("insert into thread_members values('g1','v3',4,?)", (items[2]["input_id"],))
    assert threads.thread_detail(conn, "g1", 4)["members"][2]["evidence"] == []
    conn.close()


def test_d144_existing_view_keeps_membership_without_new_update(tmp_path):
    """Value table: merged candidates resolve to existing IDs; unchanged membership is not an update."""
    conn, calls, uni, items, first = run_first(tmp_path / "views.sqlite")
    handover = base.sift(calls.raw[0], items[0], [])
    checked = matching.Checked({"c1":(matching.OUTCOMES[0], "v1", [])}, {}, [], {})
    records, affected = threads.write_threads(conn, [thread()], {"t1":"g1"}, handover, checked,
                                               writing.Written(set(), {}, {}, []), 2, items[1])
    assert records == [{"candidate_id":"c1", "view_id":"v1", "thread_id":"g1", "new_membership":False}]
    assert affected == []
    conn.close()
