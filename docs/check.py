"""The last, mechanical step after a change (D22). Refreshing the design is a reasoning pass done by Claude over every
module, its PRD and the decisions; this script only checks what a reader cannot check reliably by eye:

1. every PRD block marked <!-- generated: NAME --> still equals the design page's data (a mismatch is reported, never
   rewritten: the PRD is fixed by reasoning);
2. the PRD bundle the page shows when opened from disk is rebuilt from the .md files;
3. the classification simulation passes;
4. every node is placed, every edge and code reference resolves, every detail page renders, every module has a PRD.

    python3 docs/check.py

Exits 1 when any check fails. The sealed copies in docs/archive are not touched.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
DESIGN = DOCS / "system-design"
PRD = DOCS / "prd"

# D163: current English surfaces. Source records, frozen versions and historical
# research remain in their original language; they are not current specifications.
ENGLISH_FILES = (
    "../README.md", "CURRENT_STATE.md", "experience-prd.md", "experience-prd.html",
    "agentic-experience.md", "agentic-experience.html", "../poc/ui/README.md",
    "poc/pipeline-plan.md", "poc/grouping-improvement-plan.md", "poc/thesis-ui.md",
    "poc/service.md", "poc/idea-card.md", "system-design.html",
    "system-design/new-design.js", "system-design/new-universe.js",
    "system-design/new-config.js", "system-design/new-classification.js",
    "system-design/new-facts.js", "system-design/render.js",
    "prd/README.md", "prd/00-system.md", "prd/01-universe.md", "prd/02-classification.md",
    "prd/03-config.md", "prd/04-dispatch.md", "prd/05-extraction.md", "prd/06-views.md",
    "prd/07-final-verdict.md", "prd/08-pull-mode.md", "prd/09-review-pool.md",
)
ENGLISH_LEGACY_LITERALS = {
    "prd/05-extraction.md": ('<a id="抽取时同时确定研究归属"></a>',),
    "prd/06-views.md": ('<a id="研究主线抽取时归组"></a>',),
    "poc/grouping-improvement-plan.md": ("`YYYY年`", "`YYYY财年`", "`YYYY自然年`"),
}
CJK_TEXT = re.compile(r"[\u3400-\u9fff]")


def english_findings(path, text):
    """Find untranslated current text, excluding only exact legacy literals."""
    for literal in ENGLISH_LEGACY_LITERALS.get(path, ()):
        text = text.replace(literal, "")
    return [f"{path}:{number}: {line.strip()[:160]}"
            for number, line in enumerate(text.splitlines(), 1) if CJK_TEXT.search(line)]


def check_english(root=DOCS):
    """Every declared current surface must exist, contain text and be English."""
    problems = []
    for name in ENGLISH_FILES:
        path = root / name
        if not path.is_file():
            problems.append(f"English surface missing: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            problems.append(f"English surface empty: {name}")
        problems.extend(english_findings(name, text))
    return problems

EXTRACT = r"""
const fs = require('fs');
const PAGE_CONSTANTS = __PAGE_CONSTANTS__;
function consts(file, names) {
  const text = fs.readFileSync(file, 'utf8');
  const out = {};
  for (const name of names) {
    const match = text.match(new RegExp('\\n  const ' + name + ' = ([\\s\\S]*?);\\n'));
    if (!match) throw new Error('missing ' + name + ' in ' + file);
    out[name] = Function('return ' + match[1])();
  }
  return out;
}
console.log(JSON.stringify(Object.fromEntries(
  Object.entries(PAGE_CONSTANTS).map(([key, [file, names]]) => [key, consts(file, names)]))));
