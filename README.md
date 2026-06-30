# Meridian — Strategic Intelligence Platform

A professional AI-powered consulting dashboard that analyses company annual reports through a multi-agent RAG pipeline and presents findings in a structured, McKinsey-style interface.

---

## What It Does

Upload any company's annual report (PDF) and ask a strategic question. The platform runs it through six specialist AI agents — each grounded in the document — and assembles a complete consulting report with dynamic KPIs, risk registers, and a CEO Action Dashboard.

---

## Architecture

```
User Question + PDF
        │
        ▼
   Supervisor Agent
        │
        ├──▶ Plan Agent             (company overview, strategic intent)
        ├──▶ Market Analysis Agent  (competitive landscape, positioning)
        ├──▶ Finance Analysis Agent (revenue, EBITDA, debt, key metrics)
        ├──▶ Operations Agent       (supply chain, infrastructure, capacity)
        ├──▶ Technology Agent       (R&D, AI, digital initiatives, partners)
        ├──▶ Risk Analysis Agent    (regulatory, market, execution risks)
        └──▶ Final Report Agent     (McKinsey-style consolidated report)
                │
                ▼
        Streamlit Dashboard
```

**Stack:**
- `LangGraph` — multi-agent orchestration via StateGraph
- `LangChain` — document loading, text splitting, retrieval chain
- `ChromaDB` — vector store for semantic search
- `HuggingFace` — embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- `Groq` — LLM inference (`qwen/qwen3-32b`)
- `Streamlit` — dashboard UI

---

## Project Structure

```
Ai Consultancy/
├── app.py           # Streamlit dashboard (UI, KPI extraction, CEO dashboard)
├── checkey.py       # LangGraph pipeline (agents, RAG, graph compilation)
├── .env             # API keys (Groq)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone and create environment

```bash
cd "Ai Consultancy"
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install streamlit langchain langgraph langchain-groq langchain-chroma \
            langchain-huggingface langchain-community chromadb \
            sentence-transformers pypdf python-dotenv
```

### 3. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key at: https://console.groq.com

### 4. Run the app

```bash
streamlit run app.py
```

---

## How to Use

1. Open the app in your browser (`http://localhost:8501`)
2. Upload an annual report PDF using the **Document** section in the sidebar
3. Type a strategic question in the search bar — e.g.
   - *"How is Adani Enterprises expanding into green energy?"*
   - *"What are the key financial risks facing this company?"*
   - *"Prepare a 5-year strategic growth plan."*
4. Click **Run Analysis**
5. Navigate through the sections using the sidebar:
   - **Overview** — KPI strip + summary cards
   - **Market Analysis** — competitive landscape
   - **Financial Analysis** — revenue, margins, returns
   - **Operations** — infrastructure, supply chain
   - **Technology** — digital initiatives, R&D, partners
   - **Risk Assessment** — risk register with likelihood/impact matrix
   - **Recommendations** — prioritised strategic actions
   - **CEO Action Dashboard** — appears at the bottom of every section

---

## Key Features

| Feature | Description |
|---|---|
| Multi-agent RAG | Six specialist agents each retrieve from the PDF independently |
| Dynamic KPIs | LLM extracts real numbers from the report — no hardcoded values |
| Page citations | Every insight is cited with source page numbers from the PDF |
| Risk register | Structured table with likelihood, impact, and mitigation levers |
| CEO Action Dashboard | Prioritised initiative table with cost, timeline, and risk ratings |
| Any company | Works with any annual report — Adani, Reliance, Tata, Infosys, etc. |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Groq API key for LLM inference |

---

## Model

The pipeline uses `qwen/qwen3-32b` via Groq with `reasoning_format="hidden"`. To switch models, change the `model` parameter in `checkey.py`:

```python
model = ChatGroq(model="llama-3.3-70b-versatile", reasoning_format="hidden")
```

Available Groq models: `qwen/qwen3-32b`, `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`

---

## Notes

- First run takes 30–60 seconds to load the PDF, chunk it, and build the vector store
- Each analysis run makes approximately 8 LLM calls (one per agent)
- KPI extraction makes additional LLM calls per dashboard section — expect ~15 total calls per query
- The vector store is rebuilt on every new PDF upload; it is not persisted to disk

---

## License

Private project. Not for redistribution.