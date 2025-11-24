# main.py (FastAPI Server)

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_core.messages import HumanMessage, SystemMessage

from graph import (
    get_or_create_vectorstore,
    get_llm,
    build_graph,
    system_prompt
)

# ---------------------------------------------------
# FastAPI Setup
# ---------------------------------------------------

app = FastAPI(title="Clinic Self-RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default-session"


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


# ---------------------------------------------------
# Load LLM + Vectorstore + App
# ---------------------------------------------------

vectordb = get_or_create_vectorstore()
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

llm = get_llm()

# Build LangGraph RAG Agent
app_graph = build_graph(retriever, llm)

# System prompt message
SYSTEM = SystemMessage(content=system_prompt())


# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def extract_sources(docs):
    sources = []
    for d in docs:
        meta = d.metadata or {}
        filename = meta.get("source", "unknown")
        page = meta.get("page", "?")
        sources.append(f"{filename} (page {page})")
    return sources


# ---------------------------------------------------
# API Routes
# ---------------------------------------------------

@app.get("/")
def root():
    return {"message": "Clinic Self-RAG Assistant is running. POST /chat"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    question = req.question
    thread_id = req.thread_id

    # LangGraph config -> thread-level memory
    config = {"configurable": {"thread_id": thread_id}}

    # Call LangGraph pipeline
    result = app_graph.invoke(
        {"messages": [SYSTEM, HumanMessage(content=question)]},
        config=config
    )

    # Final bot message
    bot_msg = result["messages"][-1].content

    # Extract RAG context (PDF chunks)
    rag_docs = []
    for msg in result["messages"]:
        if msg.content.startswith("[RAG CONTEXT START]"):
            # nothing to store, but signal rag was used
            pass

    # Vectorstore retriever output for sources
    docs = retriever.invoke(question)
    sources = extract_sources(docs)

    return ChatResponse(answer=bot_msg, sources=sources)