"""

PAGE_CHECK = r"""
const fs = require('fs');
global.window = {};
global.requestAnimationFrame = () => {};
window.addEventListener = () => {};
['markdown', 'prd-bundle', 'new-design', 'new-classification', 'new-config', 'new-universe', 'new-facts'].forEach((name) => require('./' + name + '.js'));
const design = window.HIVEMIND_DESIGNS.new;
const problems = [];
const ids = Object.keys(design.nodes);
for (const view of design.views) {
  const placed = view.nodes.map((node) => node[0] || node.id);
  ids.filter((id) => !placed.includes(id)).forEach((id) => problems.push(`node ${id} is not placed in view ${view.id}`));
  view.edges.forEach((edge) => {
    const ends = Array.isArray(edge) ? [edge[0], edge[1]] : [edge.source, edge.target];
    ends.filter((id) => !ids.includes(id)).forEach((id) => problems.push(`edge end ${id} is not a node`));
  });
}
for (const id of ids) {
  const node = design.nodes[id];
  (node.refs || []).forEach((ref) => {
    const text = fs.readFileSync('../../' + ref.path, 'utf8');
    ref.symbol.split(' · ').filter((symbol) => !text.includes(symbol.trim())).forEach((symbol) => problems.push(`${id}: ${symbol} not in ${ref.path}`));
  });
  if (!node.prd) problems.push(`node ${id} has no PRD`);
  else if (!fs.existsSync('../../' + node.prd)) problems.push(`node ${id}: ${node.prd} does not exist`);
}
if (!design.prd || !fs.existsSync('../../' + design.prd)) problems.push('the system PRD is missing');
for (const key of Object.keys(design.drilldowns)) {
  try {
    const container = { innerHTML: '', querySelectorAll: () => [], querySelector: () => null };
    design.drilldowns[key].render(container, { escapeHtml: String });
    if (!container.innerHTML) problems.push(`detail page ${key} renders nothing`);
  } catch (error) { problems.push(`detail page ${key} fails: ${error.message}`); }
}
for (const [path, markdown] of Object.entries(window.HIVEMIND_PRD)) {
  const html = window.HIVEMIND_MARKDOWN.render(markdown).replace(/<pre>[\s\S]*?<\/pre>/g, '');
  if (/\*\*|^\|/m.test(html)) problems.push(`${path}: Markdown left unrendered`);
}
const alias = '<a id="historical-heading"></a>';
if (window.HIVEMIND_MARKDOWN.render(alias).trim() !== alias) problems.push('historical heading alias renders as visible text');
console.log(JSON.stringify({ nodes: ids.length, detailPages: Object.keys(design.drilldowns).length, prds: Object.keys(window.HIVEMIND_PRD).length, problems }));
"""

FORM = {"Both": "Text and tables", "Text": "Text", "Table": "Table"}


# D36/D163: one English term per concept. Historical drafts and the glossary's
# examples of retired terms remain outside this scope.
AVOIDED_WORDS = [
    (r"(?i)\b(?:company|object|theme) views?\b", "asset thesis or theme thesis"),
    (r"(?i)\b(?:active|inactive) thes(?:is|es)\b", "open or closed thesis"),
    (r"(?i)\bthesis driver\b", "focus"),
    (r"(?i)\bexpiry bucket\b", "due date"),
    (r"(?i)\bdispatch serial number\b", "sequence number"),
    (r"(?i)\bfixed five[- ]rung ladder\b", "five rungs, or two for yes/no"),
    (r"(?i)\bSEC documents?\b", "SEC filing"),
    (r"(?i)\bcategory type\b", "category or author type, according to meaning"),
    (r"(?i)\bdeleted evidence\b", "replaced evidence retained in history"),
    (r"(?i)\bviews to track\b", "candidate theses"),
    (r"(?i)\bauthor's views?\b", "author's opinions"),
    (r"(?i)\bpremises?\b", "dependencies"),
    (r"(?i)\b(?:verification|confirmation|falsification) conditions?\b", "ladder conditions"),
    (r"(?i)\b(?:thes(?:is|es)\s+(?:is|are|was|were|has been|have been)\s+(?:confirmed|falsified)|(?:confirmed|falsified)\s+thes(?:is|es))\b", "a frozen thesis state, not a separate verdict"),
]
WORD_CONTROLS = [
    ("Open a company view.", "Open an asset thesis."),
    ("Open a theme view.", "Open a theme thesis."),
    ("Update active theses.", "Update open theses."),
    ("Read the thesis driver.", "Read the focus."),
    ("Choose an expiry bucket.", "Choose a due date."),
    ("Assign a dispatch serial number.", "Assign a sequence number."),
    ("Use a fixed five-rung ladder.", "Use five rungs, or two for yes/no."),
    ("Read the SEC document.", "Read the SEC filing."),
    ("Set the category type.", "Set the category."),
    ("Remove deleted evidence.", "Keep replaced evidence in history."),
    ("The user's opinions are views to track.", "The user's opinions become candidate theses."),
    ("Read the author's view.", "Read the author's opinion."),
    ("The premise changed.", "The dependency changed."),
    ("Write the verification conditions.", "Write the ladder conditions."),
    ("Write a confirmation condition.", "Write a rung condition."),
    ("Write falsification conditions.", "Write ladder conditions."),
    ("The thesis is confirmed.", "The thesis state is frozen."),
    ("The theses are falsified.", "The theses are closed with their frozen states."),
    ("Read the confirmed thesis.", "Read the frozen thesis."),
    ("Read the falsified thesis.", "The official confirmed the event; rejudge the thesis."),
]
# The views database's page data (D38-D42): rendered into docs/prd/06-views.md and read by the wording check.
VIEWS_CONSTANTS = ["VIEW_TREE", "VIEW_KINDS", "KIND_NOTE", "LADDER_EXAMPLES", "LADDER_RULES", "POSITIONS", "TIERS", "TIER_RULES",
                   "STATE_RULES", "DEPENDENCY_TREE", "DEPENDENCY_RULES", "CHAIN_RULES", "INTAKE_SHAPE", "INTAKE_STEPS", "MATCH_OUTCOMES",
                   "MATCH_NOTES", "EVIDENCE_OUTCOMES", "EVIDENCE_NOTES", "INTAKE_EXAMPLE_TREE", "EVIDENCE_EXAMPLE",
                   "EVIDENCE_EXAMPLE_NOTE", "JUDGE_STEPS", "TRACE_FIELDS", "LIFECYCLE_TREE", "LIFECYCLE_NOTES",
                   "VIEW_FIELDS", "EVIDENCE_FIELDS", "ORDER_RULES", "STORE_NOTE", "VIEWS_OPEN", "VIEWS_PROPOSED", "GROUP_RELATIONS"]
EXTRACTION_CONSTANTS = ["TEMPLATE", "PROMPT_EXAMPLE", "PROMPT_NOTES", "CATEGORY_READS", "CATEGORY_NOTE", "EXTRACT_STEPS",
                        "EXTRACT_TWO", "EXTRACT_SORT_TREE", "SOURCE_TREE", "SOURCE_NOTES", "EXTRACT_EXAMPLE_TREE", "EXAMPLE_NOTE",
                        "EXTRACT_OPEN", "EXTRACT_RELATIONS"]
# The old final-verdict draft, still read for 07-final-verdict.md; it stays outside the wording check.
VERDICT_CONSTANTS = ["VERDICT_TRIGGERS", "VERDICT_TREE", "VERDICT_RULES", "VERDICT_EXAMPLE_NOTE"]
# Every constant the page data defines, by the key the checks read it under; the one place these lists are written.
PAGE_CONSTANTS = {
    "classification": ("new-classification.js", ["TAGS", "TREE", "ROUTING", "INPUT_SCHEMA", "OUTPUT_FIELDS", "OBJECT_RULES",
                                                 "TIME_RULES", "RULES", "LOOKUP_TABLES", "LOOKUP_RULES", "NOT_SOURCES"]),
    "config": ("new-config.js", ["CONFIG_SCHEMA", "DISPATCH_TREE", "TREE_NOTES", "RULES", "OPEN"]),
    "universe": ("new-universe.js", ["OBJECT_KINDS", "TRACKING_DEFAULTS", "THEME_LIBRARY", "TRACKING_EXAMPLES", "RULES"]),
    "extraction": ("new-facts.js", EXTRACTION_CONSTANTS + VERDICT_CONSTANTS),
    "views": ("new-facts.js", VIEWS_CONSTANTS),
}


def unlisted_constants():
    """Constants new-facts.js defines that no list above names. The wording check reads that file one constant at a
    time, so an unlisted constant would never be read; the other page-data files are read whole."""
    listed = {name for file_name, names in PAGE_CONSTANTS.values() if file_name == "new-facts.js" for name in names}
    defined = re.findall(r"\n  const ([A-Z_]+) = ", (DESIGN / "new-facts.js").read_text(encoding="utf-8"))
    return [f"new-facts.js: {name}" for name in defined if name not in listed]


def wording_scope():
    """{place: text} of the in-scope wording: the modules' PRDs and page data, and the boundary sentences."""
    places = {f"prd/{name}": re.sub(r"## Glossary[\s\S]*?(?=\n## )", "", (PRD / name).read_text(encoding="utf-8")) for name in
              ["00-system.md", "01-universe.md", "02-classification.md", "03-config.md", "04-dispatch.md",
               "05-extraction.md", "06-views.md", "09-review-pool.md"]}
    for name in ["new-universe.js", "new-classification.js", "new-config.js"]:
        places[name] = (DESIGN / name).read_text(encoding="utf-8")
    design = (DESIGN / "new-design.js").read_text(encoding="utf-8")
    places["new-design.js summary"] = design[design.index("  summary:"):design.index("  repositoryRoot:")]
    for node in ["classify", "dispatch", "extract", "views", "labels", "universe", "config", "review"]:
        start = design.index(f"    {node}: {{")
        places[f"new-design.js {node}"] = design[start:design.index("\n    },\n", start)]
    facts = (DESIGN / "new-facts.js").read_text(encoding="utf-8")
    for name in EXTRACTION_CONSTANTS + VIEWS_CONSTANTS:
        match = re.search(r"\n  const " + name + r" = [\s\S]*?;\n", facts)
        if not match:
            raise SystemExit(f"wording check: {name} not found in new-facts.js")
        places[f"new-facts.js {name}"] = match.group(0)
    start = facts.index("  design.drilldowns.extract = {")
    places["new-facts.js extract page"] = facts[start:facts.index("  design.drilldowns.views = {")]
    start = facts.index("  design.drilldowns.views = {")
    places["new-facts.js views page"] = facts[start:facts.index("  design.drilldowns.verdict = {")]
    return places


