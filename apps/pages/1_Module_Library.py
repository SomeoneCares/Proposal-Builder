"""
Module Library — read, edit, upload and version the proposal modules.

Editing needs the password in PROPOSAL_EDITOR_PASSWORD (set on the host in
~/.config/proposal-builder.env). Versions are kept in PROPOSAL_LIBRARY_DIR and
override the deployed modules until reverted; scripts/pull-library.sh brings them
into git.
"""

from __future__ import annotations

import hmac
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
import combine  # noqa: E402
import library  # noqa: E402
import vw_theme  # noqa: E402

vw_theme.page("Module library", "Proposal content — versioned and audited", icon="📚")
vw_theme.nav()

INDEX = combine.load_index(ROOT / "module_index.json")
PASSWORD = os.environ.get("PROPOSAL_EDITOR_PASSWORD", "")
LIBRARY_DIR = library.default_library_dir()

if not PASSWORD:
    st.error("Editing is disabled: no editor password is configured on the server (PROPOSAL_EDITOR_PASSWORD).")
    st.stop()
if LIBRARY_DIR is None:
    st.error("Editing is disabled: no library folder is configured on the server (PROPOSAL_LIBRARY_DIR).")
    st.stop()

if not st.session_state.get("editor_unlocked"):
    password = st.text_input("Editor password", type="password")
    if st.button("Unlock"):
        if hmac.compare_digest(password.encode("utf-8"), PASSWORD.encode("utf-8")):
            st.session_state.editor_unlocked = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()

lib = library.Library(LIBRARY_DIR, INDEX, ROOT)
MODULES = {mod["token"]: mod for mod in combine.iter_modules(INDEX)}
GROUP_SHORT = {"devicex_sdx": "DeviceX", "stackx": "StackX", "optional_sections": "Optional", "cross_cutting": "Standard"}

with st.sidebar:
    vw_theme.side_label("Editor")
    author = st.text_input("Your name (recorded with each version)", key="editor_name")
    if st.button("Lock the editor"):
        st.session_state.editor_unlocked = False
        st.rerun()


def label(token: str) -> str:
    mod = MODULES[token]
    edited = " · edited" if lib.is_overridden(token) or lib.is_overridden(token, True) else ""
    return f"{GROUP_SHORT.get(combine.module_group(INDEX, token), '')} — {mod['name']}{edited}"


token = st.selectbox("Module", list(MODULES), format_func=label)

# A product with two write-ups keeps them apart: each is edited, versioned and
# reverted on its own, and a proposal picks between them in the builder's step 2.
long = False
if lib.has_long(token):
    choice = st.radio("Write-up", ["Short", "Long"], horizontal=True, key=f"writeup_{token}",
                      help="Short is the original write-up. Long carries the product's components, "
                           "integration, exclusions, acceptance and hardware. They are separate texts "
                           "with separate histories; a proposal uses one or the other.")
    long = choice == "Long"
else:
    st.caption("This module has one write-up.")

history = lib.history(token, long)
versions = [e for e in history if "version" in e]
if lib.is_overridden(token, long) and versions:
    last = versions[-1]
    st.caption(f"In use: version {last['version']}, saved by {last['author']} on {last['saved_at']} — {last['note']}")
else:
    st.caption("In use: the deployed baseline from the repository.")

tab_preview, tab_edit, tab_upload, tab_history = st.tabs(["Preview", "Edit", "Upload a new version", "History"])

with tab_preview:
    st.caption("The preview shows every conditional block; each proposal shows only what applies to it. "
               "Tokens such as {{customer_short}} are filled at build time.")
    st.markdown(combine.prepare_module_text(lib.current_text(token, long)))

