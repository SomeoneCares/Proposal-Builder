#!/usr/bin/env python3
"""
Build the reusable base VertoWave proposal_template.docx.

This is a styled empty shell that combine.py can load as a starting point
when --base is passed. It carries:
- A header with classification (Confidential and Proprietary — Property of
  Verto Wave. Do Not Copy or Distribute.)
- A footer with page number and classification
- Document core properties (title, author, subject, category, keywords,
  comments)
- The built-in styles needed by the markdown converter:
  Heading 1/2/3, List Bullet, List Number, Table Grid, Normal
- Default body font and base sizing tuned for a formal technical proposal.

Usage:
  python build_base_template.py --out proposal_template.docx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError as exc:
    print(f"ERROR: python-docx is required. pip install python-docx", file=sys.stderr)
    raise SystemExit(2) from exc


def set_cell_or_run_font(run, name: str = "Calibri", size_pt: int = 11, color: RGBColor | None = None):
    run.font.name = name
    run.font.size = Pt(size_pt)
    if color is not None:
        run.font.color.rgb = color


def configure_base_styles(doc: Document) -> None:
    """Tune the styles used by the markdown converter."""
    styles = doc.styles

    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    # Set East Asian font as well so the style is consistent
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), "Calibri")
    rfonts.set(qn("w:hAnsi"), "Calibri")

    def style_heading(name: str, size_pt: int, color: RGBColor | None = None):
        try:
            st = styles[name]
        except KeyError:
            return
        st.font.name = "Calibri"
        st.font.size = Pt(size_pt)
        st.font.bold = True
        if color is not None:
            st.font.color.rgb = color
        # space before/after
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(6)

    style_heading("Heading 1", 16, RGBColor(0x1F, 0x38, 0x64))
    style_heading("Heading 2", 13, RGBColor(0x1F, 0x38, 0x64))
    style_heading("Heading 3", 11.5, RGBColor(0x33, 0x33, 0x33))

    for list_style in ("List Bullet", "List Number"):
        try:
            st = styles[list_style]
        except KeyError:
            continue
        st.font.name = "Calibri"
        st.font.size = Pt(11)

    try:
        st = styles["Title"]
        st.font.name = "Calibri"
        st.font.size = Pt(24)
        st.font.bold = True
        st.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    except KeyError:
        pass


def add_header_footer(doc: Document) -> None:
    """Add a light header + footer with classification and page number."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    classification = "Confidential and Proprietary — Property of Verto Wave. Do Not Copy or Distribute."

    # Header (non-first pages)
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = classification
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in hp.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
        run.font.italic = True

    # Footer (non-first pages) with page number field
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run("VertoWave — DeviceX/SDX & StackX Proposal Template   |   Page ")
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)

    # PAGE field
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run2 = fp.add_run()
    run2.font.size = Pt(8)
    run2.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    run2._r.append(fld_begin)
    run2._r.append(instr)
    run2._r.append(fld_end)

    run3 = fp.add_run(" of ")
    run3.font.size = Pt(8)
    run3.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    fld_begin2 = OxmlElement("w:fldChar")
    fld_begin2.set(qn("w:fldCharType"), "begin")
    instr2 = OxmlElement("w:instrText")
    instr2.set(qn("xml:space"), "preserve")
    instr2.text = "NUMPAGES"
    fld_end2 = OxmlElement("w:fldChar")
    fld_end2.set(qn("w:fldCharType"), "end")
    run4 = fp.add_run()
    run4.font.size = Pt(8)
    run4.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    run4._r.append(fld_begin2)
    run4._r.append(instr2)
    run4._r.append(fld_end2)

    # First-page header/footer left blank (cover page)
    first_header = section.first_page_header
    first_header.is_linked_to_previous = False
    first_footer = section.first_page_footer
    first_footer.is_linked_to_previous = False


def set_core_properties(doc: Document, title: str, author: str, subject: str, category: str, keywords: str) -> None:
    cp = doc.core_properties
    cp.title = title
    cp.author = author
    cp.subject = subject
    cp.category = category
    cp.keywords = keywords
    cp.comments = "VertoWave modular proposal template. Pricing excluded by design."


def build_outPath(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build the VertoWave proposal_template.docx base shell.")
    p.add_argument("--out", default="proposal_template.docx", help="Output docx path")
    args = p.parse_args(argv)

    out = Path(args.out)
    build_outPath(out)

    doc = Document()

    configure_base_styles(doc)
    add_header_footer(doc)
    set_core_properties(
        doc,
        title="DeviceX/SDX & StackX — Technical Proposal Template",
        author="VertoWave",
        subject="Modular technical proposal template (DeviceX/SDX & StackX)",
        category="Proposal Template",
        keywords="DeviceX, SDX, StackX, proposal template, VertoWave, modular",
    )

    # Add a placeholder first paragraph so the doc isn't empty
    doc.add_paragraph("")

    doc.save(out)
    print(f"OK: wrote base template {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