def avoided_words(text):
    return [(match.group(0), use) for pattern, use in AVOIDED_WORDS for match in re.finditer(pattern, text)]


def run_node(script):
    script = script.replace("__PAGE_CONSTANTS__", json.dumps(PAGE_CONSTANTS))
    result = subprocess.run(["node", "-e", script], cwd=DESIGN, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"node failed:\n{result.stderr}")
    return json.loads(result.stdout)


def cell(text):
    return str(text).replace("|", "／").replace("\n", " ")


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    return "\n".join(lines + ["| " + " | ".join(cell(value) for value in row) + " |" for row in rows])


def bullets(items, numbered=False):
    return "\n".join(f"{index}. {item}" if numbered else f"- {item}" for index, item in enumerate(items, 1))


def tree_children(branch, depth):
    lines = []
    for child in branch.get("children", []):
        pad = "  " * depth
        if child.get("children"):
            question = f"**Question: {child['question']}**" + (f" ({child['note']})" if child.get("note") else "")
            lines.append(f"{pad}- {child['answer']} → {child['label']}, {question}")
            lines += tree_children(child, depth + 1)
        else:
            note = f": {child['note']}" if child.get("note") else ""
            lines.append(f"{pad}- {child['answer']} → **{child['label']}**{note}")
    return lines


