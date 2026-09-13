#!/usr/bin/env python3
"""
VertoWave Proposal Builder — Streamlit web UI around combine.py.

Fill in the proposal values, tick the modules, choose a draft or an issue copy
and download the .docx. On the lab host this runs as the systemd user unit
`proposal-builder`:

    streamlit run apps/proposal_builder.py --server.address 0.0.0.0 --server.port 8501
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
COMBINE_PY = ROOT / "combine.py"
MODULE_INDEX = ROOT / "module_index.json"
VALUES_EXAMPLE = ROOT / "values-example.json"
DEFAULT_LOGO = ROOT / "assets" / "vertowave_logo.png"

INDEX = json.loads(MODULE_INDEX.read_text(encoding="utf-8"))
EXAMPLE_VALUES = json.loads(VALUES_EXAMPLE.read_text(encoding="utf-8"))
SLOTS: dict[str, str] = INDEX["customer_slots"]

MODULE_GROUPS = [
    (group["group"], group.get("description", ""), group["modules"])
    for key in ("devicex_sdx", "stackx", "cross_cutting")
    if (group := INDEX["modules"].get(key))
]
ALL_MODULES = [mod for _label, _desc, mods in MODULE_GROUPS for mod in mods]
MODULE_NAMES = {mod["token"]: mod["name"] for mod in ALL_MODULES}
REQUIRED_TOKENS = [mod["token"] for mod in ALL_MODULES if mod.get("required")]

BLANK_RULE = "Blank fields are marked TO CONFIRM in a draft and block an issue copy."
# (title, caption, slot names or a slot-name prefix, module token that uses the slots)
SLOT_GROUPS = [
    ("Customer", None,
     ["customer_name", "customer_short", "customer_primary_contact", "rfp_reference"], None),
    ("Proposal", None,
     ["proposal_title", "proposal_subtype", "engagement_name", "prepared_by", "author_name",
      "proposal_version", "proposal_status", "proposal_date", "proposal_date_iso",
      "effective_date", "validity_period_months"], None),
    ("Executive summary",
     "Short phrases that complete the executive-summary sentences. Rewrite the summary in Word "
     "if it does not fit the customer.",
     ["esg_footprint", "esg_value_1", "esg_value_2", "esg_outcome", "esg_example_a", "esg_example_b",
      "scope_services_description", "deployment_context", "objective_1", "objective_4", "objective_5"], None),
    ("Service-quality targets", f"Used by the SD-WAN module's targets table. {BLANK_RULE}",
     "ola_", "module_sdwan"),
    ("Professional Services scope numbers",
     f"Used by the Professional Services section. Every number tightens the scope. {BLANK_RULE}",
     "services_", "section_professional_services"),
]
MODE_DRAFT = "Draft for internal review"
MODE_ISSUE = "Issue copy"


def slot_groups() -> list[tuple[str, str | None, list[str], str | None]]:
    used: set[str] = set()
    groups = []
    for title, caption, spec, token in SLOT_GROUPS:
        if isinstance(spec, str):
            names = [slot for slot in SLOTS if slot.startswith(spec)]
        else:
            names = [slot for slot in spec if slot in SLOTS]
        used.update(names)
        groups.append((title, caption, names, token))
    rest = [slot for slot in SLOTS if slot not in used]
    if rest:
        groups.append(("Other", "Not used by any module yet.", rest, None))
    return groups


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def init_state() -> None:
    for slot in SLOTS:
        st.session_state.setdefault(slot, str(EXAMPLE_VALUES.get(slot, "")))
    for mod in ALL_MODULES:
        st.session_state.setdefault(f"mod_{mod['token']}", bool(mod.get("required")))
    st.session_state.setdefault("build_result", None)


def reset_to_example() -> None:
    for slot in SLOTS:
        st.session_state[slot] = str(EXAMPLE_VALUES.get(slot, ""))
    for mod in ALL_MODULES:
        st.session_state[f"mod_{mod['token']}"] = bool(mod.get("required"))
    st.session_state.build_result = None


def load_values_upload() -> None:
    """on_change callback: runs before the widgets, so it may set their state."""
    uploaded = st.session_state.get("values_upload")
    if uploaded is None:
        return
    try:
        loaded = json.loads(uploaded.getvalue().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        st.session_state.upload_message = ("error", f"Could not read values JSON: {exc}")
        return
    if not isinstance(loaded, dict):
        st.session_state.upload_message = ("error", "The values JSON must be an object of key/value pairs.")
        return
    count = 0
    for slot in SLOTS:
        if loaded.get(slot) not in (None, ""):
            st.session_state[slot] = str(loaded[slot])
            count += 1
    st.session_state.upload_message = ("success", f"Loaded {count} values from {uploaded.name}.")


def current_values() -> dict:
    return {slot: st.session_state.get(slot, "") for slot in SLOTS}


def selected_tokens() -> list[str]:
    return [mod["token"] for mod in ALL_MODULES if st.session_state.get(f"mod_{mod['token']}")]


def filled_slot_count() -> int:
    return sum(1 for slot in SLOTS if str(st.session_state.get(slot, "")).strip())


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def run_build(logo_upload, use_default_logo: bool, out_name: str, issue: bool) -> dict:
    selected = selected_tokens()
    if not selected:
        return {"ok": False, "errors": ["Select at least one module."], "warnings": [], "log": ""}
    out_name = Path(out_name.strip() or "proposal.docx").name
    if not out_name.lower().endswith(".docx"):
        out_name += ".docx"

    with tempfile.TemporaryDirectory(prefix="vw_proposal_") as tmp:
        tmp_path = Path(tmp)
        values_path = tmp_path / "values.json"
        values_path.write_text(json.dumps(current_values(), indent=2, ensure_ascii=False), encoding="utf-8")
        out_path = tmp_path / out_name
        cmd = [
            sys.executable, str(COMBINE_PY),
            "--values", str(values_path),
            "--mode", "complete",
            "--modules", ",".join(selected),
            "--out", str(out_path),
        ]
        if issue:
            cmd.append("--issue")
        if logo_upload is not None:
            logo_path = tmp_path / f"logo{Path(logo_upload.name).suffix.lower() or '.png'}"
            logo_path.write_bytes(logo_upload.getvalue())
            cmd += ["--logo", str(logo_path)]
        elif use_default_logo and DEFAULT_LOGO.exists():
            cmd += ["--logo", str(DEFAULT_LOGO)]

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=str(ROOT))
        except subprocess.TimeoutExpired:
            return {"ok": False, "errors": ["Build timed out after 180 s."], "warnings": [], "log": ""}

        log = proc.stdout + proc.stderr
        lines = log.splitlines()
        errors = [line.removeprefix("ERROR: ") for line in lines if line.startswith("ERROR:")]
        warnings = [line.split(": ", 1)[1] for line in lines if line.startswith(("WARNING:", "NOTE:"))]
        to_confirm = next((line.removeprefix("TO CONFIRM: ") for line in lines if line.startswith("TO CONFIRM:")), "")
        result = {"errors": errors, "warnings": warnings, "to_confirm": to_confirm, "log": log}
        if proc.returncode != 0 or not out_path.exists():
            result["ok"] = False
            if not errors:
                result["errors"] = [f"combine.py exited with code {proc.returncode}."]
            return result
        result.update(ok=True, out_name=out_name, data=out_path.read_bytes())
        return result


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="VertoWave Proposal Builder", page_icon="📄", layout="wide")
init_state()

st.title("VertoWave Proposal Builder")
st.caption(
    "Build a DeviceX/SDX & StackX technical proposal (.docx) from the modular template. "
    "Fill in the values, tick the modules, then build and download. "
    "Pricing is excluded by design — attach it separately."
)

with st.sidebar:
    st.header("Cover logo")
    logo_upload = st.file_uploader(
        "Upload a logo (PNG / JPG)",
        type=["png", "jpg", "jpeg"],
        help="Replaces the default logo on the cover page for this build.",
    )
    use_default_logo = st.checkbox(
        "Use the default Verto Wave logo when none is uploaded",
        value=DEFAULT_LOGO.exists(),
        disabled=not DEFAULT_LOGO.exists(),
    )
    out_name = st.text_input("Output filename", value="proposal.docx")

    st.divider()
    st.metric("Modules selected", len(selected_tokens()))
    st.metric("Values filled", filled_slot_count(), delta=f"of {len(SLOTS)}", delta_color="off")
    unticked = [MODULE_NAMES[t] for t in REQUIRED_TOKENS if not st.session_state.get(f"mod_{t}")]
    if unticked:
        st.warning("Required modules unticked: " + ", ".join(unticked))
    st.button("Reset to example values", on_click=reset_to_example)

tab_values, tab_modules, tab_build = st.tabs(["Proposal values", "Modules", "Review & build"])

with tab_values:
    st.caption("Each field fills a {{token}} in the proposal. Hover a field name for what it is used for.")
    for title, caption, names, token in slot_groups():
        needed = token is None or st.session_state.get(f"mod_{token}", False)
        with st.expander(title, expanded=token is None or needed):
            if caption:
                st.caption(caption)
            if not needed:
                st.info(f"Not used in this build — the {MODULE_NAMES.get(token, token)} module is not ticked.")
            for slot in names:
                st.text_input(slot, key=slot, help=SLOTS.get(slot, ""))

with tab_modules:
    st.caption("Required modules are ticked by default. Hover a module for when to include it.")
    for label, description, mods in MODULE_GROUPS:
        with st.expander(label, expanded=True):
            if description:
                st.caption(description)
            for mod in mods:
                name = mod["name"] + ("  — placeholder, not for live bids" if mod.get("placeholder") else "")
                st.checkbox(name, key=f"mod_{mod['token']}", help=mod.get("notes", ""))

with tab_build:
    st.subheader("Selected modules")
    chosen = selected_tokens()
    if chosen:
        for token in chosen:
            st.markdown(f"- {MODULE_NAMES[token]}  `{token}`")
        placeholders = [MODULE_NAMES[m["token"]] for m in ALL_MODULES if m.get("placeholder") and m["token"] in chosen]
        if placeholders:
            st.warning("Placeholder modules selected (content not authored yet): " + ", ".join(placeholders))
    else:
        st.warning("No modules selected.")

    st.subheader("Build")
    mode = st.radio("Output", [MODE_DRAFT, MODE_ISSUE], key="build_mode", horizontal=True)
    if mode == MODE_DRAFT:
        st.caption("Keeps bid-team notes and figure placeholders, highlighted in yellow; "
                   "blank values show as [TO CONFIRM: …].")
    else:
        st.caption("Removes all bid-team notes and figure placeholders. "
                   "The build is refused while any value used by the selected modules is blank.")

    if st.button("Build proposal", type="primary"):
        with st.spinner("Building…"):
            st.session_state.build_result = run_build(logo_upload, use_default_logo, out_name, mode == MODE_ISSUE)

    result = st.session_state.build_result
    if result:
        if result["ok"]:
            st.success(f"Build complete — {result['out_name']}")
            st.download_button(
                label="Download proposal .docx",
                data=result["data"],
                file_name=result["out_name"],
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
            )
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
    st.subheader("Reusable values sheet")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download current values as JSON",
            data=json.dumps(current_values(), indent=2, ensure_ascii=False).encode("utf-8"),
            file_name="proposal_values.json",
            mime="application/json",
            help="Save the form so you can load it again for the next revision of this bid.",
        )
    with col2:
        st.file_uploader(
            "Load a values JSON",
            type=["json"],
            key="values_upload",
            on_change=load_values_upload,
            help="Fills the form from a previously saved values sheet.",
        )
    message = st.session_state.pop("upload_message", None)
    if message:
        (st.success if message[0] == "success" else st.error)(message[1])
