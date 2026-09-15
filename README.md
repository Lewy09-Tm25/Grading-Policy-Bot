# 🎓 Guidance for Grading

An interactive academic advisor built to answer questions based strictly on the **[CUNY Uniform Grade Glossary Policies and Guidelines](https://www.cuny.edu/wp-content/uploads/sites/4/page-assets/academics/new-revised-policies/CUNY-Uniform-Grade-Glossary-Policies-and-Guidelines-FINAL-JUNE-2024.pdf)**. 

We are not using a traditional RAG system, simply because the state-of-the-art allows the usage of long context. Hence this application utilizes **Long-Context Injection**. By feeding the entire parsed policy document directly into the LLM's system prompt, we eliminate vector-search retrieval errors and ensure 100% accuracy when navigating complex tables, temporary grade definitions, and date-specific policy shifts.

## 🏗️ Architecture

- **Frontend:** Streamlit (with real-time token streaming)
- **Backend / LLM:** OpenAI API (`gpt-5.4`)
- **Parser:** Marker (Local, OCR-based PDF to Markdown extraction)
- **Memory:** Streamlit Session State (Full conversation history retention) (until the session is refreshed, as the memory is not persisted across sessions)
- **Paradigm:** Long-Context Injection with strict semantic guardrails

## 📂 Directory Structure

The codebase is highly modular, separating UI, configuration, LLM communication, and testing.

```text
cuny_chatbot/
│
├── data/
│   └── grading_policy.md         # The parsed Markdown policy document
│
├── core/
│   ├── __init__.py
│   ├── config.py                # Environment variables and file paths
│   └── prompts.py               # System Prompt construction & file loading
│
├── client/                      
│   ├── __init__.py
│   └── llm_client.py            # OpenAI API wrapper and streaming logic
│
├── tests/
│   ├── __init__.py
│   └── test_guardrails.py       # Semantic unittests for hallucination prevention
│
├── requirements.txt             # Python dependencies
├── .env                         # Git-ignored API keys
└── app.py                       # Main Streamlit application and state manager