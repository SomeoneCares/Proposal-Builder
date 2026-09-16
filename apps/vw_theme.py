"""
The CRM look for the Streamlit pages.

Colors, spacing and type are taken from the Verto Wave CRM's own components so the
builder can move into the CRM later without changing how it looks:

    accent #4666dc · active nav #e9eeff · page ground #f8f9fc · hero navy #173969
    cards: white, 1px #e2e8f0, radius 10px, shadow 0 3px 14px rgba(30,41,59,.05)
    section titles: 13px, 700, uppercase, letter-spacing .08em

Use it as:

    import vw_theme
    vw_theme.page("Build proposal", "Commercial management platform")
    vw_theme.hero("Kicker", "Title", "One sentence.")
    vw_theme.kpis([("Modules included", "23", "blue"), ...])
"""

from __future__ import annotations

import html

import streamlit as st

ACCENT = "#4666dc"
NAVY = "#173969"

_CSS = """
<style>
:root{
  --vw-ground:#f8f9fc; --vw-surface:#ffffff; --vw-line:#e2e8f0; --vw-line-soft:#f1f5f9;
  --vw-ink:#0f172a; --vw-ink-2:#334155; --vw-ink-3:#64748b; --vw-ink-4:#94a3b8;
  --vw-accent:#4666dc; --vw-accent-hover:#3858cf; --vw-accent-soft:#e9eeff; --vw-accent-tint:#eff6ff;
  --vw-navy:#173969; --vw-shadow:0 3px 14px rgba(30,41,59,.05);
}

/* ---- page frame ------------------------------------------------------ */
[data-testid="stAppViewContainer"]{background:var(--vw-ground)}
[data-testid="stHeader"]{background:transparent}
[data-testid="stMainBlockContainer"]{padding:1.2rem 2rem 4rem;max-width:1440px}
/* Set the family on the container only and let it inherit: a `*` rule also hits
   Streamlit's icon spans, whose glyphs are ligatures in the Material font, and
   turns the upload, password-eye and chevron icons into stray words. */
[data-testid="stAppViewContainer"],[data-testid="stSidebar"]{font-family:ui-sans-serif,system-ui,-apple-system,
  "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
[data-testid="stIconMaterial"],.material-icons,.material-symbols-rounded,[class*="material-symbols"]{
  font-family:"Material Symbols Rounded","Material Icons" !important}

/* ---- top bar --------------------------------------------------------- */
.vw-top{display:flex;align-items:center;gap:16px;flex-wrap:wrap;background:var(--vw-surface);
  border:1px solid var(--vw-line);border-radius:10px;padding:12px 18px;margin-bottom:16px;box-shadow:var(--vw-shadow)}
.vw-top h1{margin:0;font-size:15px;font-weight:600;color:#1e293b;letter-spacing:-.01em}
.vw-top p{margin:1px 0 0;font-size:12px;color:var(--vw-ink-4)}
.vw-top .vw-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.vw-pill{display:inline-flex;align-items:center;gap:6px;border-radius:999px;background:#ecfdf5;color:#047857;
  padding:4px 11px;font-size:12px;font-weight:500}
.vw-pill i{width:6px;height:6px;border-radius:999px;background:currentColor;display:block}

/* ---- hero ------------------------------------------------------------ */
.vw-hero{border-radius:16px;background:var(--vw-navy);color:#fff;padding:22px 24px;margin-bottom:18px;
  box-shadow:0 10px 25px rgba(23,57,105,.18)}
.vw-hero .vw-kicker{margin:0;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.18em;color:#bfdbfe}
.vw-hero h2{margin:4px 0 0;font-size:28px;line-height:1.15;font-weight:600;letter-spacing:-.02em;color:#fff}
.vw-hero p{margin:8px 0 0;max-width:70ch;font-size:14px;color:#dbeafe}

/* ---- KPI row --------------------------------------------------------- */
.vw-kpis{display:grid;gap:12px;grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:18px}
@media(max-width:1100px){.vw-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:620px){.vw-kpis{grid-template-columns:1fr}}
.vw-kpi{display:flex;align-items:center;gap:14px;background:var(--vw-surface);border:1px solid var(--vw-line);
  border-radius:10px;padding:16px 18px;box-shadow:var(--vw-shadow)}
.vw-kpi .vw-tile{display:grid;place-items:center;width:42px;height:42px;border-radius:8px;flex:none;
  font-size:17px;font-weight:700}
.vw-kpi .vw-blue{background:var(--vw-accent-tint);color:var(--vw-accent)}
.vw-kpi .vw-violet{background:#f5f3ff;color:#7c3aed}
.vw-kpi .vw-emerald{background:#ecfdf5;color:#047857}
.vw-kpi .vw-amber{background:#fffbeb;color:#b45309}
.vw-kpi .vw-label{font-size:13px;font-weight:500;color:var(--vw-ink-3);line-height:1.3}
.vw-kpi .vw-value{margin-top:2px;font-size:20px;font-weight:700;letter-spacing:-.01em;color:#020617;
  font-variant-numeric:tabular-nums;line-height:1.2}

/* ---- sidebar --------------------------------------------------------- */
[data-testid="stSidebar"]{background:var(--vw-surface);border-right:1px solid var(--vw-line)}
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:.75rem}
.vw-brand{display:flex;align-items:center;gap:10px;padding:2px 0 12px;margin-bottom:10px;
  border-bottom:1px solid var(--vw-line-soft)}
.vw-brand .vw-mark{display:grid;place-items:center;width:32px;height:32px;border-radius:6px;flex:none;
  background:var(--vw-accent-tint);color:var(--vw-accent);font-size:15px;font-weight:800}
.vw-brand b{display:block;font-size:15px;font-weight:600;color:#0f172a;line-height:1.2}
.vw-brand span{display:block;font-size:10px;font-weight:500;text-transform:uppercase;letter-spacing:.16em;color:#3b82f6}
.vw-side-label{font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--vw-ink-4);
  margin:14px 0 2px}
/* Streamlit's own nav is replaced by vw_theme.nav(), which uses CRM wording */
[data-testid="stSidebarNav"]{display:none}
[data-testid="stSidebar"] [data-testid="stPageLink"] a{border-radius:6px;padding:6px 10px;margin:1px 0}
[data-testid="stSidebar"] [data-testid="stPageLink"] a p{font-size:13px;font-weight:500;color:#475569}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover{background:var(--vw-line-soft)}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink"] a.active{background:var(--vw-accent-soft)}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] p{color:var(--vw-accent);font-weight:600}

/* the uploader has to fit a 300px sidebar without clipping its button */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]{flex-direction:column;align-items:flex-start;
  gap:8px;padding:12px}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button{width:100%;white-space:nowrap}
[data-testid="stFileUploaderDropzoneInstructions"] span{font-size:12.5px}
[data-testid="stTextInput"] button{color:var(--vw-ink-3)}

/* ---- tabs as the CRM's segmented control -----------------------------
   Streamlit 1.63 renders a plain [role="tablist"] holding [data-testid="stTab"];
   older builds used data-baseweb. Both are matched so an upgrade cannot undo it. */
[data-testid="stTabs"] [role="tablist"],[data-testid="stTabs"] [data-baseweb="tab-list"]{
  gap:2px;background:#f1f5f9;border-radius:8px;padding:3px;border-bottom:0;width:fit-content;max-width:100%;
  flex-wrap:wrap;margin-bottom:6px}
[data-testid="stTabs"] [data-testid="stTab"],[data-testid="stTabs"] [data-baseweb="tab"]{
  height:32px;min-height:32px;border-radius:6px;padding:0 14px;color:#475569;font-size:13px;font-weight:500;
  border-bottom:0}
[data-testid="stTabs"] [data-testid="stTab"]:hover,[data-testid="stTabs"] [data-baseweb="tab"]:hover{
  background:#e8edf4;color:#0f172a}
[data-testid="stTabs"] [data-testid="stTab"] p,[data-testid="stTabs"] [data-baseweb="tab"] p{
  font-size:13px;font-weight:500}
[data-testid="stTabs"] [aria-selected="true"]{background:#fff;color:#0f172a;box-shadow:0 1px 2px rgba(15,23,42,.08)}
[data-testid="stTabs"] [aria-selected="true"] p{color:#0f172a;font-weight:600}
/* Streamlit draws the strip's grey rule and the selected tab's underline as
   ::after pseudo-elements; the CRM's segmented control has neither. */
[data-testid="stTabs"] [role="tablist"]::after,[data-testid="stTabs"] [role="tablist"]::before,
[data-testid="stTabs"] [data-testid="stTab"]::after,[data-testid="stTabs"] [data-testid="stTab"]::before,
[data-testid="stTabs"] [data-testid="stTab"] *::after,
[data-testid="stTabs"] [role="tablist"]>*:not([data-testid="stTab"]),
[data-testid="stTabs"] [data-baseweb="tab-highlight"],[data-testid="stTabs"] [data-baseweb="tab-border"]{
  display:none !important;content:none !important}
/* The moving highlight is an empty div painted with the theme's primary color and
   sits outside the tablist, so it is matched by shape: a childless, untagged div. */
[data-testid="stTabs"] div:not([data-testid]):not([role="tablist"]):not(:has(*)){
  background-color:transparent !important;height:0 !important}

/* ---- cards: expanders and bordered containers ------------------------ */
[data-testid="stExpander"],[data-testid="stVerticalBlockBorderWrapper"]:has(>div>[data-testid="stVerticalBlock"]){
  background:var(--vw-surface);border-radius:10px}
[data-testid="stExpander"]{border:1px solid var(--vw-line);box-shadow:var(--vw-shadow);overflow:hidden}
[data-testid="stExpander"] summary{padding:12px 18px;font-size:13px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:#1e293b}
[data-testid="stExpander"] summary:hover{color:var(--vw-accent)}
[data-testid="stExpander"] [data-testid="stExpanderDetails"]{padding:2px 18px 14px}

/* ---- headings and captions ------------------------------------------ */
[data-testid="stMainBlockContainer"] h2{font-size:20px;font-weight:700;letter-spacing:-.01em;color:#0f172a}
[data-testid="stMainBlockContainer"] h3{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:#1e293b}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:var(--vw-ink-3);font-size:12.5px}

/* ---- controls -------------------------------------------------------- */
[data-testid="stMainBlockContainer"] .stButton>button,[data-testid="stSidebar"] .stButton>button,
.stDownloadButton>button{height:36px;border-radius:6px;font-size:14px;font-weight:500;border:1px solid var(--vw-line);
  background:#fff;color:#334155;box-shadow:none;transition:background .12s,border-color .12s}
.stButton>button:hover,.stDownloadButton>button:hover{background:#f8fafc;border-color:#cbd5e1;color:#0f172a}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"]{background:var(--vw-accent);
  border-color:var(--vw-accent);color:#fff}
.stButton>button[kind="primary"]:hover,.stDownloadButton>button[kind="primary"]:hover{
  background:var(--vw-accent-hover);border-color:var(--vw-accent-hover);color:#fff}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input{
  border-radius:6px;font-size:14px}
[data-testid="stTextInput"] div[data-baseweb="input"],[data-testid="stTextArea"] div[data-baseweb="textarea"]{
  border-color:var(--vw-line);background:#fff}
[data-testid="stWidgetLabel"] p{font-size:13px;font-weight:500;color:#334155}
[data-testid="stCheckbox"] p,[data-testid="stRadio"] p{font-size:13.5px;color:#1e293b}
[data-testid="stFileUploaderDropzone"]{background:#f8fafc;border:1px dashed var(--vw-line);border-radius:8px}

/* ---- messages -------------------------------------------------------- */
[data-testid="stAlert"]{border-radius:8px;border:1px solid transparent;font-size:13.5px}

/* ---- tables ---------------------------------------------------------- */
[data-testid="stDataFrame"],[data-testid="stDataEditor"]{border:1px solid var(--vw-line);border-radius:10px;
  overflow:hidden}
</style>
"""

