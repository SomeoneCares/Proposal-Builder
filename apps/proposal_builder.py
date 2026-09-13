#!/usr/bin/env python3
"""
VertoWave Proposal Builder — Streamlit web UI.

Fill in customer values, pick modules, optionally upload a logo, and build
a Word .docx proposal by calling combine.py. The built file is offered for
download in the browser.

Run:
    streamlit run proposal_builder.py --server.address 0.0.0.0 --server.port 8501
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Paths (relative to this script's location = skill root)
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parents[1]
COMBINE_PY = HERE / "combine.py"
MODULE_INDEX = HERE / "module_index.json"
VALUES_EXAMPLE = HERE / "values-example.json"
VENV_PYTHON = Path("/home/hermes/.hermes/hermes-agent/venv/bin/python")
DEFAULT_LOGO = HERE / "assets" / "vertowave_logo.png"

# ---------------------------------------------------------------------------
# Load schema + example once
# ---------------------------------------------------------------------------
with MODULE_INDEX.open("r", encoding="utf-8") as f:
    INDEX = json.load(f)

with VALUES_EXAMPLE.open("r", encoding="utf-8") as f:
    EXAMPLE_VALUES = json.load(f)

SLOTS = INDEX["customer_slots"]  # dict: slot_name -> description

MODULE_GROUPS = [
    (
        "DeviceX/SDX — edge & branch layer",
        INDEX["modules"]["devicex_sdx"]["modules"],
        INDEX["modules"]["devicex_sdx"].get("description", ""),
    ),
    (
        "StackX — control / orchestration / SOC / operations layer",
        INDEX["modules"]["stackx"]["modules"],
        INDEX["modules"]["stackx"].get("description", ""),
    ),
    (
        "Cross-cutting / reusable sections",
        INDEX["modules"]["cross_cutting"]["modules"],
        INDEX["modules"]["cross_cutting"].get("description", ""),
    ),
]

SLOT_GROUPS = [
    ("Customer Identity", [
        "customer_name", "customer_short", "rfp_reference",
        "customer_primary_contact", "compliance_frameworks",
    ]),
    ("Proposal Metadata", [
        "proposal_version", "proposal_status", "proposal_date",
        "proposal_date_iso", "author_name", "prepared_by",
        "engagement_name", "effective_date", "validity_period_months",
    ]),
    ("Executive Summary Content", [
        "esg_footprint", "esg_value_1", "esg_value_2", "esg_outcome",
        "esg_example_a", "esg_example_b", "deployment_context",
        "objective_1", "objective_4", "objective_5",
    ]),
    ("Scope Description", [
        "scope_services_description", "site_count", "devicex_qty_note",
    ]),
]

REQUIRED_TOKENS = {
    mod["token"] for group in INDEX["modules"].values()
    for mod in group.get("modules", [])
    if mod.get("required", False)
}

# ---------------------------------------------------------------------------
# Initialise session state from example values (once)
# ---------------------------------------------------------------------------
def _ensure_state() -> None:
    for slot in SLOTS:
        if slot not in st.session_state:
            st.session_state[slot] = EXAMPLE_VALUES.get(slot, "")
    for group_name, mods, _desc in MODULE_GROUPS:
        for mod in mods:
            key = f"mod_{mod['token']}"
            if key not in st.session_state:
                st.session_state[key] = mod.get("required", False)
    if "build_result" not in st.session_state:
        st.session_state.build_result = None


def current_values() -> dict:
    return {slot: st.session_state.get(slot, "") for slot in SLOTS}


def selected_module_tokens() -> list[str]:
    out: list[str] = []
    for _group_name, mods, _desc in MODULE_GROUPS:
        for mod in mods:
            key = f"mod_{mod['token']}"
            if st.session_state.get(key, False):
                out.append(mod["token"])
    return out


def module_count() -> int:
    return len(selected_module_tokens())


def filled_slot_count() -> int:
    return sum(1 for slot in SLOTS if str(st.session_state.get(slot, "")).strip())


def reset_to_example() -> None:
    for slot in SLOTS:
        st.session_state[slot] = EXAMPLE_VALUES.get(slot, "")
    for group_name, mods, _desc in MODULE_GROUPS:
        for mod in mods:
            st.session_state[f"mod_{mod['token']}"] = mod.get("required", False)
    st.session_state.build_result = None


# ---------------------------------------------------------------------------
# Build engine (defined before the UI code that calls it)
# ---------------------------------------------------------------------------
def _run_build(logo_file, out_name: str) -> None:
    out_name = out_name.strip() or "proposal.docx"
    if not out_name.lower().endswith(".docx"):
        out_name += ".docx"

    with tempfile.TemporaryDirectory(prefix="vw_proposal_") as tmp:
        tmp_path = Path(tmp)
        values_path = tmp_path / "values.json"
        values_path.write_text(
            json.dumps(current_values(), indent=2), encoding="utf-8"
        )

        selected = selected_module_tokens()
        modules_arg = ",".join(selected) if selected else ""

        cmd = [
            str(VENV_PYTHON), str(COMBINE_PY),
            "--values", str(values_path),
            "--mode", "complete",
        ]
        if modules_arg:
            cmd += ["--modules", modules_arg]
        out_path = tmp_path / out_name
        cmd += ["--out", str(out_path)]
        if logo_file is not None and logo_file.size > 0:
            logo_path = tmp_path / "logo.png"
            logo_path.write_bytes(logo_file.read())
            cmd += ["--logo", str(logo_path)]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )
        except subprocess.TimeoutExpired:
            st.session_state.build_result = {
                "ok": False,
                "error": "Build timed out after 180s.",
                "log": "",
            }
            return
        except Exception as exc:
            st.session_state.build_result = {
                "ok": False,
                "error": f"Build failed to start: {exc}",
                "log": "",
            }
            return

        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            st.session_state.build_result = {
                "ok": False,
                "error": f"combine.py exited with code {proc.returncode}.",
                "log": log,
            }
            return

        if not out_path.exists():
            st.session_state.build_result = {
                "ok": False,
                "error": "combine.py reported success but no output file was produced.",
                "log": log,
            }
            return

        try:
            data = out_path.read_bytes()
        except Exception as exc:
            st.session_state.build_result = {
                "ok": False,
                "error": f"Could not read output file: {exc}",
                "log": log,
            }
            return

        st.session_state.build_result = {
            "ok": True,
            "out_name": out_name,
            "data": data,
            "log": log,
        }


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="VertoWave Proposal Builder", page_icon="📄")

st.title("VertoWave Proposal Builder")
st.caption(
    "Build a DeviceX/SDX & StackX technical proposal .docx from the modular "
    "template. Fill customer values, select modules, optionally upload a logo, "
    "then build and download. Pricing is excluded by design — attach separately."
)

_ensure_state()

with st.sidebar:
    st.header("Cover Logo")
    logo_file = st.file_uploader(
        "Upload logo (PNG / JPG)",
        type=["png", "jpg", "jpeg"],
        help="Upload the Verto Wave logo (or an approved logo) to embed on the cover page. "
             "Leave blank to build without a logo.",
    )
    if DEFAULT_LOGO.exists():
        st.caption("Default logo on disk: assets/vertowave_logo.png")
    out_name = st.text_input(
        "Output filename",
        value="proposal.docx",
        help="Name of the .docx file you will download after build.",
    )
    if not out_name.strip().lower().endswith(".docx"):
        out_name = out_name.strip() + ".docx"

    st.divider()
    st.metric("Modules selected", module_count())
    st.metric("Values fields filled", filled_slot_count(), delta=f"of {len(SLOTS)}")
    required_missing = [t for t in REQUIRED_TOKENS if not st.session_state.get(f"mod_{t}", False)]
    if required_missing:
        st.warning("Required modules unchecked: " + ", ".join(required_missing))

    if st.button("Reset to example values", type="secondary"):
        reset_to_example()
        st.rerun()

# ---------------------------------------------------------------------------
# Tab 1 — Customer Details
# ---------------------------------------------------------------------------
tab_values, tab_modules, tab_review = st.tabs(
    ["Customer Details", "Modules", "Review & Build"]
)

with tab_values:
    st.subheader("Customer values")
    st.caption("Edit the fields below. Each field maps to a {{customer_*}} or {{proposal_*}} token in the proposal.")
    for group_name, slots in SLOT_GROUPS:
        with st.expander(group_name, expanded=True):
            for slot in slots:
                desc = SLOTS.get(slot, "")
                cur = st.session_state.get(slot, "")
                st.text_input(
                    slot,
                    value=cur,
                    key=slot,
                    help=desc,
                    placeholder="",
                )

# ---------------------------------------------------------------------------
# Tab 2 — Modules
# ---------------------------------------------------------------------------
with tab_modules:
    st.subheader("Module selection")
    st.caption(
        "Pick the capability modules to include. Required modules are checked by "
        "default. Each module's note explains its provenance and when to include it."
    )
    for group_name, mods, desc in MODULE_GROUPS:
        with st.expander(group_name, expanded=True):
            if desc:
                st.info(desc)
            for mod in mods:
                token = mod["token"]
                st.checkbox(
                    mod["name"],
                    key=f"mod_{token}",
                    value=st.session_state.get(f"mod_{token}", mod.get("required", False)),
                    help=mod.get("notes", ""),
                    disabled=False,
                )

# ---------------------------------------------------------------------------
# Tab 3 — Review & Build
# ---------------------------------------------------------------------------
with tab_review:
    st.subheader("Review")
    st.markdown("### Customer values (JSON)")
    st.json(current_values(), expanded=False)

    st.markdown("### Selected modules")
    selected = selected_module_tokens()
    if selected:
        for tok in selected:
            found = None
            for _gn, mods, _d in MODULE_GROUPS:
                for m in mods:
                    if m["token"] == tok:
                        found = m
                        break
                if found:
                    break
            if found:
                st.markdown(f"- **{found['name']}**  `{tok}`")
                if found.get("notes"):
                    st.caption(found["notes"])
    else:
        st.warning("No modules selected. At least the required cross-cutting sections are recommended.")

    st.markdown("### Build")
    with st.form("build_form"):
        st.markdown(
            "Press **Build Proposal** to assemble the .docx. The file is built in "
            "memory and offered for download below. No file is written to disk "
            "outside the builder."
        )
        build_pressed = st.form_submit_button("Build Proposal", type="primary")

    if build_pressed:
        _run_build(logo_file, out_name)

    if st.session_state.build_result:
        res = st.session_state.build_result
        if res.get("ok"):
            st.success(f"Build complete — {res['out_name']}")
            st.download_button(
                label="Download proposal .docx",
                data=res["data"],
                file_name=res["out_name"],
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
            )
        else:
            st.error(res.get("error", "Build failed"))
        with st.expander("Build log"):
            st.code(res.get("log", ""))

    st.divider()
    st.markdown(
        "### Reusable values sheet (optional)"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download current values as JSON",
            data=json.dumps(current_values(), indent=2).encode("utf-8"),
            file_name="proposal_values_current.json",
            mime="application/json",
            help="Save the current form values to a JSON file you can re-upload on the next bid.",
        )
    with col2:
        uploaded = st.file_uploader(
            "Upload a values JSON to prefill",
            type=["json"],
            help="Load a previously saved values sheet to prefill the form.",
        )
        if uploaded is not None:
            try:
                loaded = json.loads(uploaded.read().decode("utf-8"))
                for slot in SLOTS:
                    if slot in loaded and loaded[slot]:
                        st.session_state[slot] = loaded[slot]
                st.success("Values loaded from JSON.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not read values JSON: {exc}")


# ---------------------------------------------------------------------------
# Build engine
# ---------------------------------------------------------------------------
def _run_build(logo_file, out_name: str) -> None:
    out_name = out_name.strip() or "proposal.docx"
    if not out_name.lower().endswith(".docx"):
        out_name += ".docx"

    with tempfile.TemporaryDirectory(prefix="vw_proposal_") as tmp:
        tmp_path = Path(tmp)
        values_path = tmp_path / "values.json"
        values_path.write_text(
            json.dumps(current_values(), indent=2), encoding="utf-8"
        )

        selected = selected_module_tokens()
        modules_arg = ",".join(selected) if selected else ""

        cmd = [
            str(VENV_PYTHON), str(COMBINE_PY),
            "--values", str(values_path),
            "--mode", "complete",
        ]
        if modules_arg:
            cmd += ["--modules", modules_arg]
        out_path = tmp_path / out_name
        cmd += ["--out", str(out_path)]
        if logo_file is not None and logo_file.size > 0:
            logo_path = tmp_path / "logo.png"
            logo_path.write_bytes(logo_file.read())
            cmd += ["--logo", str(logo_path)]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
            )
        except subprocess.TimeoutExpired:
            st.session_state.build_result = {
                "ok": False,
                "error": "Build timed out after 180s.",
                "log": "",
            }
            return
        except Exception as exc:
            st.session_state.build_result = {
                "ok": False,
                "error": f"Build failed to start: {exc}",
                "log": "",
            }
            return

        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            st.session_state.build_result = {
                "ok": False,
                "error": f"combine.py exited with code {proc.returncode}.",
                "log": log,
            }
            return

        if not out_path.exists():
            st.session_state.build_result = {
                "ok": False,
                "error": "combine.py reported success but no output file was produced.",
                "log": log,
            }
            return

        try:
            data = out_path.read_bytes()
        except Exception as exc:
            st.session_state.build_result = {
                "ok": False,
                "error": f"Could not read output file: {exc}",
                "log": log,
            }
            return

        st.session_state.build_result = {
            "ok": True,
            "out_name": out_name,
            "data": data,
            "log": log,
        }
