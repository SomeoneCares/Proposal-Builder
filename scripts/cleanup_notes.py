#!/usr/bin/env python3
"""
Batch-clean module final-notes and StackX placeholder notes to remove
all prior-customer / MOE-specific references.

DeviceX modules: rewrite final italic notes to generic
"Include when X is in scope. Confirm with the customer."

StackX placeholder modules: replace "MOE proposal Appendix 5.x" and
related references with generic "a prior proposal appendix" framing.

Run from the skill root directory.
"""

from pathlib import Path
import re

SKILL_ROOT = Path(__file__).resolve().parents[1]  # scripts/ -> skill root
STACKX_DIR = SKILL_ROOT / "modules" / "stackx"
DEVICE_X_DIR = SKILL_ROOT / "modules" / "devicex"

# Generic rewrites for DeviceX module final notes (exact old -> new)
DEVICE_X_NOTE_FIXES = {
    "module_network_services.md": (
        "*This module is a reusable building block. Include when on-demand branch "
        "network services (DNS/DHCP/LDAP/RADIUS) are in scope for the current "
        "engagement. Confirm with the customer.*"
    ),
    "module_sase.md": (
        "*This module is a reusable building block. Include when SASE / Zero Trust "
        "edge access is in scope for the current engagement. Confirm with the "
        "customer.*"
    ),
    "module_virtualization.md": (
        "*This module is a reusable building block. Include when local "
        "virtualization / container hosting at the branch is in scope for the "
        "current engagement. Confirm with the customer.*"
    ),
}

# Generic rewrites for StackX placeholder "MOE proposal" references
STACKX_MOE_REPLACEMENTS = [
    ("MOE proposal Appendix 5.1.1 (StackX Endpoint Management and Analytics)",
     "a prior proposal appendix describing StackX Endpoint Management and Analytics"),
    ("MOE proposal Appendix 5.1.2 (StackX Automation and Orchestration)",
     "a prior proposal appendix describing StackX Automation and Orchestration"),
    ("MOE proposal Appendix 5.1.3 (StackX Observability and APM)",
     "a prior proposal appendix describing StackX Observability and APM"),
    ("MOE proposal Appendix 5.1.4 (StackX TrueView)",
     "a prior proposal appendix describing StackX TrueView"),
    ("MOE proposal Appendix 5.1.5 (StackX Identity Management (IDM))",
     "a prior proposal appendix describing StackX Identity Management (IDM)"),
    ("MOE proposal Appendix 5.1.6 (StackX Backup)",
     "a prior proposal appendix describing StackX Backup"),
    ("MOE proposal Appendix 5.1.7 (StackX Operations Monitoring & Configuration Management Enterprise Management)",
     "a prior proposal appendix describing StackX Operations Monitoring & Configuration Management Enterprise Management"),
    ("MOE proposal Appendix 5.1.8 (StackX Network Operations Enterprise Management)",
     "a prior proposal appendix describing StackX Network Operations Enterprise Management"),
    ("MOE proposal Appendix 5.1.10 (StackX Application Lifecycle Management (ALM) Enterprise Management)",
     "a prior proposal appendix describing StackX Application Lifecycle Management (ALM) Enterprise Management"),
    ("MOE proposal Appendix 5.1.11 (StackX Compliance Assurance System)",
     "a prior proposal appendix describing StackX Compliance Assurance System"),
    ("MOE proposal Appendix 5.1.11.1–5.1.11.3 (StackX Operations Integrity Platform)",
     "a prior proposal appendix describing StackX Operations Integrity Platform"),
    ("MOE proposal Appendix 5.1.11.1 (Systems Operations Integrity)",
     "a prior proposal appendix describing Systems Operations Integrity"),
    ("MOE proposal Appendix 5.1.11.2 (DeviceX SASE & ZTNA Framework)",
     "a prior proposal appendix describing DeviceX SASE & ZTNA Framework"),
    ("MOE proposal Appendix 5.1.11.3 (Integrated Security Controls & Case Management)",
     "a prior proposal appendix describing Integrated Security Controls & Case Management"),
    ("MOE proposal Appendix 5.1.12 (StackX Call Center Management)",
     "a prior proposal appendix describing StackX Call Center Management"),
    ("MOE proposal Appendix 3 (DevOps Framework)",
     "a prior proposal appendix describing the DevOps Framework"),
    # Generic fallback patterns
    ("MOE proposal", "a prior proposal"),
    ("the MOE proposal", "the prior proposal"),
    ("MOE Appendix", "the prior proposal appendix"),
    ("the MOE Appendix", "the prior proposal appendix"),
    ("Ministry of Education's", "the customer's"),
    ("Prior MOE", "A prior"),
]


def rewrite_devicex_note(path: Path, new_note: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Find the LAST italic note line in the file (starts+ends with *, >4 chars)
    note_idx = None
    for i in range(len(lines) - 1, -1, -1):
        s = lines[i].strip()
        if s.startswith("*") and s.endswith("*") and len(s) > 6:
            note_idx = i
            break
    if note_idx is None:
        print(f"  WARN: no italic note in {path.name}")
        return False
    lines[note_idx] = new_note
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def rewrite_stackx_moe(text: str) -> str:
    before = text
    for old, new in STACKX_MOE_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def main():
    updated = 0

    # --- DeviceX modules ---
    for fname, new_note in DEVICE_X_NOTE_FIXES.items():
        path = DEVICE_X_DIR / fname
        if not path.exists():
            print(f"SKIP missing: {fname}")
            continue
        before = path.read_text(encoding="utf-8")
        if rewrite_devicex_note(path, new_note):
            print(f"OK  devicex note: {fname}")
            updated += 1
        else:
            print(f"WARN note rewrite failed: {fname}")

    # --- StackX placeholder modules ---
    stackx_files = sorted(STACKX_DIR.glob("module_stackx_*.md"))
    for path in stackx_files:
        text = path.read_text(encoding="utf-8")
        new_text = rewrite_stackx_moe(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"OK  stackx moe-clean: {path.name}")
            updated += 1

    # --- Final full scan ---
    print("\n=== Final contamination scan ===")
    still_dirty = []
    pattern = re.compile(
        r"EGYCash|MCI|CPC|30-June|MOE|Ministry of Education|October|Roxy|RDH"
        r"|Educational City|NVR without AI|Variant A|Variant B|MOE model"
        r"|30-June Schools|MCI",
        re.IGNORECASE,
    )
    for path in sorted((SKILL_ROOT / "modules").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            line_num = text[: match.start()].count("\n") + 1
            snippet = text[ max(0, match.start()-30): match.end()+30]
            still_dirty.append(f"{path.relative_to(SKILL_ROOT)}:L{line_num}  '{snippet.strip()}'")
    if still_dirty:
        print(f"STILL DIRTY ({len(still_dirty)} refs):")
        for line in still_dirty:
            print("  " + line)
    else:
        print("CLEAN — no client/sector-specific references remain.")


if __name__ == "__main__":
    main()
