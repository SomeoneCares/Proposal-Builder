#!/usr/bin/env python3
"""
proposal-template combine script

Reads module_index.json, selected module Markdown files, and a customer
values JSON, then assembles a Word .docx.

Two modes:
  --mode complete   Replace {{module_*}} tokens with assembled module
                    content; replace {{customer_*}} tokens with values.
  --mode template   Keep {{module_*}} and {{customer_*}} tokens in place
                    (produces a token-based docx template for per-bid fill).

Markdown -> docx is a basic converter:
  - # / ## / ### -> Heading 1 / 2 / 3
  - - / * bullet lines -> List Bullet
  - 1. numbered lines -> List Number
  - | table rows -> a Word table (first row bold as header if header marker present)
  - blank lines separate paragraphs
  - everything else -> Normal paragraph

New (this turn): --logo <path> embeds the Verto Wave logo into the cover
page paragraph found via the "[VERTO WAVE LOGO" placeholder marker.

Limitations:
  - No inline formatting (bold/italic/code) beyond what is trivial to add.
  - Complex markdown (nested lists, blockquotes, images, links) is not rendered.
  - Tables are basic pipe tables only.
  - If a referenced module file is missing in --mode complete, the token is
    left unresolved and a warning is printed — the docx is still produced.

Usage:
  python combine.py --values values-xxx.json --modules sdwan,firewall,nvr \
      --mode complete --out proposal-xxx.docx

  python combine.py --values values-xxx.json --modules sdwan,firewall,nvr \
      --mode template --out proposal-xxx-template.docx

  python combine.py --values values-xxx.json --mode complete \
      --logo assets/vertowave_logo.png --out proposal-with-logo.docx

If --modules is omitted, all modules (devicex + stackx + cross_cutting) are used.
If a module is listed in module_index.json as required=true and is omitted from
--modules, a warning is printed but the build continues.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError as exc:
    print(f"ERROR: python-docx is required. Install with: pip install python-docx", file=sys.stderr)
    raise SystemExit(2) from exc

# Logger for logo embedding status
LOGOS: list[str] = []


def embed_logo(doc: Document, logo_path: str | None, max_width_in: float = 3.5) -> None:
    """Embed a logo image into the document, centered, if logo_path is given.

    Searches the document body for the first paragraph containing a logo
    placeholder marker (``[VERTO WAVE LOGO`` or ``[LOGO``) and replaces that
    paragraph's content with the picture, centered. If no placeholder is found,
    the picture is inserted at the very start of the document body.

    Returns early (and logs) when the file does not exist or cannot be read.
    """
    if not logo_path:
        LOGOS.append("logo: no --logo path given; skipping embed")
        return
    lp = Path(logo_path)
    if not lp.exists():
        LOGOS.append(f"logo: path not found: {logo_path}")
        return
    try:
        with lp.open("rb") as fh:
            fh.read(1)
    except OSError as exc:
        LOGOS.append(f"logo: cannot read {logo_path}: {exc}")
        return

    pic_paragraph: Document.Paragraph | None = None
    for p in doc.paragraphs:
        if "[VERTO WAVE LOGO" in p.text or "[LOGO" in p.text:
            pic_paragraph = p
            break

    if pic_paragraph is None:
        LOGOS.append("logo: no placeholder paragraph found; inserting at document start")
        first_p = doc.paragraphs[0] if doc.paragraphs else None
        if first_p is not None:
            new_p = OxmlElement("w:p")
            first_p._p.addprevious(new_p)
            pic_paragraph = first_p
        else:
            pic_paragraph = doc.add_paragraph()

    run = pic_paragraph.add_run()
    run.add_picture(str(lp), width=Inches(max_width_in))
    pic_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    LOGOS.append(f"logo: embedded {lp.name} ({lp.suffix})")


def _logo_status() -> str:
    return " | ".join(LOGOS)


SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_INDEX = SCRIPT_DIR / "module_index.json"
MODULES_DIR = SCRIPT_DIR / "modules"


def load_index() -> dict:
    if not MODULE_INDEX.exists():
        print(f"ERROR: module_index.json not found at {MODULE_INDEX}", file=sys.stderr)
        raise SystemExit(2)
    with MODULE_INDEX.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_module_file(token: str, index: dict) -> Path | None:
    for group_key, group in index.get("modules", {}).items():
        for mod in group.get("modules", []):
            if mod.get("token") == token:
                rel = mod.get("file", "")
                if not rel:
                    return None
                candidate = SCRIPT_DIR / rel
                if candidate.exists():
                    return candidate
                alt = MODULES_DIR / f"{token}.md"
                if alt.exists():
                    return alt
                return None
    return None


def parse_markdown_blocks(text: str) -> list[dict]:
    """Split markdown text into a list of block dicts for basic docx building."""
    blocks: list[dict] = []
    lines = text.splitlines()
    i = 0
    n = len(lines)

    def flush_paragraph(start: int) -> None:
        nonlocal i
        para_lines: list[str] = []
        while start < n and lines[start].strip() != "":
            para_lines.append(lines[start])
            start += 1
        if para_lines:
            blocks.append({"type": "paragraph", "text": "\n".join(para_lines)})
        i = start

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped == "":
            i += 1
            continue

        if stripped.startswith("#"):
            heading_match = re.match(r"^(#{1,3})\s+(.*)$", stripped)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                blocks.append({"type": "heading", "level": level, "text": text})
                i += 1
                continue

        if stripped.startswith("|"):
            table_rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                row_line = lines[i].strip()
                cells = [c.strip() for c in row_line.strip("|").split("|")]
                table_rows.append(cells)
                i += 1
            if table_rows:
                blocks.append({"type": "table", "rows": table_rows})
            continue

        if re.match(r"^[\s]*[-*]\s+", line):
            bullet_lines: list[str] = []
            while i < n and re.match(r"^[\s]*[-*]\s+", lines[i]):
                bullet_lines.append(lines[i].strip())
                i += 1
            blocks.append({"type": "bullet_list", "items": bullet_lines})
            continue

        if re.match(r"^[\s]*\d+\.\s+", line):
            num_lines: list[str] = []
            while i < n and re.match(r"^[\s]*\d+\.\s+", lines[i]):
                num_lines.append(lines[i].strip())
                i += 1
            blocks.append({"type": "numbered_list", "items": num_lines})
            continue

        flush_paragraph(i)

    return blocks


def _is_metadata_block(block: dict) -> bool:
    if block.get("type") != "paragraph":
        return False
    text = block.get("text", "")
    if not text.strip():
        return False
    first_line = text.splitlines()[0].strip()
    return bool(re.match(r"^\*\*(Token|Group|Required|Present in|To be authored|Sub-components|Note|Format|Duration|Attendees|Audience|Focus|Overview)\s*:?\s*\*\*", first_line))


def build_docx_from_blocks(doc: Document, blocks: list[dict]) -> None:
    for block in blocks:
        if _is_metadata_block(block):
            continue
        t = block.get("type")
        if t == "heading":
            level = block.get("level", 1)
            doc.add_heading(block.get("text", ""), level=level)
        elif t == "paragraph":
            doc.add_paragraph(block.get("text", ""))
        elif t == "bullet_list":
            for item in block.get("items", []):
                clean = re.sub(r"^[\s]*[-*]\s+", "", item)
                doc.add_paragraph(clean, style="List Bullet")
        elif t == "numbered_list":
            for item in block.get("items", []):
                clean = re.sub(r"^[\s]*\d+\.\s+", "", item)
                doc.add_paragraph(clean, style="List Number")
        elif t == "table":
            rows = block.get("rows", [])
            if not rows:
                continue
            table = doc.add_table(rows=0, cols=len(rows[0]))
            table.style = "Table Grid"
            for r_idx, row in enumerate(rows):
                cells = table.add_row().cells
                for c_idx, cell_text in enumerate(row):
                    if c_idx >= len(cells):
                        break
                    cells[c_idx].text = cell_text
                    if r_idx == 0:
                        for paragraph in cells[c_idx].paragraphs:
                            for run in paragraph.runs:
                                run.bold = True
        else:
            doc.add_paragraph(f"[UNHANDLED BLOCK: {t}] {block}")


def load_markdown_module(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def _strip_module_metadata(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    seen_title = False
    metadata_patterns = re.compile(
        r"^\*\*(Token|Group|Required|Present in|To be authored|Sub-components|Note|Format|Duration|Attendees|Audience|Focus|Overview)\s*:?\s*\*\*"
    )
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append(line)
            continue
        if not seen_title and stripped.startswith("#"):
            out.append(line)
            seen_title = True
            continue
        if metadata_patterns.match(stripped):
            continue
        if stripped == "---":
            continue
        out.append(line)
    return "\n".join(out)


def _escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def add_toc_field(doc: Document) -> None:
    """Insert a Word auto-updating Table of Contents field."""
    instruction = doc.add_paragraph()
    instr_run = instruction.add_run(
        "Table of Contents — if entries are missing or show \"No table of contents entries found\", "
        "select the table below, right-click, and choose \"Update Field\" → \"Update entire table\"."
    )
    instr_run.italic = True
    instr_run.font.size = Pt(9)
    instr_run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)

    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = ' TOC \\o "1-3" \\h \\z \\u '
    fld_separate = OxmlElement("w:fldChar")
    fld_separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:r")
    ph_run = OxmlElement("w:t")
    ph_run.set(qn("xml:space"), "preserve")
    ph_run.text = "Right-click and choose \"Update Field\" to build the Table of Contents."
    placeholder.append(ph_run)
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    p = doc.add_paragraph()
    run = p.add_run()
    run._r.append(fld_begin)
    run._r.append(instr_text)
    run._r.append(fld_separate)
    run._r.append(placeholder)
    run._r.append(fld_end)

    doc.add_paragraph("")


def set_update_fields_on_open(doc: Document) -> None:
    """Set w:updateFields val="true" in settings.xml so Word refreshes fields on open."""
    settings = doc.settings.element
    existing = settings.find(qn("w:updateFields"))
    if existing is None:
        existing = OxmlElement("w:updateFields")
        settings.append(existing)
    existing.set(qn("w:val"), "true")


def _render_inline_markdown(text: str) -> str:
    """Very basic inline rendering: strip **markers** for clean text."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def _section_display_name(token: str, index: dict) -> str | None:
    for group in index.get("modules", {}).values():
        for mod in group.get("modules", []):
            if mod.get("token") == token:
                return mod.get("name") or token
    return None


def apply_customer_values(text: str, values: dict, index: dict | None = None) -> str:
    """Replace {{customer_*}} and {{proposal_*}} style tokens with values dict.

    For tokens not found in *values*, if *index* is provided and the token is a
    known ``section_*`` or ``module_*`` token, emit a readable cross-reference
    sentence instead of leaving the raw token in the document.
    """
    if not values:
        values = {}
    if index is None:
        index = {}

    name_by_token: dict[str, str] = {}
    if index:
        for group in index.get("modules", {}).values():
            for mod in group.get("modules", []):
                tok = mod.get("token", "")
                if tok:
                    name_by_token[tok] = mod.get("name", tok) or tok

    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        if key in values and values[key]:
            return str(values[key])
        if key in name_by_token:
            display = name_by_token[key]
            if key.startswith("section_"):
                kind = "section"
            elif key.startswith("module_"):
                kind = "module"
            else:
                kind = "item"
            return f"(See the {display} {kind} in this proposal for details.)"
        return match.group(0)

    return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", replacer, text)


def assemble_complete_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
) -> tuple[Document, list[str]]:
    """Build a complete docx by resolving each selected module's markdown."""
    doc = Document()
    warnings: list[str] = []

    ordered_tokens: list[str] = []
    for group_key in ("devicex_sdx", "stackx", "cross_cutting"):
        group = index.get("modules", {}).get(group_key, {})
        for mod in group.get("modules", []):
            tok = mod.get("token", "")
            if tok in selected_tokens:
                ordered_tokens.append(tok)

    # Ensure the cover page is assembled first so the proposal opens
    # with the cover / executive summary rather than a capability module.
    if 'section_cover_execsummary' in ordered_tokens:
        ordered_tokens.remove('section_cover_execsummary')
        ordered_tokens.insert(0, 'section_cover_execsummary')

    for token in ordered_tokens:
        mod_file = resolve_module_file(token, index)
        if mod_file is None:
            warnings.append(f"Module token '{token}': source file not found; token left unresolved.")
            doc.add_paragraph(f"[MODULE: {token} — source not found]")
            continue

        try:
            text = load_markdown_module(mod_file)
        except Exception as exc:
            warnings.append(f"Module token '{token}': error reading source: {exc}")
            doc.add_paragraph(f"[MODULE: {token} — read error: {exc}]")
            continue

        text = _strip_module_metadata(text)
        text = _render_inline_markdown(text)
        text = apply_customer_values(text, values)
        blocks = parse_markdown_blocks(text)
        build_docx_from_blocks(doc, blocks)
        doc.add_paragraph("")

    add_toc_field(doc)
    set_update_fields_on_open(doc)
    embed_logo(doc, logo_path)
    return doc, warnings


def assemble_template_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
) -> tuple[Document, list[str]]:
    """Build a token-based docx template."""
    doc = Document()
    warnings: list[str] = []

    title = doc.add_heading("DeviceX/SDX & StackX — Technical Proposal Template", level=0)
    subtitle = doc.add_paragraph()
    subtitle.add_run("VertoWave — Modular Proposal Template v0.1.0").italic = True
    doc.add_paragraph("")

    intro = doc.add_paragraph(
        "This is a token-based proposal template. Replace each {{customer_*}} and "
        "{{module_*}} token with the current bid's content before issuance. "
        "Pricing is excluded by design and attached separately."
    )
    intro.italic = True
    doc.add_paragraph("")

    add_toc_field(doc)
    embed_logo(doc, logo_path)

    doc.add_heading("Document Control", level=1)
    dc_blocks = parse_markdown_blocks(
        load_markdown_module(resolve_module_file("section_document_control", index))
    )
    build_docx_from_blocks(doc, dc_blocks)
    doc.add_paragraph("")

    for token in selected_tokens:
        mod_info: dict | None = None
        for group_key, group in index.get("modules", {}).items():
            for mod in group.get("modules", []):
                if mod.get("token") == token:
                    mod_info = mod
                    break
            if mod_info:
                break

        name = mod_info.get("name", token) if mod_info else token
        group_label = mod_info.get("group", "") if mod_info else ""

        doc.add_heading(f"Module: {name}", level=1)
        if group_label:
            doc.add_paragraph(f"Group: {group_label}").italic = True

        token_line = doc.add_paragraph()
        token_run = token_line.add_run(f"{{{token}}}")
        token_run.bold = True
        token_line.add_run("  <!-- replace with module content -->")

        doc.add_paragraph("")

    doc.add_heading("Module Selection Checklist", level=1)
    doc.add_paragraph("Confirm the modules included in this proposal against the current RFP/ITB:")
    for token in selected_tokens:
        mod_info: dict | None = None
        for group_key, group in index.get("modules", {}).items():
            for mod in group.get("modules", []):
                if mod.get("token") == token:
                    mod_info = mod
                    break
            if mod_info:
                break
        name = mod_info.get("name", token) if mod_info else token
        required = mod_info.get("required", False) if mod_info else False
        note = mod_info.get("notes", "") if mod_info else ""
        line = doc.add_paragraph(style="List Bullet")
        line.add_run(f"[{'REQUIRED' if required else 'OPTIONAL'}] {name}")
        if note:
            line.add_run(f" — {note}")

    return doc, warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Assemble a VertoWave DeviceX/SDX & StackX proposal docx from modular markdown."
    )
    p.add_argument("--values", required=True, help="Path to customer values JSON")
    p.add_argument("--modules", help="Comma-separated list of module tokens to include (default: all)")
    p.add_argument("--mode", choices=["complete", "template"], default="complete",
                   help="complete = fill tokens with module content; template = keep tokens as placeholders")
    p.add_argument("--out", required=True, help="Output .docx path")
    p.add_argument("--index", default=None, help="Path to module_index.json (default: alongside this script)")
    p.add_argument("--logo", default=None, help="Path to logo image (PNG/JPG) to embed in the cover page")
    return p.parse_args(argv)


