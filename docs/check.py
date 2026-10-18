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

EXTRACT = r"""
const fs = require('fs');
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
console.log(JSON.stringify({
  classification: consts('new-classification.js', ['TAGS', 'TREE', 'ROUTING', 'INPUT_SCHEMA', 'OUTPUT_FIELDS',
    'OBJECT_RULES', 'TIME_RULES', 'RULES', 'LOOKUP_TABLES', 'LOOKUP_RULES', 'NOT_SOURCES']),
  config: consts('new-config.js', ['CONFIG_SCHEMA', 'DISPATCH_TREE', 'TREE_NOTES', 'RULES', 'OPEN']),
  universe: consts('new-universe.js', ['OBJECT_KINDS', 'TRACKING_DEFAULTS', 'THEME_LIBRARY', 'TRACKING_EXAMPLES', 'RULES']),
  extraction: consts('new-facts.js', ['TEMPLATE', 'PROMPT_EXAMPLE', 'PROMPT_NOTES', 'CATEGORY_READS', 'CATEGORY_NOTE', 'EXTRACT_STEPS', 'WRITE_STEPS', 'DECIDE_TREE',
    'DECIDE_NOTES', 'SOURCE_TREE', 'SOURCE_NOTES', 'EXTRACT_EXAMPLE_TREE', 'WRITE_EXAMPLE_TREE', 'EXAMPLE_NOTE', 'VIEW_TREE', 'OBJECT_EXAMPLES', 'VIEW_FIELDS',
    'EVIDENCE_FIELDS', 'TIERS', 'LEVEL_RULES', 'LEVEL_TREE', 'PROPAGATION_TREE', 'ORDER_RULES', 'CONFLICT_RULES',
    'VERDICT_TRIGGERS', 'VERDICT_TREE', 'VERDICT_RULES']),
}));
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
console.log(JSON.stringify({ nodes: ids.length, detailPages: Object.keys(design.drilldowns).length, prds: Object.keys(window.HIVEMIND_PRD).length, problems }));
"""

FORM = {"两者": "文字和表格", "文本": "文字", "结构化": "表格"}


# Wording: one word per concept in the universe, classification, dispatch and extraction (glossary in
# docs/prd/00-system.md, decision D36). Each entry is a pattern that must not appear in their text, and the word to use.
AVOIDED_WORDS = [
    (r"原件", "原来那条"), (r"不算信息", "不算材料"), (r"发布那天", "发布日"), (r"发布日期", "发布时间"),
    (r"讲谁", "讲的是谁"), (r"讲的是哪家公司", "讲的是谁"), (r"讲的是哪些公司", "讲的是谁"),
    (r"上游给的编号", "上游编号"), (r"被拒", "不合格"), (r"数据记录", "表格数据"), (r"SEC 文件", "SEC 申报"),
    (r"申报文件", "申报"), (r"表格代码", "申报代码"), (r"(?<!人工)复核池", "人工复核池"), (r"NVDA 层", "对象层（NVDA）"),
    (r"(?<!提示词)(?<!上传)模板", "提示词模板或上传模板"), (r"发布方", "作者"), (r"(?<!数据)接口", "数据接口"),
    (r"文档", "文件"), (r"12 个大类", "12 组"), (r"作者的观点", "作者的看法"), (r"观点和估计", "看法和估计"),
    (r"每份文件整份", "每条信息整份"), (r"读文件|原文件|每一类文件|文件编号", "信息、或写明是哪张表"),
    (r"对象代码|只看代码|表里没有的代码|查不到的代码|代码和对象|代码的种类|代码按种类|哪种代码|代码本身|主题代码|(?<!股票|申报|商品|货币)代码对应",
     "对象标识或申报代码"),
    (r"SEC 编号", "CIK"), (r"加密代码", "加密货币代码"), (r"主题库里?的编号", "主题编号"), (r"由程序|测试程序", "代码"),
    (r"作者的种类|作者是哪种|默认类型", "作者类型"), (r"(?<!作者)类型", "类别"), (r"分析师身份", "分析师角色"),
    (r"原表格|持股类表格", "申报"), (r"官方行为", "官方行动"),
    (r"加密(?!货币)", "加密货币"), (r"定稿", "已冻结"), (r"(?i)ticker", "股票代码"), (r"一只股票|只新股票|这只股票|股票要看|股票、加密", "公司"),
]
EXTRACTION_CONSTANTS = ["TEMPLATE", "PROMPT_EXAMPLE", "PROMPT_NOTES", "CATEGORY_READS", "CATEGORY_NOTE", "EXTRACT_STEPS",
                        "SOURCE_TREE", "SOURCE_NOTES", "EXTRACT_EXAMPLE_TREE", "EXAMPLE_NOTE", "EXTRACT_OPEN"]


