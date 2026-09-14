#!/usr/bin/env python3
"""
Assemble a Verto Wave DeviceX/SDX & StackX technical proposal (.docx) from the
Markdown modules in modules/, the registry in module_index.json and a values JSON.

Modes:
  --mode complete   Module bodies are inserted and {{value}} tokens filled.
                    A draft (the default) keeps bid-team notes and figure
                    placeholders, highlighted. --issue removes them and refuses
                    to build while any value is unfilled.
  --mode template   Token-based template: one {{module_...}} placeholder per
                    module plus a module selection checklist.

Offering (--offering, default "licenses,services"): any of licenses, services,
managed_services. Together with the selected modules it decides what appears.

Conditional content in module Markdown:
  <!-- if EXPR -->  ...  <!-- endif -->   a block
  some line <!-- if EXPR -->              a single line (bullet, table row, paragraph)
EXPR uses module tokens, the offering flags, "devicex" / "stackx" (any module of
that family selected), and / or / not and parentheses. A module whose
module_index.json "requires" expression is false is left out.

Directives (a line on its own):
  [[figure: slug | Caption]]   image from the library or assets/figures/<slug>.png|jpg;
                               a placeholder box in a draft, omitted from an issue copy
  [[scope_table]]              the selected modules with their one-line summaries
  [[compliance_matrix]]        rows from the values key "compliance_matrix"
  [[glossary]]                 glossary.json terms that appear in the document

Every build is checked before it is saved: no {{tokens}} (complete mode), no
HTML comment text, no banned prior-customer terms and no third-party product
names (module_index.json "banned_terms" / "third_party_terms"). A failed check
prints ERROR lines, writes nothing and exits with status 3.

Markdown support is deliberately small: # / ## / ### headings, paragraphs,
- bullets (two levels), 1. numbered items, > quotes, pipe tables and
**bold**, *italic* and `code` inline. "#! text" uses the Title style and
"\\newpage" starts a new page. <!-- comments --> are never rendered.

Module overrides saved from the portal's Module Library live in
--library (default $PROPOSAL_LIBRARY_DIR): <library>/modules/<token>/current.md
and <library>/figures/<slug>.<ext> take precedence over the repo copies.

Usage:
  python combine.py --values values.json --out proposal.docx
  python combine.py --values values.json --offering licenses,services,managed_services \\
      --modules module_sdwan,section_ola --logo assets/vertowave_logo.png --issue --out p.docx
  python combine.py --values values.json --mode template --out template.docx
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_TAB_ALIGNMENT, WD_TAB_LEADER
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Mm, Pt, RGBColor
except ImportError as exc:
    print("ERROR: python-docx is required. Install with: pip install python-docx", file=sys.stderr)
    raise SystemExit(2) from exc

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import build_base_template  # noqa: E402

DEFAULT_INDEX = SCRIPT_DIR / "module_index.json"
GLOSSARY_FILE = "glossary.json"
GROUP_ORDER = ("devicex_sdx", "stackx", "optional_sections", "cross_cutting")
FAMILY_FLAGS = {"devicex_sdx": "devicex", "stackx": "stackx"}
OFFERINGS = ("licenses", "services", "managed_services", "premier_support")
DEFAULT_OFFERING = ("licenses", "services")
# Sections placed before the table of contents, in this order.
FRONT_MATTER = ("section_cover_execsummary", "section_document_control")
LOGO_MARKER = "[VERTO WAVE LOGO"
TO_CONFIRM = "[TO CONFIRM: {}]"
EXIT_CHECK_FAILED = 3
FIGURE_EXTENSIONS = (".png", ".jpg", ".jpeg")

METADATA_RE = re.compile(
    r"^\*\*(Token|Group|Required|Present in|To be authored|Sub-components|Note|Notes|"
    r"Format|Duration|Attendees|Audience|Focus|Overview)\s*:?\s*\*\*"
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")
INLINE_RE = re.compile(r"\*\*(.+?)\*\*|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])|`([^`]+)`")
SEPARATOR_CELL_RE = re.compile(r":?-{3,}:?")
TO_CONFIRM_RE = re.compile(r"\[TO CONFIRM: ([A-Za-z0-9_]+)\]")
DIRECTIVE_RE = re.compile(r"^\[\[\s*([a-z_]+)\s*(?::\s*(.*?))?\s*\]\]$")
COND_BLOCK_START_RE = re.compile(r"^\s*<!--\s*if\s+(.+?)\s*-->\s*$")
COND_BLOCK_END_RE = re.compile(r"^\s*<!--\s*endif\s*-->\s*$")
# A line condition may also sit just before a table row's closing pipe: "| a | b <!-- if x --> |".
COND_LINE_RE = re.compile(r"^(.*\S)\s*<!--\s*if\s+(.+?)\s*-->\s*(\|?)\s*$")

NOTE_GREY = RGBColor(0x59, 0x59, 0x59)
NAVY = RGBColor(0x1F, 0x38, 0x64)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEADER_FILL = "1F3864"
BAND_FILL = "F2F5F9"
BORDER_COLOR = "BFBFBF"
PLACEHOLDER_FILL = "EDEDED"
TEXT_WIDTH_MM = 160  # A4 minus 25 mm margins, set in build_base_template
HEADING_SEPARATOR = " "  # en space between a section number and its title

# Table of contents: entries are written at build time with a placeholder page
# number, which fill_toc_page_numbers() replaces after a LibreOffice render.
TOC_PLACEHOLDER = "000"
TOC_LINE_RE = re.compile(r"(?:\.\s*){3,}000$|\s000$")
TOC_TAB_POSITION = Mm(TEXT_WIDTH_MM)


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
    """Every module in registry group order."""
    for group_key in GROUP_ORDER:
        for mod in index.get("modules", {}).get(group_key, {}).get("modules", []):
            yield mod


def module_group(index: dict, token: str) -> str:
    for group_key, group in index.get("modules", {}).items():
        if any(mod.get("token") == token for mod in group.get("modules", [])):
            return group_key
    return ""


def find_module(index: dict, token: str) -> dict | None:
    return next((mod for mod in iter_modules(index) if mod.get("token") == token), None)


def display_names(index: dict) -> dict[str, str]:
    return {mod["token"]: mod.get("name") or mod["token"] for mod in iter_modules(index)}


def document_order(index: dict) -> list[str]:
    """Tokens in document order: module_index "document_order", then anything unlisted."""
    listed = [t for t in index.get("document_order", []) if find_module(index, t)]
    return listed + [mod["token"] for mod in iter_modules(index) if mod["token"] not in listed]


def resolve_module_file(token: str, index: dict, root: Path = SCRIPT_DIR, library: Path | None = None) -> Path | None:
    if library is not None:
        override = Path(library) / "modules" / token / "current.md"
        if override.is_file():
            return override
    mod = find_module(index, token)
    if mod is None or not mod.get("file"):
        return None
    candidate = root / mod["file"]
    return candidate if candidate.exists() else None


def resolve_figure(slug: str, root: Path = SCRIPT_DIR, library: Path | None = None) -> Path | None:
    for folder in ([Path(library) / "figures"] if library else []) + [root / "assets" / "figures"]:
        for ext in FIGURE_EXTENSIONS:
            candidate = folder / f"{slug}{ext}"
            if candidate.is_file():
                return candidate
    return None


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------

def parse_condition(expr: str):
    """Parse 'a or (b and not c)' into a small tuple tree. Raises ValueError."""
    tokens = re.findall(r"\(|\)|[A-Za-z_][A-Za-z0-9_]*", expr)
    if "".join(tokens) != re.sub(r"\s+", "", expr):
        raise ValueError(f"invalid characters in condition: {expr!r}")
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        if pos >= len(tokens):
            raise ValueError(f"incomplete condition: {expr!r}")
        pos += 1
        return tokens[pos - 1]

    def parse_or():
        node = parse_and()
        while peek() == "or":
            take()
            node = ("or", node, parse_and())
        return node

    def parse_and():
        node = parse_not()
        while peek() == "and":
            take()
            node = ("and", node, parse_not())
        return node

    def parse_not():
        if peek() == "not":
            take()
            return ("not", parse_not())
        if peek() == "(":
            take()
            node = parse_or()
            if take() != ")":
                raise ValueError(f"missing ')' in condition: {expr!r}")
            return node
        name = take() if peek() not in (None, ")", "and", "or") else None
        if name is None:
            raise ValueError(f"incomplete condition: {expr!r}")
        return ("name", name)

    tree = parse_or()
    if pos != len(tokens):
        raise ValueError(f"unexpected {tokens[pos]!r} in condition: {expr!r}")
    return tree


def evaluate_condition(tree, context: set[str]) -> bool:
    kind = tree[0]
    if kind == "name":
        return tree[1] in context
    if kind == "not":
        return not evaluate_condition(tree[1], context)
    if kind == "and":
        return evaluate_condition(tree[1], context) and evaluate_condition(tree[2], context)
    return evaluate_condition(tree[1], context) or evaluate_condition(tree[2], context)


def condition_names(tree) -> set[str]:
    if tree[0] == "name":
        return {tree[1]}
    return set().union(*(condition_names(child) for child in tree[1:]))


def known_condition_names(index: dict) -> set[str]:
    return {mod["token"] for mod in iter_modules(index)} | set(OFFERINGS) | set(FAMILY_FLAGS.values())


def conditions_in(text: str) -> list[str]:
    """Every condition expression used in a module's Markdown."""
    found = []
    for line in text.splitlines():
        block = COND_BLOCK_START_RE.match(line)
        inline = COND_LINE_RE.match(line)
        if block:
            found.append(block.group(1))
        elif inline:
            found.append(inline.group(2))
    return found


