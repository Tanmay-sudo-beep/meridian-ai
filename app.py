import streamlit as st
import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Strategic Intelligence Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Root palette ── */
:root {
    --bg:          #0d0f12;
    --surface:     #13161b;
    --surface-2:   #1a1e25;
    --border:      #252932;
    --border-light:#2e3440;
    --text-primary:#e8eaf0;
    --text-secondary:#8b909e;
    --text-muted:  #535862;
    --accent:      #c9a96e;        /* warm gold – the one risk */
    --accent-dim:  rgba(201,169,110,0.12);
    --accent-dim2: rgba(201,169,110,0.06);
    --positive:    #4a9d7f;
    --negative:    #c0635a;
    --neutral:     #5a7fa8;
}

/* ── App shell ── */
.stApp {
    background-color: var(--bg);
    color: var(--text-primary);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem 2.5rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem;
}

/* ── Sidebar nav items ── */
.nav-label {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 1.8rem 0 0.5rem 0;
}
.nav-item {
    display: block;
    padding: 0.55rem 0.75rem;
    margin-bottom: 2px;
    border-radius: 4px;
    color: var(--text-secondary);
    font-size: 13px;
    font-weight: 400;
    cursor: pointer;
    border: none;
    background: transparent;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: var(--surface-2); color: var(--text-primary); }
.nav-item.active {
    background: var(--accent-dim);
    color: var(--accent);
    font-weight: 500;
}
.nav-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}

/* ── Wordmark ── */
.wordmark {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: 0.04em;
    margin-bottom: 2px;
}
.wordmark-sub {
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Page header ── */
.page-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 1.4rem;
    margin-bottom: 2rem;
}
.page-eyebrow {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.5rem;
}
.page-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.3;
    margin: 0;
}
.page-meta {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── KPI strip ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
    margin-bottom: 2rem;
}
.kpi-cell {
    background: var(--surface);
    padding: 1.25rem 1.5rem;
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}
.kpi-delta {
    font-size: 11px;
    color: var(--positive);
    margin-top: 0.35rem;
    font-family: 'IBM Plex Mono', monospace;
}
.kpi-delta.neg { color: var(--negative); }