def wording_scope():
    """{place: text} of the in-scope wording: the four modules' PRDs and page data, and the boundary sentences."""
    places = {f"prd/{name}": re.sub(r"## 用词[\s\S]*?(?=\n## )", "", (PRD / name).read_text(encoding="utf-8")) for name in
              ["00-system.md", "01-universe.md", "02-classification.md", "03-config.md", "04-dispatch.md",
               "05-extraction.md", "09-review-pool.md"]}
    for name in ["new-universe.js", "new-classification.js", "new-config.js"]:
        places[name] = (DESIGN / name).read_text(encoding="utf-8")
    design = (DESIGN / "new-design.js").read_text(encoding="utf-8")
    places["new-design.js summary"] = design[design.index("  summary:"):design.index("  repositoryRoot:")]
    for node in ["classify", "dispatch", "extract", "universe", "config", "review"]:
        start = design.index(f"    {node}: {{")
        places[f"new-design.js {node}"] = design[start:design.index("\n    },\n", start)]
    facts = (DESIGN / "new-facts.js").read_text(encoding="utf-8")
    for name in EXTRACTION_CONSTANTS:
        match = re.search(r"\n  const " + name + r" = [\s\S]*?;\n", facts)
        if not match:
            raise SystemExit(f"wording check: {name} not found in new-facts.js")
        places[f"new-facts.js {name}"] = match.group(0)
    start = facts.index("  design.drilldowns.extract = {")
    places["new-facts.js extract page"] = facts[start:facts.index("  design.drilldowns.views = {")]
    return places


def avoided_words(text):
    return [(match.group(0), use) for pattern, use in AVOIDED_WORDS for match in re.finditer(pattern, text)]


def run_node(script):
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
            question = f"**问：{child['question']}**" + (f"（{child['note']}）" if child.get("note") else "")
            lines.append(f"{pad}- {child['answer']} → {child['label']}，{question}")
            lines += tree_children(child, depth + 1)
        else:
            note = f"：{child['note']}" if child.get("note") else ""
            lines.append(f"{pad}- {child['answer']} → **{child['label']}**{note}")
    return lines


def node_text(branch):
    """One box of a design-page tree as one line: answer → label｜question（note）."""
    text = (f"{branch['answer']} → " if branch.get("answer") else "") + branch["label"]
    if branch.get("question"):
        text += f"｜{branch['question']}"
    if branch.get("note"):
        text += f"（{branch['note']}）"
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
    lines = [start] + [f"  ↓ {step['code']} {step['name']}（{step['who']}）：{step['does']}" for step in steps]
    return "```\n" + "\n".join(lines) + "\n```"