def apply_conditions(text: str, context: set[str]) -> str:
    out: list[str] = []
    stack: list[bool] = []
    for line in text.splitlines():
        start = COND_BLOCK_START_RE.match(line)
        if start:
            stack.append(evaluate_condition(parse_condition(start.group(1)), context))
            continue
        if COND_BLOCK_END_RE.match(line):
            if not stack:
                raise ValueError("<!-- endif --> without a matching <!-- if -->")
            stack.pop()
            continue
        if not all(stack):
            continue
        inline = COND_LINE_RE.match(line)
        if inline and not line.lstrip().startswith("<!--"):
            if evaluate_condition(parse_condition(inline.group(2)), context):
                out.append(inline.group(1) + (" |" if inline.group(3) else ""))
            continue
        out.append(line)
    if stack:
        raise ValueError("<!-- if --> without a matching <!-- endif -->")
    return "\n".join(out)


def build_context(index: dict, selected: list[str], offering: list[str]) -> set[str]:
    context = set(selected) | set(offering)
    for group_key, flag in FAMILY_FLAGS.items():
        if any(module_group(index, t) == group_key for t in selected):
            context.add(flag)
    return context


def module_applies(mod: dict, context: set[str]) -> bool:
    requires = mod.get("requires")
    return not requires or evaluate_condition(parse_condition(requires), context)


