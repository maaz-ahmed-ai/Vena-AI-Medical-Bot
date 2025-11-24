# **Riverside Wellness Clinic – AI Virtual Doctor Assistant**

### *Built with FastAPI, LangGraph, OpenAI, ChromaDB, and a Modern Frontend UI*

---

## 🏥 **Overview**

This project is a **full-stack AI-powered medical assistant** designed for clinics and healthcare organizations.
It simulates a **real virtual doctor consultation**, supports **safe medical triage**, and integrates a **RAG (Retrieval-Augmented Generation)** pipeline built with PDF knowledge bases.

Patients can:

* Ask medical questions
* Get safe & empathetic guidance (without diagnosis)
* Understand symptoms
* Receive medication education
* Book clinic appointments
* Chat through a polished clinic website interface
* Maintain session memory per thread
* See formatted appointment summaries

---

## 🚀 **Tech Stack**

### **Backend**

| Layer         | Technology                         |
| ------------- | ---------------------------------- |
| Language      | Python 3.10+                       |
| API Framework | FastAPI                            |
| LLM Workflow  | LangGraph                          |
| Vector Search | ChromaDB                           |
| Embeddings    | OpenAI `text-embedding-3-large`    |
| LLM           | OpenAI `gpt-4o-mini`               |
| Retrieval     | RAG over PDFs                      |
| Memory        | LangGraph checkpointer             |
| Prompting     | Custom medical-safe doctor persona |

---

### **Frontend**

| Feature    | Technology                        |
| ---------- | --------------------------------- |
| UI         | HTML, CSS (Premium Medical Theme) |
| Templating | Jinja2                            |
| Logic      | Vanilla JavaScript (Fetch API)    |
| Chat Popup | Real-time UI, smooth animations   |
| Branding   | Riverside Wellness Clinic         |
| AI Doctor  | “Vena AI”                         |

---

## 📁 **Project Structure**

```
Riverside-Clinic-AI/
│
├── Data/                      # Clinic PDFs (symptoms, diseases, policies)
├── vectorstore/               # Auto-generated ChromaDB
├── templates/
│   └── chat.html              # Entire Clinic Website + Chat Popup
├── static/
│   └── style.css              # Premium clinic-style CSS
│
├── graph.py                   # LangGraph agent pipeline
├── main.py                    # Backend API (RAG + Agent)
├── frontend.py                # Frontend server (UI + chat endpoint)
├── prompts.py                 # System prompt (doctor persona)
│
├── README.md                  # Documentation
└── requirements.txt           # Dependencies
```

---

## 🧠 **How It Works**

### 1️⃣ **User Sends a Message**

The frontend sends:

```json
{
  "question": "I have chest tightness",
  "thread_id": "frontend-session-001"
}
```

### 2️⃣ **Backend Pipeline (LangGraph)**

```
User Message → Retriever → RAG Context → LLM Generate → Final AI Reply
```

* Query PDFs using semantic search
* Create RAG context chunk
* Feed context + prompt + history to LLM
* Produce empathetic, safe medical response
* Memory preserved per session (`thread_id`)

### 3️⃣ **Safety Layer**

* Detect emergency signals (e.g., chest pain)
* Block non-medical questions
* Provide disclaimers
* Avoid diagnosis
* Ask **one question at a time** like a real doctor

### 4️⃣ **Appointment Assistant**

Vena AI guides booking:

* Reason for visit
* Date preference
* Available slots
* Name / Email / Phone / DOB
* Doctor notes

Final summary is auto-formatted.

---

## 🖥 **Run the Backend**

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Start Backend (RAG + Agent)

```bash
uvicorn main:app --reload --port 8000
```

---

## 🌐 **Run the Frontend**

```bash
uvicorn frontend:app --reload --port 8001
```

Then open:

```
http://127.0.0.1:8001
```

You'll see a **modern USA-style clinic website** with a **floating chat widget**.

---

## 🏗 **Architecture Diagram (High-Level)**

```
                    ┌────────────────────┐
                    │      Frontend       │
                    │  (HTML/CSS/JS)      │
                    │  Riverside Clinic   │
                    └──────────┬──────────┘
                               │ /send
                               ▼
                     ┌────────────────────┐
                     │   Frontend API     │
                     │   (FastAPI)        │
                     └──────────┬──────────┘
                               │ /chat
                               ▼
             ┌──────────────────────────────────────┐
             │          LangGraph Agent              │
             │  ─ System Prompt (Doctor)             │
             │  ─ Memory (thread_id)                 │
             │  ─ Retrieval Node (Chroma)            │
             │  ─ Generate Node (LLM)                │
             └──────────────────┬───────────────────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │    ChromaDB        │
                    │  (Vectorstore)     │
                    └────────────────────┘
```

---

## 📚 **Knowledge Base (RAG)**

* Upload medical PDFs to `/Data/`
* System auto-ingests, chunks, embeds, and stores in ChromaDB.

You can include:

* Symptom explainers
* Disease overviews
* Medication guides
* Clinic policies
* Appointment instructions

---

## 👨‍⚕️ **Doctor Persona (Vena AI)**

Vena AI:

* Talks like a real US clinic doctor
* Uses warm + empathetic tone
* Avoids diagnosis
* Uses natural, conversational explanations
* Handles booking
* Uses retrieval first, then safe fallback
* Asks **one question at a time**

---

## 📦 **Production-Ready Features**

✔ Modular backend
✔ Vectorstore persistence
✔ Thread-based memory
✔ Safety checks
✔ Appointment workflow
✔ Fully designed medical website
✔ Real chat popup UI
✔ Loading indicators
✔ Mobile responsive
✔ US clinic branding
✔ Future-ready: scheduling agent, analytics, dashboard, etc.

---

## 🧩 **Possible Next Add-Ons**

* Patient login + auth
* Doctor dashboard
* Appointment calendar integration
* Stripe payments
* Voice assistant mode
* SMS follow-ups
* CRM analytics

---

## 📜 **License**

MIT (modify for clinic use)

