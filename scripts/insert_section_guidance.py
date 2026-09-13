"""Add generic image-placement guidance to any section_*.md that lacks one."""

import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SECTIONS_DIR = SKILL_ROOT / "modules" / "cross_cutting"

GENERIC = """---

## Figure — <Insert approved generic diagram / screenshot here>

<!-- IMAGE PLACEMENT GUIDANCE — insert approved generic image here -->
<!-- Recommended image: a generic diagram or screenshot relevant to this section's content (architecture, flow, dashboard, or topology as appropriate). No customer-specific names, environment, architecture, site names, or branding. -->
<!-- Generic-only rule: do not insert any image that names or depicts the customer's specific environment, architecture, site names, or branding. Replace customer-specific labels before use. -->
<!-- To embed: place the approved image file at this location in the final docx (deferred — combine.py is text-only for now). -->

*[Figure placeholder — insert approved generic image here. See image-placement guidance notes.]*

---"""


def has_guidance(path: Path) -> bool:
    return "IMAGE PLACEMENT" in path.read_text(encoding="utf-8")


def find_blank_near_center(lines):
    n = len(lines)
    mid = n // 2
    # search forward for blank within ~12 lines
    for i in range(mid, min(mid + 12, n)):
        if lines[i].strip() == "":
            return i
    # search backward
    for i in range(mid - 1, max(mid - 12, -1), -1):
        if lines[i].strip() == "":
            return i
    return mid


def insert(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    idx = find_blank_near_center(lines)
    new_lines = lines[:idx] + [GENERIC, ""] + lines[idx:]
    path.write_text("\n".join(new_lines), encoding="utf-8")


def main():
    updated = []
    for md in sorted(SECTIONS_DIR.glob("section_*.md")):
        if has_guidance(md):
            continue
        insert(md)
        updated.append(md.name)
    print(f"Updated {len(updated)} sections: {updated}")


if __name__ == "__main__":
    main()