def blocks(data):
    """{(PRD file, block name): Markdown} of every generated block."""
    classification, config, universe, extraction = data["classification"], data["config"], data["universe"], data["extraction"]
    tags = classification["TAGS"]
    order = sorted(tags, key=lambda code: int(code[1:]))
    family = {code: branch["label"] for branch in classification["TREE"]["children"] for code in branch["tags"]}
    tree = config["DISPATCH_TREE"]
    root = f"- {tree['label']} → **问：{tree['question']}**" + (f"（{tree['note']}）" if tree.get("note") else "")
    return {
        ("01-universe.md", "kinds"): table(["种类", "用什么认出它", "例子"],
                                           [[row["label"], row["identifiers"], row["example"]] for row in universe["OBJECT_KINDS"]]),
        ("01-universe.md", "defaults"): table(["种类", "要看的信息", "类别编号"],
                                              [[row["kind"], row["plain"], row["codes"]] for row in universe["TRACKING_DEFAULTS"]]),
        ("01-universe.md", "themes"): table(["分组", "主题"], [[row["category"], row["themes"]] for row in universe["THEME_LIBRARY"]]),
        ("01-universe.md", "examples"): table(["主题", "要看的信息", "类别编号"],
                                              [[row["theme"], row["tracked"], row["codes"]] for row in universe["TRACKING_EXAMPLES"]]),
        ("01-universe.md", "rules"): bullets(universe["RULES"], numbered=True),
        ("02-classification.md", "tags"): table(["编号", "类别", "形式", "所在大类", "怎么判", "例子"],
                                                [[code, tags[code]["label"], FORM[tags[code]["forms"]], family[code], tags[code]["decide"],
                                                  tags[code]["examples"]] for code in order]),
        ("02-classification.md", "definitions"): "\n".join(f"- **{code} {tags[code]['label']}**：{tags[code]['definition']}" for code in order),
        ("02-classification.md", "routing"): bullets(classification["ROUTING"], numbered=True),
        ("02-classification.md", "lookup"): table(["表", "拿什么查，查出什么", "例子"],
                                                  [[row["table"], row["lookup"], row["example"]] for row in classification["LOOKUP_TABLES"]])
        + "\n\n" + bullets(classification["LOOKUP_RULES"]),
        ("02-classification.md", "objects"): bullets(classification["OBJECT_RULES"], numbered=True),
        ("02-classification.md", "time"): bullets(classification["TIME_RULES"], numbered=True),
        ("02-classification.md", "rules"): bullets(classification["RULES"], numbered=True),
        ("02-classification.md", "not-inputs"): bullets(classification["NOT_SOURCES"]),
        ("02-classification.md", "fields"): table(["分组", "字段", "意思", "必填", "分类时用"],
                                                  [[row["group"], f"`{row['field']}`", row["meaning"], row["required"],
                                                    "✓" if row.get("classify") else ""] for row in classification["INPUT_SCHEMA"]])
        + f"\n\n**分类给出**：{classification['OUTPUT_FIELDS']}",
        ("03-config.md", "schema"): table(["内容", "说明", "怎么来"], [[row["item"], row["meaning"], row["source"]] for row in config["CONFIG_SCHEMA"]]),
        ("03-config.md", "rules"): bullets(config["RULES"], numbered=True),
        ("03-config.md", "open"): bullets(config["OPEN"]),
        ("04-dispatch.md", "tree"): "\n".join([root] + tree_children(tree, 1)),
        ("04-dispatch.md", "notes"): bullets(config["TREE_NOTES"]),
        ("05-extraction.md", "steps"): step_flow("一条信息进来（带类别和顺序号）", extraction["EXTRACT_STEPS"]),
        ("05-extraction.md", "example"): ascii_tree(extraction["EXTRACT_EXAMPLE_TREE"]) + "\n\n" + extraction["EXAMPLE_NOTE"],
        ("05-extraction.md", "template"): table(["部分", "写什么", "从哪来"],
                                                [[row["part"], row["content"], row["source"]] for row in extraction["TEMPLATE"]]),
        ("05-extraction.md", "prompt"): ascii_tree(extraction["PROMPT_EXAMPLE"]) + "\n\n" + bullets(extraction["PROMPT_NOTES"]),
        ("05-extraction.md", "sources"): ascii_tree(extraction["SOURCE_TREE"]) + "\n\n" + bullets(extraction["SOURCE_NOTES"]),
        ("05-extraction.md", "categories"): table(["类别", "这一类要读出什么", "证据一般在哪一层"],
                                                  [[f"{code} {tags[code]['label']}", extraction["CATEGORY_READS"][code]["read"],
                                                    extraction["CATEGORY_READS"][code]["tier"]] for code in order])
        + "\n\n" + extraction["CATEGORY_NOTE"],
        ("06-views.md", "write"): step_flow("抽取交来的候选观点和证据", extraction["WRITE_STEPS"]),
        ("06-views.md", "decide"): ascii_tree(extraction["DECIDE_TREE"]) + "\n\n" + bullets(extraction["DECIDE_NOTES"]),
        ("06-views.md", "write-example"): ascii_tree(extraction["WRITE_EXAMPLE_TREE"]),
        ("06-views.md", "structure"): ascii_tree(extraction["VIEW_TREE"]),
        ("06-views.md", "levels"): ascii_tree(extraction["LEVEL_TREE"]) + "\n\n" + bullets(extraction["LEVEL_RULES"]),
        ("06-views.md", "objects"): table(["对象", "主题层观点", "对象层观点", "证据从哪来"],
                                          [[row["kind"], row["theme"], row["object"], row["evidence"]] for row in extraction["OBJECT_EXAMPLES"]]),
        ("06-views.md", "propagation"): ascii_tree(extraction["PROPAGATION_TREE"]),
        ("06-views.md", "tiers"): table(["哪一层", "例子", "能做什么"], [[row["tier"], row["examples"], row["counts"]] for row in extraction["TIERS"]]),
        ("06-views.md", "conflicts"): bullets(extraction["CONFLICT_RULES"]),
        ("06-views.md", "fields"): table(["部分", "写什么", "例子"], [[row["part"], row["meaning"], row["example"]] for row in extraction["VIEW_FIELDS"]]),
        ("06-views.md", "evidence"): table(["部分", "写什么"], [[row["part"], row["meaning"]] for row in extraction["EVIDENCE_FIELDS"]]),
        ("06-views.md", "order"): bullets(extraction["ORDER_RULES"]),
        ("07-final-verdict.md", "triggers"): table(["触发", "谁发现"], [[row["trigger"], row["who"]] for row in extraction["VERDICT_TRIGGERS"]]),
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

    if len(avoided_words("并到原件；见复核池；按模板")) != 3:
        problems.append("the wording check misses its own control sentence")
    places = wording_scope()
    misused = [f"{place}: {word} (use {use})" for place, body in places.items() for word, use in avoided_words(body)]
    print(f"wording: {len(places)} places read, {len(misused)} avoided words")
    problems += [f"wording: {item}" for item in misused]

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
