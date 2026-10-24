"""Zero-call diagnosis of self-targets; never changes the registered experiment or its scores."""
import argparse
import copy
import json
from pathlib import Path

import ingestion_threads as threads
import study
from hivemind import universe


class StoredFirstArticle:
    def __init__(self, source, repair):
        self.source, self.repair, self.edits = source, repair, []
        self.cfg = study.config.load(str(study.ROOT / "poc/config/poc-v7.json"))

    def stage(self, name, prompt, payload, schema, setting):
        assert name.startswith("item1-")
        record = json.loads((self.source / (name + ".json")).read_text())
        if record["status"] != "complete":
            raise ValueError("Stored call did not complete; no repair or new call")
        value = copy.deepcopy(record["answer"])
        if self.repair:
            for match in value.get("thread_matches", []):
                if match["id"] == match["target_thread_id"]:
                    self.edits.append({"id":match["id"], "from":match["target_thread_id"], "to":""})
                    match["target_thread_id"] = ""
        return value


def diagnose(source, out):
    if out.exists():
        raise ValueError("Use a new dated output directory")
    out.mkdir(parents=True)
    item = json.loads((source / "items.json").read_text())[0]
    uni = universe.load(str(study.ROOT / "poc/universe.json"))
    census, results = [], []
    for folder in sorted(source.glob("sample-*-threads")):
        for path in sorted(folder.glob("item*-match.json")):
            value = json.loads(path.read_text())
            if value["status"] != "complete":
                continue
            matches = value["answer"]["thread_matches"]
            census.append({"file":str(path), "decisions":len(matches),
                           "self_targets":[v for v in matches if v["id"] == v["target_thread_id"]]})
        for repair in [False, True]:
            calls = StoredFirstArticle(folder, repair)
            conn = threads.open_db(out / f"{folder.name}-{'edited' if repair else 'original'}.sqlite")
            result = {"sample":folder.name, "edited":repair}
            try:
                event = threads.process(conn, calls, uni, item, 1)
                result.update(status="written", views=len(event["views"]), threads=len(event["threads"]),
                              memberships=len(event["memberships"]))
            except Exception as error:
                conn.rollback()
                result.update(status="failed", error=str(error))
            result["edits"] = calls.edits
            result["stored_views"] = conn.execute("select count(*) from views").fetchone()[0]
            results.append(result)
            conn.close()
    report = {"notice":"Edited stored responses diagnose a format mismatch only. They do not pass acceptance or prove later grouping.",
              "network_calls":0, "census":census, "first_article_replays":results}
    study.write_json(out / "diagnosis.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    diagnose(args.source.resolve(), args.out.resolve())
