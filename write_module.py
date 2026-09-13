#!/usr/bin/env python3
"""
Create a new proposal module from the standard skeleton and register it in
module_index.json.

Usage:
  python write_module.py --token module_foo --name "Module Foo" \\
      [--group devicex_sdx|stackx|cross_cutting] [--required] [--notes "when to include it"]

The file follows references/module_authoring.md: title, metadata block closed
by ---, then the recommended sections with bid-team notes in *[...]*.
Refuses to overwrite an existing module file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
INDEX = SCRIPT_DIR / "module_index.json"

GROUP_LABELS = {
    "devicex_sdx": "DeviceX/SDX — Edge & Branch Layer",
    "stackx": "StackX — Control / Orchestration / SOC / Operations Layer",
    "cross_cutting": "Cross-Cutting",
}

GROUP_DIR = {
    "devicex_sdx": "modules/devicex",
    "stackx": "modules/stackx",
    "cross_cutting": "modules/cross_cutting",
}


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


def build_skeleton(token: str, name: str, group: str, required: bool, notes: str) -> str:
    lines = [
        f"# {name}",
        "",
        f"**Token:** `{{{{{token}}}}}`  ",
        f"**Group:** {GROUP_LABELS[group]}  ",
        f"**Required:** {'Yes' if required else 'No (optional module)'}",
    ]
    if notes:
        lines.append(f"**Note:** {notes}")
    lines += [
        "",
        "---",
        "",
        "## Solution Overview",
        "",
        "*[To be authored — replace this placeholder before the module is used in a live proposal.]*",
        "",
        "## Key Capabilities",
        "",
        "- *[Capability — to be authored]*",
        "",
        "## Out-of-Scope (explicitly)",
        "",
        "- *[Out-of-scope item — mirror modules/cross_cutting/section_out_of_scope.md]*",
        "",
        "---",
        "",
        "*This module is a reusable building block. Validate each capability claim against the current "
        "customer's RFP/ITB before issue. Do not assert certifications or compliance claims not validated "
        "for the current engagement.*",
        "",
    ]
    return "\n".join(lines)


def register_module(index: dict, token: str, name: str, group: str, required: bool, notes: str) -> None:
    group_cfg = index.setdefault("modules", {}).setdefault(group, {})
    group_cfg.setdefault("group", GROUP_LABELS[group])
    group_cfg.setdefault("description", "")
    modules = group_cfg.setdefault("modules", [])
    entry = {
        "token": token,
        "file": f"{GROUP_DIR[group]}/{token}.md",
        "name": name,
        "required": required,
        "placeholder": True,
    }
    if notes:
        entry["notes"] = notes
    modules.append(entry)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Create a new proposal module and register it in module_index.json")
    p.add_argument("--token", required=True, help="Module token, e.g. module_foo (module_ or section_ prefix)")
    p.add_argument("--name", required=True, help="Human-readable module name")
    p.add_argument("--group", choices=sorted(GROUP_DIR), default="cross_cutting", help="Module group")
    p.add_argument("--required", action="store_true", help="Mark the module as required")
    p.add_argument("--notes", default="", help="When to include the module (shown in the builder)")
    args = p.parse_args(argv)

    if not re.match(r"^(module_|section_)[a-zA-Z0-9_]+$", args.token):
        print(f"ERROR: token must match (module_|section_)[a-zA-Z0-9_]+; got {args.token}", file=sys.stderr)
        return 2

    index = load_index()
    registered = {m.get("token") for grp in index.get("modules", {}).values() for m in grp.get("modules", [])}
    if args.token in registered:
        print(f"ERROR: token already registered: {args.token}", file=sys.stderr)
        return 2

    path = SCRIPT_DIR / GROUP_DIR[args.group] / f"{args.token}.md"
    if path.exists():
        print(f"ERROR: {path} already exists", file=sys.stderr)
        return 2
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_skeleton(args.token, args.name, args.group, args.required, args.notes), encoding="utf-8")
    print(f"Wrote module file: {path}")

    register_module(index, args.token, args.name, args.group, args.required, args.notes)
    save_index(index)
    print(f"Registered {args.token} in {INDEX} (marked as a placeholder until authored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
