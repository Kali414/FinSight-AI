# 📊 FinSight AI

**FinSight AI** is a smart financial research assistant that helps users explore companies, track stock trends, and gather real-time data using LLMs, LangGraph, and dynamic tool integration.

Built with **LangGraph**, **Groq's LLMs**, **Streamlit**, and tools like **Yahoo Finance** and **Wikipedia**, this app offers an intelligent and conversational interface for financial exploration.

---

## 🚀 Features

- 💬 Natural language queries about companies (e.g., "Tell me about Tesla")
- 📈 Real-time stock analysis using Yahoo Finance
- 🌐 Wikipedia-powered company overviews
- 🔁 Tool routing using LangGraph and memory
- 🧠 Fast LLM responses via Groq's `gemma-2-9b-it` model
- 🎛️ Chat-style Streamlit UI with sidebar for API key and ticker selection

---

## 🛠️ Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — Graph-based multi-agent framework  
- **[LangChain](https://www.langchain.com/)** — Tool binding & agent interface  
- **[Groq + Gemma-2-9b-it](https://console.groq.com/)** — Ultra-fast LLM inference  
- **[Streamlit](https://streamlit.io/)** — Web UI  
- **[yfinance](https://pypi.org/project/yfinance/)** — Real-time stock data  
- **[Wikipedia API](https://python.langchain.com/docs/integrations/tools/wikipedia)** — Company descriptions  

---

## 🧑‍💻 How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/FinSight-AI.git
   cd FinSight-AI
   ```

2. **Install dependencies **

    ``` bash
    pip install -r requirements.txt
    ```

3. ** Create a .env file and add your Groq API Key: **
    ``` bash
    GROQ_API_KEY=your_groq_api_key_here
    ```
4. ** Run the app **

    ```bash
    streamlit run app.py
    ```