# ---------------------------------------------------------------------------
# Markdown -> blocks
# ---------------------------------------------------------------------------

def prepare_module_text(text: str, keep_title: bool = True, context: set[str] | None = None) -> str:
    """Apply conditions, then drop HTML comments, the metadata header and horizontal rules."""
    if context is not None:
        text = apply_conditions(text, context)
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
        if isinstance(value, str) and value.strip():
            return value.strip()
        if value is not None and not isinstance(value, (str, list, dict)) and str(value).strip():
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
        or DIRECTIVE_RE.match(stripped)
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
        directive = DIRECTIVE_RE.match(stripped)
        if directive:
            blocks.append({"type": "directive", "name": directive.group(1), "arg": directive.group(2) or ""})
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
# docx helpers
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


def _shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def _repeat_as_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    element = OxmlElement("w:tblHeader")
    element.set(qn("w:val"), "true")
    tr_pr.append(element)


def _set_borders(table, color: str = BORDER_COLOR) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)
        borders.append(element)
    tbl_pr.append(borders)


def _column_widths(rows: list[list[str]], cols: int) -> list[float]:
    weights = []
    for c in range(cols):
        longest = max((len(plain(row[c])) for row in rows if c < len(row)), default=4)
        weights.append(min(max(longest, 4), 60) ** 0.8)
    total = sum(weights)
    return [TEXT_WIDTH_MM * w / total for w in weights]


def build_table(doc, rows: list[list[str]], header: bool, note: bool = False):
    """A styled table: navy header row repeated on each page, banded rows, light borders."""
    cols = max(len(row) for row in rows)
    table = doc.add_table(rows=0, cols=cols)
    table.style = "Table Grid"
    table.autofit = False
    _set_borders(table)
    widths = _column_widths(rows, cols)
    for r_idx, row in enumerate(rows):
        table_row = table.add_row()
        is_header = header and r_idx == 0
        if is_header:
            _repeat_as_header(table_row)
        for c_idx, cell in enumerate(table_row.cells):
            cell.width = Mm(widths[c_idx])
            value = row[c_idx] if c_idx < len(row) else ""
            paragraph = cell.paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(0)
            add_inline(paragraph, value, note=note, bold=is_header)
            for run in paragraph.runs:
                run.font.size = Pt(10)
                if is_header and not note:
                    run.font.color.rgb = WHITE
            if not note:
                if is_header:
                    _shade(cell, HEADER_FILL)
                elif (r_idx - (1 if header else 0)) % 2 == 1:
                    _shade(cell, BAND_FILL)
    return table


def _delete_paragraph(paragraph) -> None:
    element = paragraph._element
    element.getparent().remove(element)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