def node_text(branch):
    """One box of a design-page tree as one line: answer → label | question (note)."""
    text = (f"{branch['answer']} → " if branch.get("answer") else "") + branch["label"]
    if branch.get("question"):
        text += f" | {branch['question']}"
    if branch.get("note"):
        text += f" ({branch['note']})"
    return text


def ascii_tree(root):
    """A design-page tree drawn with box characters in a code block, so the PRD shows the same picture."""
    lines = [node_text(root)]

    def walk(branch, prefix):
        children = branch.get("children", [])
        for index, child in enumerate(children):
            last = index == len(children) - 1
            lines.append(prefix + ("└─ " if last else "├─ ") + node_text(child))
            walk(child, prefix + ("    " if last else "│   "))

    walk(root, "")
    return "```\n" + "\n".join(lines) + "\n```"


def step_flow(start, steps):
    """The steps of a process as a downward chain in a code block."""
    lines = [start] + [f"  ↓ {step['code']} {step['name']} ({step['who']}): {step['does']}" for step in steps]
    return "```\n" + "\n".join(lines) + "\n```"


def blocks(data):
    """{(PRD file, block name): Markdown} of every generated block."""
    classification, config, universe, extraction, views = (data["classification"], data["config"], data["universe"],
                                                            data["extraction"], data["views"])
    tags = classification["TAGS"]
    order = sorted(tags, key=lambda code: int(code[1:]))
    family = {code: branch["label"] for branch in classification["TREE"]["children"] for code in branch["tags"]}
    tree = config["DISPATCH_TREE"]
    root = f"- {tree['label']} → **Question: {tree['question']}**" + (f" ({tree['note']})" if tree.get("note") else "")
    return {
        ("01-universe.md", "kinds"): table(["Kind", "Identifiers", "Example"],
                                           [[row["label"], row["identifiers"], row["example"]] for row in universe["OBJECT_KINDS"]]),
        ("01-universe.md", "defaults"): table(["Kind", "Tracked information", "Category IDs"],
                                              [[row["kind"], row["plain"], row["codes"]] for row in universe["TRACKING_DEFAULTS"]]),
        ("01-universe.md", "themes"): table(["Group", "Theme"], [[row["category"], row["themes"]] for row in universe["THEME_LIBRARY"]]),
        ("01-universe.md", "examples"): table(["Theme", "Tracked information", "Category IDs"],
                                              [[row["theme"], row["tracked"], row["codes"]] for row in universe["TRACKING_EXAMPLES"]]),
        ("01-universe.md", "rules"): bullets(universe["RULES"], numbered=True),
        ("02-classification.md", "tags"): table(["ID", "Category", "Form", "Family", "Decision rule", "Example"],
                                                [[code, tags[code]["label"], FORM[tags[code]["forms"]], family[code], tags[code]["decide"],
                                                  tags[code]["examples"]] for code in order]),
        ("02-classification.md", "definitions"): "\n".join(f"- **{code} {tags[code]['label']}**: {tags[code]['definition']}" for code in order),
        ("02-classification.md", "routing"): bullets(classification["ROUTING"], numbered=True),
        ("02-classification.md", "lookup"): table(["Table", "Lookup input and result", "Example"],
                                                  [[row["table"], row["lookup"], row["example"]] for row in classification["LOOKUP_TABLES"]])
        + "\n\n" + bullets(classification["LOOKUP_RULES"]),
        ("02-classification.md", "objects"): bullets(classification["OBJECT_RULES"], numbered=True),
        ("02-classification.md", "time"): bullets(classification["TIME_RULES"], numbered=True),
        ("02-classification.md", "rules"): bullets(classification["RULES"], numbered=True),
        ("02-classification.md", "not-inputs"): bullets(classification["NOT_SOURCES"]),
        ("02-classification.md", "fields"): table(["Group", "Field", "Meaning", "Required", "Used for classification"],
                                                  [[row["group"], f"`{row['field']}`", row["meaning"], row["required"],
                                                    "✓" if row.get("classify") else ""] for row in classification["INPUT_SCHEMA"]])
        + f"\n\n**Classification returns**: {classification['OUTPUT_FIELDS']}",
        ("03-config.md", "schema"): table(["Item", "Meaning", "Source"], [[row["item"], row["meaning"], row["source"]] for row in config["CONFIG_SCHEMA"]]),
        ("03-config.md", "rules"): bullets(config["RULES"], numbered=True),
        ("03-config.md", "open"): bullets(config["OPEN"]),
        ("04-dispatch.md", "tree"): "\n".join([root] + tree_children(tree, 1)),
        ("04-dispatch.md", "notes"): bullets(config["TREE_NOTES"]),
        ("05-extraction.md", "relations"): bullets(extraction["EXTRACT_RELATIONS"]),
        ("06-views.md", "relations"): bullets(views["GROUP_RELATIONS"]),
        ("05-extraction.md", "steps"): step_flow("An item arrives with category and sequence number", extraction["EXTRACT_STEPS"]),
        ("05-extraction.md", "two"): table(["", "Evidence", "Candidate thesis"],
                                           [[row["aspect"], row["evidence"], row["candidate"]] for row in extraction["EXTRACT_TWO"]])
        + "\n\n" + ascii_tree(extraction["EXTRACT_SORT_TREE"]),
        ("05-extraction.md", "open"): bullets(extraction["EXTRACT_OPEN"]),
        ("05-extraction.md", "example"): ascii_tree(extraction["EXTRACT_EXAMPLE_TREE"]) + "\n\n" + extraction["EXAMPLE_NOTE"],
        ("05-extraction.md", "template"): table(["Part", "Writes", "Source"],
                                                [[row["part"], row["content"], row["source"]] for row in extraction["TEMPLATE"]]),
        ("05-extraction.md", "prompt"): ascii_tree(extraction["PROMPT_EXAMPLE"]) + "\n\n" + bullets(extraction["PROMPT_NOTES"]),
        ("05-extraction.md", "sources"): ascii_tree(extraction["SOURCE_TREE"]) + "\n\n" + bullets(extraction["SOURCE_NOTES"]),
        ("05-extraction.md", "categories"): table(["Category", "What to extract", "Typical evidence tier"],
                                                  [[f"{code} {tags[code]['label']}", extraction["CATEGORY_READS"][code]["read"],
                                                    extraction["CATEGORY_READS"][code]["tier"]] for code in order])
        + "\n\n" + extraction["CATEGORY_NOTE"],
        ("06-views.md", "structure"): ascii_tree(views["VIEW_TREE"]),
        ("06-views.md", "kinds"): table(["Kind", "Subject kind", "Ladder rungs", "Example"],
                                        [[row["kind"], row["on"], row["rungs"], row["example"]] for row in views["VIEW_KINDS"]])
        + "\n\n" + views["KIND_NOTE"],
        ("06-views.md", "ladder"): ascii_tree(views["LADDER_EXAMPLES"]) + "\n\n" + bullets(views["LADDER_RULES"], numbered=True),
        ("06-views.md", "positions"): table(["", "Meaning", "Decision maker", "Example"],
                                            [[row["position"], row["means"], row["moves"], row["example"]] for row in views["POSITIONS"]]) + "\n\n" + bullets(views["STATE_RULES"]),
        ("06-views.md", "tiers"): table(["Tier", "Example", "Role"], [[row["tier"], row["examples"], row["counts"]] for row in views["TIERS"]])
        + "\n\n" + bullets(views["TIER_RULES"]),
        ("06-views.md", "dependencies"): ascii_tree(views["DEPENDENCY_TREE"]) + "\n\n" + bullets(views["DEPENDENCY_RULES"]),
        ("06-views.md", "chain"): bullets(views["CHAIN_RULES"]),
        ("06-views.md", "shape"): table(["", "Candidate thesis", "Evidence"], [[row["aspect"], row["views"], row["evidence"]] for row in views["INTAKE_SHAPE"]]),
        ("06-views.md", "intake"): step_flow("Evidence and candidates from extraction: one round per item", views["INTAKE_STEPS"]),
        ("06-views.md", "outcomes"): table(["Destination", "When", "Writes"], [[row["outcome"], row["when"], row["writes"]] for row in views["MATCH_OUTCOMES"]])
        + "\n\n" + bullets(views["MATCH_NOTES"]),
        ("06-views.md", "evidence-outcomes"): table(["Destination", "When", "Writes"],
                                                     [[row["outcome"], row["when"], row["writes"]] for row in views["EVIDENCE_OUTCOMES"]])
        + "\n\n" + bullets(views["EVIDENCE_NOTES"]),
        ("06-views.md", "intake-example"): ascii_tree(views["INTAKE_EXAMPLE_TREE"]),
        ("06-views.md", "evidence-example"): table(["Item", "Evidence comparison", "Library result", "Rejudgement"],
                                                    [[row["item"], row["matched"], row["store"], row["rejudge"]] for row in views["EVIDENCE_EXAMPLE"]])
        + "\n\n" + views["EVIDENCE_EXAMPLE_NOTE"],
        ("06-views.md", "judge"): step_flow("First version: general-purpose model matching", views["JUDGE_STEPS"]),
        ("06-views.md", "trace"): table(["Part", "Recorded content"], [[row["part"], row["meaning"]] for row in views["TRACE_FIELDS"]]),
        ("06-views.md", "lifecycle"): ascii_tree(views["LIFECYCLE_TREE"]) + "\n\n" + bullets(views["LIFECYCLE_NOTES"]),
        ("06-views.md", "fields"): table(["Part", "Writes", "Example"], [[row["part"], row["meaning"], row["example"]] for row in views["VIEW_FIELDS"]]),
        ("06-views.md", "evidence"): table(["Part", "Writes"], [[row["part"], row["meaning"]] for row in views["EVIDENCE_FIELDS"]]),
        ("06-views.md", "order"): bullets(views["ORDER_RULES"]) + "\n\n" + views["STORE_NOTE"],
        ("06-views.md", "open"): bullets(views["VIEWS_OPEN"]),
        ("06-views.md", "proposed"): bullets(views["VIEWS_PROPOSED"], numbered=True),
        ("07-final-verdict.md", "triggers"): table(["Trigger", "Detected by"], [[row["trigger"], row["who"]] for row in extraction["VERDICT_TRIGGERS"]]),
        ("07-final-verdict.md", "verdict"): ascii_tree(extraction["VERDICT_TREE"]),
        ("07-final-verdict.md", "rules"): bullets(extraction["VERDICT_RULES"], numbered=True),
    }


