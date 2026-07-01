# 🎭 UNMASKED

**Know the Character. Unmask Their Mind.**

UNMASKED is an AI-powered conversational RAG application that lets you chat with fictional characters through a psychological lens.

Instead of simply answering factual questions, UNMASKED retrieves grounded knowledge about a character and analyzes the motivations, beliefs, trauma, relationships, and decisions that shaped them.

It doesn't roleplay as the character.
It helps you unmask them.

---

## Table of Contents

1. [What is UNMASKED](#-what-is-unmasked)
2. [Features](#-features)
3. [Example Conversation](#-example-conversation)
4. [Architecture](#-architecture)
5. [Project Structure](#-project-structure)
6. [How It Works — Data Flow](#-how-it-works--data-flow)
7. [Memory Model](#-memory-model)
8. [Tech Stack](#-tech-stack)
9. [LangChain Concepts Used](#-langchain-concepts-used)
10. [Setup](#-setup)
11. [Usage](#-usage)
12. [Current Status](#-current-status)

---

## ✨ What is UNMASKED?

Every great character hides something beneath the surface.

Batman isn't just a vigilante.
Johan Liebert isn't just a villain.
Walter White isn't just a chemistry teacher.

UNMASKED lets you have natural conversations about these characters while using Retrieval-Augmented Generation (RAG) to provide grounded, context-aware psychological analysis instead of hallucinated answers.

Ask follow-up questions naturally, dig deeper into their choices, and uncover what truly drives them.

---

## 🚀 Features

- 💬 Chat naturally with fictional characters, entirely from the terminal
- 🧠 Psychological character analysis — motivations, trauma, defense mechanisms, philosophy
- 📚 Wikipedia-powered Retrieval-Augmented Generation (RAG)
- 🔍 Context-aware document retrieval via ChromaDB
- 💭 Multi-turn conversations with session memory
- 🔄 History-aware question rewriting for accurate follow-up retrieval
- ⚡ Fast responses powered by Groq + Llama 3.1
- 🗂️ Per-character vector store caching — no re-scraping on repeat runs

---

## 🧠 Example Conversation

```
$ python main.py

Who do you want to unmask today?: Johan Liebert

Scraping sources for Johan Liebert...
Embedding and indexing...
Ready. Ask anything.

You: Who is Johan Liebert?
UNMASKED: Johan is not a villain in the traditional sense...

You: Why does he smile while manipulating people?
UNMASKED: Because the smile is the only face that was never taken from him...

You: Was he born evil?
UNMASKED: No. That's the entire point of Monster...

You: What belief drives all of his actions?
UNMASKED: ...

You: quit
Session ended.
```

Each question builds on the previous conversation without losing context — "he", "that", and "his actions" all resolve correctly because of session memory and history-aware retrieval.

---

## 🏗 Architecture

```
                        ┌──────────────────┐
                        │   CLI (main.py)   │
                        │  banner + loop    │
                        └────────┬──────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
         ┌──────────────┐ ┌────────────┐ ┌───────────────┐
         │  chain.py    │ │ memory.py  │ │  prompts.py   │
         │  RAG pipeline│ │ session    │ │  UNMASKED     │
         │  assembly    │ │ store dict │ │  persona      │
         └──────┬───────┘ └─────┬──────┘ └───────┬───────┘
                │                │                │
                ▼                │                │
       ┌─────────────────┐       │                │
       │ Wikipedia Loader│       │                │
       │ (data source)   │       │                │
       └────────┬────────┘       │                │
                │                │                │
                ▼                │                │
       ┌─────────────────┐       │                │
       │ Text Splitter   │       │                │
       │ (chunking)      │       │                │
       └────────┬────────┘       │                │
                │                │                │
                ▼                │                │
       ┌─────────────────┐       │                │
       │ HuggingFace     │       │                │
       │ Embeddings      │       │                │
       └────────┬────────┘       │                │
                │                │                │
                ▼                │                │
       ┌─────────────────┐       │                │
       │ ChromaDB        │       │                │
       │ (vector store,  │       │                │
       │ cached per      │       │                │
       │ character)      │       │                │
       └────────┬────────┘       │                │
                │                │                │
                ▼                │                │
       ┌──────────────────────┐  │                │
       │ History-Aware        │◄─┘                │
       │ Retriever            │                   │
       └────────┬─────────────┘                   │
                │                                  │
                ▼                                  │
       ┌──────────────────────┐                    │
       │ Document Chain        │◄──────────────────┘
       │ (context stuffing)    │
       └────────┬─────────────┘
                │
                ▼
       ┌──────────────────────┐
       │ Retrieval Chain        │
       └────────┬─────────────┘
                │
                ▼
       ┌──────────────────────┐
       │ Groq LLM                │
       │ (Llama 3.1 8B Instant)  │
       └────────┬─────────────┘
                │
                ▼
       ┌──────────────────────┐
       │ Grounded Psychological │
       │ Response                │
       └──────────────────────┘
```

---

## 📁 Project Structure

```
unmasked/
├── main.py            # CLI entrypoint — banner, character load, chat loop
├── chain.py            # RAG pipeline: retriever, history-aware retriever,
│                        # document chain, retrieval chain assembly
├── prompts.py           # ChatPromptTemplate definitions — UNMASKED persona
├── memory.py             # Session store — RunnableWithMessageHistory wiring
├── chroma_db/             # Auto-created, persisted vector collections
│                          # one collection per character (cached)
├── .env                    # GROQ_API_KEY
└── requirements.txt
```

**Design principle:** one file, one responsibility. `chain.py` never touches CLI logic. `main.py` never touches embedding logic. This separation is what makes a future FastAPI/React version a drop-in swap of only `main.py`.

---

## ⚙️ How It Works — Data Flow

```
1. User enters character name
        │
        ▼
2. Check ChromaDB for existing collection
        │
   ┌────┴────┐
   │ cached? │
   └────┬────┘
    yes │ no
        │  └──► Scrape Wikipedia → Chunk (RecursiveCharacterTextSplitter)
        │       → Embed (HuggingFace all-MiniLM-L6-v2) → Store in ChromaDB
        │
        ▼
3. Build retriever from collection
        │
        ▼
4. Assemble chain:
   history_aware_retriever + document_chain → retrieval_chain
        │
        ▼
5. Wrap chain with RunnableWithMessageHistory (session_id generated)
        │
        ▼
6. CLI loop begins — user asks questions
        │
        ▼
7. For each message:
   a. Fetch chat_history for session_id
   b. Rewrite follow-up question into standalone query (if needed)
   c. Similarity search in ChromaDB → top-k relevant chunks
   d. Stuff chunks into {context} of UNMASKED prompt
   e. Send to Groq LLM
   f. Save exchange back to session history
   g. Print response
        │
        ▼
8. User types "quit" → session ends, memory cleared
```

---

## 🧩 Memory Model

Session history is held **in-memory only**, for the lifetime of the running process.

```python
store = {}  # session_id → ChatMessageHistory

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
```

| Event | History State |
|---|---|
| Chatting within one CLI run | Persists — every prior message remembered |
| Typing `quit` | Cleared — process exits, dict is gone |
| Running `python main.py` again | Fresh start, empty store |

This is intentional for v1 — the goal is to prove `RunnableWithMessageHistory` mechanics cleanly. Persistent storage (SQLite/file-based) is a v2 concern, and swapping it in later only requires changing `memory.py` — the chain logic in `chain.py` stays untouched.

**Separate from this:** the ChromaDB vector store persists across runs regardless — once a character is scraped and embedded, reloading them is instant on future runs.

---

## 🛠 Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python | Core application |
| Orchestration | LangChain | Chain composition, RAG pipeline |
| LLM Provider | Groq | Fast inference |
| Model | Llama 3.1 8B Instant | Response generation |
| Vector Store | ChromaDB | Embedding storage + similarity search |
| Embeddings | HuggingFace (`all-MiniLM-L6-v2`) | Local, free, 384-dim vectors |
| Data Source | Wikipedia Loader | Character source material |
| Memory | In-memory dict + `ChatMessageHistory` | Session-scoped conversation memory |

---

## 🔗 LangChain Concepts Used

| Concept | Role in UNMASKED |
|---|---|
| `ChatPromptTemplate` | Defines the UNMASKED persona and structures system/history/human messages |
| `MessagesPlaceholder` | Injects variable-length chat history into the prompt cleanly |
| `create_stuff_documents_chain` | Stuffs retrieved chunks into `{context}` before generation |
| `create_retrieval_chain` | Combines retriever + document chain into one callable pipeline |
| `create_history_aware_retriever` | Rewrites follow-up questions ("why does he smile?") into standalone queries before retrieval |
| `RunnableWithMessageHistory` | Adds multi-turn session memory to an otherwise stateless chain |

---

## 🔧 Setup

```bash
# clone / navigate to project
cd unmasked

# install dependencies
pip install -r requirements.txt

# add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env
```

**requirements.txt**
```
langchain
langchain-groq
langchain-huggingface
langchain-chroma
langchain-community
chromadb
python-dotenv
wikipedia
```

---

## ▶️ Usage

```bash
python main.py
```

```
Who do you want to unmask today?: Batman

Scraping sources for Batman...
Embedding and indexing...
Ready. Ask anything.

You: Why does Batman refuse to kill?
UNMASKED: ...

You: quit
Session ended.
```

**Commands during chat:**
- `quit` / `exit` — end the session
- Any character name at startup — loads fresh or from cache automatically

---

## 📌 Current Status

UNMASKED v1 is a **CLI-only, Character Mode application.**

It focuses entirely on deep, grounded psychological conversations about a single fictional character per session, with full multi-turn memory and history-aware retrieval.

There is no persistent storage, no UI, and no self-reflection ("Mirror Mode") in this version — the goal of v1 is to master and demonstrate the core LangChain conversational RAG stack cleanly, end to end.

---

*Every character wears a mask. UNMASKED helps you understand what's underneath.*