class Renderer:
    """Writes parsed blocks into a document.

    Draft mode keeps bid-team notes and figure placeholders. Section numbering
    starts once number_headings is switched on (after the table of contents).
    """

    def __init__(self, doc, draft: bool, context: set[str] | None = None, index: dict | None = None,
                 values: dict | None = None, root: Path = SCRIPT_DIR, library: Path | None = None):
        self.doc = doc
        self.draft = draft
        self.context = context or set()
        self.index = index or {}
        self.values = values or {}
        self.root = root
        self.library = library
        self.number_headings = False
        # Set before a module that must start on a new page; applied to the module's first paragraph as
        # "page break before", which never leaves a blank page the way a separate break paragraph can.
        self.break_before = False
        self.appendix_letter: str | None = None
        self.counters = [0, 0, 0]
        self.appendix_count = 0
        self.figure_count = 0
        self.deferred: list[tuple[str, object]] = []
        self.problems: list[str] = []

    # -- structure -----------------------------------------------------------
    def start_module(self, appendix: bool) -> None:
        if appendix:
            self.appendix_count += 1
            self.appendix_letter = chr(ord("A") + self.appendix_count - 1)
        else:
            self.appendix_letter = None
        if self.appendix_letter:
            self.counters[1:] = [0, 0]

    def _number(self, level: int) -> str:
        if not self.number_headings:
            return ""
        if self.appendix_letter:
            if level == 1:
                return f"Appendix {self.appendix_letter}:"
            self.counters[level - 1] += 1
            for deeper in range(level, 3):
                self.counters[deeper] = 0
            return ".".join([self.appendix_letter] + [str(c) for c in self.counters[1:level]])
        self.counters[level - 1] += 1
        for deeper in range(level, 3):
            self.counters[deeper] = 0
        return ".".join(str(c) for c in self.counters[:level])

    def _mark(self, paragraph):
        if self.break_before:
            paragraph.paragraph_format.page_break_before = True
            self.break_before = False
        return paragraph

    def _paragraph(self, style: str | None = None):
        if style:
            try:
                return self._mark(self.doc.add_paragraph(style=style))
            except KeyError:
                pass
        return self._mark(self.doc.add_paragraph())

    def note(self, text: str, bold: bool = False) -> None:
        add_inline(self._paragraph(), text, note=True, bold=bold)

    # -- blocks --------------------------------------------------------------
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
                number = self._number(level)
                title = plain(block["text"])
                self._mark(self.doc.add_heading(f"{number}{HEADING_SEPARATOR}{title}" if number else title,
                                                level=level))
                continue
            if kind == "pagebreak":
                # Page breaks survive even inside a removed bid-team section.
                self.doc.add_page_break()
                continue
            if skip_level is not None:
                continue
            in_note = note_level is not None

            if kind == "title":
                self._mark(self.doc.add_heading(plain(block["text"]), level=0))
            elif kind == "directive":
                self._directive(block["name"], block["arg"], in_note)
            elif kind == "paragraph":
                raw = block["text"]
                if LOGO_MARKER in raw:
                    p = self._paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    add_inline(p, unwrap_note(raw), note=True)
                    continue
                note = in_note or is_note(raw)
                if note and not self.draft:
                    continue
                add_inline(self._paragraph(), unwrap_note(raw) if is_note(raw) else raw, note=note)
            elif kind == "bullets":
                for level, text in block["items"]:
                    p = self._paragraph("List Bullet 2" if level else "List Bullet")
                    add_inline(p, text, note=in_note)
            elif kind == "numbered":
                for text in block["items"]:
                    p = self._paragraph()
                    p.paragraph_format.left_indent = Inches(0.25)
                    add_inline(p, text, note=in_note)
            elif kind == "table":
                build_table(self.doc, block["rows"], block["header"], note=in_note)
                self.doc.add_paragraph()

    # -- directives ----------------------------------------------------------
    def _directive(self, name: str, arg: str, in_note: bool) -> None:
        if name == "figure":
            self._figure(arg)
        elif name == "scope_table":
            self._scope_table()
        elif name == "compliance_matrix":
            self._compliance_matrix()
        elif name == "glossary":
            anchor = self.doc.add_paragraph()
            self.deferred.append(("glossary", anchor))
        else:
            self.problems.append(f"unknown directive [[{name}]]")

    def _figure(self, arg: str) -> None:
        slug, _, caption = (part.strip() for part in arg.partition("|"))
        image = resolve_figure(slug, self.root, self.library)
        if image is None and not self.draft:
            return
        self.figure_count += 1
        label = f"Figure {self.figure_count}: {caption or slug}"
        if image is not None:
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(str(image), width=Mm(TEXT_WIDTH_MM - 10))
        else:
            box = self.doc.add_table(rows=1, cols=1)
            box.autofit = False
            _set_borders(box, "A6A6A6")
            cell = box.rows[0].cells[0]
            cell.width = Mm(TEXT_WIDTH_MM)
            _shade(cell, PLACEHOLDER_FILL)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_inline(p, f"[Figure placeholder — {caption or slug}. Upload the image as '{slug}' "
                          "in the Module Library to place it here.]", note=True)
        caption_p = self.doc.add_paragraph()
        caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = caption_p.add_run(label)
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = NAVY

    def _scope_table(self) -> None:
        rows = [["Area", "Module", "What it delivers"]]
        areas = {"devicex_sdx": "DeviceX/SDX", "stackx": "StackX"}
        for mod in iter_modules(self.index):
            group = module_group(self.index, mod["token"])
            if group in areas and mod["token"] in self.context:
                rows.append([areas[group], mod.get("name", mod["token"]), mod.get("summary", "")])
        services = [
            ("services", "Professional services", "Architecture, design, implementation and roll-out of the selected modules."),
            ("managed_services", "Managed services", "Operation of the implemented solution under the agreed Operations Level Agreement."),
        ]
        for flag, name, summary in services:
            if flag in self.context:
                rows.append(["Services", name, summary])
        if len(rows) > 1:
            build_table(self.doc, rows, header=True)
            self.doc.add_paragraph()

    def _compliance_matrix(self) -> None:
        entries = self.values.get("compliance_matrix") or []
        if not entries:
            if self.draft:
                self.note("[Upload the RFP requirements in the builder's Compliance matrix step to fill this table.]")
            else:
                self.problems.append("the compliance matrix is selected but has no requirement rows")
            return
        rows = [["Ref.", "Requirement", "Code", "Verto Wave response", "Section"]]
        for entry in entries:
            rows.append([str(entry.get(k, "")).strip() for k in ("ref", "requirement", "code", "response", "section")])
        build_table(self.doc, rows, header=True)
        self.doc.add_paragraph()

    def fill_deferred(self, glossary: dict[str, str]) -> None:
        for kind, anchor in self.deferred:
            if kind != "glossary":
                continue
            _delete_paragraph_text = anchor  # keep a reference while the text is scanned
            text = document_text(self.doc)
            used = sorted(
                (term for term in glossary
                 if re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text)),
                key=str.lower,
            )
            if used:
                table = build_table(self.doc, [["Term", "Meaning"]] + [[t, glossary[t]] for t in used], header=True)
                anchor._p.addnext(table._tbl)
            _delete_paragraph(_delete_paragraph_text)
        self.deferred.clear()


