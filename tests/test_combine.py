"""Tests for combine.py and the module sources.

Run from the repo root:  python -m unittest discover -s tests -v
Needs python-docx (the Hermes venv on the lab host has it).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import combine  # noqa: E402
from docx import Document  # noqa: E402

INDEX = combine.load_index(ROOT / "module_index.json")
EXAMPLE_VALUES = json.loads((ROOT / "values-example.json").read_text(encoding="utf-8"))
LOGO = ROOT / "assets" / "vertowave_logo.png"
ALL_TOKENS = [mod["token"] for mod in combine.iter_modules(INDEX)]
BANNED_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(t) for t in INDEX["banned_terms"]) + r")(?![A-Za-z0-9])", re.I
)


def full_values() -> dict:
    values = dict(EXAMPLE_VALUES)
    for slot in INDEX["customer_slots"]:
        if not str(values.get(slot, "")).strip():
            values[slot] = f"Value for {slot}"
    return values


def build(values: dict, tokens=None, issue: bool = False, logo=LOGO):
    doc, warnings = combine.assemble_complete_document(
        INDEX, tokens or ALL_TOKENS, values, str(logo) if logo else None, issue
    )
    problems, unconfirmed = combine.check_document(doc, values, INDEX["banned_terms"], "complete", issue)
    return doc, problems, unconfirmed


class ModuleSourceTests(unittest.TestCase):
    def test_every_registered_module_file_exists(self):
        for mod in combine.iter_modules(INDEX):
            self.assertTrue((ROOT / mod["file"]).is_file(), mod["file"])

    def test_module_sources_name_no_prior_customer(self):
        for md in (ROOT / "modules").rglob("*.md"):
            for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                self.assertIsNone(BANNED_RE.search(line), f"{md.name}:{n}: {line[:80]}")

    def test_registry_names_no_prior_customer(self):
        self.assertIsNone(BANNED_RE.search(json.dumps(INDEX["modules"])))

    def test_every_token_in_modules_is_a_slot_or_module(self):
        known = set(INDEX["customer_slots"]) | set(ALL_TOKENS)
        for md in (ROOT / "modules").rglob("*.md"):
            body = combine.prepare_module_text(md.read_text(encoding="utf-8"))
            for token in re.findall(r"\{\{([^}]*)\}\}", body):
                self.assertIn(token, known, f"{md.name}: {{{{{token}}}}}")

    def test_every_slot_has_an_example_value_key(self):
        self.assertEqual(set(INDEX["customer_slots"]) - set(EXAMPLE_VALUES), set())

    def test_figure_blocks_sit_at_section_boundaries(self):
        for md in (ROOT / "modules").rglob("*.md"):
            lines = md.read_text(encoding="utf-8").splitlines()
            figures = [i for i, line in enumerate(lines) if line.startswith("## Figure —")]
            self.assertLessEqual(len(figures), 1, md.name)
            for i in figures:
                before = [line for line in lines[:i] if line.strip() and line.strip() != "---"]
                self.assertFalse(before[-1].startswith("#"), f"{md.name}: figure directly under a heading")
                self.assertFalse(before[-1].rstrip().endswith(":"), f"{md.name}: figure splits a list intro")


class CompleteBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.values = full_values()
        cls.draft, cls.draft_problems, _ = build(cls.values)
        cls.issue, cls.issue_problems, _ = build(cls.values, issue=True)
        cls.draft_text = combine.document_text(cls.draft)
        cls.issue_text = combine.document_text(cls.issue)

    def test_draft_and_issue_pass_the_checks(self):
        self.assertEqual(self.draft_problems, [])
        self.assertEqual(self.issue_problems, [])

    def test_no_markdown_or_comment_residue(self):
        for text in (self.draft_text, self.issue_text):
            for residue in ("<!--", "-->", "{{", "}}", ":---", "**", "\\newpage"):
                self.assertNotIn(residue, text)

    def test_logo_replaces_the_placeholder(self):
        self.assertNotIn(combine.LOGO_MARKER, self.issue_text)
        self.assertEqual(len(self.issue.inline_shapes), 1)

    def test_issue_copy_without_logo_drops_the_placeholder_line(self):
        doc, problems, _ = build(self.values, issue=True, logo=None)
        self.assertEqual(problems, [])
        self.assertNotIn(combine.LOGO_MARKER, combine.document_text(doc))

    def test_cover_then_toc_then_capability_modules(self):
        paragraphs = [p.text for p in self.issue.paragraphs]
        self.assertLess(paragraphs.index(self.values["proposal_title"]), paragraphs.index("Table of Contents"))
        self.assertLess(paragraphs.index("Table of Contents"), paragraphs.index("SD-WAN"))
        self.assertNotIn("Cover Page & Executive Summary", paragraphs)

    def test_issue_copy_drops_bid_team_material(self):
        for phrase in ("Figure placeholder", "for the bid team", "This module is a reusable building block",
                       "Author per bid", "SECONDARY LOGO"):
            self.assertIn(phrase.lower(), self.draft_text.lower())
            self.assertNotIn(phrase.lower(), self.issue_text.lower())

    def test_table_separator_rows_are_not_rendered(self):
        for table in self.issue.tables:
            for row in table.rows:
                self.assertFalse(all(re.fullmatch(r":?-{3,}:?", c.text.strip()) for c in row.cells))

    def test_module_references_become_names(self):
        self.assertIn("StackX SOC Operations", self.draft_text)


class CheckTests(unittest.TestCase):
    def test_blank_values_are_marked_in_a_draft_and_refused_in_an_issue_copy(self):
        values = full_values()
        values["services_branches"] = ""
        _doc, problems, unconfirmed = build(values, tokens=["section_professional_services"])
        self.assertEqual(problems, [])
        self.assertEqual(unconfirmed, ["services_branches"])
        _doc, problems, _ = build(values, tokens=["section_professional_services"], issue=True)
        self.assertTrue(any("services_branches" in p for p in problems))

    def test_banned_term_in_the_output_is_refused(self):
        doc = Document()
        doc.add_paragraph("As delivered for the Telemedicine network last year.")
        problems, _ = combine.check_document(doc, full_values(), INDEX["banned_terms"], "complete", False)
        self.assertTrue(any("Telemedicine" in p for p in problems))

    def test_banned_term_allowed_when_it_is_the_current_customer(self):
        doc = Document()
        doc.add_paragraph("Prepared for EGYCash.")
        values = dict(full_values(), customer_name="EGYCash")
        problems, _ = combine.check_document(doc, values, INDEX["banned_terms"], "complete", False)
        self.assertEqual(problems, [])


class TemplateModeTests(unittest.TestCase):
    def test_template_keeps_double_brace_tokens(self):
        doc, _warnings = combine.assemble_template_document(INDEX, ALL_TOKENS, EXAMPLE_VALUES)
        text = combine.document_text(doc)
        self.assertIn("{{module_sdwan}}", text)
        self.assertNotRegex(text, r"(?<!\{)\{module_sdwan\}(?!\})")
        problems, _ = combine.check_document(doc, EXAMPLE_VALUES, INDEX["banned_terms"], "template", False)
        self.assertEqual(problems, [])


class CliTests(unittest.TestCase):
    def run_cli(self, values: dict, *extra: str):
        with tempfile.TemporaryDirectory() as tmp:
            values_path = Path(tmp) / "values.json"
            values_path.write_text(json.dumps(values), encoding="utf-8")
            out = Path(tmp) / "out.docx"
            proc = subprocess.run(
                [sys.executable, str(ROOT / "combine.py"), "--values", str(values_path), "--out", str(out), *extra],
                capture_output=True, text=True,
            )
            return proc, out.exists()

    def test_issue_build_with_blank_values_writes_nothing(self):
        proc, written = self.run_cli(EXAMPLE_VALUES, "--modules", "section_professional_services", "--issue")
        self.assertEqual(proc.returncode, combine.EXIT_CHECK_FAILED)
        self.assertFalse(written)
        self.assertIn("ERROR: an issue copy cannot contain unfilled values", proc.stderr)

    def test_draft_build_with_example_values_succeeds(self):
        proc, written = self.run_cli(EXAMPLE_VALUES, "--logo", str(LOGO))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(written)
        self.assertIn("TO CONFIRM: ", proc.stderr)


if __name__ == "__main__":
    unittest.main()
