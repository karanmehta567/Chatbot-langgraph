# 💬 AI Chatbot using Streamlit, OpenAI, and LangGraph

This project is an **AI-powered conversational assistant** built with **Streamlit**, **OpenAI**, and **LangGraph**.  
It allows users to have dynamic, context-aware conversations — with **conversation context saved locally using SQLite** for seamless continuity between chat sessions.

---

## 🚀 Features

- 🧩 **LangGraph-powered workflow** for modular and structured conversation flow  
- 💬 **OpenAI API integration** for intelligent and natural responses  
- 🧠 **Context persistence** — each conversation has a **unique thread ID** stored in SQLite  
- ⚡ **Streamlit UI** for an interactive chat interface  
- 🗃️ **Local database (SQLite)** for efficient context management and thread retrieval  
- 🔄 **Reset & start new conversations** dynamically  

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend/UI | Streamlit |
| Backend Logic | LangGraph |
| AI Model | OpenAI (ChatGPT model via API) |
| Database | SQLite |
| Language | Python |

---
## Used Streaming in Langgraph to accomodate larger feedback,improved readability


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/karanmehta567/Chatbot-langgraph.git
cd <directory>
create a virtual env and install the required deps in requiremnets.txt using pip install -r requirements.txt
ALL SET!!
```
# Run the application
streamlit run langgraph_frontend.py

## How It Works

A unique thread ID is created for each conversation session.

LangGraph manages the flow and state transitions of messages.

SQLite saves context (thread ID, user messages, and assistant responses).

Streamlit renders an interactive interface to chat in real time.


This project is open-source and available under the MIT License.