def resolve_index_path(arg: str | None, script_dir: Path) -> Path:
    if arg:
        return Path(arg)
    return script_dir / "module_index.json"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    index_path = resolve_index_path(args.index, SCRIPT_DIR)
    global MODULE_INDEX
    MODULE_INDEX = index_path

    index = load_index()

    values_path = Path(args.values)
    if not values_path.exists():
        print(f"ERROR: values file not found: {values_path}", file=sys.stderr)
        return 2
    with values_path.open("r", encoding="utf-8") as f:
        try:
            values = json.load(f)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid values JSON: {exc}", file=sys.stderr)
            return 2

    if args.modules:
        selected_tokens = [t.strip() for t in args.modules.split(",") if t.strip()]
    else:
        selected_tokens = []
        for group_key, group in index.get("modules", {}).items():
            for mod in group.get("modules", []):
                selected_tokens.append(mod.get("token", ""))

    known_tokens: set[str] = set()
    for group in index.get("modules", {}).values():
        for mod in group.get("modules", []):
            known_tokens.add(mod.get("token", ""))

    unknown = [t for t in selected_tokens if t not in known_tokens]
    if unknown:
        print(f"WARNING: unknown module tokens (not in module_index.json): {', '.join(unknown)}", file=sys.stderr)

    for group in index.get("modules", {}).values():
        for mod in group.get("modules", []):
            tok = mod.get("token", "")
            if mod.get("required", False) and tok not in selected_tokens:
                print(f"NOTE: required module omitted: {tok} ({mod.get('name', '')})", file=sys.stderr)

    if args.mode == "complete":
        doc, warnings = assemble_complete_document(index, selected_tokens, values, logo_path=args.logo)
    else:
        doc, warnings = assemble_template_document(index, selected_tokens, values, logo_path=args.logo)

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    set_update_fields_on_open(doc)
    doc.save(out_path)
    print(f"OK: wrote {out_path}")
    if _logo_status():
        print(f"LOGO: {_logo_status()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