_PILL = '<span class="vw-pill"><i></i>Secure workspace</span>'


def page(title: str, subtitle: str = "Commercial management platform", *, page_title: str | None = None,
         icon: str = "📄", sidebar_title: str = "Proposal builder") -> None:
    """Page config, the CRM stylesheet, the sidebar brand block and the top bar."""
    st.set_page_config(page_title=page_title or f"{title} — Verto Wave", page_icon=icon, layout="wide")
    st.markdown(_CSS, unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<div class="vw-brand"><span class="vw-mark">V</span>'
        f'<span><b>Verto Wave CRM</b><span>{html.escape(sidebar_title)}</span></span></div>',
        unsafe_allow_html=True)
    st.markdown(
        f'<div class="vw-top"><div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>'
        f'<div class="vw-right">{_PILL}</div></div>',
        unsafe_allow_html=True)


def hero(kicker: str, title: str, text: str = "") -> None:
    """The navy banner the CRM uses at the top of a workspace."""
    body = f'<p>{html.escape(text)}</p>' if text else ""
    st.markdown(
        f'<section class="vw-hero"><p class="vw-kicker">{html.escape(kicker)}</p>'
        f'<h2>{html.escape(title)}</h2>{body}</section>',
        unsafe_allow_html=True)


def kpis(items: list[tuple[str, str, str, str]]) -> None:
    """A row of KPI cards: (label, value, tint, glyph); tint is blue | violet | emerald | amber."""
    cards = "".join(
        f'<div class="vw-kpi"><span class="vw-tile vw-{tint}">{html.escape(glyph)}</span>'
        f'<div><div class="vw-label">{html.escape(label)}</div>'
        f'<div class="vw-value">{html.escape(str(value))}</div></div></div>'
        for label, value, tint, glyph in items)
    st.markdown(f'<div class="vw-kpis">{cards}</div>', unsafe_allow_html=True)


def nav() -> None:
    """The sidebar's page links, worded like the CRM rather than after the file names."""
    pages = [("proposal_builder.py", "Build proposal", ":material/description:"),
             ("pages/1_Module_Library.py", "Module library", ":material/library_books:")]
    with st.sidebar:
        side_label("Solution sales")
        for path, label, icon in pages:
            try:
                st.page_link(path, label=label, icon=icon)
            except Exception:  # a renamed or moved page must not break the builder
                st.markdown(f'<div class="vw-side-label">{html.escape(label)}</div>', unsafe_allow_html=True)


def side_label(text: str) -> None:
    """A small uppercase group label in the sidebar."""
    st.sidebar.markdown(f'<div class="vw-side-label">{html.escape(text)}</div>', unsafe_allow_html=True)
