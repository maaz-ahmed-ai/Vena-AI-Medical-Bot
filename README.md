# Vena-AI-Medical-Bot
This project implements a **Healthcare RAG (Retrieval-Augmented Generation) System** with multi-agent orchestration, tool integration, appointment scheduling, and structured knowledge retrieval. It is designed for clinics, telemedicine apps, or healthcare assistants needing automated patient interaction, policy-aware AI responses, and scheduling workflows.

---

## **📌 Key Features**

### ✅ **Multi-Agent Architecture**

* **Router Agent** – Determines user intent (medical explanation, policy question, scheduling request, rewriting).
* **Doctor Agent** – Provides medical-context responses using RAG from clinic policies, doctor profiles, and FAQs.
* **Appointment Scheduler Agent** – Handles available slots, patient intake, scheduling, and notifications.
* **Rewrite Agent** – Reformulates outputs (e.g., to patient-friendly formats).

### ✅ **RAG Pipeline**

* Vector embeddings created from **Knowledge Base PDFs**.
* Context retrieved using a **Vector Store + Context Retriever**.
* LLM generates medically aligned responses with guardrails.

### ✅ **Tooling Integrations**

The Tool Node can call:

* **Google Calendar Availability Tool**
* **Google Sheets Tool** (patient request DB)
* **Email/SMS Notification Tool**
* **Appointment Slot Recommender**

### ✅ **Frontend Web Chat**

* HTML/CSS Chat UI (`templates/chat.html`)
* API interaction through `frontend.py` and `main.py`

---

## **📂 Project Structure**

```
01_RAG_HEALTHCARE/
├── Data/                         # PDFs and medical documents for vector embeddings
│   ├── 25346041.pdf
│   ├── health-education-materials-assessment-tool.pdf
│   ├── The-Gale-Encyclopedia-of-Medicine-3rd-Ed.pdf
│
├── graph-diagram/
│   └── healthcare_rag_graph.mmd  # Mermaid graph of multi-agent system
│
├── static/
│   ├── img/                      # UI images
│   │   ├── desk1.jpg
│   │   └── doctor1.jpg
│   └── style.css                 # Web UI styling
│
├── templates/
│   └── chat.html                 # Chat interface
│
├── vectorstore/                  # Generated embeddings + index
│
├── frontend.py                   # Web server / chat interface logic
├── main.py                       # Entry point for backend API
├── graph.py                      # Multi-agent routing & graph orchestration
├── mermaid.py                    # Mermaid diagram exporter
├── prompts.py                    # Agent prompt templates
├── extra_prompts.py              # Additional crafted instructions
│
├── requirements.txt
├── readme.md
└── .env                          # API keys (not tracked)
```

---

## **🏗️ System Architecture Overview**

### **Data Flow (Simplified)**

1. **User → Frontend Chat**
2. **Router Agent** determines intent
3. If medical → **Doctor Agent**
4. If scheduling → **Appointment Scheduler Agent**
5. Agents may request:

   * Vector Store Retrieval
   * Google Calendar
   * Google Sheets DB
   * Email/SMS Notification
6. **Guardrail Check**
7. **Final Response → User**

---

## **🧠 RAG Workflow**

1. PDFs in `/Data` are embedded into vectors using:

   * OpenAI embeddings or HuggingFace embeddings.
2. Stored in `/vectorstore`
3. Context retrieval uses similarity search
4. LLM produces grounded responses using retrieved chunks
5. Guardrail ensures:

   * no hallucinations
   * no diagnostics
   * no unsafe medical claims
   * adherence to clinic policies

---

## **🚀 How to Run Locally**

### **1. Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Add Your API Keys**

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
GOOGLE_CREDENTIALS_PATH=credentials.json
```

### **4. Build the Vector Store**

If embeddings not yet generated:

```bash
python vectorstore/build_vectors.py
```

### **5. Launch the App**

```bash
python main.py
```

### **6. Open Browser**

```
http://localhost:8000
```

---

## **🧩 Agents in Detail**

### 🔸 **Router Agent**

Decides which agent should handle the user message.

### 🔸 **Doctor Agent**

* Uses RAG
* Retrieves policies, FAQs, doctor profiles
* Generates safe, educational responses

### 🔸 **Appointment Scheduler Agent**

* Reads Google Calendar availability
* Logs patient requests into Google Sheets
* Sends reminders via Gmail API

### 🔸 **Rewrite Agent**

Optional: improves style, formatting, tone.

---

## **🛠️ Tools Integrated**

| Tool                         | Purpose                         |
| ---------------------------- | ------------------------------- |
| Google Calendar Tool         | Fetch doctor availability       |
| Google Sheets Tool           | Store incoming patient requests |
| Gmail/SMS Tool               | Notify patients or staff        |
| Appointment Slot Recommender | Suggests best times             |

---

## **🌐 Frontend**

Located in **templates/chat.html**, styled via **static/style.css**.

Features:

* Real-time chat interface
* Avatar images from `/static/img`
* Smooth message flow

---

## **📦 Future Improvements**

* Clinical triage agent
* Insurance eligibility checker
* Voice-to-text and text-to-speech
* Multi-doctor load balancing

---

## **📄 License**

MIT License (or specify your preferred one)

---

Just tell me!
