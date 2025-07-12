import streamlit as st
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain.tools import tool
from tools import get_stock_info, search_stock
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage

# === Sidebar ===
st.sidebar.title("🔐 Configuration")
api_key = st.sidebar.text_input("Enter your GROQ API Key", type="password")
if not api_key:
    st.warning("Please enter your GROQ API key in the sidebar.")
    st.stop()

# === Memory Checkpoint ===
memory = MemorySaver()

# === LangGraph Shared State ===
class AgentState(TypedDict):
    query: str
    stock_ticker: str
    messages: Annotated[list, add_messages]

# === ChatBot Node ===
def chatbot(state: AgentState) -> AgentState:
    response = llm_tools.invoke(state["messages"])
    return {
        **state,
        "messages": [response]  # add_messages will append it
    }

# === LLM Setup ===
llm = ChatGroq(model_name="gemma2-9b-it", api_key=api_key)
llm_tools = llm.bind_tools([get_stock_info, search_stock])

# === Graph ===
builder = StateGraph(AgentState)
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode([get_stock_info, search_stock]))
builder.set_entry_point("chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.set_finish_point("chatbot")
graph = builder.compile(checkpointer=memory)

# === App Layout ===
st.title("📊 FinSight AI")

st.markdown("""
### Intelligent Stock & Company Insights with LLMs

**FinSight AI** is a smart financial assistant that helps you explore company details and stock trends using LLMs, real-time data, and Wikipedia insights — all inside a chat-style interface.

---

### 🚀 How to Use:
1. **Enter your GROQ API key** in the sidebar.
2. **Ask a question** about a company (e.g., *"Tell me about Apple"*).
3. Or, **select a stock ticker** to view key financial stats and trends.
4. Get **AI-powered responses** with real-time insights.

---
""")

tab1, tab2 = st.tabs(["💬 Ask a Company Question", "🏷️ Stock Ticker Info"])

# === TAB 1: Freeform Question ===
with tab1:
    query = st.text_input("Ask anything about a company (e.g., 'Tell me about Apple')", key="free_query")
    if st.button("Submit Query", key="btn1") and query:
        with st.spinner("Processing..."):
            state = {
                "query": query,
                "stock_ticker": "",  # optional here
                "messages": [HumanMessage(content=query)]
            }
            config = {"configurable": {"thread_id": "1"}}
            result = graph.invoke(state, config=config)

            for msg in result["messages"]:
                if msg.type == "human":
                    st.chat_message("user").markdown(msg.content.capitalize())
                elif msg.type == "ai":
                    st.chat_message("assistant").markdown(msg.content)

# === TAB 2: Select or Enter Ticker ===
with tab2:
    common_tickers = [
    "",  # default empty
    # US Tech
    "AAPL",   # Apple Inc.
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet (Class A)
    "AMZN",   # Amazon
    "META",   # Meta Platforms (Facebook)
    "TSLA",   # Tesla
    "NFLX",   # Netflix
    "NVDA",   # NVIDIA

    # US Finance & Retail
    "JPM",    # JPMorgan Chase
    "BAC",    # Bank of America
    "WMT",    # Walmart
    "V",      # Visa
    "MA",     # Mastercard
    "DIS",    # Walt Disney

    # Indian Stocks (NSE/BSE - suffix `.NS`)
    "RELIANCE.NS",  # Reliance Industries
    "TCS.NS",       # Tata Consultancy Services
    "INFY.NS",      # Infosys
    "HDFCBANK.NS",  # HDFC Bank
    "ICICIBANK.NS", # ICICI Bank
    "SBIN.NS",      # State Bank of India
    "BAJAJ-AUTO.NS",# Bajaj Auto
    "ITC.NS",       # ITC Limited
    "WIPRO.NS",     # Wipro
    "LT.NS",        # Larsen & Toubro

    # European & Global
    "SAP.DE",       # SAP (Germany)
    "SIE.DE",       # Siemens (Germany)
    "AIR.PA",       # Airbus (France)
    "NESN.SW",      # Nestlé (Switzerland)

    # ETFs (Optional)
    "QQQ",          # NASDAQ-100 ETF
    "SPY",          # S&P 500 ETF
    "VTI"           # Total US Market ETF
    ]

    selected = st.selectbox("Select a popular stock ticker:", options=common_tickers)
    custom = st.text_input("Or enter a stock ticker (e.g., RELIANCE)", key="custom_ticker")
    ticker = custom.strip().upper() if custom else selected.strip().upper()

    if st.button("Run Ticker Analysis", key="btn2") and ticker:
        query = f"Give detailed information about {ticker} stock"
        with st.spinner("Analyzing stock..."):
            state = {
                "query": query,
                "stock_ticker": ticker,
                "messages": [HumanMessage(content=query)]
            }
            config = {"configurable": {"thread_id": "2"}}
            result = graph.invoke(state, config=config)

            for msg in result["messages"]:
                if msg.type == "human" and msg.content :
                    st.chat_message("user").markdown(msg.content.capitalize())
                elif msg.type == "ai" and msg.content:
                    st.chat_message("assistant").markdown(msg.content)
