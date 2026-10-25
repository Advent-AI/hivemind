"""D163: verify current-language coverage and its decisive scratch controls."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[3]


def main():
    spec = importlib.util.spec_from_file_location("english_doc_check", ROOT / "docs/check.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    assert checker.ENGLISH_FILES, "empty language population is unexercised"
    assert not checker.check_english(), checker.check_english()

    with tempfile.TemporaryDirectory(prefix="hivemind-english-docs-") as temporary:
        scratch = Path(temporary)
        docs = scratch / "docs"
        for name in checker.ENGLISH_FILES:
            target = docs / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / "docs" / name, target)
        assert not checker.check_english(docs)

        # D163: untranslated current text cannot hide outside the PRD body.
        target = scratch / "README.md"
        original = target.read_text()
        target.write_text(original + "\n还没定的\n")
        assert len(checker.check_english(docs)) == 1, "untranslated README not caught"
        target.write_text(original)

        # D163: a missing/empty declared surface is not a pass.
        target.unlink()
        assert checker.check_english(docs) == ["English surface missing: ../README.md"]
        target.write_text("")
        assert checker.check_english(docs) == ["English surface empty: ../README.md"]
        target.write_text(original)

        # D163: historical aliases permit only themselves, not nearby Chinese prose.
        name = "prd/05-extraction.md"
        target = docs / name
        target.write_text(target.read_text() + "\n还没定的\n")
        assert len(checker.check_english(docs)) == 1, "legacy alias hid unrelated text"

        # The checker mutant must fail the decisive assertion, not fail to import.
        source = (ROOT / "docs/check.py").read_text()
        needle = "if CJK_TEXT.search(line)]"
        assert source.count(needle) == 1
        mutant = scratch / "mutant.py"
        mutant.write_text(source.replace(needle, "if False]"))
        probe = (
            "import runpy, sys; m=runpy.run_path(sys.argv[1]); "
            "assert m['english_findings']('prd/00-system.md', '还没定的'), "
            "'untranslated heading not caught'"
        )
        result = subprocess.run([sys.executable, "-c", probe, str(mutant)], capture_output=True, text=True)
        assert result.returncode != 0
        assert "AssertionError: untranslated heading not caught" in result.stderr, result.stderr

        # D36/D163: restore all three retired-concept controls in English.
        retired = [
            (r"\bpremises?", "The premise changed."),
            (r"(?:verification|confirmation|falsification)", "Write the verification conditions."),
            (r"thes(?:is|es)\s+", "The thesis is confirmed."),
        ]
        for index, (marker, sentence) in enumerate(retired):
            lines = [line for line in source.splitlines(keepends=True) if marker in line]
            assert len(lines) == 1, lines
            rule_mutant = scratch / f"terminology-mutant-{index}.py"
            rule_mutant.write_text(source.replace(lines[0], ""))
            assert checker.avoided_words(sentence), sentence
            probe = (
                "import runpy, sys; m=runpy.run_path(sys.argv[1]); "
                "assert m['avoided_words'](sys.argv[2]), 'retired concept not caught'"
            )
            result = subprocess.run([sys.executable, "-c", probe, str(rule_mutant), sentence], capture_output=True, text=True)
            assert result.returncode != 0
            assert "AssertionError: retired concept not caught" in result.stderr, result.stderr

        # The rendered alias must be an invisible anchor, not escaped source text.
        renderer = ROOT / "docs/system-design/markdown.js"
        js_probe = (
            "global.window={};require(process.argv[1]);"
            "const a='<a id=\"historical-heading\"></a>';"
            "if(window.HIVEMIND_MARKDOWN.render(a).trim()!==a)"
            "throw Error('historical anchor shown as text');"
        )
        subprocess.run(["node", "-e", js_probe, str(renderer)], check=True, capture_output=True, text=True)
        js = renderer.read_text()
        assert js.count("if (anchor) {") == 1
        mutant_js = scratch / "markdown-mutant.js"
        mutant_js.write_text(js.replace("if (anchor) {", "if (false) {"))
        result = subprocess.run(["node", "-e", js_probe, str(mutant_js)], capture_output=True, text=True)
        assert result.returncode != 0
        assert "Error: historical anchor shown as text" in result.stderr, result.stderr

    print(json.dumps({
        "current_files_judged": len(checker.ENGLISH_FILES),
        "unexpected_chinese_text": 0,
        "input_controls": ["untranslated README", "missing file", "empty file", "text beside legacy alias"],
        "scratch_mutants_caught": ["disabled CJK detection", "removed premise rule", "removed verification-condition rule", "removed confirmed-thesis rule", "disabled historical anchor rendering"],
        "scope": "Documentation only; no runtime-language or model-quality claim",
    }, indent=2))


if __name__ == "__main__":
    main()
