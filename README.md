# Vena-AI-Medical-Bot

This project implements a **Healthcare RAG (Retrieval-Augmented Generation) System** powered by a **multi-agent architecture**, tool integrations, appointment scheduling workflows, and knowledge retrieval using clinic documents.

It is ideal for clinics, healthcare startups, and telemedicine platforms wanting automated patient support, contextual medical explanations, AI-assisted scheduling, and policy-safe responses.

---

# **📌 Key Features**

### ✅ Multi-Agent Architecture

* **Router Agent** — Routes user intents (medical, policy, scheduling, rewrite).
* **Doctor Agent** — Medical context answers using RAG retrieval.
* **Appointment Scheduler Agent** — Books appointments using Google Calendar, Sheets, and notification tools.
* **Rewrite Agent** — Reformats or simplifies answers.

### ✅ RAG (Retrieval-Augmented Generation)

* Uses clinic PDFs (policies, doctor profiles, FAQs).
* Vector embeddings stored in `/vectorstore`.
* Context retrieved automatically for each query.
* Safe and controlled LLM generation via guardrails.

### ✅ Tool Integrations

* Google Calendar Availability Tool
* Google Sheets (Patient Request DB)
* Email/SMS Notification Tool
* Appointment Slot Recommender

### ✅ Frontend Chat Interface

* Clean HTML-based chat UI
* Real-time conversations with the assistant
* Served via FastAPI (`frontend.py`)

---

# **📂 Project Structure**

```
01_RAG_HEALTHCARE/
├── Data/                         # Add clinic PDFs here
│   ├── Clinic-Policies.pdf
│   ├── Doctor-Profiles.pdf
│   ├── Medical-FAQs.pdf
│   └── ...
│
├── graph-diagram/
│   └── healthcare_rag_graph.mmd  # Mermaid graph of architecture
│
├── static/
│   ├── img/
│   │   ├── desk1.jpg
│   │   └── doctor1.jpg
│   └── style.css
│
├── templates/
│   └── chat.html                 # Chat UI
│
├── vectorstore/                  # Auto-generated embeddings
│
├── frontend.py                   # Chat UI FastAPI app
├── main.py                       # Backend + agents FastAPI app
├── graph.py                      # Orchestration logic
├── prompts.py                    # Prompt templates
├── extra_prompts.py              # Additional prompt instructions
├── mermaid.py                    # Generates diagram from architecture
│
├── requirements.txt
├── readme.md
└── .env                          # Environment variables
```

---

# **🧠 Architecture Overview**

The system flows like this:

1. User sends a message via the web chat UI
2. Router Agent analyzes intent
3. Sends request to:

   * Doctor Agent (medical RAG info)
   * Appointment Scheduler Agent
   * Rewrite Agent
4. Agents may request:

   * Vector store retrieval
   * Google Calendar availability
   * Google Sheets DB updates
   * Email/SMS notifications
5. Guardrails validate safety
6. Final response returned to user

---

# **🚀 Run the Project Locally**

Below are complete instructions for **Linux/macOS**, **Windows**, installing dependencies, adding clinic data, generating vectors, and running both backend servers.

---

# **1️⃣ Create & Activate Virtual Environment**

## 🔹 **Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

## 🔹 **Windows (CMD or PowerShell)**

```bash
python -m venv venv
venv\Scripts\activate
```

You should now see:

```
(venv)
```

---

# **2️⃣ Install Requirements**

```bash
pip install -r requirements.txt
```

---

# **3️⃣ Add Clinic Data**

Place all your clinic PDFs in:

```
/Data
```

Examples:

* Clinic-Policies.pdf
* Staff-Credentials.pdf
* Medical-FAQs.pdf

These documents become part of the RAG knowledge base.

---

# **4️⃣ Build Vector Store (First Time Only)**

If vectors don't exist, build them:

```bash
python vectorstore/build_vectors.py
```

This generates embeddings in `/vectorstore`.

---

# **5️⃣ Create `.env` File**

Create a `.env` file in the root:

```
OPENAI_API_KEY=your_openai_key
GOOGLE_CREDENTIALS_PATH=credentials.json
```

If using Google tools, place your `credentials.json` in the project root.

---

# **6️⃣ Start Backend API (Agents, RAG, Tools)**

Run:

```bash
uvicorn main:app --reload
```

This typically runs the backend at:

👉 **[http://localhost:8000](http://localhost:8000)**

---

# **7️⃣ Start Frontend Chat UI**

Run:

```bash
uvicorn frontend:app --reload --port 8001
```

This launches the chat interface at:

👉 **[http://localhost:8001](http://localhost:8001)**

---

# **8️⃣ Use the Healthcare Chatbot**

Open your browser:

```
http://localhost:8001
```

You can now chat with the healthcare assistant.

---

# **🧩 Agent Responsibilities**

### **Router Agent**

Routes every incoming user message.

### **Doctor Agent**

* Retrieves medical context
* Uses clinic PDFs
* Generates safe educational responses

### **Appointment Scheduler Agent**

* Suggests open times
* Logs patient requests to Google Sheets
* Sets calendar events
* Sends reminders

### **Rewrite Agent**

Cleans or rephrases content for improved readability.

---

# **🛠️ Tools Integrated**

| Tool                         | Purpose                     |
| ---------------------------- | --------------------------- |
| Google Calendar Availability | Doctor’s free/busy schedule |
| Google Sheets DB             | Logs appointment requests   |
| Email/SMS Notification       | Sends confirmations         |
| Appointment Slot Recommender | AI-based slot ranking       |

---

# **🌐 Frontend UI**

* Located in `templates/chat.html`
* Styled via `static/style.css`
* Uses FastAPI backend `frontend.py`

---

# **📦 Future Enhancements**

* Multi-doctor load balancing
* Patient triage scoring
* Insurance/eligibility checks
* Voice input & text-to-speech

---

# **📄 License**

MIT License .