# ---------------------------------------------------------------------------
# Table of contents
# ---------------------------------------------------------------------------

def add_toc(doc, draft: bool, page_break_before: bool = False):
    """Add the 'Table of Contents' title; return an anchor paragraph for write_toc_field()."""
    title = doc.add_paragraph()
    title.paragraph_format.page_break_before = page_break_before
    run = title.add_run("Table of Contents")
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = NAVY
    if draft:
        add_inline(
            doc.add_paragraph(),
            "[Page numbers are filled in at build time; Word refreshes the table when the file is opened.]",
            note=True,
        )
    return doc.add_paragraph()


def collect_headings(doc, anchor, max_level: int = 3) -> list[tuple[int, str, bool]]:
    """(level, text, comes after the TOC) for every Heading 1..max_level paragraph, in order."""
    entries = []
    after = False
    for p in doc.paragraphs:
        if p._p is anchor._p:
            after = True
            continue
        match = re.fullmatch(r"Heading ([1-3])", p.style.name if p.style is not None else "")
        if match and int(match.group(1)) <= max_level and p.text.strip():
            entries.append((int(match.group(1)), p.text.strip(), after))
    return entries


def _field_char(run, kind: str) -> None:
    element = OxmlElement("w:fldChar")
    element.set(qn("w:fldCharType"), kind)
    run._r.append(element)


def _toc_instruction(run, levels: int) -> None:
    element = OxmlElement("w:instrText")
    element.set(qn("xml:space"), "preserve")
    element.text = f' TOC \\o "1-{levels}" \\h \\z \\u '
    run._r.append(element)


