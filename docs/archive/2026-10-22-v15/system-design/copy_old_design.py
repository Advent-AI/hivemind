"""Copy the old system design into old-design.js, the data the Old tab of system-design.html renders.

The source is the reviewed diagram in the old repository (its embedded DATA object). The copy keeps every node,
view, edge and recorded issue as the source states them, and rewrites only their shape into the one the page's
renderer reads for both designs. Run it again whenever the source page changes:

    python3 docs/system-design/copy_old_design.py [path/to/old/system-design.html]
"""

import hashlib
import json
import sys
from pathlib import Path

PAGE_DIRECTORY = Path(__file__).resolve().parent
DEFAULT_SOURCE = PAGE_DIRECTORY.parents[2] / "tn-hivemind" / "docs" / "system-design.html"
OUTPUT_PATH = PAGE_DIRECTORY / "old-design.js"

# The old repository's root, relative to docs/system-design.html, where every source reference resolves.
OLD_REPOSITORY_FROM_PAGE = "../../tn-hivemind/"

# The source page names its profiles by these short ids in its URL hash and by the long keys in its data.
PROFILE_KEYS = {"current": "current", "v2": "factor-v2", "v13": "factor-v13"}
PROFILE_LABELS = {
    "current": "current.json · main dossier",
    "v2": "factor-v2 · opt-in factor default",
    "v13": "factor-v13 · local, unadopted",
}

# Issues the source page records as repaired or local-only; it counts only the others on a node.
SETTLED_ISSUE_KEYS = {"handoff", "references", "dates"}

# Reference-only notices the source page shows on a view under a profile that does not run it.
VIEW_NOTICES = {
    "formation": {"current": "Reference only: this factor diagram does not execute under current.json."},
    "movement": {"current": "Reference only: this factor diagram does not execute under current.json."},
    "dossier": {
        profile_id: "Reference only: the factor preset selects the cohort path instead of this sampled-view company build."
        for profile_id in ("v2", "v13")
    },
}

VARIANT_FALLBACK = "This factor-specific contract is not enabled under current.json."

FOOTER_DOCUMENTS = [
    ("Diagram review and corrections", "docs/system-design-review.md"),
    ("Architecture", "docs/ARCHITECTURE.md"),
    ("Factor PRD", "docs/FACTOR_PRD.md"),
    ("Current state", "docs/CURRENT_STATE.md"),
    ("Handover and evidence", "docs/HANDOVER_2026-10-15.md"),
]


def read_embedded_data(page_text):
    """Return the DATA object the source page embeds as `const DATA = {...};`."""
    marker = "const DATA = "
    start = page_text.index(marker) + len(marker)
    data, _ = json.JSONDecoder().raw_decode(page_text[start:])
    return data


def plain_reference(reference):
    """A source reference as a repository path, symbol and line; the page builds the link."""
    return {"path": reference["path"], "symbol": reference["symbol"], "line": reference["line"]}


def profile_banners(data):
    """The context line the source page shows for each profile."""
    current_profile = data["profiles"]["current"]
    factor_v2 = data["presets"]["factor-v2"]
    factor_v13 = data["presets"]["factor-v13"]
    return {
        "current": {
            "tag": "Main dossier default",
            "lines": ["current.json · no factor stage enabled.", current_profile["decide_policy"]],
        },
        "v2": {
            "tag": "Opt-in factor preset",
            "lines": [
                f"{factor_v2['ladder_policy']} · {factor_v2['registry_policy']}",
                "This is a separate explicit preset, not the main dossier default.",
            ],
        },
        "v13": {
            "tag": "Local / unadopted",
            "lines": [
                f"{factor_v13['ladder_policy']} · {factor_v13['registry_policy']}",
                "Typed loading slots and condition-only states; combined semantic acceptance remains open.",
            ],
        },
    }


