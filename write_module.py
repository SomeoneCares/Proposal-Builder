#!/usr/bin/env python3
"""
proposal-template module writer helper

Quick helper to create a new module Markdown file from a minimal
skeleton, and register it in module_index.json under the correct
group and token.

Usage:
  python write_module.py --token module_foo --name "Module Foo" \\
      [--group devicex_sdx|stackx|cross_cutting] \\
      [--required] [--notes "optional notes"]
  python write_module.py --init  (prints an interactive prompt guide)

The skeleton pre-fills the Token/Group/Required/Notes metadata block
and a placeholder Overview plus an Out-of-Scope block.

Do not use this script to back-fill content for modules that already
have a source proposal appendix to author from (e.g. the StackX
placeholder modules). For those, edit the .md file directly and add
the **(To be authored)** marker until the content is complete.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INDEX = SCRIPT_DIR / "module_index.json"


def load_index() -> dict:
    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found", file=sys.stderr)
        raise SystemExit(2)
    with INDEX.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index: dict) -> None:
    with INDEX.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")


GROUP_GROUPS = {
    "devicex_sdx": "DeviceX/SDX — edge & branch layer",
    "stackx": "StackX — control / orchestration / SOC / operations layer",
    "cross_cutting": "Cross-cutting / reusable sections",
}

GROUP_DIR = {
    "devicex_sdx": "modules/devicex",
    "stackx": "modules/stackx",
    "cross_cutting": "modules/cross_cutting",
}


def token_to_filename(token: str) -> str:
    return f"{token}.md"


def build_skeleton(token: str, name: str, group: str, required: bool, notes: str) -> str:
    note_block = ""
    if notes:
        note_block = f"\n**Notes:** {notes}\n"

    return f"""# {name}

**Token:** `{{{token}}}`  
**Group:** {GROUP_GROUPS[group]}  
**Required:** {"Yes" if required else "No"}**Notes:** {notes}
---

## Overview

*[To be authored — replace this placeholder before the module is included in a live proposal.]*

## Capabilities

- *[Capability 1 — to be authored]*

## Out-of-Scope (explicitly)

- *[Out-of-scope item — to be authored]*

---

*This module is a reusable building block. Validate each capability claim against the current customer's RFP/ITB before issuance. Do not assert certifications or compliance claims not validated for the current engagement.*
""".strip() + "\n"


def register_module(index: dict, token: str, name: str, group: str, required: bool, notes: str) -> dict:
    group_cfg = index.setdefault("modules", {}).setdefault(group, {})
    group_cfg.setdefault("group", GROUP_GROUPS[group])
    group_cfg.setdefault("description", "")
    group_cfg.setdefault("modules", [])
    modules = group_cfg["modules"]

    if any(m.get("token") == token for m in modules):
        print(f"WARNING: token already registered: {token}", file=sys.stderr)
        return index

    entry = {
        "token": token,
        "file": f"{GROUP_DIR[group]}/{token_to_filename(token)}",
        "name": name,
        "required": required,
    }
    if notes:
        entry["notes"] = notes
    modules.append(entry)
    return index


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Create a new proposal-template module and register it in module_index.json")
    p.add_argument("--token", required=True, help="Module token, e.g. module_foo (use module_ or section_ prefix)")
    p.add_argument("--name", required=True, help="Human-readable module name")
    p.add_argument("--group", choices=["devicex_sdx", "stackx", "cross_cutting"], default="cross_cutting", help="Module group")
    p.add_argument("--required", action="store_true", help="Mark module as required")
    p.add_argument("--notes", default="", help="Optional notes for the module registry")
    args = p.parse_args(argv)

    if not re.match(r"^(module_|section_)[a-zA-Z0-9_]+$", args.token):
        print(f"ERROR: token must match pattern (module_|section_)[a-zA-Z0-9_]+; got {args.token}", file=sys.stderr)
        return 2

    index = load_index()
    if args.token in {m.get("token") for grp in index.get("modules", {}).values() for m in grp.get("modules", [])}:
        print(f"NOTE: token already present; rewriting file only.", file=sys.stderr)

    group_dir = SCRIPT_DIR / GROUP_DIR[args.group]
    group_dir.mkdir(parents=True, exist_ok=True)
    path = group_dir / token_to_filename(args.token)

    skeleton = build_skeleton(args.token, args.name, args.group, args.required, args.notes)
    path.write_text(skeleton, encoding="utf-8")
    print(f"Wrote module file: {path}")

    register_module(index, args.token, args.name, args.group, args.required, args.notes)
    save_index(index)
    print(f"Registered token {args.token} in {INDEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
