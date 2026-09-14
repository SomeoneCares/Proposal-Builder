"""Smoke tests for the Streamlit pages (skipped where Streamlit is not installed)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps"))

try:
    from streamlit.testing.v1 import AppTest
except ImportError:  # pragma: no cover
    AppTest = None

import hermes_research  # noqa: E402


@unittest.skipIf(AppTest is None, "Streamlit not installed")
class BuilderPageTests(unittest.TestCase):
    def test_page_loads_and_builds_a_draft(self):
        at = AppTest.from_file(str(ROOT / "apps" / "proposal_builder.py"), default_timeout=240).run()
        self.assertFalse(at.exception, at.exception)
        next(b for b in at.button if b.label == "Build proposal").click().run()
        self.assertFalse(at.exception, at.exception)
        self.assertTrue(any("Build complete" in s.value for s in at.success), [e.value for e in at.error])

    def test_managed_services_offering_adds_the_ola(self):
        at = AppTest.from_file(str(ROOT / "apps" / "proposal_builder.py"), default_timeout=240).run()
        at.checkbox(key="off_managed_services").check().run()
        review = " ".join(m.value for m in at.markdown)
        self.assertIn("Operations Level Agreement", review)


@unittest.skipIf(AppTest is None, "Streamlit not installed")
class LibraryPageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.saved_env = {k: os.environ.get(k) for k in ("PROPOSAL_EDITOR_PASSWORD", "PROPOSAL_LIBRARY_DIR")}
        os.environ["PROPOSAL_LIBRARY_DIR"] = self.tmp.name

    def tearDown(self):
        for key, value in self.saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.tmp.cleanup()

    def page(self):
        return AppTest.from_file(str(ROOT / "apps" / "pages" / "1_Module_Library.py"), default_timeout=120)

    def test_locked_without_a_configured_password(self):
        os.environ.pop("PROPOSAL_EDITOR_PASSWORD", None)
        at = self.page().run()
        self.assertTrue(any("disabled" in e.value for e in at.error))

    def test_wrong_password_is_refused_and_right_one_unlocks(self):
        os.environ["PROPOSAL_EDITOR_PASSWORD"] = "correct-horse"
        at = self.page().run()
        at.text_input[0].input("wrong").run()
        at.button[0].click().run()
        self.assertTrue(any("Wrong password" in e.value for e in at.error))
        at.text_input[0].input("correct-horse").run()
        at.button[0].click().run()
        self.assertFalse(at.exception, at.exception)
        self.assertTrue(any(s.label == "Module" for s in at.selectbox))


class HermesReplyTests(unittest.TestCase):
    def test_reply_parsing_keeps_known_fields_and_http_sources(self):
        reply = "Here you go:\n" + json.dumps({"customer_profile": "A bank.", "objective_1": "Grow",
                                                "unexpected": "x", "sources": ["https://example.com", "file:///etc"]})
        parsed = hermes_research.parse_reply(reply)
        self.assertEqual(parsed["fields"]["customer_profile"], "A bank.")
        self.assertEqual(parsed["fields"]["esg_footprint"], "")
        self.assertNotIn("unexpected", parsed["fields"])
        self.assertEqual(parsed["sources"], ["https://example.com"])

    def test_non_json_reply_is_an_error(self):
        with self.assertRaises(hermes_research.ResearchError):
            hermes_research.parse_reply("I could not find anything.")


if __name__ == "__main__":
    unittest.main()
