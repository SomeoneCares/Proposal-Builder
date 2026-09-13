#!/usr/bin/env python3
"""
Styled base document for VertoWave proposals.

combine.py starts every build from new_document(), which carries:
- a header with the classification line (not on the cover page)
- a footer with a label and "Page X of Y"
- document core properties (title, author, subject, category, keywords)
- the styles the Markdown converter uses (Heading 1-3, Title, lists, Normal)

Run directly to write an empty shell:
  python build_base_template.py --out proposal_base.docx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor
except ImportError as exc:
    print("ERROR: python-docx is required. pip install python-docx", file=sys.stderr)
    raise SystemExit(2) from exc

CLASSIFICATION = "Confidential and Proprietary — Property of Verto Wave. Do Not Copy or Distribute."
GREY = RGBColor(0x70, 0x70, 0x70)
NAVY = RGBColor(0x1F, 0x38, 0x64)


def configure_base_styles(doc) -> None:
    """Tune the styles used by the markdown converter."""
    styles = doc.styles

    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), "Calibri")
    rfonts.set(qn("w:hAnsi"), "Calibri")

    def style_heading(name: str, size_pt: float, color: RGBColor | None = None) -> None:
        try:
            st = styles[name]
        except KeyError:
            return
        st.font.name = "Calibri"
        st.font.size = Pt(size_pt)
        st.font.bold = True
        if color is not None:
            st.font.color.rgb = color
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(6)

    style_heading("Heading 1", 16, NAVY)
    style_heading("Heading 2", 13, NAVY)
    style_heading("Heading 3", 11.5, RGBColor(0x33, 0x33, 0x33))

    for list_style in ("List Bullet", "List Bullet 2", "List Number"):
        try:
            st = styles[list_style]
        except KeyError:
            continue
        st.font.name = "Calibri"
        st.font.size = Pt(11)

    try:
        st = styles["Title"]
        st.font.name = "Calibri"
        st.font.size = Pt(26)
        st.font.bold = True
        st.font.color.rgb = NAVY
    except KeyError:
        pass


def _field_run(paragraph, instruction: str) -> None:
    run = paragraph.add_run()
    run.font.size = Pt(8)
    run.font.color.rgb = GREY
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(end)


def _grey_run(paragraph, text: str) -> None:
    run = paragraph.add_run(text)
    run.font.size = Pt(8)
    run.font.color.rgb = GREY


def add_header_footer(doc, footer_label: str) -> None:
    """Classification header and 'label | Page X of Y' footer; the cover page has neither."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = hp.add_run(CLASSIFICATION)
    run.font.size = Pt(8)
    run.font.color.rgb = GREY
    run.font.italic = True

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _grey_run(fp, f"{footer_label}   |   Page ")
    _field_run(fp, "PAGE")
    _grey_run(fp, " of ")
    _field_run(fp, "NUMPAGES")

    section.first_page_header.is_linked_to_previous = False
    section.first_page_footer.is_linked_to_previous = False


def set_core_properties(doc, title: str, author: str, subject: str, category: str, keywords: str) -> None:
    cp = doc.core_properties
    cp.title = title
    cp.author = author
    cp.subject = subject
    cp.category = category
    cp.keywords = keywords
    cp.comments = "Technical proposal. Pricing is excluded by design and attached separately."


def new_document(
    title: str = "DeviceX/SDX & StackX — Technical Proposal",
    footer_label: str = "VertoWave — Technical Proposal",
    author: str = "VertoWave",
    subject: str = "DeviceX/SDX & StackX technical proposal",
    keywords: str = "DeviceX, SDX, StackX, VertoWave, technical proposal",
):
    """Return an empty, styled document ready for the Markdown renderer."""
    doc = Document()
    configure_base_styles(doc)
    add_header_footer(doc, footer_label)
    set_core_properties(doc, title, author, subject, "Technical Proposal", keywords)
    return doc


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Write the styled VertoWave proposal base shell.")
    p.add_argument("--out", default="proposal_base.docx", help="Output docx path")
    args = p.parse_args(argv)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = new_document(
        title="DeviceX/SDX & StackX — Technical Proposal Template",
        footer_label="VertoWave — DeviceX/SDX & StackX Proposal Template",
    )
    doc.add_paragraph("")
    doc.save(out)
    print(f"OK: wrote base document {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
