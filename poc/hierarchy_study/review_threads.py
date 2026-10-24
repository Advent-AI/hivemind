"""D144: trace fixed source spans through real stored evidence and memberships for review."""
import argparse
import json
from pathlib import Path

import ingestion_groups as base
import study


def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default


def review(out, membership=False, flat=False, retained=False):
    items = read(out / "items.json") + [read(out / "extra-item.json")]
    sealed = study.read_only(base.SEALED)
    anchors = []
    for item, ident in zip(items, ["e7", "e55", "e724", "e519"]):
        body = base.extraction.normalise(item["text"])
        quote = base.extraction.normalise(sealed.execute("select quote from evidence where evidence_id=?", (ident,)).fetchone()[0])
        left = body.find(quote)
        if left < 0:
            raise ValueError("Known source passage absent: " + ident)
        anchors.append((body, left, left + len(quote)))
    sealed.close()
    totals, streams = {}, []
    arms = (["flat", "retained"] if retained else ["membership", "flat"] if flat
            else ["threads", "membership"] if membership else ["control", "threads"])
    folders = sorted(out / f"sample-{sample}-{arm}" for sample in [1, 2, 3] for arm in arms)
    if any(not folder.is_dir() for folder in folders):
        raise ValueError("Expected six independent streams")
    for folder in folders:
        arm = folder.name.rsplit("-", 1)[-1]
        conn = study.read_only(folder / "views.sqlite")
        is_new = conn.execute("select 1 from sqlite_master where type='table' and name='threads'").fetchone() is not None
        group_table = "threads" if is_new else "research_groups"
        member_table = "thread_members" if is_new else "group_members"
        group_key = "thread_id" if is_new else "group_id"
        group_field = "threads" if is_new else "groups"
        members_field = "memberships" if is_new else "members"
        affected_field = "affected_threads" if is_new else "affected_groups"
        totals.setdefault(arm, {"calls":0, "completed_calls":0, "failed_calls":0,
                                "unknown_cost_reservation":0, "estimated_usd":0, "input_tokens":0, "output_tokens":0})
        for path in sorted(folder.glob("item*.json")):
            call = read(path)
            if "request" not in call or "reused_from" in call:
                continue
            totals[arm]["calls"] += 1
            totals[arm]["completed_calls"] += call["status"] == "complete"
            totals[arm]["failed_calls"] += call["status"] == "failed"
            if call["status"] != "complete":
                totals[arm]["unknown_cost_reservation"] += call.get("reserved_usd", 0)
            for key in ["estimated_usd", "input_tokens", "output_tokens"]:
                totals[arm][key] += call.get(key, 0)
        events = {i:read(folder / f"item{i}-result.json") for i in range(1, 5)}
        passages = []
        for seq, (body, left, right) in enumerate(anchors, 1):
            def overlaps(quote):
                normalized = base.extraction.normalise(quote)
                start = body.find(normalized)
                return bool(normalized) and start >= 0 and start < right and start + len(normalized) > left
            extracted = read(folder / f"item{seq}-extract.json", {}).get("answer", {}).get("evidence", [])
            raw_hits = [e for e in extracted if overlaps(e["quote"])]
            hits = []
            for row in conn.execute("select * from evidence where created_seq=?", (seq,)):
                if not overlaps(row["quote"]):
                    continue
                destinations = [dict(v) for v in conn.execute("""select distinct v.view_id,v.question from views v
                    join evidence_links l on l.view_id=v.view_id where l.evidence_id=?""", (row["evidence_id"],))]
                hits.append({"evidence_id":row["evidence_id"], "quote":row["quote"], "destinations":destinations})
            passages.append({"raw_hits":raw_hits, "stored_hits":hits})
        destinations = [{v["view_id"] for e in passage["stored_hits"] for v in e["destinations"]} for passage in passages]
        shipment, deployment, risk, extra = destinations
        shared = []
        if events[2]:
            for group in events[2][group_field]:
                members = {m["view_id"] for m in events[2][members_field] if m[group_key] == group[group_key]}
                if any(s != d and s in members and d in members for s in shipment for d in deployment):
                    shared.append(group[group_key])
        affected = set(events[3][affected_field]) if events[3] else set()
        details = []
        for row in conn.execute(f"select * from {group_table}"):
            members = [dict(m) for m in conn.execute(f"""select v.view_id,v.question,m.seq from {member_table} m
                join views v on v.view_id=m.view_id where m.{group_key}=? order by m.seq,m.rowid""", (row[group_key],))]
            details.append(dict(row) | {"members":members})
        extra_shared = [g[group_key] for g in details if g[group_key] in shared and
                        any(m["view_id"] in extra and m["view_id"] not in shipment | deployment for m in g["members"])]
        result = {"stream":folder.name, "completed_articles":sum(e is not None for e in events.values()),
            "passages":passages, "shared_groups":shared, "risk_reaches_shipment":bool(risk & shipment),
            "risk_reaches_shared_group":bool(risk & shipment) and bool(set(shared) & affected),
            "extra_distinct_thesis_reuses_group":extra_shared, "groups":details,
            "dropped":{i:e["dropped"] for i,e in events.items() if e},
            "resend":read(folder / "resend.json"), "extra_resend":read(folder / "extra-resend.json"),
            "failure":read(folder / "failed.json"), "extra_failure":read(folder / "extra-failed.json")}
        streams.append(result)
        conn.close()
    report = {"streams":streams, "totals":totals, "source_anchors":["e7", "e55", "e724", "e519"],
              "note":"Source-span tracing identifies possible coverage; semantic acceptance requires reading all destinations and group members."}
    filename = ("retained-measurements.json" if retained else "flat-measurements.json" if flat
                else "membership-measurements.json" if membership else "measurements.json")
    study.write_json(out / filename, report)
    for stream in streams:
        print(stream["stream"], "completed", stream["completed_articles"], "shared", stream["shared_groups"],
              "risk", stream["risk_reaches_shared_group"], "extra", stream["extra_distinct_thesis_reuses_group"],
              "failure", stream["failure"] or stream["extra_failure"])
    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--membership", action="store_true")
    parser.add_argument("--flat", action="store_true")
    parser.add_argument("--retained", action="store_true")
    args = parser.parse_args()
    review(args.out.resolve(), args.membership, args.flat, args.retained)
