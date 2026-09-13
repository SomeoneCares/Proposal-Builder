#!/usr/bin/env python3
"""
Assemble a VertoWave DeviceX/SDX & StackX technical proposal (.docx) from the
Markdown modules in modules/, the registry in module_index.json and a values JSON.

Modes:
  --mode complete   Module bodies are inserted and {{value}} tokens filled.
                    A draft (the default) keeps bid-team notes, figure
                    placeholders and "(for the bid team)" sections, highlighted
                    in yellow. --issue removes them and refuses to build while
                    any value is still unfilled.
  --mode template   Token-based template: one {{module_...}} placeholder per
                    module plus a module selection checklist.

Every build is checked before it is saved: no {{tokens}} (complete mode), no
HTML comment text and no banned prior-customer terms (module_index.json
"banned_terms") may reach the document. A failed check prints ERROR lines,
writes nothing and exits with status 3.

Markdown support is deliberately small: # / ## / ### headings, paragraphs,
- bullets (one nesting level), 1. numbered items, > quotes, pipe tables and
**bold**, *italic* and `code` inline. Two extras for the cover page: a line
starting with "#! " uses the Title style and a line containing only \\newpage
starts a new page. <!-- comments --> are always dropped.

Usage:
  python combine.py --values values.json --out proposal.docx
  python combine.py --values values.json --modules module_sdwan,section_ola \\
      --logo assets/vertowave_logo.png --issue --out proposal.docx
  python combine.py --values values.json --mode template --out template.docx
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError as exc:
    print("ERROR: python-docx is required. Install with: pip install python-docx", file=sys.stderr)
    raise SystemExit(2) from exc

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import build_base_template  # noqa: E402

DEFAULT_INDEX = SCRIPT_DIR / "module_index.json"
GROUP_ORDER = ("devicex_sdx", "stackx", "cross_cutting")
# Sections placed before the table of contents, in this order.
FRONT_MATTER = ("section_cover_execsummary", "section_document_control")
LOGO_MARKER = "[VERTO WAVE LOGO"
TO_CONFIRM = "[TO CONFIRM: {}]"
EXIT_CHECK_FAILED = 3

METADATA_RE = re.compile(
    r"^\*\*(Token|Group|Required|Present in|To be authored|Sub-components|Note|Notes|"
    r"Format|Duration|Attendees|Audience|Focus|Overview)\s*:?\s*\*\*"
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")
INLINE_RE = re.compile(r"\*\*(.+?)\*\*|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|`([^`]+)`")
SEPARATOR_CELL_RE = re.compile(r":?-{3,}:?")
TO_CONFIRM_RE = re.compile(r"\[TO CONFIRM: ([A-Za-z0-9_]+)\]")

NOTE_GREY = RGBColor(0x59, 0x59, 0x59)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def load_index(path: Path = DEFAULT_INDEX) -> dict:
    if not path.exists():
        print(f"ERROR: module_index.json not found at {path}", file=sys.stderr)
        raise SystemExit(2)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_modules(index: dict):
    for group_key in GROUP_ORDER:
        for mod in index.get("modules", {}).get(group_key, {}).get("modules", []):
            yield mod


def find_module(index: dict, token: str) -> dict | None:
    return next((mod for mod in iter_modules(index) if mod.get("token") == token), None)


def display_names(index: dict) -> dict[str, str]:
    return {mod["token"]: mod.get("name") or mod["token"] for mod in iter_modules(index)}


def resolve_module_file(token: str, index: dict, root: Path = SCRIPT_DIR) -> Path | None:
    mod = find_module(index, token)
    if mod is None or not mod.get("file"):
        return None
    candidate = root / mod["file"]
    return candidate if candidate.exists() else None


# ---------------------------------------------------------------------------
# Markdown -> blocks
# ---------------------------------------------------------------------------

def prepare_module_text(text: str, keep_title: bool = True) -> str:
    """Drop HTML comments, the module metadata header and horizontal rules."""
    text = HTML_COMMENT_RE.sub("", text)
    out: list[str] = []
    title_seen = False
    in_header = False
    for line in text.splitlines():
        stripped = line.strip()
        if not title_seen and stripped.startswith("# "):
            title_seen = True
            in_header = True
            if keep_title:
                out.append(line)
            continue
        if in_header:
            if stripped == "---":
                in_header = False
                continue
            if not stripped or METADATA_RE.match(stripped):
                continue
            in_header = False
        if stripped == "---":
            out.append("")
            continue
        out.append(line)
    return "\n".join(out)


def fill_tokens(text: str, values: dict, names: dict[str, str]) -> str:
    """Fill {{value}} tokens; module/section tokens become their display name.

    Values that are missing or blank become a visible [TO CONFIRM: key] marker.
    """
    def replace(match: re.Match) -> str:
        key = match.group(1)
        value = values.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
        if key in names:
            return names[key]
        return TO_CONFIRM.format(key)

    return TOKEN_RE.sub(replace, text)


def _starts_block(stripped: str) -> bool:
    return bool(
        re.match(r"^#{1,6}\s", stripped)
        or stripped.startswith("#! ")
        or stripped.startswith("|")
        or re.match(r"^[-*]\s+", stripped)
        or re.match(r"^\d+\.\s+", stripped)
        or stripped == "\\newpage"
    )


def parse_blocks(text: str) -> list[dict]:
    blocks: list[dict] = []
    lines = text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped == "\\newpage":
            blocks.append({"type": "pagebreak"})
            i += 1
            continue
        if stripped.startswith("#! "):
            blocks.append({"type": "title", "text": stripped[3:].strip()})
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = min(len(heading.group(1)), 3)
            blocks.append({"type": "heading", "level": level, "text": heading.group(2).strip()})
            i += 1
            continue
        if stripped.startswith("|"):
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            is_separator = [all(SEPARATOR_CELL_RE.fullmatch(c) or not c for c in row) for row in rows]
            header = len(rows) > 1 and is_separator[1]
            rows = [row for row, sep in zip(rows, is_separator) if not sep]
            if rows:
                blocks.append({"type": "table", "rows": rows, "header": header})
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items: list[tuple[int, str]] = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                raw = lines[i]
                indent = len(raw) - len(raw.lstrip())
                items.append((1 if indent >= 2 else 0, re.sub(r"^\s*[-*]\s+", "", raw).strip()))
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            numbered: list[str] = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                numbered.append(lines[i].strip())
                i += 1
            blocks.append({"type": "numbered", "items": numbered})
            continue
        para: list[str] = [re.sub(r"^>\s?", "", stripped)]
        i += 1
        while i < n and lines[i].strip() and not _starts_block(lines[i].strip()):
            para.append(re.sub(r"^>\s?", "", lines[i].strip()))
            i += 1
        blocks.append({"type": "paragraph", "text": " ".join(para)})
    return blocks


def is_note(raw: str) -> bool:
    """Bid-team notes are whole-paragraph *italic* or **[bracketed bold]** text."""
    s = raw.strip()
    if s.startswith("**[") and s.endswith("]**"):
        return True
    return s.startswith("*") and not s.startswith("**") and s.endswith("*") and not s.endswith("**")


def unwrap_note(raw: str) -> str:
    s = raw.strip()
    if s.startswith("**[") and s.endswith("]**"):
        return s[2:-2]
    if is_note(s):
        return s[1:-1]
    return s


def is_bid_team_heading(text: str) -> bool:
    return text.startswith("Figure —") or "(for the bid team)" in text.lower()


def plain(text: str) -> str:
    return INLINE_RE.sub(lambda m: next(g for g in m.groups() if g is not None), text)


# ---------------------------------------------------------------------------
# Blocks -> docx
# ---------------------------------------------------------------------------

def _style_note(run) -> None:
    run.italic = True
    run.font.color.rgb = NOTE_GREY
    run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def add_inline(paragraph, text: str, note: bool = False, bold: bool = False) -> None:
    def add(segment: str, seg_bold: bool, seg_italic: bool) -> None:
        if not segment:
            return
        run = paragraph.add_run(segment)
        if seg_bold:
            run.bold = True
        if seg_italic:
            run.italic = True
        if note:
            _style_note(run)

    pos = 0
    for match in INLINE_RE.finditer(text):
        add(text[pos:match.start()], bold, False)
        strong, emphasis, code = match.groups()
        if strong is not None:
            add(strong.replace("*", ""), True, False)
        elif emphasis is not None:
            add(emphasis, bold, True)
        else:
            add(code, bold, False)
        pos = match.end()
    add(text[pos:], bold, False)


class Renderer:
    """Writes parsed blocks into a document. Draft mode keeps bid-team notes."""

    def __init__(self, doc, draft: bool):
        self.doc = doc
        self.draft = draft

    def _paragraph(self, style: str | None = None):
        if style:
            try:
                return self.doc.add_paragraph(style=style)
            except KeyError:
                pass
        return self.doc.add_paragraph()

    def note(self, text: str, bold: bool = False) -> None:
        add_inline(self.doc.add_paragraph(), text, note=True, bold=bold)

    def render(self, blocks: list[dict]) -> None:
        skip_level: int | None = None
        note_level: int | None = None
        for block in blocks:
            kind = block["type"]
            if kind == "heading":
                level = block["level"]
                if skip_level is not None and level <= skip_level:
                    skip_level = None
                if note_level is not None and level <= note_level:
                    note_level = None
                if skip_level is not None:
                    continue
                if is_bid_team_heading(block["text"]):
                    if self.draft:
                        note_level = level
                        self.note(plain(block["text"]), bold=True)
                    else:
                        skip_level = level
                    continue
                self.doc.add_heading(plain(block["text"]), level=level)
                continue
            if skip_level is not None:
                continue
            in_note = note_level is not None

            if kind == "title":
                self.doc.add_heading(plain(block["text"]), level=0)
            elif kind == "pagebreak":
                self.doc.add_page_break()
            elif kind == "paragraph":
                raw = block["text"]
                if LOGO_MARKER in raw:
                    p = self.doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_inline(p, unwrap_note(raw), note=True)
                    continue
                note = in_note or is_note(raw)
                if note and not self.draft:
                    continue
                add_inline(self.doc.add_paragraph(), unwrap_note(raw) if is_note(raw) else raw, note=note)
            elif kind == "bullets":
                for level, text in block["items"]:
                    p = self._paragraph("List Bullet 2" if level else "List Bullet")
                    add_inline(p, text, note=in_note)
            elif kind == "numbered":
                for text in block["items"]:
                    p = self.doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.25)
                    add_inline(p, text, note=in_note)
            elif kind == "table":
                self._table(block["rows"], block["header"], in_note)

    def _table(self, rows: list[list[str]], header: bool, note: bool) -> None:
        table = self.doc.add_table(rows=0, cols=max(len(row) for row in rows))
        table.style = "Table Grid"
        for r_idx, row in enumerate(rows):
            cells = table.add_row().cells
            for c_idx, value in enumerate(row[: len(cells)]):
                add_inline(cells[c_idx].paragraphs[0], value, note=note, bold=header and r_idx == 0)
        self.doc.add_paragraph()


def add_toc(doc, draft: bool) -> None:
    """Insert a 'Table of Contents' title and a Word TOC field (headings 1-3)."""
    title = doc.add_paragraph()
    run = title.add_run("Table of Contents")
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    if draft:
        add_inline(
            doc.add_paragraph(),
            "[If the table below is empty, right-click it in Word and choose Update Field → Update entire table.]",
            note=True,
        )
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = ' TOC \\o "1-3" \\h \\z \\u '
    fld_separate = OxmlElement("w:fldChar")
    fld_separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.set(qn("xml:space"), "preserve")
    placeholder.text = "Right-click and choose \"Update Field\" to build the Table of Contents."
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run = doc.add_paragraph().add_run()
    for element in (fld_begin, instr_text, fld_separate, placeholder, fld_end):
        run._r.append(element)


def set_update_fields_on_open(doc) -> None:
    """Set w:updateFields so Word refreshes the TOC and page fields on open."""
    settings = doc.settings.element
    existing = settings.find(qn("w:updateFields"))
    if existing is None:
        existing = OxmlElement("w:updateFields")
        settings.append(existing)
    existing.set(qn("w:val"), "true")


def _delete_paragraph(paragraph) -> None:
    element = paragraph._element
    element.getparent().remove(element)


def embed_logo(doc, logo_path: str | None, draft: bool) -> str:
    """Put the logo where the [VERTO WAVE LOGO ...] placeholder is.

    Without a placeholder the logo goes at the start of the document. Without a
    usable logo, an issue copy loses the placeholder line; a draft keeps it.
    """
    target = next((p for p in doc.paragraphs if LOGO_MARKER in p.text), None)
    logo = Path(logo_path) if logo_path else None
    if logo is None or not logo.is_file():
        if target is not None and not draft:
            _delete_paragraph(target)
        return "no logo given" if logo is None else f"logo not found: {logo_path}"
    if target is None:
        first = doc.paragraphs[0] if doc.paragraphs else None
        target = first.insert_paragraph_before() if first is not None else doc.add_paragraph()
    else:
        target.clear()
    target.add_run().add_picture(str(logo), width=Inches(3.0))
    target.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return f"embedded {logo.name}"


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def document_text(doc) -> str:
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    for section in doc.sections:
        for part in (section.header, section.footer, section.first_page_header, section.first_page_footer):
            parts.extend(p.text for p in part.paragraphs)
    props = doc.core_properties
    parts.extend([props.title or "", props.subject or "", props.keywords or "", props.comments or ""])
    return "\n".join(parts)


def check_document(doc, values: dict, banned_terms: list[str], mode: str, issue: bool) -> tuple[list[str], list[str]]:
    """Return (problems, keys still to confirm). Any problem blocks the build."""
    text = document_text(doc)
    problems: list[str] = []
    if mode == "complete" and ("{{" in text or "}}" in text):
        leftover = sorted(set(re.findall(r"\{\{[^}]*\}\}", text)))
        problems.append(f"unresolved token text in the document: {', '.join(leftover) or '{{ or }}'}")
    if "<!--" in text or "-->" in text:
        problems.append("HTML comment text reached the document")
    value_text = " ".join(str(v) for v in values.values()).lower()
    for term in banned_terms:
        if term.lower() in value_text:
            continue  # the current customer may legitimately be a past customer
        match = re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.I)
        if match:
            context = text[max(0, match.start() - 40): match.end() + 40].replace("\n", " ")
            problems.append(f"banned term '{term}' in the document: ...{context}...")
    unconfirmed = sorted(set(TO_CONFIRM_RE.findall(text)))
    if issue and unconfirmed:
        problems.append("an issue copy cannot contain unfilled values: " + ", ".join(unconfirmed))
    return problems, unconfirmed


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def _new_document(values: dict, template: bool):
    prepared_by = str(values.get("prepared_by") or "VertoWave").strip()
    if template:
        return build_base_template.new_document(
            title="DeviceX/SDX & StackX — Technical Proposal Template",
            footer_label="VertoWave — DeviceX/SDX & StackX Proposal Template",
        )
    engagement = str(values.get("engagement_name") or "").strip()
    customer = str(values.get("customer_short") or "").strip()
    return build_base_template.new_document(
        title=f"{engagement} — Technical Proposal" if engagement else "Technical Proposal",
        footer_label=f"{prepared_by} — {customer} Technical Proposal" if customer else f"{prepared_by} — Technical Proposal",
        author=prepared_by,
    )


def ordered_tokens(index: dict, selected: list[str]) -> tuple[list[str], list[str]]:
    ordered = [mod["token"] for mod in iter_modules(index) if mod["token"] in selected]
    front = [t for t in FRONT_MATTER if t in ordered]
    return front, [t for t in ordered if t not in front]


def assemble_complete_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
    issue: bool = False,
    root: Path = SCRIPT_DIR,
):
    doc = _new_document(values, template=False)
    renderer = Renderer(doc, draft=not issue)
    names = display_names(index)
    warnings: list[str] = []

    def add_module(token: str) -> None:
        path = resolve_module_file(token, index, root)
        if path is None:
            warnings.append(f"module '{token}': source file not found; skipped.")
            renderer.note(f"[Module {token}: source file not found]")
            return
        mod = find_module(index, token) or {}
        text = prepare_module_text(path.read_text(encoding="utf-8"), keep_title=mod.get("show_title", True))
        renderer.render(parse_blocks(fill_tokens(text, values, names)))

    front, rest = ordered_tokens(index, selected_tokens)
    for i, token in enumerate(front):
        if i:
            doc.add_page_break()
        add_module(token)
    if front:
        doc.add_page_break()
    add_toc(doc, draft=not issue)
    for token in rest:
        doc.add_page_break()
        add_module(token)

    warnings.append("logo: " + embed_logo(doc, logo_path, draft=not issue))
    set_update_fields_on_open(doc)
    return doc, warnings


def assemble_template_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
    root: Path = SCRIPT_DIR,
):
    doc = _new_document(values, template=True)
    renderer = Renderer(doc, draft=True)
    warnings: list[str] = []

    doc.add_heading("DeviceX/SDX & StackX — Technical Proposal Template", level=0)
    run = doc.add_paragraph().add_run("VertoWave — Modular Proposal Template")
    run.italic = True
    run = doc.add_paragraph().add_run(
        "Replace each {{…}} token with the current bid's content before issue. "
        "Pricing is excluded by design and attached separately."
    )
    run.italic = True
    add_toc(doc, draft=True)

    doc_control = resolve_module_file("section_document_control", index, root)
    if doc_control is not None:
        renderer.render(parse_blocks(prepare_module_text(doc_control.read_text(encoding="utf-8"))))

    chosen = [mod for mod in iter_modules(index) if mod["token"] in selected_tokens]
    for mod in chosen:
        doc.add_heading(f"Module: {mod.get('name', mod['token'])}", level=1)
        group = find_group_label(index, mod["token"])
        if group:
            doc.add_paragraph().add_run(f"Group: {group}").italic = True
        token_line = doc.add_paragraph()
        token_line.add_run("{{" + mod["token"] + "}}").bold = True
        token_line.add_run("  — replace with the module content")

    doc.add_heading("Module Selection Checklist", level=1)
    doc.add_paragraph("Confirm the modules included in this proposal against the current RFP/ITB:")
    for mod in chosen:
        line = doc.add_paragraph(style="List Bullet")
        line.add_run(f"[{'REQUIRED' if mod.get('required') else 'OPTIONAL'}] {mod.get('name', mod['token'])}")
        if mod.get("notes"):
            line.add_run(f" — {mod['notes']}")

    if logo_path:
        warnings.append("logo: " + embed_logo(doc, logo_path, draft=True))
    set_update_fields_on_open(doc)
    return doc, warnings


def find_group_label(index: dict, token: str) -> str:
    for group in index.get("modules", {}).values():
        if any(mod.get("token") == token for mod in group.get("modules", [])):
            return group.get("group", "")
    return ""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Assemble a VertoWave DeviceX/SDX & StackX proposal docx from modular Markdown."
    )
    p.add_argument("--values", required=True, help="Path to the proposal values JSON")
    p.add_argument("--modules", help="Comma-separated module tokens to include (default: all)")
    p.add_argument("--mode", choices=["complete", "template"], default="complete")
    p.add_argument("--issue", action="store_true",
                   help="Issue copy: drop bid-team notes and refuse to build with unfilled values")
    p.add_argument("--out", required=True, help="Output .docx path")
    p.add_argument("--index", default=None, help="Path to module_index.json (default: next to this script)")
    p.add_argument("--logo", default=None, help="Logo image (PNG/JPG) for the cover page")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    index_path = Path(args.index) if args.index else DEFAULT_INDEX
    index = load_index(index_path)
    root = index_path.resolve().parent

    values_path = Path(args.values)
    if not values_path.exists():
        print(f"ERROR: values file not found: {values_path}", file=sys.stderr)
        return 2
    try:
        values = json.loads(values_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid values JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(values, dict):
        print("ERROR: the values JSON must be an object of key/value pairs", file=sys.stderr)
        return 2

    known = [mod["token"] for mod in iter_modules(index)]
    if args.modules:
        selected = [t.strip() for t in args.modules.split(",") if t.strip()]
    else:
        selected = list(known)

    unknown = [t for t in selected if t not in known]
    if unknown:
        print(f"WARNING: unknown module tokens (not in module_index.json): {', '.join(unknown)}", file=sys.stderr)
    for mod in iter_modules(index):
        if mod.get("required") and mod["token"] not in selected:
            print(f"NOTE: required module omitted: {mod['token']} ({mod.get('name', '')})", file=sys.stderr)
        if mod.get("placeholder") and mod["token"] in selected:
            print(f"WARNING: {mod.get('name', mod['token'])} is a placeholder module — not for live bids.",
                  file=sys.stderr)

    if args.mode == "complete":
        doc, warnings = assemble_complete_document(index, selected, values, args.logo, args.issue, root)
    else:
        doc, warnings = assemble_template_document(index, selected, values, args.logo, root)

    problems, unconfirmed = check_document(
        doc, values, index.get("banned_terms", []), args.mode, args.issue and args.mode == "complete"
    )
    for warning in warnings:
        stream = sys.stdout if warning.startswith("logo:") else sys.stderr
        print(("LOGO: " + warning[5:].strip()) if warning.startswith("logo:") else f"WARNING: {warning}", file=stream)
    if unconfirmed and args.mode == "complete":
        print("TO CONFIRM: " + ", ".join(unconfirmed), file=sys.stderr)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print("ERROR: build refused — nothing was written.", file=sys.stderr)
        return EXIT_CHECK_FAILED

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