def convert(data, source_digest):
    banners = profile_banners(data)
    profiles = [
        {
            "id": profile_id,
            "label": PROFILE_LABELS[profile_id],
            "tag": banners[profile_id]["tag"],
            "lines": banners[profile_id]["lines"],
            "showIssueCount": profile_id != "current",
        }
        for profile_id in PROFILE_KEYS
    ]

    nodes = {}
    for node_id, node in data["nodes"].items():
        converted_node = {
            "title": node["title"],
            "subtitle": node["subtitle"],
            "kind": node["kind"],
            "purpose": node["purpose"],
            "inputs": node["inputs"],
            "outputs": node["outputs"],
            "checks": node["checks"],
            "inspect": node["inspect"],
            "refs": [plain_reference(reference) for reference in node["refs"]],
            "issues": node["issues"],
        }
        if node.get("variant"):
            converted_node["variant"] = node["variant"]
            converted_node["variantFallback"] = VARIANT_FALLBACK
        nodes[node_id] = converted_node

    views = []
    for graph in data["graphs"]:
        edges = []
        for edge in graph["edges"]:
            converted_edge = {key: edge[key] for key in ("source", "target", "label", "style", "route") if edge.get(key)}
            if edge.get("candidate"):
                converted_edge["profiles"] = ["v13"]
            edges.append(converted_edge)
        views.append({
            "id": graph["id"],
            "title": graph["title"],
            "kind": graph["kind"],
            "caption": graph["caption"],
            "width": graph["width"],
            "height": graph["height"],
            "nodes": [{"id": placed["id"], "x": placed["x"], "y": placed["y"]} for placed in graph["nodes"]],
            "edges": edges,
            "order": graph["order"],
            "notices": VIEW_NOTICES.get(graph["id"], {}),
        })

    issues = {
        issue_key: {
            "label": issue["label"],
            "status": issue["status"],
            "detail": issue["detail"],
            "evidence": issue["evidence"],
            "refs": [plain_reference(reference) for reference in issue["refs"]],
            "open": issue_key not in SETTLED_ISSUE_KEYS,
        }
        for issue_key, issue in data["issues"].items()
    }

    return {
        "id": "old",
        "title": "Old",
        "heading": "旧系统设计",
        "summary": "tn-hivemind 现有系统的源码对照图（review r3），原样复制，只换成统一的米色界面。",
        "source": {
            "page": OLD_REPOSITORY_FROM_PAGE + "docs/system-design.html",
            "sha256": source_digest,
            "snapshot": data["snapshot"],
            "revision": data["revision"],
            "head": data["head"],
            "note": data["note"],
        },
        "repositoryRoot": OLD_REPOSITORY_FROM_PAGE,
        "profiles": profiles,
        "defaultProfile": "current",
        "nodes": nodes,
        "views": views,
        "issues": issues,
        "documents": [{"label": label, "path": path} for label, path in FOOTER_DOCUMENTS],
        "configuration": {
            "references": [plain_reference(reference) for reference in data["config_refs"]],
            "flags": {profile_id: data["config_flags"][key] for profile_id, key in PROFILE_KEYS.items()},
            "factorDirection": {profile_id: data["config_direction"][key] for profile_id, key in PROFILE_KEYS.items()},
            "profiles": {profile_id: data["profiles"][key] for profile_id, key in PROFILE_KEYS.items()},
            "presets": {profile_id: data["presets"][key] for profile_id, key in PROFILE_KEYS.items()},
        },
        "drilldowns": {},
    }


def main():
    source_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SOURCE
    page_bytes = source_path.read_bytes()
    source_digest = hashlib.sha256(page_bytes).hexdigest()
    design = convert(read_embedded_data(page_bytes.decode("utf-8")), source_digest)
    script = (
        "// Generated by copy_old_design.py from ../tn-hivemind/docs/system-design.html; do not edit by hand.\n"
        f"// Source sha256 {source_digest}.\n"
        "window.HIVEMIND_DESIGNS = window.HIVEMIND_DESIGNS || {};\n"
        "window.HIVEMIND_DESIGNS.old = "
        + json.dumps(design, ensure_ascii=False, indent=1)
        + ";\n"
    )
    OUTPUT_PATH.write_text(script, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} from {source_path}: {len(design['nodes'])} nodes, {len(design['views'])} views, "
          f"{sum(len(view['edges']) for view in design['views'])} edges, {len(design['issues'])} issues")


if __name__ == "__main__":
    main()
