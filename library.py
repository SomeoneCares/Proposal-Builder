"""
Versioned module and figure overrides edited from the portal's Module Library.

Layout under the library folder ($PROPOSAL_LIBRARY_DIR on the host):
  modules/<token>/v0001.md, v0002.md ...   every saved version
  modules/<token>/current.md               the active version (combine.py uses it)
  modules/<token>/history.json             who saved what, when and why
  figures/<slug>.png|jpg                   uploaded diagrams for [[figure: slug | ...]]

The repo copy of a module is the baseline; a library version overrides it until
it is reverted. scripts/pull-library.sh brings saved versions back into git.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import combine

FIGURE_RE = re.compile(r"^\[\[\s*figure\s*:\s*([^|\]]+?)\s*(?:\|\s*(.*?))?\s*\]\]\s*$", re.M)


def default_library_dir() -> Path | None:
    value = os.environ.get("PROPOSAL_LIBRARY_DIR")
    return Path(value) if value else None


def validate_module_text(text: str, index: dict) -> list[str]:
    """Problems that would stop a module version from being saved."""
    problems: list[str] = []
    stripped = text.lstrip()
    if not stripped.startswith("# "):
        problems.append("the module must start with a '# Title' line")
    if not re.search(r"(?m)^---\s*$", text):
        problems.append("the metadata block must be closed by a '---' line")
    known = combine.known_condition_names(index)
    for expr in combine.conditions_in(text):
        try:
            unknown = combine.condition_names(combine.parse_condition(expr)) - known
        except ValueError as exc:
            problems.append(str(exc))
            continue
        if unknown:
            problems.append(f"unknown name(s) in condition '{expr}': {', '.join(sorted(unknown))}")
    try:
        combine.apply_conditions(text, set())
    except ValueError as exc:
        problems.append(str(exc))
    slots = set(index.get("customer_slots", {})) | {m["token"] for m in combine.iter_modules(index)}
    for token in sorted(set(re.findall(r"\{\{([^}]*)\}\}", text))):
        if token.strip() not in slots:
            problems.append(f"unknown value token {{{{{token}}}}} — add it to customer_slots first")
    problems += combine._term_problems(text, index.get("banned_terms", []), {}, "banned term")
    problems += combine._term_problems(text, index.get("third_party_terms", []), {}, "third-party product name",
                                       ignore_case=False)
    return problems


class Library:
    def __init__(self, root: Path, index: dict, repo: Path = combine.SCRIPT_DIR):
        self.root = Path(root)
        self.index = index
        self.repo = Path(repo)

    # -- modules ---------------------------------------------------------------
    def module_dir(self, token: str) -> Path:
        if not combine.find_module(self.index, token):
            raise KeyError(f"unknown module {token}")
        return self.root / "modules" / token

    def history(self, token: str) -> list[dict]:
        path = self.module_dir(token) / "history.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []

    def is_overridden(self, token: str) -> bool:
        return (self.module_dir(token) / "current.md").is_file()

    def baseline_text(self, token: str) -> str:
        mod = combine.find_module(self.index, token) or {}
        path = self.repo / mod.get("file", "")
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def current_text(self, token: str) -> str:
        current = self.module_dir(token) / "current.md"
        return current.read_text(encoding="utf-8") if current.is_file() else self.baseline_text(token)

    def version_text(self, token: str, version: int) -> str:
        return (self.module_dir(token) / f"v{version:04d}.md").read_text(encoding="utf-8")

    def _record(self, token: str, entry: dict) -> None:
        history = self.history(token)
        history.append(entry)
        (self.module_dir(token) / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")

    def save(self, token: str, text: str, author: str, note: str, source: str = "editor") -> dict:
        problems = validate_module_text(text, self.index)
        if problems:
            raise ValueError("; ".join(problems))
        folder = self.module_dir(token)
        folder.mkdir(parents=True, exist_ok=True)
        text = text.replace("\r\n", "\n")
        version = max((e["version"] for e in self.history(token) if "version" in e), default=0) + 1
        (folder / f"v{version:04d}.md").write_text(text, encoding="utf-8", newline="\n")
        (folder / "current.md").write_text(text, encoding="utf-8", newline="\n")
        entry = {"version": version, "saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "author": author.strip() or "unknown", "note": note.strip(), "source": source}
        self._record(token, entry)
        return entry

    def restore(self, token: str, version: int, author: str) -> dict:
        return self.save(token, self.version_text(token, version), author, f"Restored version {version}", "restore")

    def revert_to_baseline(self, token: str, author: str) -> None:
        current = self.module_dir(token) / "current.md"
        if current.exists():
            current.unlink()
        self._record(token, {"saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                             "author": author.strip() or "unknown", "note": "Reverted to the deployed baseline",
                             "source": "revert"})

    # -- figures ---------------------------------------------------------------
    def figure_references(self) -> list[dict]:
        refs = []
        for mod in combine.iter_modules(self.index):
            for slug, caption in FIGURE_RE.findall(self.current_text(mod["token"])):
                image = combine.resolve_figure(slug, self.repo, self.root)
                refs.append({"slug": slug, "caption": caption, "token": mod["token"], "module": mod.get("name", ""),
                             "image": str(image) if image else ""})
        return refs

    def save_figure(self, slug: str, data: bytes, suffix: str) -> Path:
        suffix = suffix.lower()
        if suffix not in combine.FIGURE_EXTENSIONS:
            raise ValueError("figures must be PNG or JPG")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            raise ValueError("invalid figure name")
        folder = self.root / "figures"
        folder.mkdir(parents=True, exist_ok=True)
        for ext in combine.FIGURE_EXTENSIONS:
            (folder / f"{slug}{ext}").unlink(missing_ok=True)
        path = folder / f"{slug}{suffix}"
        path.write_bytes(data)
        return path