def write_toc_field(doc, anchor, entries: list[tuple[int, str, bool]], levels: int = 2) -> dict:
    """Replace the anchor with a Word TOC field whose result lists the entries.

    Each entry gets a placeholder page number; the returned runs let
    fill_toc_page_numbers() set the real ones. Without entries the field shows
    Word's usual "Update Field" prompt.
    """
    runs = []
    if not entries:
        p = anchor.insert_paragraph_before()
        start = p.add_run()
        _field_char(start, "begin")
        _toc_instruction(start, levels)
        _field_char(start, "separate")
        p.add_run('Right-click and choose "Update Field" to build the Table of Contents.')
        _field_char(p.add_run(), "end")
    for i, (level, text, _after) in enumerate(entries):
        p = anchor.insert_paragraph_before()
        fmt = p.paragraph_format
        fmt.left_indent = Inches(0.25 * (level - 1))
        fmt.space_after = Pt(2)
        fmt.tab_stops.add_tab_stop(TOC_TAB_POSITION, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        if i == 0:
            start = p.add_run()
            _field_char(start, "begin")
            _toc_instruction(start, levels)
            _field_char(start, "separate")
        p.add_run(text).bold = True if level == 1 else None
        p.add_run("\t")
        runs.append(p.add_run(TOC_PLACEHOLDER))
        if i == len(entries) - 1:
            _field_char(p.add_run(), "end")
    _delete_paragraph(anchor)
    return {"entries": entries, "runs": runs}


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def find_heading_pages(entries: list[tuple[int, str, bool]], pages: list[str]) -> list[int | None]:
    """Page number (1-based) of each heading in the rendered text, searched in document order."""
    page_lines = [[_normalise(line) for line in page.splitlines()] for page in pages]
    toc_pages = [i for i, lines in enumerate(page_lines) if any(TOC_LINE_RE.search(l) for l in lines)]
    toc_end = max(toc_pages) if toc_pages else -1
    numbers: list[int | None] = []
    cursor = 0
    for _level, text, after_toc in entries:
        if after_toc:
            cursor = max(cursor, toc_end + 1)
        target = _normalise(text)
        found = None
        for i in range(cursor, len(page_lines)):
            for line in page_lines[i]:
                if not line or TOC_LINE_RE.search(line):
                    continue
                if line == target or (len(line) >= 12 and target.startswith(line)):
                    found = i
                    break
            if found is not None:
                break
        numbers.append(found + 1 if found is not None else None)
        if found is not None:
            cursor = found
    return numbers


def fill_toc_page_numbers(doc) -> tuple[bool, str]:
    """Render the document with LibreOffice and put real page numbers in the TOC entries.

    The .docx itself is never round-tripped through LibreOffice; only the page
    numbers are read from a temporary PDF. Returns (all numbers found, message).
    """
    toc = getattr(doc, "_vw_toc", None)
    if not toc or not toc["runs"]:
        return True, "no table of contents entries"
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    pdftotext = shutil.which("pdftotext")
    if not soffice or not pdftotext:
        return False, "page numbers not filled — LibreOffice or pdftotext is not installed"
    with tempfile.TemporaryDirectory(prefix="vw_toc_") as tmp:
        tmp_path = Path(tmp)
        docx_path = tmp_path / "toc-pass.docx"
        doc.save(docx_path)
        try:
            subprocess.run(
                [soffice, f"-env:UserInstallation={(tmp_path / 'lo-profile').as_uri()}",
                 "--headless", "--convert-to", "pdf", "--outdir", str(tmp_path), str(docx_path)],
                capture_output=True, timeout=240, check=True,
            )
            text = subprocess.run(
                [pdftotext, "-layout", str(tmp_path / "toc-pass.pdf"), "-"],
                capture_output=True, text=True, timeout=120, check=True,
            ).stdout
        except (subprocess.SubprocessError, OSError) as exc:
            return False, f"page numbers not filled — render failed: {exc}"
    numbers = find_heading_pages(toc["entries"], text.split("\f"))
    for run, number in zip(toc["runs"], numbers):
        run.text = str(number) if number else ""
    missing = [entry[1] for entry, number in zip(toc["entries"], numbers) if number is None]
    if missing:
        return False, f"page numbers not found for {len(missing)} headings: {', '.join(missing[:5])}"
    return True, f"table of contents filled with {len(numbers)} page numbers"


def set_update_fields_on_open(doc) -> None:
    """Set w:updateFields so Word refreshes the TOC and page fields on open."""
    settings = doc.settings.element
    existing = settings.find(qn("w:updateFields"))
    if existing is None:
        existing = OxmlElement("w:updateFields")
        settings.append(existing)
    existing.set(qn("w:val"), "true")


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


def _term_problems(text: str, terms: list[str], values: dict, label: str, ignore_case: bool = True) -> list[str]:
    problems = []
    value_text = " ".join(str(v) for v in values.values() if isinstance(v, str)).lower()
    for term in terms:
        if term.lower() in value_text:
            continue  # the current customer may legitimately be a past customer or use the product
        match = re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.I if ignore_case else 0)
        if match:
            context = text[max(0, match.start() - 40): match.end() + 40].replace("\n", " ")
            problems.append(f"{label} '{term}' in the document: ...{context}...")
    return problems


