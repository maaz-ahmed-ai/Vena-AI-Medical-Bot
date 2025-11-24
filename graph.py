# graph.py

import os
from pathlib import Path
from typing import List, TypedDict

from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
# from extra_prompts import system_prompt
from prompts import system_prompt




# ------------------------
#   PATHS & CONFIG
# ------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"                 # D:\Upwork_projects\01_RAG_HealthCare\Data
VECTORSTORE_DIR = BASE_DIR / "vectorstore"   # created automatically
GRAPH_DIAGRAM_DIR = BASE_DIR / "graph-diagram"  # D:\Upwork_projects\01_RAG_HealthCare\graph-diagram

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


# ------------------------
#   LANGGRAPH STATE
# ------------------------
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]



# ------------------------
#   ENV & MODELS
# ------------------------

load_dotenv()  # reads .env in project root


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-large")


# ------------------------
#   DATA INGEST + VECTORSTORE
# ------------------------

def load_pdfs() -> List[Document]:
    """
    Load all PDFs from the Data/ directory.
    """
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    docs = loader.load()
    return docs


def chunk_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(docs)


def build_vectorstore() -> Chroma:
    """
    Build and persist a Chroma vector store from PDFs in Data/.
    """
    print(f"[RAG] Loading PDFs from: {DATA_DIR}")
    docs = load_pdfs()
    print(f"[RAG] Loaded {len(docs)} pages. Chunking...")
    chunks = chunk_documents(docs)
    print(f"[RAG] Split into {len(chunks)} chunks. Creating embeddings…")

    embeddings = get_embeddings()
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )
    vectordb.persist()
    print(f"[RAG] Vector store created at: {VECTORSTORE_DIR}")
    return vectordb


def get_or_create_vectorstore() -> Chroma:
    """
    Load existing vector store if present, otherwise build it.
    """
    if VECTORSTORE_DIR.exists() and any(VECTORSTORE_DIR.iterdir()):
        print(f"[RAG] Loading existing vector store from: {VECTORSTORE_DIR}")
        embeddings = get_embeddings()
        vectordb = Chroma(
            embedding_function=embeddings,
            persist_directory=str(VECTORSTORE_DIR),
        )
        return vectordb

    return build_vectorstore()


# ------------------------
#   LANGGRAPH NODES
# ------------------------

def make_retriever_node(retriever):
    def retrieve(state: AgentState):
        # Last user message
        last_message = state["messages"][-1]
        question = last_message.content

        docs = retriever.invoke(question)

        context_text = "\n\n".join([d.page_content for d in docs])

        rag_msg = AIMessage(
            content=f"[RAG CONTEXT START]\n{context_text}\n[RAG CONTEXT END]"
        )

        return {"messages": [rag_msg]}
    return retrieve



def make_generate_node(llm: ChatOpenAI):
    def generate(state: AgentState):

        # All messages so far
        msgs = [SYSTEM] + list(state["messages"])

        response = llm.invoke(msgs)

        return {"messages": [AIMessage(content=response.content)]}

    return generate

SYSTEM = SystemMessage(content=system_prompt())

# ------------------------
#   BUILD LANGGRAPH
# ------------------------
def build_graph(retriever, llm):
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", make_retriever_node(retriever))
    graph.add_node("generate", make_generate_node(llm))

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)



def save_mermaid_diagram(app) -> None:
    """
    Save a Mermaid diagram of the graph under graph-diagram/.
    """
    try:
        GRAPH_DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
        mermaid_str = app.get_graph().draw_mermaid()
        out_path = GRAPH_DIAGRAM_DIR / "healthcare_rag_graph.mmd"
        out_path.write_text(mermaid_str, encoding="utf-8")
        print(f"[RAG] Mermaid diagram saved to: {out_path}")
    except Exception as e:
        print(f"[RAG] Could not save Mermaid diagram: {e}")


# ------------------------
#   SIMPLE CLI (Q/A)
# ------------------------
def main():
    vectordb = get_or_create_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = get_llm()

    app = build_graph(retriever, llm)

    print("\n=== Medical RAG Agent (Reducer Version) ===\n")

    config = {"configurable": {"thread_id": "cli-session-001"}}

    while True:
        user_q = input("You: ").strip()
        if user_q.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break

        result = app.invoke(
            {"messages": [HumanMessage(content=user_q)]},
            config=config,
        )

        final_message = result["messages"][-1]
        print(f"Assistant: {final_message.content}\n")


if __name__ == "__main__":
    main()
