"""Tests for combine.py, library.py and the module sources.

Run from the repo root:  python -m unittest discover -s tests -v
Needs python-docx (the builder's venv on the lab host has it).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import combine  # noqa: E402
import library  # noqa: E402
from docx import Document  # noqa: E402

INDEX = combine.load_index(ROOT / "module_index.json")
EXAMPLE_VALUES = json.loads((ROOT / "values-example.json").read_text(encoding="utf-8"))
LOGO = ROOT / "assets" / "vertowave_logo.png"
ALL_TOKENS = [mod["token"] for mod in combine.iter_modules(INDEX)]
FULL_OFFERING = ["licenses", "services", "managed_services", "premier_support"]
CORE = ["section_cover_execsummary", "section_document_control", "section_exec_summary", "section_assumptions",
        "section_out_of_scope", "section_change_mgmt", "section_pm_methodology", "section_roles",
        "section_professional_services", "section_training", "section_ola", "section_validity",
        "section_support_warranty", "section_glossary"]
BANNED_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(t) for t in INDEX["banned_terms"]) + r")(?![A-Za-z0-9])", re.I
)
THIRD_PARTY_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(t) for t in INDEX["third_party_terms"]) + r")(?![A-Za-z0-9])"
)
MODULE_FILES = sorted((ROOT / "modules").rglob("*.md"))


def full_values() -> dict:
    values = dict(EXAMPLE_VALUES)
    for slot in INDEX["customer_slots"]:
        if not str(values.get(slot, "")).strip():
            values[slot] = f"Value for {slot}"
    values["key_requirements"] = "- First requirement\n- Second requirement"
    values["compliance_matrix"] = [
        {"ref": "R-1", "requirement": "Encrypted site links", "code": "C-DX", "response": "IPsec overlay", "section": "SD-WAN"},
        {"ref": "R-2", "requirement": "Central log retention", "code": "C-SX", "response": "Tiered retention", "section": "Logs"},
    ]
    return values


class without_corporate_base:
    """Build with the built-in shell, as a deployment without the Word template does."""

    def __enter__(self):
        self.saved = combine.BASE_TEMPLATE
        combine.BASE_TEMPLATE = ROOT / "templates" / "no-such-base.docx"
        return self

    def __exit__(self, *exc):
        combine.BASE_TEMPLATE = self.saved
        return False


def build(values: dict, tokens=None, issue: bool = False, logo=LOGO, offering=None, library_dir=None, toc_levels=2,
          named_products=None):
    doc, warnings = combine.assemble_complete_document(
        INDEX, tokens or ALL_TOKENS, values, str(logo) if logo else None, issue,
        offering=offering or FULL_OFFERING, toc_levels=toc_levels, library=library_dir,
        named_products=named_products,
    )
    problems, unconfirmed = combine.check_document(doc, values, INDEX["banned_terms"], "complete", issue,
                                                   INDEX["third_party_terms"],
                                                   getattr(doc, "_vw_allowed_terms", set()))
    return doc, list(doc._vw_problems) + problems, unconfirmed


def text(doc) -> str:
    return combine.document_text(doc)


def document_text_of(doc) -> str:
    return combine.document_text(doc)


def headings(doc, level: int | None = None) -> list[str]:
    names = ("Heading 1", "Heading 2", "Heading 3") if level is None else (f"Heading {level}",)
    return [p.text for p in doc.paragraphs if p.style.name in names]


class ModuleSourceTests(unittest.TestCase):
    def test_every_registered_module_file_exists_and_every_file_is_registered(self):
        registered = {(ROOT / mod["file"]).resolve() for mod in combine.iter_modules(INDEX)}
        for path in registered:
            self.assertTrue(path.is_file(), path)
        self.assertEqual({p.resolve() for p in MODULE_FILES}, registered)

    def test_document_order_lists_every_module_once(self):
        order = INDEX["document_order"]
        self.assertEqual(len(order), len(set(order)))
        self.assertEqual(set(order), set(ALL_TOKENS))

    def test_modules_name_no_prior_customer(self):
        for md in MODULE_FILES:
            for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                self.assertIsNone(BANNED_RE.search(line), f"{md.name}:{n}: {line[:80]}")

    def test_modules_name_no_third_party_product(self):
        """Only the vendor product modules may name a product, and only their own."""
        vendor_files = {Path(mod["file"]).name for mod in combine.iter_modules(INDEX) if mod.get("vendor_name")}
        for md in MODULE_FILES:
            if md.name in vendor_files:
                continue
            for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                self.assertIsNone(THIRD_PARTY_RE.search(line), f"{md.name}:{n}: {line[:80]}")

    def test_vendor_modules_name_only_their_own_product(self):
        for mod in combine.iter_modules(INDEX):
            if not mod.get("vendor_name"):
                continue
            own = set(mod.get("vendor_terms", [])) | {mod["vendor_name"]}
            text_ = (ROOT / mod["file"]).read_text(encoding="utf-8")
            others = [t for t in INDEX["third_party_terms"] if t not in own]
            self.assertEqual(combine._term_problems(text_, others, {}, "name", ignore_case=False), [], mod["token"])

    def test_registry_is_clean(self):
        self.assertIsNone(BANNED_RE.search(json.dumps(INDEX["modules"])))
        # Product names live only in the vendor fields, which exist to carry them.
        without_vendor_fields = json.dumps([
            {k: v for k, v in mod.items() if k not in ("vendor_name", "vendor_terms")}
            for mod in combine.iter_modules(INDEX)])
        self.assertIsNone(THIRD_PARTY_RE.search(without_vendor_fields))
        self.assertNotIn("VertoWave", json.dumps(INDEX["modules"]))

    def test_modules_pass_library_validation(self):
        by_file = {Path(mod["file"]).name: mod["token"] for mod in combine.iter_modules(INDEX)}
        for md in MODULE_FILES:
            problems = library.validate_module_text(md.read_text(encoding="utf-8"), INDEX, by_file.get(md.name))
            self.assertEqual(problems, [], md.name)

    def test_every_requires_expression_is_valid(self):
        known = combine.known_condition_names(INDEX)
        for mod in combine.iter_modules(INDEX):
            if mod.get("requires"):
                self.assertLessEqual(combine.condition_names(combine.parse_condition(mod["requires"])), known)

    def test_every_slot_has_an_example_value_key(self):
        self.assertEqual(set(INDEX["customer_slots"]) - set(EXAMPLE_VALUES), set())

    def test_exclusions_live_only_in_the_out_of_scope_section(self):
        for md in MODULE_FILES:
            if md.name != "section_out_of_scope.md":
                self.assertNotIn("Out-of-Scope (explicitly)", md.read_text(encoding="utf-8"), md.name)

    def test_modules_use_us_spelling_and_the_brand_name(self):
        uk = re.compile(r"(?i)\b(organis|optimis|centralis|prioritis|modernis|virtualis|licence|behaviour|catalogue|"
                        r"programme|analyse|colour|defence|datacentre)")
        for md in MODULE_FILES:
            content = md.read_text(encoding="utf-8")
            self.assertIsNone(uk.search(content), f"{md.name}: {uk.search(content)}")
            self.assertNotIn("VertoWave", content, md.name)

    def test_figure_slugs_are_unique(self):
        slugs = [s for md in MODULE_FILES for s, _ in library.FIGURE_RE.findall(md.read_text(encoding="utf-8"))]
        self.assertEqual(len(slugs), len(set(slugs)))


class ConditionTests(unittest.TestCase):
    def test_expressions(self):
        tree = combine.parse_condition("module_nvr or (services and not managed_services)")
        self.assertTrue(combine.evaluate_condition(tree, {"module_nvr"}))
        self.assertTrue(combine.evaluate_condition(tree, {"services"}))
        self.assertFalse(combine.evaluate_condition(tree, {"services", "managed_services"}))
        for bad in ("module_nvr or", "(services", "services & licenses", ""):
            with self.assertRaises(ValueError):
                combine.parse_condition(bad)

    def test_blocks_lines_and_table_rows(self):
        source = "\n".join([
            "keep",
            "- only nvr <!-- if module_nvr -->",
            "| a | b <!-- if services --> |",
            "<!-- if licenses -->",
            "licensed",
            "<!-- if services -->",
            "nested",
            "<!-- endif -->",
            "<!-- endif -->",
        ])
        self.assertEqual(combine.apply_conditions(source, {"services"}), "keep\n| a | b |")
        self.assertEqual(combine.apply_conditions(source, {"licenses", "services", "module_nvr"}),
                         "keep\n- only nvr\n| a | b |\nlicensed\nnested")
        with self.assertRaises(ValueError):
            combine.apply_conditions("<!-- if services -->\nx", set())
        with self.assertRaises(ValueError):
            combine.apply_conditions("x\n<!-- endif -->", set())


class CompleteBuildTests(unittest.TestCase):
    """The built-in shell: its own cover module, its own logo placement."""

    @classmethod
    def setUpClass(cls):
        with without_corporate_base():
            cls.values = full_values()
            cls.draft, cls.draft_problems, _ = build(cls.values)
            cls.issue, cls.issue_problems, _ = build(cls.values, issue=True)
            cls.draft_text = text(cls.draft)
            cls.issue_text = text(cls.issue)
    def test_draft_and_issue_pass_the_checks(self):
        self.assertEqual(self.draft_problems, [])
        self.assertEqual(self.issue_problems, [])

    def test_no_markdown_or_comment_residue(self):
        for content in (self.draft_text, self.issue_text):
            for residue in ("<!--", "-->", "{{", "}}", ":---", "**", "\\newpage", "[["):
                self.assertNotIn(residue, content)

    def test_customer_name_used_instead_of_the_customer(self):
        self.assertNotRegex(self.issue_text, r"(?i)\bthe customer\b")
        self.assertIn(self.values["customer_short"], self.issue_text)

    def test_corporate_template_supplies_the_cover(self):
        """The Word template's cover carries the branding and this bid's own values."""
        self.assertTrue(combine.BASE_TEMPLATE.is_file(), "the corporate base document is missing")
        values = full_values()
        doc, problems, _ = build(values, tokens=["section_document_control", "module_sdwan"], issue=True)
        self.assertEqual(problems, [])
        # The cover sits in Word text boxes, so read the part rather than paragraph text.
        cover_xml = doc.element.body.xml
        self.assertIn(values["customer_name"], cover_xml)
        self.assertIn(values["engagement_name"], cover_xml)
        for placeholder in ("\u201cCustomer Name\u201d", "\u201cProject/Operation Name\u201d",
                            "\u201cProposal Released Date\u201d"):
            self.assertNotIn(placeholder, cover_xml, "a cover placeholder was left unfilled")
        self.assertNotIn("VERTO WAVE LOGO", document_text_of(doc), "the cover module must not repeat the cover")
        header = " ".join(p.text for p in doc.sections[0].header.paragraphs)
        self.assertIn("Technical Proposal", header, "the template's running header is missing")

    def test_logo_replaces_the_placeholder(self):
        self.assertNotIn(combine.LOGO_MARKER, self.issue_text)
        self.assertEqual(len(self.issue.inline_shapes), 1)
    def test_front_matter_then_toc_then_numbered_sections(self):
        paragraphs = [p.text for p in self.issue.paragraphs]
        toc = paragraphs.index("Table of Contents")
        self.assertLess(paragraphs.index(self.values["proposal_title"]), toc)
        self.assertLess(paragraphs.index("Document Control"), toc)
        body_h1 = [h for h in headings(self.issue, 1) if h != "Document Control"]
        self.assertTrue(body_h1[0].startswith("1" + combine.HEADING_SEPARATOR + "Executive Summary"), body_h1[0])
        for heading in body_h1:
            self.assertRegex(heading, r"^(\d+|Appendix [A-Z]:)" + combine.HEADING_SEPARATOR)
        self.assertTrue(any(h.startswith("Appendix A:" + combine.HEADING_SEPARATOR) for h in body_h1))
    def test_toc_lists_two_levels(self):
        levels = {entry[0] for entry in self.issue._vw_toc["entries"]}
        self.assertEqual(levels, {1, 2})

    def test_scope_table_lists_selected_capability_modules(self):
        self.assertIn("SD-WAN", self.issue_text)
        self.assertIn("StackX Call Center Management", self.issue_text)
        self.assertIn("Operation of the implemented solution under the agreed Operations Level Agreement.",
                      self.issue_text)

    def test_glossary_and_compliance_matrix(self):
        self.assertIn("Software-defined wide-area network", self.issue_text)
        self.assertIn("Encrypted site links", self.issue_text)

    def test_tables_have_a_shaded_header(self):
        xml = self.issue.tables[0]._tbl.xml
        self.assertIn(f'w:fill="{combine.HEADER_FILL}"', xml)
        self.assertIn("w:tblHeader", xml)

    def test_a_figure_without_an_image_is_left_out_entirely(self):
        """An empty box in front of a customer is worse than no figure, draft included."""
        for content in (self.draft_text, self.issue_text):
            self.assertNotIn("Figure placeholder", content)
            self.assertNotRegex(content, r"Figure \d+:")

    def test_the_build_reports_the_figures_it_left_out(self):
        with without_corporate_base():
            _doc, warnings = combine.assemble_complete_document(
                INDEX, ["module_sdwan"], full_values(), offering=["licenses", "services"])
        left_out = [w for w in warnings if w.startswith("figures left out")]
        self.assertTrue(left_out, "the build must say which figures had no image")
        self.assertIn("sdwan-topology", left_out[0])

    def test_issue_copy_drops_bid_team_material(self):
        for phrase in ("for the bid team", "This module is a reusable building block", "Author per bid",
                       "SECONDARY LOGO"):
            self.assertIn(phrase.lower(), self.draft_text.lower())
            self.assertNotIn(phrase.lower(), self.issue_text.lower())
    def test_sections_start_on_a_new_page_without_blank_pages(self):
        heading = next(p for p in self.issue.paragraphs
                       if p.text.endswith("Executive Summary") and p.style.name == "Heading 1")
        self.assertTrue(heading.paragraph_format.page_break_before)
        # No separate page-break paragraphs between modules (they can leave a blank page).
        breaks = [p for p in self.issue.paragraphs if 'w:type="page"' in p._p.xml and not p.text.strip()]
        self.assertEqual(breaks, [])
    def test_one_level_toc_is_short(self):
        doc, problems, _ = build(self.values, issue=True, toc_levels=1)
        self.assertEqual(problems, [])
        self.assertEqual({entry[0] for entry in doc._vw_toc["entries"]}, {1})
        # One entry per selected module; the registry now carries 57 of them.
        self.assertLess(len(doc._vw_toc["entries"]), 70)


class OfferingTests(unittest.TestCase):
    def issue_text(self, tokens, offering) -> str:
        doc, problems, _ = build(full_values(), tokens=tokens, issue=True, offering=offering)
        self.assertEqual(problems, [])
        return text(doc)

    def test_licenses_only(self):
        content = self.issue_text(CORE + ["module_sdwan"], ["licenses"])
        self.assertIn("deemed delivered", content)
        self.assertNotIn("acceptance criteria", content)
        for absent in ("Professional Services", "Project Management Methodology", "Operations Level Agreement",
                       "managed services", "Change Management Procedure"):
            self.assertNotIn(absent.lower(), content.lower(), absent)

    def test_services_only(self):
        content = self.issue_text(CORE + ["module_sdwan"], ["services"])
        self.assertIn("accepted against acceptance criteria", content)
        self.assertNotIn("deemed delivered", content)
        self.assertNotIn("Support and Warranty", content)
        self.assertNotIn("managed services", content.lower())

    def test_managed_services_appear_only_when_selected(self):
        without = self.issue_text(CORE + ["module_stackx_security", "module_stackx_soc"], ["licenses", "services"])
        self.assertNotIn("Operations Level Agreement", without)
        self.assertNotIn("SOC Operations", without)
        with_ms = self.issue_text(CORE + ["module_stackx_security", "module_stackx_soc"], FULL_OFFERING)
        self.assertIn("Operations Level Agreement", with_ms)
        self.assertIn("StackX SOC Operations", with_ms)

    def test_module_specific_lines_follow_the_selection(self):
        content = self.issue_text(CORE + ["module_sdwan"], FULL_OFFERING)
        for absent in ("NVR", "PBX", "call-flow", "extension fault", "analog cameras", "Surveillance"):
            self.assertNotIn(absent, content, absent)
        content = self.issue_text(CORE + ["module_sdwan", "module_nvr", "module_ipbx"], FULL_OFFERING)
        for present in ("NVR not recording", "Call-flow administration", "analog cameras"):
            self.assertIn(present, content, present)

    def test_stackx_only_bid_has_no_devicex_material(self):
        content = self.issue_text(CORE + ["module_stackx_itSM", "section_hardware_sizing"], FULL_OFFERING)
        for absent in ("DeviceX/SDX Assumptions", "Connectivity, Carriers", "site roll-out", "customs"):
            self.assertNotIn(absent.lower(), content.lower(), absent)

    def test_hardware_section_covers_stackx_without_devicex_specifics(self):
        """A StackX-only bid still states its infrastructure and environment requirements."""
        content = self.issue_text(CORE + ["module_stackx_itSM", "section_hardware_sizing"], FULL_OFFERING)
        for present in ("Hardware Specifications", "StackX Platform Infrastructure",
                        "Site and Data Center Requirements"):
            self.assertIn(present.lower(), content.lower(), present)
        for absent in ("DeviceX Appliance Specifications", "Site Sizing Classes", "Mid-Range",
                       "## Central Management"):
            self.assertNotIn(absent.lower(), content.lower(), absent)
        devicex = self.issue_text(CORE + ["module_sdwan", "section_hardware_sizing"], FULL_OFFERING)
        for present in ("DeviceX Appliance Specifications", "Site Sizing Classes", "Rack space"):
            self.assertIn(present.lower(), devicex.lower(), present)

    def test_the_services_scope_follows_the_products_sold(self):
        """The scope of work names the work each selected product needs, not a generic phase list."""
        stackx = self.issue_text(CORE + ["module_stackx_network_ops",
                                         "module_stackx_automation_orchestration"], FULL_OFFERING).lower()
        opentext = self.issue_text(CORE + ["product_ot_smax", "product_ot_ucmdb",
                                           "product_ot_obm"], FULL_OFFERING).lower()
        elastic = self.issue_text(CORE + ["product_el_observability", "product_el_logs",
                                          "product_el_apm"], FULL_OFFERING).lower()
        for phrase in ("catalog items and request workflows", "configuration item classes",
                       "event sources"):
            self.assertIn(phrase, opentext, phrase)
            self.assertNotIn(phrase, stackx, phrase)
            self.assertNotIn(phrase, elastic, phrase)
        for phrase in ("log sources", "hosts and services"):
            self.assertIn(phrase, elastic, phrase)
            self.assertNotIn(phrase, opentext, phrase)

    def test_vendor_product_named_or_described_by_function(self):
        """The same module ships named or functional, and the check follows the choice."""
        tokens = CORE + ["product_ot_smax", "product_el_logs"]
        generic, problems, _ = build(full_values(), tokens=tokens, issue=True)
        self.assertEqual(problems, [])
        generic_text = text(generic)
        for absent in ("OpenText", "SMAX", "Elastic", "Logstash"):
            self.assertNotIn(absent, generic_text, absent)
        for present in ("Service Management Platform", "Log Management and Analytics"):
            self.assertIn(present, generic_text, present)

        named, problems, _ = build(full_values(), tokens=tokens, issue=True,
                                   named_products=["product_ot_smax", "product_el_logs"])
        self.assertEqual(problems, [], "a named product must pass the third-party check")
        named_text = text(named)
        for present in ("OpenText SMAX", "Elastic Log Management"):
            self.assertIn(present, named_text, present)

    def test_naming_is_per_product(self):
        """One product may be named while another in the same proposal is not."""
        tokens = CORE + ["product_ot_smax", "product_el_logs"]
        doc, problems, _ = build(full_values(), tokens=tokens, issue=True, named_products=["product_ot_smax"])
        self.assertEqual(problems, [])
        content = text(doc)
        self.assertIn("OpenText SMAX", content)
        self.assertIn("Log Management and Analytics", content)
        for absent in ("Elastic", "Logstash"):
            self.assertNotIn(absent, content, absent)

    def test_a_product_name_is_refused_when_that_product_is_not_named(self):
        """Naming one product licenses its names only."""
        doc, _warnings = combine.assemble_complete_document(
            INDEX, CORE + ["product_ot_smax", "product_ot_nom"], full_values(), None, True,
            offering=FULL_OFFERING, named_products=["product_ot_smax"])
        allowed = doc._vw_allowed_terms
        self.assertIn("OpenText SMAX", allowed)
        for absent in ("OpenText NOM", "Elastic APM", "Universal Discovery"):
            self.assertNotIn(absent, allowed, absent)

    def test_premier_support_is_optional(self):
        self.assertNotIn("Premier Support", self.issue_text(CORE, ["licenses"]))
        self.assertIn("Premier Support", self.issue_text(CORE, ["licenses", "premier_support"]))


class CheckTests(unittest.TestCase):
    def test_blank_values_are_marked_in_a_draft_and_refused_in_an_issue_copy(self):
        values = full_values()
        values["services_integrations"] = ""
        _doc, problems, unconfirmed = build(values, tokens=["section_professional_services"])
        self.assertEqual(problems, [])
        self.assertEqual(unconfirmed, ["services_integrations"])
        _doc, problems, _ = build(values, tokens=["section_professional_services"], issue=True)
        self.assertTrue(any("services_integrations" in p for p in problems))

    def test_empty_compliance_matrix_blocks_an_issue_copy(self):
        values = full_values()
        values["compliance_matrix"] = []
        _doc, problems, _ = build(values, tokens=["section_compliance_matrix"], issue=True)
        self.assertTrue(any("compliance matrix" in p for p in problems))

    def check(self, sentence: str, values: dict | None = None) -> list[str]:
        doc = Document()
        doc.add_paragraph(sentence)
        problems, _ = combine.check_document(doc, values or full_values(), INDEX["banned_terms"], "complete", False,
                                             INDEX["third_party_terms"])
        return problems

    def test_banned_and_third_party_terms_are_refused(self):
        self.assertTrue(any("Telemedicine" in p for p in self.check("As delivered for the Telemedicine network.")))
        self.assertTrue(any("Kibana" in p for p in self.check("Dashboards are built in Kibana.")))

    def test_ordinary_words_and_the_current_customer_are_allowed(self):
        self.assertEqual(self.check("Changes run in agreed maintenance windows."), [])
        self.assertEqual(self.check("Prepared for EGYCash.", dict(full_values(), customer_name="EGYCash")), [])


class PageAndTocTests(unittest.TestCase):
    def test_pages_are_a4(self):
        doc, _problems, _ = build(full_values(), tokens=["section_validity"], issue=True)
        section = doc.sections[0]
        self.assertEqual((round(section.page_width.mm), round(section.page_height.mm)), (210, 297))

    def test_find_heading_pages_skips_toc_lines(self):
        entries = [(1, "Executive Summary", False), (1, "SD-WAN", True), (2, "Key Capabilities", True)]
        pages = [
            "Cover",
            "Executive Summary\nText",
            "Table of Contents\nExecutive Summary ........ 000\nSD-WAN ........ 000\nKey Capabilities ..... 000",
            "SD-WAN\nIntro\nKey Capabilities\n- item",
        ]
        self.assertEqual(combine.find_heading_pages(entries, pages), [2, 4, 4])

    @unittest.skipUnless(shutil.which("soffice") and shutil.which("pdftotext"), "LibreOffice not installed")
    def test_toc_page_numbers_filled_from_a_render(self):
        tokens = ["section_cover_execsummary", "section_document_control", "section_exec_summary", "module_sdwan",
                  "section_validity"]
        doc, problems, _ = build(full_values(), tokens=tokens, issue=True)
        self.assertEqual(problems, [])
        filled, message = combine.fill_toc_page_numbers(doc)
        self.assertTrue(filled, message)
        numbers = [int(run.text) for run in doc._vw_toc["runs"]]
        self.assertEqual(numbers, sorted(numbers))


class TemplateModeTests(unittest.TestCase):
    def test_template_keeps_double_brace_tokens(self):
        doc, _warnings = combine.assemble_template_document(INDEX, ALL_TOKENS, EXAMPLE_VALUES)
        content = text(doc)
        self.assertIn("{{module_sdwan}}", content)
        self.assertNotRegex(content, r"(?<!\{)\{module_sdwan\}(?!\})")
        problems, _ = combine.check_document(doc, EXAMPLE_VALUES, INDEX["banned_terms"], "template", False,
                                             INDEX["third_party_terms"], doc._vw_allowed_terms)
        self.assertEqual(problems, [])

    def test_template_may_name_every_product_it_carries(self):
        """The internal template lists every module, so it names every product we sell."""
        doc, _warnings = combine.assemble_template_document(INDEX, ALL_TOKENS, EXAMPLE_VALUES)
        self.assertIn("OpenText SMAX", doc._vw_allowed_terms)
        self.assertIn("Elastic APM", doc._vw_allowed_terms)


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lib = library.Library(Path(self.tmp.name), INDEX, ROOT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_saved_version_overrides_the_repo_copy_until_reverted(self):
        edited = self.lib.current_text("section_validity").replace("## Validity", "## Validity\n\nEdited in the portal.")
        entry = self.lib.save("section_validity", edited, "Basem", "wording")
        self.assertEqual(entry["version"], 1)
        doc, problems, _ = build(full_values(), tokens=["section_validity"], issue=True, library_dir=Path(self.tmp.name))
        self.assertEqual(problems, [])
        self.assertIn("Edited in the portal.", text(doc))
        self.lib.revert_to_baseline("section_validity", "Basem")
        doc, _p, _ = build(full_values(), tokens=["section_validity"], issue=True, library_dir=Path(self.tmp.name))
        self.assertNotIn("Edited in the portal.", text(doc))
        self.assertEqual(self.lib.restore("section_validity", 1, "Basem")["version"], 2)
        self.assertEqual(len(self.lib.history("section_validity")), 3)

    def test_invalid_versions_are_refused(self):
        base = self.lib.current_text("section_validity")
        for bad in (base + "\nDelivered for the Telemedicine network.", base + "\nBuilt on Kibana.",
                    base + "\n- line <!-- if module_nope -->", base + "\n{{unknown_slot}}",
                    base + "\n<!-- if services -->\nunclosed"):
            with self.assertRaises(ValueError):
                self.lib.save("section_validity", bad, "Basem", "bad")
        self.assertEqual(self.lib.history("section_validity"), [])

    def test_figure_upload_is_used_by_the_build(self):
        with without_corporate_base():
            self.lib.save_figure("change-request-flow", LOGO.read_bytes(), ".png")
            doc, problems, _ = build(full_values(), tokens=["section_change_mgmt"], issue=True,
                                     library_dir=Path(self.tmp.name))
            self.assertEqual(problems, [])
            self.assertEqual(len(doc.inline_shapes), 2)  # the shell's cover logo plus the figure
            self.assertIn("Figure 1: Change request process", text(doc))


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
        proc, written = self.run_cli(EXAMPLE_VALUES, "--logo", str(LOGO), "--no-toc-pages")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(written)
        self.assertIn("TO CONFIRM: ", proc.stderr)

    def test_invalid_offering_is_refused(self):
        proc, written = self.run_cli(EXAMPLE_VALUES, "--offering", "licenses,hardware")
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(written)


if __name__ == "__main__":
    unittest.main()
