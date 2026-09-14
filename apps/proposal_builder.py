#!/usr/bin/env python3
"""
Verto Wave Proposal Builder — Streamlit web UI around combine.py.

Steps: offering → modules → sections → customer → compliance matrix → review and build.
The Module Library page (apps/pages) edits and versions the modules themselves.
On the lab host this runs as the systemd user unit `proposal-builder`
(scripts/proposal-builder.service).
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import combine  # noqa: E402
import hermes_research  # noqa: E402

COMBINE_PY = ROOT / "combine.py"
INDEX = combine.load_index(ROOT / "module_index.json")
EXAMPLE_VALUES = json.loads((ROOT / "values-example.json").read_text(encoding="utf-8"))
DEFAULT_LOGO = ROOT / "assets" / "vertowave_logo.png"
SLOTS: dict[str, str] = INDEX["customer_slots"]
MODULES = {mod["token"]: mod for mod in combine.iter_modules(INDEX)}
GROUPS = INDEX["modules"]

OFFERING_LABELS = {
    "licenses": "Software licenses (DeviceX / StackX)",
    "services": "Professional services — architecture, design, implementation and roll-out",
    "managed_services": "Managed services — operation under an Operations Level Agreement",
    "premier_support": "Premier Support visits (with licenses)",
}
OFFERING_HELP = {
    "licenses": "Licenses are deemed delivered on license delivery — no acceptance. Adds the support and warranty terms.",
    "services": "Adds professional services, project methodology, timeline and roles. Services are accepted against agreed criteria.",
    "managed_services": "Adds the OLA, operations roles and SOC operations. When not selected, managed services are not mentioned anywhere.",
    "premier_support": "Adds monthly, then quarterly, on-site Premier Support visits to the support section.",
}
CODES = ["C-DX", "C-SX", "CC", "IS", "AS", "PC", "NC"]
TEXT_AREAS = {"customer_profile", "requirement_summary", "key_requirements"}
BLANK_RULE = "Blank fields are marked TO CONFIRM in a draft and block an issue copy."
# (title, caption, slot names or a slot-name prefix, module token that uses the slots)
SLOT_GROUPS = [
    ("Customer", None, ["customer_name", "customer_short", "customer_primary_contact", "rfp_reference"], None),
    ("Proposal", None,
     ["proposal_title", "proposal_subtype", "engagement_name", "prepared_by", "author_name", "proposal_version",
      "proposal_status", "proposal_date", "proposal_date_iso", "effective_date", "validity_period_months"], None),
    ("Executive summary",
     "Phrases that complete the executive-summary sentences. Hermes can draft them above; a person must approve the draft.",
     ["customer_profile", "esg_footprint", "esg_value_1", "esg_value_2", "esg_outcome", "esg_example_a",
      "esg_example_b", "scope_services_description", "deployment_context", "objective_1", "objective_4",
      "objective_5"], None),
    ("Understanding of the requirement", "Key requirements: one per line, each starting with '- '.",
     ["requirement_summary", "key_requirements", "compliance_frameworks", "site_count"], "section_understanding"),
    ("Service-quality targets", f"Used by the SD-WAN targets table. {BLANK_RULE}", "ola_", "module_sdwan"),
    ("Professional services scope numbers", f"Every number bounds the scope. {BLANK_RULE}", "services_",
     "section_professional_services"),
    ("Implementation timeline", "Phase durations in weeks.", "timeline_", "section_timeline"),
    ("Support and warranty", None, ["support_term_months", "hardware_warranty_months", "support_coverage"],
     "section_support_warranty"),
    ("Hardware quantities", None, ["devicex_qty_note"], "section_hardware_sizing"),
]
MODE_DRAFT = "Draft for internal review"
MODE_ISSUE = "Issue copy"
HEADER_ALIASES = {
    "ref": {"ref", "ref.", "reference", "id", "req id", "requirement id", "#", "no", "no."},
    "requirement": {"requirement", "requirements", "description", "requirement text"},
    "code": {"code", "compliance", "response code", "compliance code"},
    "response": {"response", "verto wave response", "comment", "comments", "remarks"},
    "section": {"section", "proposal section", "reference section", "section reference"},
}


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def init_state() -> None:
    for slot in SLOTS:
        st.session_state.setdefault(slot, str(EXAMPLE_VALUES.get(slot, "")))
    for token, mod in MODULES.items():
        st.session_state.setdefault(f"mod_{token}", bool(mod.get("required")))
    for flag in OFFERING_LABELS:
        st.session_state.setdefault(f"off_{flag}", flag in combine.DEFAULT_OFFERING)
    st.session_state.setdefault("toc_levels", 2)
    # The data editor edits compliance_base; its output is kept in compliance_rows. Feeding the output back
    # in as the editor's input would re-apply edits, so a new base gets a new editor key instead.
    st.session_state.setdefault("compliance_base", [])
    st.session_state.setdefault("compliance_rows", [])
    st.session_state.setdefault("editor_version", 0)
    st.session_state.setdefault("build_result", None)


def set_compliance_rows(rows: list[dict]) -> None:
    st.session_state.compliance_base = rows
    st.session_state.compliance_rows = rows
    st.session_state.editor_version = st.session_state.get("editor_version", 0) + 1


def selected_tokens() -> list[str]:
    return [t for t in MODULES if st.session_state.get(f"mod_{t}")]


def current_offering() -> list[str]:
    return [flag for flag in OFFERING_LABELS if st.session_state.get(f"off_{flag}")]


def current_values() -> dict:
    values = {slot: st.session_state.get(slot, "") for slot in SLOTS}
    values["compliance_matrix"] = [row for row in st.session_state.compliance_rows if row.get("requirement")]
    return values


def bid_file() -> dict:
    return {"bid_file_version": 1, "values": {s: st.session_state.get(s, "") for s in SLOTS},
            "offering": current_offering(), "modules": selected_tokens(),
            "compliance_matrix": st.session_state.compliance_rows, "toc_levels": st.session_state.toc_levels}


def reset_to_example() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith(("mod_", "off_", "ai_")) or key in SLOTS:
            del st.session_state[key]
    set_compliance_rows([])
    st.session_state.build_result = None


def load_bid_file() -> None:
    """on_change callback: runs before the widgets, so it may set their state."""
    uploaded = st.session_state.get("bid_upload")
    if uploaded is None:
        return
    try:
        loaded = json.loads(uploaded.getvalue().decode("utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError("the file must contain a JSON object")
    except (UnicodeDecodeError, ValueError) as exc:
        st.session_state.upload_message = ("error", f"Could not read the file: {exc}")
        return
    values = loaded.get("values", loaded)
    for slot in SLOTS:
        if values.get(slot) not in (None, ""):
            st.session_state[slot] = str(values[slot])
    if "offering" in loaded:
        for flag in OFFERING_LABELS:
            st.session_state[f"off_{flag}"] = flag in loaded["offering"]
    if "modules" in loaded:
        for token in MODULES:
            st.session_state[f"mod_{token}"] = token in loaded["modules"]
    if isinstance(loaded.get("compliance_matrix"), list):
        set_compliance_rows(loaded["compliance_matrix"])
    if loaded.get("toc_levels") in (1, 2):
        st.session_state.toc_levels = loaded["toc_levels"]
    st.session_state.upload_message = ("success", f"Loaded {uploaded.name}.")


def apply_ai_draft() -> None:
    draft = st.session_state.get("ai_draft") or {}
    applied = []
    for field in draft.get("fields", {}):
        if st.session_state.get(f"ai_use_{field}"):
            st.session_state[field] = st.session_state.get(f"ai_text_{field}", "")
            applied.append(field)
    approver = st.session_state.get("ai_approver", "").strip()
    st.session_state.ai_message = f"Applied {len(applied)} field(s), approved by {approver}."
    st.session_state.ai_draft = None


def parse_requirements_csv(data: bytes) -> list[dict]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    mapping = {}
    for header in reader.fieldnames or []:
        for key, aliases in HEADER_ALIASES.items():
            if header.strip().lower() in aliases and key not in mapping.values():
                mapping[header] = key
    if "requirement" not in mapping.values():
        raise ValueError("the CSV needs a 'Requirement' column")
    rows = []
    for raw in reader:
        row = {key: "" for key in HEADER_ALIASES}
        for header, key in mapping.items():
            row[key] = (raw.get(header) or "").strip()
        if row["requirement"]:
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def run_build(logo_upload, use_default_logo: bool, out_name: str, issue: bool) -> dict:
    selected = selected_tokens()
    offering = current_offering()
    if not selected:
        return {"ok": False, "errors": ["Select at least one module."], "warnings": [], "log": ""}
    if not offering:
        return {"ok": False, "errors": ["Select at least one offering."], "warnings": [], "log": ""}
    out_name = Path(out_name.strip() or "proposal.docx").name
    if not out_name.lower().endswith(".docx"):
        out_name += ".docx"
    with tempfile.TemporaryDirectory(prefix="vw_proposal_") as tmp:
        tmp_path = Path(tmp)
        values_path = tmp_path / "values.json"
        values_path.write_text(json.dumps(current_values(), indent=2, ensure_ascii=False), encoding="utf-8")
        out_path = tmp_path / out_name
        cmd = [sys.executable, str(COMBINE_PY), "--values", str(values_path), "--mode", "complete",
               "--modules", ",".join(selected), "--offering", ",".join(offering),
               "--toc-levels", str(st.session_state.toc_levels), "--out", str(out_path)]
        if issue:
            cmd.append("--issue")
        if logo_upload is not None:
            logo_path = tmp_path / f"logo{Path(logo_upload.name).suffix.lower() or '.png'}"
            logo_path.write_bytes(logo_upload.getvalue())
            cmd += ["--logo", str(logo_path)]
        elif use_default_logo and DEFAULT_LOGO.exists():
            cmd += ["--logo", str(DEFAULT_LOGO)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(ROOT))
        except subprocess.TimeoutExpired:
            return {"ok": False, "errors": ["The build timed out after 300 s."], "warnings": [], "log": ""}
        log = proc.stdout + proc.stderr
        lines = log.splitlines()
        result = {
            "errors": [line.removeprefix("ERROR: ") for line in lines if line.startswith("ERROR:")],
            "warnings": [line.split(": ", 1)[1] for line in lines if line.startswith(("WARNING:", "NOTE:"))],
            "to_confirm": next((line.removeprefix("TO CONFIRM: ") for line in lines if line.startswith("TO CONFIRM:")), ""),
            "log": log,
        }
        if proc.returncode != 0 or not out_path.exists():
            result["ok"] = False
            result["errors"] = result["errors"] or [f"combine.py exited with code {proc.returncode}."]
            return result
        result.update(ok=True, out_name=out_name, data=out_path.read_bytes())
        return result


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Verto Wave Proposal Builder", page_icon="📄", layout="wide")
init_state()

st.title("Verto Wave Proposal Builder")
st.caption("Build a DeviceX/SDX & StackX technical proposal from the modular template. "
           "Work through the tabs from left to right, then build. Pricing is excluded by design.")

included, skipped, context = combine.plan_modules(INDEX, selected_tokens(), current_offering() or ["licenses"])

with st.sidebar:
    st.header("Cover logo")
    logo_upload = st.file_uploader("Upload a logo (PNG / JPG)", type=["png", "jpg", "jpeg"],
                                   help="Replaces the default logo on the cover page for this build.")
    use_default_logo = st.checkbox("Use the default Verto Wave logo when none is uploaded",
                                   value=DEFAULT_LOGO.exists(), disabled=not DEFAULT_LOGO.exists())
    out_name = st.text_input("Output filename", value="proposal.docx")
    st.divider()
    st.metric("Sections in this proposal", len(included))
    filled = sum(1 for s in SLOTS if str(st.session_state.get(s, "")).strip())
    st.metric("Values filled", filled, delta=f"of {len(SLOTS)}", delta_color="off")
    st.button("Start a new proposal (reset)", on_click=reset_to_example)

tabs = st.tabs(["1 · Offering", "2 · Modules", "3 · Sections", "4 · Customer", "5 · Compliance matrix",
                "6 · Review & build"])

with tabs[0]:
    st.subheader("What are we offering?")
    st.caption("The offering decides which sections, clauses and lines appear. Anything that does not apply is left out.")
    for flag, label in OFFERING_LABELS.items():
        st.checkbox(label, key=f"off_{flag}", help=OFFERING_HELP[flag])
    if not current_offering():
        st.error("Select at least one offering.")
    if st.session_state.get("off_premier_support") and not st.session_state.get("off_licenses"):
        st.warning("Premier Support applies to licensed software — select software licenses as well.")

for tab, group_key in ((tabs[1], "devicex_sdx"), (tabs[1], "stackx")):
    with tab:
        group = GROUPS[group_key]
        with st.expander(group["group"], expanded=True):
            st.caption(group.get("description", ""))
            for mod in group["modules"]:
                token = mod["token"]
                st.checkbox(mod["name"], key=f"mod_{token}", help=mod.get("notes") or mod.get("summary"))
                if st.session_state.get(f"mod_{token}") and token in skipped:
                    st.caption(f"↳ Left out: requires {mod['requires'].replace('_', ' ')}.")

with tabs[2]:
    optional = GROUPS["optional_sections"]
    with st.expander(optional["group"], expanded=True):
        st.caption(optional.get("description", ""))
        for mod in optional["modules"]:
            token = mod["token"]
            st.checkbox(mod["name"], key=f"mod_{token}", help=mod.get("summary"))
            if st.session_state.get(f"mod_{token}") and token in skipped:
                st.caption(f"↳ Left out: requires {mod['requires'].replace('_', ' ')}.")
    cross = GROUPS["cross_cutting"]
    with st.expander(cross["group"], expanded=False):
        st.caption(cross.get("description", ""))
        for mod in cross["modules"]:
            token = mod["token"]
            st.checkbox(mod["name"], key=f"mod_{token}", help=mod.get("summary"))
            if st.session_state.get(f"mod_{token}") and token in skipped:
                st.caption(f"↳ Left out: requires {mod['requires'].replace('_', ' ')}.")
    st.radio("Table of contents depth", [1, 2], key="toc_levels", horizontal=True,
             format_func=lambda n: "Main sections only" if n == 1 else "Sections and subsections")

with tabs[3]:
    with st.expander("Draft the customer profile with Hermes (a person must approve it)", expanded=False):
        st.caption("Hermes searches public web pages and drafts the executive-summary fields. Nothing is used "
                   "until you review it, choose what to keep and approve it with your name.")
        hint = st.text_input("Anything Hermes should know (optional)", key="ai_hint",
                             placeholder="e.g. the customer's sector or country")
        name = str(st.session_state.get("customer_name", "")).strip()
        if st.button("Research the customer with Hermes", disabled=not name):
            with st.spinner("Hermes is researching — this can take a few minutes…"):
                try:
                    draft = hermes_research.draft(name, str(st.session_state.get("customer_short", "")), hint)
                    st.session_state.ai_draft = draft
                    for field, suggestion in draft["fields"].items():
                        st.session_state[f"ai_text_{field}"] = suggestion
                        st.session_state[f"ai_use_{field}"] = bool(suggestion)
                except hermes_research.ResearchError as exc:
                    st.error(str(exc))
        draft = st.session_state.get("ai_draft")
        if draft:
            st.info("Review each suggestion. Untick anything you do not want to use.")
            for field in draft["fields"]:
                cols = st.columns([1, 5])
                cols[0].checkbox("Use", key=f"ai_use_{field}")
                cols[1].text_area(field, key=f"ai_text_{field}", height=90 if field == "customer_profile" else 68)
            if draft.get("sources"):
                st.markdown("**Sources**\n" + "\n".join(f"- {url}" for url in draft["sources"]))
            approver = st.text_input("Approved by (your name)", key="ai_approver")
            st.button("Approve and apply to the form", on_click=apply_ai_draft, disabled=not approver.strip(),
                      type="primary")
        message = st.session_state.pop("ai_message", None)
        if message:
            st.success(message)

    for title, caption, spec, token in SLOT_GROUPS:
        names = [s for s in SLOTS if s.startswith(spec)] if isinstance(spec, str) else [s for s in spec if s in SLOTS]
        needed = token is None or token in context
        with st.expander(title, expanded=needed and token is None):
            if caption:
                st.caption(caption)
            if not needed:
                st.info(f"Not used in this proposal — {MODULES[token]['name']} is not included.")
            for slot in names:
                if slot in TEXT_AREAS:
                    st.text_area(slot, key=slot, help=SLOTS.get(slot, ""))
                else:
                    st.text_input(slot, key=slot, help=SLOTS.get(slot, ""))

with tabs[4]:
    if "section_compliance_matrix" not in context:
        st.info("Tick “Compliance Matrix” in the Sections tab to include this appendix.")
    st.caption("Upload the RFP's requirement list as CSV (from Excel: File → Save As → CSV UTF-8). Columns: "
               "Ref, Requirement, Code, Response, Section — only Requirement is mandatory. Then edit the rows below.")
    uploaded = st.file_uploader("Requirements CSV", type=["csv"], key="req_csv")
    if uploaded is not None and st.button("Load requirements from the CSV"):
        try:
            set_compliance_rows(parse_requirements_csv(uploaded.getvalue()))
            st.success(f"Loaded {len(st.session_state.compliance_rows)} requirements.")
        except (UnicodeDecodeError, ValueError, csv.Error) as exc:
            st.error(f"Could not read the CSV: {exc}")
    frame = pd.DataFrame(st.session_state.compliance_base or [], columns=list(HEADER_ALIASES))
    edited = st.data_editor(
        frame, num_rows="dynamic", use_container_width=True,
        key=f"compliance_editor_{st.session_state.editor_version}",
        column_config={
            "ref": st.column_config.TextColumn("Ref.", width="small"),
            "requirement": st.column_config.TextColumn("Requirement", width="large"),
            "code": st.column_config.SelectboxColumn("Code", options=CODES, width="small"),
            "response": st.column_config.TextColumn("Verto Wave response", width="large"),
            "section": st.column_config.TextColumn("Section", width="medium"),
        },
    )
    st.session_state.compliance_rows = edited.fillna("").to_dict("records")
    st.caption("Codes: C-DX / C-SX native DeviceX / StackX · CC on configuration · IS integrated solution · "
               "AS assurance and supervision · PC partial · NC not compliant.")

with tabs[5]:
    st.subheader("This proposal will contain")
    names = combine.display_names(INDEX)
    st.markdown("\n".join(f"{i}. {names[t]}" for i, t in enumerate(included, 1)) or "_Nothing selected._")
    if skipped:
        st.caption("Left out because they do not apply to the offering: " + ", ".join(names[t] for t in skipped))
    st.subheader("Build")
    mode = st.radio("Output", [MODE_DRAFT, MODE_ISSUE], key="build_mode", horizontal=True)
    st.caption("A draft keeps bid-team notes and figure placeholders, highlighted. An issue copy removes them and is "
               "refused while any value used by the proposal is blank." if mode == MODE_DRAFT else
               "Removes all bid-team notes and figure placeholders. Refused while any value used by the proposal is blank.")
    if st.button("Build proposal", type="primary"):
        with st.spinner("Building…"):
            st.session_state.build_result = run_build(logo_upload, use_default_logo, out_name, mode == MODE_ISSUE)
    result = st.session_state.build_result
    if result:
        if result["ok"]:
            st.success(f"Build complete — {result['out_name']}")
            st.download_button("Download proposal .docx", data=result["data"], file_name=result["out_name"],
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               type="primary")
        else:
            for error in result["errors"]:
                st.error(error)
        if result.get("to_confirm"):
            st.warning("Values still to confirm: " + result["to_confirm"])
        for warning in result["warnings"]:
            st.warning(warning)
        with st.expander("Build log"):
            st.code(result["log"] or "(empty)")

    st.divider()
    st.subheader("Save or load this bid")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download the bid file (JSON)",
                           data=json.dumps(bid_file(), indent=2, ensure_ascii=False).encode("utf-8"),
                           file_name="proposal_bid.json", mime="application/json",
                           help="Values, offering, modules and compliance matrix — load it again to continue.")
    with col2:
        st.file_uploader("Load a bid file or values JSON", type=["json"], key="bid_upload", on_change=load_bid_file)
    message = st.session_state.pop("upload_message", None)
    if message:
        (st.success if message[0] == "success" else st.error)(message[1])
