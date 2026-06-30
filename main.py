from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
class State(TypedDict):
    question:             str
    vector_store:         Any
    plan:                 str
    market_analysis:      str
    finance_analysis:     str
    operations_analysis:  str
    technology_analysis:  str
    risk_analysis:        str
    final_report:         str
    next_agent:           str


# ─────────────────────────────────────────────
# MAIN FUNCTION — called from app.py
# ─────────────────────────────────────────────
def build_graph(pdf_path: str):

    # ── 1. Load & chunk ──────────────────────
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500,
        separators=["\n\n", "\n", ".", ""]
    )
    splitted_docs = splitter.split_documents(docs)

    # ── 2. Embeddings & retriever ─────────────
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = Chroma.from_documents(
        embedding=embeddings,
        documents=splitted_docs,
    )
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 7, "lambda_mult": 0.5}
    )

    # ── 3. Model ──────────────────────────────
    model = ChatGroq(model="qwen/qwen3-32b", reasoning_format="hidden")

    # ── 4. Agent functions ────────────────────

    def Supervisor(state: State) -> Command:
        next_node = state.get("next_agent", "plan")
        print(f"Supervisor routing to: {next_node}")
        if next_node == "plan":
            return Command(goto="plan")
        elif next_node == "market_analysis":
            return Command(goto="market_analysis")
        elif next_node == "finance_analysis":
            return Command(goto="finance_analysis")
        elif next_node == "operations_analysis":
            return Command(goto="operations_analysis")
        elif next_node == "technology_analysis":
            return Command(goto="technology_analysis")
        elif next_node == "risk_analysis":
            return Command(goto="risk_analysis")
        elif next_node == "final_report":
            return Command(goto="final_report")
        else:
            return Command(goto=END)

    def plan(state: State):
        print("plan agent running...")
        prompt = f"""
You are an AI Assistant whose job is to create a strategic plan for solving the given business problem.
Use page numbers whenever possible.

Example:
Revenue increased significantly. (Source: Page 42)
Digital investments accelerated. (Source: Page 87)

Business Question:
{state['question']}
"""
        retrieved = retriever.invoke(f"""
Business Question:
{state['question']}

Retrieve information about:
- Company Overview
- Business Model
- Industry
- Products & Services
- Strategic Objectives
- Recent Performance
""")
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:1500]}")
        return {"plan": response.content, "next_agent": "market_analysis"}

    def market_analysis(state: State):
        print("market_analysis agent running...")
        prompt = f"""
You are an AI Assistant whose job is to perform a detailed market analysis.
Use page numbers whenever possible.

Example:
Revenue increased significantly. (Source: Page 42)

Research Plan:
{state['plan'][:500]}
"""
        retrieved = retriever.invoke(prompt)
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:1500]}")
        return {"market_analysis": response.content, "next_agent": "finance_analysis"}

    def finance_analysis(state: State):
        print("finance_analysis agent running...")
        prompt = f"""
You are an AI Assistant whose work is to perform a detailed finance analysis.
You MUST extract and clearly state exact numbers for:
- Total Revenue
- EBITDA or Operating Profit
- Net Debt or Total Debt
- One key business metric (subscribers, stores, capacity, employees, market share etc.)

Format each number clearly like:
Revenue: ₹X,XXX Cr (Source: Page N)
EBITDA: ₹X,XXX Cr (Source: Page N)
Net Debt: ₹X,XXX Cr (Source: Page N)
Key Metric: XXX (label) (Source: Page N)

Use page numbers whenever possible.

Plan:
{state['plan'][:500]}

Market Analysis:
{state['market_analysis'][:500]}
"""
        retrieved = retriever.invoke(prompt)
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:2000]}")
        return {"finance_analysis": response.content, "next_agent": "operations_analysis"}

    def operations_analysis(state: State):
        print("operations_analysis agent running...")
        prompt = f"""
You are an AI Assistant whose work is to perform an operations analysis.
Use page numbers whenever possible.

Example:
Revenue increased significantly. (Source: Page 42)

Plan:
{state['plan'][:500]}

Market Analysis:
{state['market_analysis'][:500]}

Finance Analysis:
{state['finance_analysis'][:500]}
"""
        retrieved = retriever.invoke(prompt)
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:1500]}")
        return {"operations_analysis": response.content, "next_agent": "technology_analysis"}

    def technology_analysis(state: State):
        print("technology_analysis agent running...")
        prompt = f"""
You are an AI Assistant whose work is to perform a technology analysis.
Use page numbers whenever possible.

Example:
Revenue increased significantly. (Source: Page 42)

Plan:
{state['plan'][:500]}

Market Analysis:
{state['market_analysis'][:500]}

Finance Analysis:
{state['finance_analysis'][:500]}

Operations Analysis:
{state['operations_analysis'][:500]}
"""
        retrieved = retriever.invoke(prompt)
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:1500]}")
        return {"technology_analysis": response.content, "next_agent": "risk_analysis"}

    def risk_analysis(state: State):
        print("risk_analysis agent running...")
        prompt = f"""
You are an AI Assistant whose work is to perform a risk analysis.
Use page numbers whenever possible.

Example:
Revenue increased significantly. (Source: Page 42)

Plan:
{state['plan'][:500]}

Market Analysis:
{state['market_analysis'][:500]}

Finance Analysis:
{state['finance_analysis'][:500]}

Operations Analysis:
{state['operations_analysis'][:500]}

Technology Analysis:
{state['technology_analysis'][:500]}
"""
        retrieved = retriever.invoke(prompt)
        context = "\n\n".join(
            f"Page {doc.metadata.get('page', 0) + 1}\n{doc.page_content}"
            for doc in retrieved
        )
        response = model.invoke(f"{prompt}\n\nRelevant Context:\n\n{context[:1500]}")
        return {"risk_analysis": response.content, "next_agent": "final_report"}

    def final_report(state: State):
        print("Generating final report...")
        report_prompt = f"""
You are a Senior Strategy Consultant at McKinsey.

Prepare a professional business report.
Use ONLY the information provided below.
Do not invent numbers.
If any information is missing, clearly mention: "Not Available in the Annual Report."
Use page number citations wherever possible like (Source: Page N).

Business Question:
{state["question"][:200]}

--------------------
Strategic Plan
{state["plan"][:800]}

--------------------
Market Analysis
{state["market_analysis"][:800]}

--------------------
Finance Analysis
{state["finance_analysis"][:800]}

--------------------
Operations Analysis
{state["operations_analysis"][:1500]}

--------------------
Technology Analysis
{state["technology_analysis"][:1500]}

--------------------
Risk Analysis
{state["risk_analysis"][:1500]}

--------------------

Generate the report in this exact format with these exact headings:

# Executive Summary

# Business Overview

# Market Analysis

# Financial Analysis

IMPORTANT: Under Financial Analysis you MUST include a clearly labelled section like:
Key Financials:
- Revenue: [exact number from Finance Analysis above]
- EBITDA: [exact number from Finance Analysis above]
- Net Debt: [exact number from Finance Analysis above]
- [Key Metric label]: [exact number from Finance Analysis above]

# Operations Analysis

# Technology Analysis

# Risk Assessment

# Strategic Recommendations

List each recommendation on its own line in this format:
1. Short Title
Brief description of the recommendation.

2. Short Title
Brief description of the recommendation.

(up to 6 recommendations)

# Conclusion

Keep the report professional.
"""
        response = model.invoke(report_prompt)
        return {"final_report": response.content, "next_agent": "END"}

    # ── 5. Build & compile graph ──────────────
    builder = StateGraph(State)
    builder.add_node("Supervisor",            Supervisor)
    builder.add_node("plan",                  plan)
    builder.add_node("market_analysis",       market_analysis)
    builder.add_node("finance_analysis",      finance_analysis)
    builder.add_node("operations_analysis",   operations_analysis)
    builder.add_node("technology_analysis",   technology_analysis)
    builder.add_node("risk_analysis",         risk_analysis)
    builder.add_node("final_report",          final_report)

    builder.add_edge(START,                "Supervisor")
    builder.add_edge("plan",               "Supervisor")
    builder.add_edge("market_analysis",    "Supervisor")
    builder.add_edge("finance_analysis",   "Supervisor")
    builder.add_edge("operations_analysis","Supervisor")
    builder.add_edge("technology_analysis","Supervisor")
    builder.add_edge("risk_analysis",      "Supervisor")
    builder.add_edge("final_report",       "Supervisor")

    graph = builder.compile()
    return graph