def check_document(doc, values: dict, banned_terms: list[str], mode: str, issue: bool,
                   third_party_terms: list[str] | None = None) -> tuple[list[str], list[str]]:
    """Return (problems, keys still to confirm). Any problem blocks the build."""
    text = document_text(doc)
    problems: list[str] = []
    if mode == "complete" and ("{{" in text or "}}" in text):
        leftover = sorted(set(re.findall(r"\{\{[^}]*\}\}", text)))
        problems.append(f"unresolved token text in the document: {', '.join(leftover) or '{{ or }}'}")
    if "<!--" in text or "-->" in text:
        problems.append("HTML comment text reached the document")
    problems += _term_problems(text, banned_terms, values, "banned term")
    # Product names are proper nouns: match case-sensitively so "maintenance windows" is not "Windows".
    problems += _term_problems(text, third_party_terms or [], values, "third-party product name", ignore_case=False)
    unconfirmed = sorted(set(TO_CONFIRM_RE.findall(text)))
    if issue and unconfirmed:
        problems.append("an issue copy cannot contain unfilled values: " + ", ".join(unconfirmed))
    return problems, unconfirmed


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def load_glossary(root: Path = SCRIPT_DIR) -> dict[str, str]:
    path = root / GLOSSARY_FILE
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _new_document(values: dict, template: bool):
    prepared_by = str(values.get("prepared_by") or "Verto Wave").strip()
    if template:
        return build_base_template.new_document(
            title="DeviceX/SDX & StackX — Technical Proposal Template",
            footer_label="Verto Wave — DeviceX/SDX & StackX Proposal Template",
        )
    engagement = str(values.get("engagement_name") or "").strip()
    customer = str(values.get("customer_short") or "").strip()
    return build_base_template.new_document(
        title=f"{engagement} — Technical Proposal" if engagement else "Technical Proposal",
        footer_label=f"{prepared_by} — {customer} Technical Proposal" if customer else f"{prepared_by} — Technical Proposal",
        author=prepared_by,
    )


def plan_modules(index: dict, selected: list[str], offering: list[str]) -> tuple[list[str], list[str], set[str]]:
    """Return (included tokens in document order, skipped tokens, condition context)."""
    context = build_context(index, selected, offering)
    included, skipped = [], []
    for token in document_order(index):
        if token not in selected:
            continue
        (included if module_applies(find_module(index, token) or {}, context) else skipped).append(token)
    # Modules that were left out no longer count for conditions.
    context = build_context(index, included, offering)
    return included, skipped, context


def assemble_complete_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
    issue: bool = False,
    root: Path = SCRIPT_DIR,
    offering: list[str] | None = None,
    toc_levels: int = 2,
    library: Path | None = None,
):
    offering = list(offering or DEFAULT_OFFERING)
    doc = _new_document(values, template=False)
    included, skipped, context = plan_modules(index, selected_tokens, offering)
    renderer = Renderer(doc, draft=not issue, context=context, index=index, values=values,
                        root=root, library=library)
    names = display_names(index)
    warnings = [f"{names.get(t, t)} left out — it does not apply to this offering." for t in skipped]

    def add_module(token: str) -> None:
        path = resolve_module_file(token, index, root, library)
        if path is None:
            warnings.append(f"module '{token}': source file not found; skipped.")
            renderer.note(f"[Module {token}: source file not found]")
            return
        mod = find_module(index, token) or {}
        renderer.start_module(bool(mod.get("appendix")))
        text = prepare_module_text(path.read_text(encoding="utf-8"),
                                   keep_title=mod.get("show_title", True), context=context)
        renderer.render(parse_blocks(fill_tokens(text, values, names)))

    front = [t for t in FRONT_MATTER if t in included]
    rest = [t for t in included if t not in front]
    for i, token in enumerate(front):
        renderer.break_before = i > 0
        add_module(token)
    toc_anchor = add_toc(doc, draft=not issue, page_break_before=bool(front))
    renderer.number_headings = True
    for token in rest:
        renderer.break_before = True
        add_module(token)
    renderer.break_before = False

    renderer.fill_deferred(load_glossary(root))
    doc._vw_toc = write_toc_field(doc, toc_anchor, collect_headings(doc, toc_anchor, toc_levels), toc_levels)
    doc._vw_problems = renderer.problems
    warnings.append("logo: " + embed_logo(doc, logo_path, draft=not issue))
    set_update_fields_on_open(doc)
    return doc, warnings


def assemble_template_document(
    index: dict,
    selected_tokens: list[str],
    values: dict,
    logo_path: str | None = None,
    root: Path = SCRIPT_DIR,
    library: Path | None = None,
):
    doc = _new_document(values, template=True)
    renderer = Renderer(doc, draft=True, index=index, values=values, root=root, library=library)
    warnings: list[str] = []

    doc.add_heading("DeviceX/SDX & StackX — Technical Proposal Template", level=0)
    run = doc.add_paragraph().add_run("Verto Wave — Modular Proposal Template")
    run.italic = True
    run = doc.add_paragraph().add_run(
        "Replace each {{…}} token with the current bid's content before issue. "
        "Pricing is excluded by design and attached separately."
    )
    run.italic = True
    write_toc_field(doc, add_toc(doc, draft=True), [])

    doc_control = resolve_module_file("section_document_control", index, root, library)
    if doc_control is not None:
        text = HTML_COMMENT_RE.sub("", doc_control.read_text(encoding="utf-8"))
        text = re.sub(r"(?m)^\s*<!--.*$", "", text)
        renderer.render(parse_blocks(prepare_module_text(text)))

    chosen = [find_module(index, t) for t in document_order(index) if t in selected_tokens]
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
    doc._vw_problems = []
    return doc, warnings