/* ── Section card ── */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
}
.section-tag {
    display: inline-block;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-dim2);
    border: 1px solid var(--accent-dim);
    padding: 2px 8px;
    border-radius: 2px;
    margin-bottom: 0.75rem;
}
.section-heading {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.section-body {
    font-size: 13.5px;
    line-height: 1.8;
    color: var(--text-secondary);
}
.section-body p { margin: 0 0 0.9rem 0; }
.section-body p:last-child { margin-bottom: 0; }

/* ── Insight block ── */
.insight-block {
    border-left: 2px solid var(--accent);
    padding: 0.75rem 1rem;
    background: var(--accent-dim2);
    border-radius: 0 4px 4px 0;
    margin: 1.2rem 0;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* ── Risk table ── */
.risk-row {
    display: grid;
    grid-template-columns: 2fr 80px 80px 1fr;
    gap: 1rem;
    align-items: center;
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
}
.risk-row:last-child { border-bottom: none; }
.risk-header {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
}
.badge-high   { background: rgba(192,99,90,0.15);  color: #c0635a; }
.badge-medium { background: rgba(201,169,110,0.12); color: var(--accent); }
.badge-low    { background: rgba(74,157,127,0.12);  color: var(--positive); }

/* ── Recommendation card ── */
.rec-card {
    display: grid;
    grid-template-columns: 36px 1fr;
    gap: 1rem;
    padding: 1.1rem 0;
    border-bottom: 1px solid var(--border);
    align-items: start;
}
.rec-card:last-child { border-bottom: none; }
.rec-num {
    font-size: 11px;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--accent);
    padding-top: 2px;
}
.rec-title { font-size: 13.5px; font-weight: 600; color: var(--text-primary); margin-bottom: 0.3rem; }
.rec-desc  { font-size: 12.5px; color: var(--text-secondary); line-height: 1.65; }

/* ── Footer bar ── */
.footer-bar {
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--text-muted);
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Text input styling ── */
.stTextArea textarea, .stTextInput input {
    background-color: var(--surface-2) !important;
    border: 1px solid var(--border-light) !important;
    color: var(--text-primary) !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13.5px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent-dim) !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0f12 !important;
    border: none !important;
    border-radius: 4px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Select / radio ── */
.stSelectbox select, .stRadio label {
    color: var(--text-primary) !important;
    font-size: 13px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.1rem !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 1.5rem 0 0 0 !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Selectbox popup ── */
[data-baseweb="popover"] { background: var(--surface-2) !important; border: 1px solid var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "active_section" not in st.session_state:
    st.session_state.active_section = "overview"
if "report" not in st.session_state:
    st.session_state.report = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="wordmark">MERIDIAN</div>
        <div class="wordmark-sub">Strategic Intelligence</div>
    """, unsafe_allow_html=True)
    st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Analysis</div>', unsafe_allow_html=True)

    nav_items = {
        "overview":           "Overview",
        "market_analysis":    "Market Analysis",
        "finance_analysis":   "Financial Analysis",
        "operations_analysis":"Operations",
        "technology_analysis":"Technology",
        "risk_analysis":      "Risk Assessment",
        "recommendations":    "Recommendations",
    }

    for key, label in nav_items.items():
        active_cls = "active" if st.session_state.active_section == key else ""
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.active_section = key

    st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Settings</div>', unsafe_allow_html=True)

    model_choice = st.selectbox(
        "Model",
        ["qwen/qwen3-32b", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        label_visibility="collapsed"
    )

   # Auto-detect company name from uploaded PDF filename
    # Auto-detect company name from uploaded PDF filename
    pdf_name = ""
    if st.session_state.get("pdf_path"):
        import os
        pdf_name = os.path.splitext(
            os.path.basename(st.session_state["pdf_path"])
        )[0].replace("_", " ").replace("-", " ").title()

    company_ctx = st.text_input(
        "Company / Report Context",
        value=pdf_name if pdf_name else "Upload a PDF to begin",
        label_visibility="collapsed"
    )

    st.markdown(
        f'<div style="font-size:11px; color:var(--text-muted); margin-top:0.5rem;">'
        f'{company_ctx}</div>',
        unsafe_allow_html=True
    )

    st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)
st.markdown('<div class="nav-label">Document</div>', unsafe_allow_html=True)

uploaded_pdf = st.file_uploader(
    "Upload Annual Report (PDF)",
    type=["pdf"],
    label_visibility="collapsed"
)

if uploaded_pdf is not None:
    # Save to disk so checkey.py can read it
    import os, tempfile
    pdf_path = os.path.join(os.getcwd(), uploaded_pdf.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())
    st.session_state.pdf_path = pdf_path
    st.markdown(
        f'<div style="font-size:11px; color:var(--text-muted); margin-top:0.4rem;">'
        f'{uploaded_pdf.name} &nbsp;·&nbsp; ready</div>',
        unsafe_allow_html=True
    )
else:
    st.session_state.pdf_path = None

    st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:10px; color:var(--text-muted); font-family:\'IBM Plex Mono\',monospace;">'
        f'{datetime.datetime.now().strftime("%d %b %Y  %H:%M")}</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def section_card(tag: str, heading: str, body: str, insight: str = ""):
    insight_html = f'<div class="insight-block">{insight}</div>' if insight else ""
    paras = "".join(f"<p>{p.strip()}</p>" for p in body.strip().split("\n") if p.strip())
    st.markdown(f"""
    <div class="section-card">
        <div class="section-tag">{tag}</div>
        <div class="section-heading">{heading}</div>
        <div class="section-body">{paras}{insight_html}</div>
    </div>
    """, unsafe_allow_html=True)


def kpi_strip(items):
    cells = ""
    for label, value, delta, neg in items:
        neg_cls = "neg" if neg else ""
        cells += f"""
        <div class="kpi-cell">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta {neg_cls}">{delta}</div>
        </div>"""
    st.markdown(f'<div class="kpi-row">{cells}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# QUERY INPUT
# ─────────────────────────────────────────────
col_q, col_btn = st.columns([5, 1])
with col_q:
    question = st.text_input(
        "Research query",
        placeholder="Enter your strategic question — e.g. How is Reliance expanding its market in India?",
        label_visibility="collapsed",
    )
with col_btn:
    run = st.button("Run Analysis", use_container_width=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RUN THE PIPELINE (mocked here — wire to your LangGraph graph)
# ─────────────────────────────────────────────




def run_pipeline(q):
    from checkey import build_graph   # ← changed

    pdf_path = st.session_state.get("pdf_path")
    if not pdf_path:
        st.error("Upload a PDF report first.")
        return None

    import threading, time

    result_container = {}

    def run_graph():
        graph = build_graph(pdf_path)   # ← builds graph from uploaded PDF
        result_container["result"] = graph.invoke({"question": q})

    progress = st.progress(0, text="Initialising pipeline...")
    stages = [
        "Retrieving document context...",
        "Running strategic plan agent...",
        "Running market analysis agent...",
        "Running financial analysis agent...",
        "Running operations analysis agent...",
        "Running technology analysis agent...",
        "Running risk analysis agent...",
        "Composing final report...",
    ]

    thread = threading.Thread(target=run_graph)
    thread.start()

    i = 0
    while thread.is_alive():
        stage = stages[min(i, len(stages) - 1)]
        progress.progress(min(int((i + 1) / len(stages) * 100), 95), text=stage)
        time.sleep(2)
        i = min(i + 1, len(stages) - 1)

    thread.join()
    progress.progress(100, text="Report ready.")
    progress.empty()

    return result_container.get("result", None)

if run and question.strip():
    with st.spinner(""):
        result = run_pipeline(question)
        st.session_state.report = result
        st.session_state.active_section = "overview"
elif run and not question.strip():
    st.warning("Enter a research question before running the analysis.")

def ceo_dashboard(report):
    import re, json
    from langchain_groq import ChatGroq

    final     = report.get("final_report", "")
    risk_text = report.get("risk_analysis", "")
    plan_text = report.get("plan", "")

    prompt = f"""
You are a senior McKinsey consultant.

Based on the strategic report below, extract the top 6 CEO-level priority actions.

Return ONLY a JSON array. No explanation. No markdown. No backticks.

Format:
[
  {{
    "priority": "High",
    "initiative": "Expand Green Hydrogen capacity",
    "impact": "High",
    "cost": "$$$",
    "timeline": "2 Years",
    "risk": "Medium"
  }}
]

Rules:
- Priority: High / Medium / Low
- Impact: High / Medium / Low  
- Cost: $ (low) / $$ (medium) / $$$ (high)
- Timeline: in months or years (e.g. "12 Months", "2 Years")
- Risk: High / Medium / Low
- Use ONLY information from the text below. Do not invent initiatives.

Report:
{final[:2000]}

Risk Analysis:
{risk_text[:800]}

Strategic Plan:
{plan_text[:800]}
"""

    kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
    raw = kpi_model.invoke(prompt).content.strip()

    try:
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if match:
            raw = match.group(0)
        actions = json.loads(raw)
    except Exception as e:
        
        st.warning(f"CEO Dashboard parse issue: {e}")
        actions = []

    priority_color = {"High": "#c0635a", "Medium": "#c9a96e", "Low": "#4a9d7f"}
    risk_color     = {"High": "#c0635a", "Medium": "#c9a96e", "Low": "#4a9d7f"}

    rows = ""
    for a in actions[:6]:
        pc = priority_color.get(a.get("priority", "Medium"), "#c9a96e")
        rc = risk_color.get(a.get("risk", "Medium"), "#c9a96e")
        rows += f"""
        <tr>
            <td><span style="color:{pc}; font-weight:600; font-family:'IBM Plex Mono',monospace; font-size:11px;">{a.get("priority","—")}</span></td>
            <td style="color:var(--text-primary); font-weight:500;">{a.get("initiative","—")}</td>
            <td><span style="color:#4a9d7f; font-size:12px;">{a.get("impact","—")}</span></td>
            <td style="font-family:'IBM Plex Mono',monospace; color:var(--accent); font-size:12px;">{a.get("cost","—")}</td>
            <td style="font-family:'IBM Plex Mono',monospace; color:var(--text-secondary); font-size:12px;">{a.get("timeline","—")}</td>
            <td><span style="color:{rc}; font-size:12px;">{a.get("risk","—")}</span></td>
        </tr>"""

    st.markdown(f"""
    <div class="section-card" style="margin-top:2rem;">
        <div class="section-tag">Executive Decision Support</div>
        <div class="section-heading">CEO Action Dashboard</div>
        <table style="width:100%; border-collapse:collapse; margin-top:0.5rem;">
            <thead>
                <tr style="border-bottom:1px solid var(--border);">
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 1rem 0.75rem 0;">Priority</th>
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 1rem 0.75rem 0;">Initiative</th>
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 1rem 0.75rem 0;">Impact</th>
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 1rem 0.75rem 0;">Cost</th>
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 1rem 0.75rem 0;">Timeline</th>
                    <th style="text-align:left; font-size:9px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--text-muted); padding:0 0 0.75rem 0;">Risk</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
report = st.session_state.report

if report is None:
    # ── Landing state ──
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Strategic Intelligence Platform</div>
        <div class="page-title">Enterprise Research & Analysis</div>
        <div class="page-meta">RAG · Multi-Agent · Annual Report Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="max-width:680px;">
        <div class="section-tag">How It Works</div>
        <div class="section-heading">Six-Agent Analysis Pipeline</div>
        <div class="section-body">
            <p>Enter a strategic research question above and the platform will route it through a sequence of specialist agents — each grounded in the uploaded annual report via retrieval-augmented generation. Results are assembled into a structured consulting report.</p>
            <p>Agents: Strategic Plan &rarr; Market Analysis &rarr; Financial Analysis &rarr; Operations &rarr; Technology &rarr; Risk Assessment &rarr; Final Report.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    section = st.session_state.active_section

    # ── Page header ──
    section_titles = {
        "overview":            ("Report Overview",        "Consolidated strategic intelligence"),
        "market_analysis":     ("Market Analysis",        "Competitive landscape and positioning"),
        "finance_analysis":    ("Financial Analysis",     "Performance, returns, and capital structure"),
        "operations_analysis": ("Operations",             "Infrastructure, logistics, and execution"),
        "technology_analysis": ("Technology",             "Platform capabilities and innovation pipeline"),
        "risk_analysis":       ("Risk Assessment",        "Material risks and mitigation outlook"),
        "recommendations":     ("Recommendations",        "Prioritised strategic actions"),
    }
    title, sub = section_titles.get(section, ("Analysis", ""))

    st.markdown(f"""
    <div class="page-header">
        <div class="page-eyebrow">{company_ctx}</div>
        <div class="page-title">{title}</div>
        <div class="page-meta">Generated {datetime.datetime.now().strftime("%d %b %Y  %H:%M")} &nbsp;·&nbsp; {sub}</div>
    </div>
    """, unsafe_allow_html=True)

    # ─── OVERVIEW ───────────────────────────────
    if section == "overview":
        import re, json

        # ── Ask LLM to extract KPIs from the actual report text ──
        finance_text = report.get("finance_analysis", "")
        market_text  = report.get("market_analysis", "")
        plan_text    = report.get("plan", "")

        kpi_prompt = f"""
Extract exactly 4 key financial or business metrics from the text below.
Return ONLY a JSON array. No explanation. No markdown. No backticks.

Format:
[
  {{"label": "Revenue", "value": "₹10.2L Cr", "delta": "+8.4% YoY"}},
  {{"label": "EBITDA",  "value": "₹1.84L Cr", "delta": "+11.2% YoY"}},
  {{"label": "Net Debt","value": "₹1.12L Cr", "delta": "-6.1% YoY"}},
  {{"label": "Metric4", "value": "497M",       "delta": "+4.3% YoY"}}
]

Rules:
- Pick ANY 4 meaningful numbers you find — revenue, profit, debt, subscribers, stores, capacity, market share, etc.
- If growth rate is mentioned use it as delta, otherwise write "—"
- Do NOT write "Not Available" — always pick the best number you can find
- Labels should be 2-3 words max

Text:
{finance_text[:2000]}

Additional context:
{market_text[:1000]}

{plan_text[:500]}
"""

        import re, json
        from langchain_groq import ChatGroq

        finance_text = report.get("finance_analysis", "")
        market_text  = report.get("market_analysis", "")
        plan_text    = report.get("plan", "")
        final_text   = report.get("final_report", "")

        kpi_prompt = f"""
Extract exactly 4 key financial metrics from the text below.
Return ONLY a raw JSON array. No explanation. No markdown. No backticks. No extra text.

Example output:
[
  {{"label": "Revenue", "value": "₹10.2L Cr", "delta": "+8.4% YoY"}},
  {{"label": "EBITDA",  "value": "₹1.84L Cr", "delta": "+11.2% YoY"}},
  {{"label": "Net Debt","value": "₹1.12L Cr", "delta": "-6.1% YoY"}},
  {{"label": "Stores",  "value": "18,000+",   "delta": "+22% YoY"}}
]

Rules:
- Look for Revenue, EBITDA, Net Debt, and any 4th metric (subscribers, stores, employees, capacity, market share)
- Use exact numbers from the text
- If growth rate is mentioned write it as delta, otherwise write "—"
- Labels must be 2-3 words max
- If a number truly cannot be found write "See Report"

Finance Analysis:
{finance_text[:2000]}

Final Report (Key Financials section):
{final_text[:1000]}
"""
        kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
        kpi_raw = kpi_model.invoke(kpi_prompt).content.strip()

        try:
            match = re.search(r'\[.*?\]', kpi_raw, re.DOTALL)
            if match:
                kpi_raw = match.group(0)
            kpis = json.loads(kpi_raw)
        except Exception as e:
            st.warning(f"KPI parse issue: {e}")
            kpis = [
                {"label": "Revenue",    "value": "See Report", "delta": "—"},
                {"label": "EBITDA",     "value": "See Report", "delta": "—"},
                {"label": "Net Debt",   "value": "See Report", "delta": "—"},
                {"label": "Key Metric", "value": "See Report", "delta": "—"},
            ]

        kpi_strip([
            (k["label"], k["value"], k["delta"], str(k["delta"]).startswith("-"))
            for k in kpis[:4]
        ])

        col1, col2 = st.columns(2)
        with col1:
            section_card(
                "Strategic Plan",
                "Business Overview & Strategic Intent",
                report["plan"],
            )
        with col2:
            section_card(
                "Market",
                "Market Position Summary",
                report["market_analysis"][:500] + "...",
            )

        col3, col4 = st.columns(2)
        with col3:
            section_card(
                "Finance",
                "Financial Highlights",
                report["finance_analysis"][:500] + "...",
            )
        with col4:
            section_card(
                "Risk",
                "Top Risk Factors",
                report["risk_analysis"][:500] + "...",
            )

    # ─── MARKET ANALYSIS ────────────────────────
    elif section == "market_analysis":
        import re, json
        from langchain_groq import ChatGroq

        market_text = report.get("market_analysis", "")
        final_text  = report.get("final_report", "")

        mkt_prompt = f"""
Extract exactly 4 market or business metrics from the text below.
Return ONLY a raw JSON array. No explanation. No markdown. No backticks.

Example:
[
  {{"label": "Market Share",  "value": "~47%",    "delta": "+2pp YoY"}},
  {{"label": "Retail Stores", "value": "18,000+", "delta": "+22% YoY"}},
  {{"label": "ARPU",          "value": "₹182",    "delta": "+9% YoY"}},
  {{"label": "Subscribers",   "value": "497M",    "delta": "+4.3% YoY"}}
]

Rules:
- Pick any 4 market metrics — market share, stores, subscribers, ARPU, customers, penetration
- Use exact numbers from the text only
- Labels 2-3 words max
- If not found write "See Report"

Market Analysis:
{market_text[:2000]}

Final Report:
{final_text[:800]}
"""
        kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
        mkt_raw = kpi_model.invoke(mkt_prompt).content.strip()

        try:
            match = re.search(r'\[.*?\]', mkt_raw, re.DOTALL)
            if match:
                mkt_raw = match.group(0)
            mkt_kpis = json.loads(mkt_raw)
        except Exception:
            mkt_kpis = [
                {"label": "Metric 1", "value": "See Report", "delta": "—"},
                {"label": "Metric 2", "value": "See Report", "delta": "—"},
                {"label": "Metric 3", "value": "See Report", "delta": "—"},
                {"label": "Metric 4", "value": "See Report", "delta": "—"},
            ]

        kpi_strip([
            (k["label"], k["value"], k["delta"], str(k["delta"]).startswith("-"))
            for k in mkt_kpis[:4]
        ])
        section_card(
            "Market Analysis",
            "Competitive Landscape & Market Positioning",
            report["market_analysis"],
        )

    # ─── FINANCE ANALYSIS ───────────────────────
    elif section == "finance_analysis":
        import re, json
        from langchain_groq import ChatGroq

        finance_text = report.get("finance_analysis", "")
        final_text   = report.get("final_report", "")

        fin_prompt = f"""
Extract exactly 4 financial ratios or metrics from the text below.
Return ONLY a raw JSON array. No explanation. No markdown. No backticks.

Example:
[
  {{"label": "Revenue",    "value": "₹10.2L Cr", "delta": "+8.4% YoY"}},
  {{"label": "EBITDA Mgn", "value": "18.0%",     "delta": "+49bps"}},
  {{"label": "FCF",        "value": "₹68,000 Cr","delta": "Positive"}},
  {{"label": "ROCE",       "value": "11.2%",      "delta": "+80bps"}}
]

Rules:
- Pick any 4 — margins, returns, cash flow, debt ratios, revenue
- Use exact numbers from the text only
- Labels 2-3 words max
- If not found write "See Report"

Finance Analysis:
{finance_text[:2000]}

Final Report:
{final_text[:800]}
"""
        kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
        fin_raw = kpi_model.invoke(fin_prompt).content.strip()

        try:
            match = re.search(r'\[.*?\]', fin_raw, re.DOTALL)
            if match:
                fin_raw = match.group(0)
            fin_kpis = json.loads(fin_raw)
        except Exception:
            fin_kpis = [
                {"label": "Revenue",    "value": "See Report", "delta": "—"},
                {"label": "EBITDA Mgn", "value": "See Report", "delta": "—"},
                {"label": "FCF",        "value": "See Report", "delta": "—"},
                {"label": "ROCE",       "value": "See Report", "delta": "—"},
            ]

        kpi_strip([
            (k["label"], k["value"], k["delta"], str(k["delta"]).startswith("-"))
            for k in fin_kpis[:4]
        ])
        section_card(
            "Financial Analysis",
            "Revenue, Returns & Capital Structure",
            report["finance_analysis"],
        )

    # ─── OPERATIONS ─────────────────────────────
    elif section == "operations_analysis":
        import re, json
        from langchain_groq import ChatGroq

        ops_text   = report.get("operations_analysis", "")
        final_text = report.get("final_report", "")

        ops_prompt = f"""
Extract exactly 4 operational metrics from the text below.
Return ONLY a raw JSON array. No explanation. No markdown. No backticks.

Example:
[
  {{"label": "Cities Covered","value": "100+",    "delta": "18-month rollout"}},
  {{"label": "Retail Stores", "value": "18,000+", "delta": "+22% YoY"}},
  {{"label": "Plants",        "value": "42",       "delta": "—"}},
  {{"label": "Employees",     "value": "2.36L",    "delta": "+8% YoY"}}
]

Rules:
- Pick any 4 — stores, cities, plants, employees, capacity, logistics, infrastructure
- Use exact numbers from the text only
- Labels 2-3 words max
- If not found write "See Report"

Operations Analysis:
{ops_text[:2000]}

Final Report:
{final_text[:800]}
"""
        kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
        ops_raw = kpi_model.invoke(ops_prompt).content.strip()

        try:
            match = re.search(r'\[.*?\]', ops_raw, re.DOTALL)
            if match:
                ops_raw = match.group(0)
            ops_kpis = json.loads(ops_raw)
        except Exception:
            ops_kpis = [
                {"label": "Metric 1", "value": "See Report", "delta": "—"},
                {"label": "Metric 2", "value": "See Report", "delta": "—"},
                {"label": "Metric 3", "value": "See Report", "delta": "—"},
                {"label": "Metric 4", "value": "See Report", "delta": "—"},
            ]

        kpi_strip([
            (k["label"], k["value"], k["delta"], str(k["delta"]).startswith("-"))
            for k in ops_kpis[:4]
        ])
        section_card(
            "Operations",
            "Infrastructure, Supply Chain & Execution",
            report["operations_analysis"],
        )

    # ─── TECHNOLOGY ─────────────────────────────
    elif section == "technology_analysis":
        import re, json
        from langchain_groq import ChatGroq

        tech_text  = report.get("technology_analysis", "")
        final_text = report.get("final_report", "")

        tech_prompt = f"""
Extract exactly 4 technology or innovation metrics from the text below.
Return ONLY a raw JSON array. No explanation. No markdown. No backticks.

Example:
[
  {{"label": "Key Partners",  "value": "Google, Meta","delta": "Strategic"}},
  {{"label": "AI Initiatives","value": "3 Active",    "delta": "Growing"}},
  {{"label": "R&D Spend",     "value": "₹X,XXX Cr",  "delta": "+X% YoY"}},
  {{"label": "Patents Filed", "value": "XXX",         "delta": "—"}}
]

Rules:
- Pick any 4 — partners, AI bets, R&D spend, patents, data centres, platforms, digital initiatives
- Use exact information from the text only
- Labels 2-3 words max
- If not found write "See Report"

Technology Analysis:
{tech_text[:2000]}

Final Report:
{final_text[:800]}
"""
        kpi_model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")
        tech_raw = kpi_model.invoke(tech_prompt).content.strip()

        try:
            match = re.search(r'\[.*?\]', tech_raw, re.DOTALL)
            if match:
                tech_raw = match.group(0)
            tech_kpis = json.loads(tech_raw)
        except Exception:
            tech_kpis = [
                {"label": "Metric 1", "value": "See Report", "delta": "—"},
                {"label": "Metric 2", "value": "See Report", "delta": "—"},
                {"label": "Metric 3", "value": "See Report", "delta": "—"},
                {"label": "Metric 4", "value": "See Report", "delta": "—"},
            ]

        kpi_strip([
            (k["label"], k["value"], k["delta"], str(k["delta"]).startswith("-"))
            for k in tech_kpis[:4]
        ])
        section_card(
            "Technology",
            "Platform Capabilities & Innovation Pipeline",
            report["technology_analysis"],
        )

    # ─── RISK ASSESSMENT ────────────────────────
    elif section == "risk_analysis":
        st.markdown("""
        <div class="section-card">
            <div class="section-tag">Risk Assessment</div>
            <div class="section-heading">Material Risk Register</div>
            <div class="risk-row">
                <span class="risk-header">Risk Factor</span>
                <span class="risk-header">Likelihood</span>
                <span class="risk-header">Impact</span>
                <span class="risk-header">Primary Lever</span>
            </div>
            <div class="risk-row">
                <span>Regulatory / spectrum pricing shift</span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span><div class="badge badge-high">High</div></span>
                <span>Policy monitoring, scenario planning</span>
            </div>
            <div class="risk-row">
                <span>Telecom price war resumption</span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span><div class="badge badge-high">High</div></span>
                <span>Ecosystem lock-in, ARPU diversification</span>
            </div>
            <div class="risk-row">
                <span>New Energy execution / technology risk</span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span>Stage-gate capex, partner agreements</span>
            </div>
            <div class="risk-row">
                <span>Conglomerate valuation discount</span>
                <span><div class="badge badge-high">High</div></span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span>Demerger optionality, segment disclosure</span>
            </div>
            <div class="risk-row">
                <span>FDI policy change in retail</span>
                <span><div class="badge badge-low">Low</div></span>
                <span><div class="badge badge-high">High</div></span>
                <span>Domestic ownership structure</span>
            </div>
            <div class="risk-row">
                <span>Management succession uncertainty</span>
                <span><div class="badge badge-low">Low</div></span>
                <span><div class="badge badge-medium">Medium</div></span>
                <span>Governance disclosure, board structure</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        section_card(
            "Risk Narrative",
            "Detailed Risk Assessment",
            report["risk_analysis"],
        )

# ─── RECOMMENDATIONS ────────────────────────
    elif section == "recommendations":
        import re
        final = report.get("final_report", "")

        rec_text = ""
        if "Strategic Recommendations" in final:
            rec_text = final.split("Strategic Recommendations")[-1]
            for stopper in ["# Conclusion", "# Appendix"]:
                if stopper in rec_text:
                    rec_text = rec_text.split(stopper)[0]

        st.markdown("""
        <div class="section-card">
            <div class="section-tag">Strategic Recommendations</div>
            <div class="section-heading">Prioritised Actions</div>
        """, unsafe_allow_html=True)

        if rec_text.strip():
            items = re.split(r'\n(?=\d+\.|[-•])', rec_text.strip())
            items = [item.strip() for item in items if item.strip()]

            for i, item in enumerate(items, 1):
                lines = item.split("\n", 1)
                title_r = re.sub(r'^[\d\.\-•\*]+\s*', '', lines[0]).strip()
                desc = lines[1].strip() if len(lines) > 1 else ""

                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-num">0{i}</div>
                    <div>
                        <div class="rec-title">{title_r}</div>
                        <div class="rec-desc">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="section-body" style="font-size:13.5px; line-height:1.8; color:var(--text-secondary);">
                {final}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        # ── CEO Action Dashboard ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    ceo_dashboard(report)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    <span>Meridian Strategic Intelligence &nbsp;·&nbsp; Powered by LangGraph + Groq</span>
    <span>{datetime.datetime.now().strftime("%d %b %Y")}</span>
</div>
""", unsafe_allow_html=True)