with tab_edit:
    st.caption("Rules: US spelling, the brand is Verto Wave, no prior-customer or third-party product names, "
               "conditions as <!-- if module_x --> — see references/module_authoring.md.")
    text = st.text_area("Markdown", value=lib.current_text(token, long), height=560,
                        key=f"edit_{token}_{long:d}")
    note = st.text_input("What changed and why (required)", key=f"note_{token}_{long:d}")
    col1, col2 = st.columns(2)
    if col1.button("Check", key=f"check_{token}_{long:d}"):
        problems = library.validate_module_text(text, INDEX, token)
        if problems:
            for problem in problems:
                st.error(problem)
        else:
            st.success("No problems found.")
    if col2.button("Save as a new version", type="primary", key=f"save_{token}_{long:d}",
                   disabled=not (author.strip() and note.strip())):
        try:
            entry = lib.save(token, text, author, note, long=long)
            st.success(f"Saved version {entry['version']}. New builds use it immediately.")
        except ValueError as exc:
            st.error(f"Not saved: {exc}")
    if not (author.strip() and note.strip()):
        st.caption("Enter your name in the sidebar and a change note to save.")

with tab_upload:
    uploaded = st.file_uploader("Module file (.md)", type=["md"], key=f"upload_{token}_{long:d}")
    upload_note = st.text_input("What changed and why (required)", key=f"upload_note_{token}_{long:d}")
    if uploaded is not None:
        try:
            uploaded_text = uploaded.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            st.error("The file must be UTF-8 text.")
            uploaded_text = ""
        if uploaded_text:
            problems = library.validate_module_text(uploaded_text, INDEX, token)
            for problem in problems:
                st.error(problem)
            if not problems and st.button("Save the uploaded file as a new version", type="primary",
                                          disabled=not (author.strip() and upload_note.strip())):
                entry = lib.save(token, uploaded_text, author, upload_note, source="upload", long=long)
                st.success(f"Saved version {entry['version']}.")

with tab_history:
    if history:
        st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    else:
        st.caption("No versions saved yet — the deployed baseline is in use.")
    if versions:
        chosen = st.selectbox("Version", [e["version"] for e in versions][::-1],
                              key=f"version_{token}_{long:d}")
        st.code(lib.version_text(token, chosen, long), language="markdown")
        col1, col2 = st.columns(2)
        if col1.button(f"Restore version {chosen}", key=f"restore_{token}_{long:d}",
                       disabled=not author.strip()):
            entry = lib.restore(token, chosen, author, long)
            st.success(f"Restored as version {entry['version']}.")
        if col2.button("Revert to the deployed baseline", key=f"revert_{token}_{long:d}",
                       disabled=not (author.strip() and lib.is_overridden(token, long))):
            lib.revert_to_baseline(token, author, long)
            st.success("The deployed baseline is in use again.")
    st.download_button("Download the version in use (.md)", data=lib.current_text(token, long).encode("utf-8"),
                       file_name=Path(MODULES[token].get("long_file") if long else MODULES[token]["file"]).name,
                       mime="text/markdown")

st.divider()
st.subheader("Figures")
st.caption("Each [[figure: name | caption]] in a module shows the image uploaded here. Without an image, drafts show "
           "a placeholder and issue copies leave the figure out. Use generic diagrams only — no customer names.")
refs = lib.figure_references()
if refs:
    st.dataframe(pd.DataFrame([{"figure": r["slug"], "module": r["module"], "caption": r["caption"],
                                "image": "uploaded" if r["image"] else "—"} for r in refs]),
                 use_container_width=True, hide_index=True)
    slug = st.selectbox("Figure", [r["slug"] for r in refs], key="figure_slug")
    current = next(r for r in refs if r["slug"] == slug)
    if current["image"]:
        st.image(current["image"], caption=current["caption"])
    image = st.file_uploader("Image (PNG / JPG)", type=["png", "jpg", "jpeg"], key=f"figure_{slug}")
    if image is not None and st.button("Save figure", disabled=not author.strip()):
        path = lib.save_figure(slug, image.getvalue(), Path(image.name).suffix)
        st.success(f"Saved {path.name}. New builds use it immediately.")