def find_group_label(index: dict, token: str) -> str:
    for group in index.get("modules", {}).values():
        if any(mod.get("token") == token for mod in group.get("modules", [])):
            return group.get("group", "")
    return ""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_offering(text: str | None) -> list[str]:
    if not text:
        return list(DEFAULT_OFFERING)
    offering = [part.strip() for part in text.split(",") if part.strip()]
    unknown = [part for part in offering if part not in OFFERINGS]
    if unknown or not offering:
        raise SystemExit(f"ERROR: --offering takes a comma list of {', '.join(OFFERINGS)}; got {text!r}")
    return offering


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Assemble a Verto Wave DeviceX/SDX & StackX proposal docx from modular Markdown."
    )
    p.add_argument("--values", required=True, help="Path to the proposal values JSON")
    p.add_argument("--modules", help="Comma-separated module tokens to include (default: all)")
    p.add_argument("--offering", default=None,
                   help="Comma list of licenses, services, managed_services (default: licenses,services)")
    p.add_argument("--mode", choices=["complete", "template"], default="complete")
    p.add_argument("--issue", action="store_true",
                   help="Issue copy: drop bid-team notes and refuse to build with unfilled values")
    p.add_argument("--out", required=True, help="Output .docx path")
    p.add_argument("--index", default=None, help="Path to module_index.json (default: next to this script)")
    p.add_argument("--library", default=os.environ.get("PROPOSAL_LIBRARY_DIR"),
                   help="Module Library folder with portal overrides (default: $PROPOSAL_LIBRARY_DIR)")
    p.add_argument("--logo", default=None, help="Logo image (PNG/JPG) for the cover page")
    p.add_argument("--toc-levels", type=int, choices=[1, 2, 3], default=1,
                   help="Heading levels listed in the table of contents (default 1: main sections)")
    p.add_argument("--no-toc-pages", action="store_true",
                   help="Skip the LibreOffice render that fills in table-of-contents page numbers")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    index_path = Path(args.index) if args.index else DEFAULT_INDEX
    index = load_index(index_path)
    root = index_path.resolve().parent
    library = Path(args.library) if args.library and Path(args.library).is_dir() else None
    offering = parse_offering(args.offering)

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
    selected = [t.strip() for t in args.modules.split(",") if t.strip()] if args.modules else list(known)

    unknown = [t for t in selected if t not in known]
    if unknown:
        print(f"WARNING: unknown module tokens (not in module_index.json): {', '.join(unknown)}", file=sys.stderr)
    for mod in iter_modules(index):
        if mod.get("required") and mod["token"] not in selected:
            print(f"NOTE: required module omitted: {mod['token']} ({mod.get('name', '')})", file=sys.stderr)
        if mod.get("placeholder") and mod["token"] in selected:
            print(f"WARNING: {mod.get('name', mod['token'])} is a placeholder module — not for live bids.",
                  file=sys.stderr)

    try:
        if args.mode == "complete":
            doc, warnings = assemble_complete_document(index, selected, values, args.logo, args.issue, root,
                                                       offering, args.toc_levels, library)
        else:
            doc, warnings = assemble_template_document(index, selected, values, args.logo, root, library)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_CHECK_FAILED

    problems, unconfirmed = check_document(
        doc, values, index.get("banned_terms", []), args.mode, args.issue and args.mode == "complete",
        index.get("third_party_terms", []),
    )
    problems = list(getattr(doc, "_vw_problems", [])) + problems
    for warning in warnings:
        if warning.startswith("logo:"):
            print("LOGO: " + warning[5:].strip())
        else:
            print(f"WARNING: {warning}", file=sys.stderr)
    if unconfirmed and args.mode == "complete":
        print("TO CONFIRM: " + ", ".join(unconfirmed), file=sys.stderr)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print("ERROR: build refused — nothing was written.", file=sys.stderr)
        return EXIT_CHECK_FAILED

    if args.mode == "complete" and not args.no_toc_pages:
        filled, message = fill_toc_page_numbers(doc)
        print(f"TOC: {message}" if filled else f"WARNING: {message}", file=sys.stdout if filled else sys.stderr)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