def replace_block(text, name, body):
    start_marker, end_marker = f"<!-- generated: {name} -->", f"<!-- /generated: {name} -->"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        return None
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker)
    return text[:start] + "\n" + body + "\n" + text[end:]


def main():
    problems = []
    data = run_node(EXTRACT)

    drifted = []
    for (file, name), body in blocks(data).items():
        text = (PRD / file).read_text(encoding="utf-8")
        expected = replace_block(text, name, body)
        if expected is None:
            problems.append(f"{file}: generated block {name!r} is missing or doubled")
        elif expected != text:
            drifted.append(f"{file}#{name}")
    print(f"PRD blocks from page data: {len(blocks(data))} checked, {len(drifted)} differ from the page")
    problems += [f"{block} differs from the design page; fix the PRD" for block in drifted]

    if len(avoided_words("An active thesis uses a thesis driver and an expiry bucket.")) != 3:
        problems.append("the wording check misses its own control sentence")
    for caught, passed in WORD_CONTROLS:
        if not avoided_words(caught):
            problems.append(f"the wording check misses its control sentence {caught!r}")
        if avoided_words(passed):
            problems.append(f"the wording check flags the corrected sentence {passed!r}: {avoided_words(passed)}")
    print(f"wording controls: {len(WORD_CONTROLS)} pairs checked")
    missing = unlisted_constants()
    print(f"page constants: {sum(len(names) for _, names in PAGE_CONSTANTS.values())} listed, {len(missing)} unlisted")
    problems += [f"page constant not listed in check.py: {item}" for item in missing]
    places = wording_scope()
    misused = [f"{place}: {word} (use {use})" for place, body in places.items() for word, use in avoided_words(body)]
    print(f"wording: {len(places)} places read, {len(misused)} avoided words")
    problems += [f"wording: {item}" for item in misused]

    if not english_findings("prd/00-system.md", "## 还没定的"):
        problems.append("the English coverage check misses its untranslated-heading control")
    if english_findings("prd/00-system.md", "## Open questions"):
        problems.append("the English coverage check rejects its English control")
    for name, literals in ENGLISH_LEGACY_LITERALS.items():
        if english_findings(name, "\n".join(literals)):
            problems.append(f"the English coverage check rejects legacy literals in {name}")
        if not english_findings(name, "\n".join(literals) + "\n还没定的"):
            problems.append(f"legacy exceptions hide unrelated untranslated text in {name}")
    english_problems = check_english()
    print(f"English coverage: {len(ENGLISH_FILES)} current files checked, {len(english_problems)} findings")
    problems += english_problems

    bundle = subprocess.run([sys.executable, str(PRD / "build_bundle.py")], capture_output=True, text=True)
    print(bundle.stdout.strip())
    check = subprocess.run([sys.executable, str(PRD / "build_bundle.py"), "--check"], capture_output=True, text=True)
    if check.returncode != 0:
        problems.append(check.stdout.strip())

    simulation = subprocess.run([sys.executable, "simulate_classification.py"], cwd=DESIGN, capture_output=True, text=True)
    passed = "RESULT: PASS" in simulation.stdout
    print("classification simulation:", "PASS" if passed else "FAIL")
    if not passed:
        problems.append("the classification simulation fails; run python3 docs/system-design/simulate_classification.py")

    page = run_node(PAGE_CHECK)
    print(f"design page: {page['nodes']} nodes, {page['detailPages']} detail pages, {page['prds']} PRDs bundled")
    problems += page["problems"]

    if problems:
        print("\nFAIL")
        for problem in problems:
            print("  -", problem)
        return 1
    print("\nOK: the mechanical checks pass (the reasoning pass is separate)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
