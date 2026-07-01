<div align="center">

# 🎭 UNMASKED

**Know the character. Unmask their mind.**

A conversational RAG application for exploring the psychology of fictional characters —  grounded, context-aware, and hallucination-free.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-F55036?style=flat-square)](https://groq.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-4B0082?style=flat-square)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/license-MIT-000000?style=flat-square)](#license)



</div>

---

## Overview

Every great character hides something beneath the surface.

> Batman isn't just a vigilante. Johan Liebert isn't just a villain. Walter White isn't just a chemistry teacher.

**UNMASKED** is a Retrieval-Augmented Generation (RAG) application that lets you have natural, multi-turn conversations about fictional characters. Instead of relying on an LLM's internal (and often hallucinated) knowledge, every response is grounded in retrieved facts from a dedicated per-character knowledge base.

It doesn't roleplay as the character — **it helps you analyze them.**

```
Who is Batman?
Why does he refuse to kill?
What shaped his moral code?
Was he always this way?
How did his parents' death shape his identity?
```

A history-aware retrieval pipeline rewrites ambiguous follow-ups ("him", "that", "why") into standalone search queries, so conversations stay natural without repeating the character's name every turn.

<table>
<tr>
<td width="33%" valign="top">

**🧠 Grounded, not generic**
Every answer is backed by retrieved source chunks — not model hallucination.

</td>
<td width="33%" valign="top">

**💬 Multi-turn memory**
Follow-up questions resolve pronouns and context automatically.

</td>
<td width="33%" valign="top">

**⚡ Fast inference**
Powered by Groq's Llama 3.1 8B Instant for near-instant responses.

</td>
</tr>
</table>

---

## Demo

```text
$ python main.py

  UNMASKED
  Know the character. Unmask their mind.

 ─────────────────────────────────────────────

  Enter a character name to begin.
  Try: Batman · Walter White · Johan Liebert

  character › Batman

  ✓ Batman · indexed
  Ask anything about the character.  q to quit.

 ─────────────────────────────────────────────

  › Who is Batman?

  UNMASKED
  Batman is the alias of Bruce Wayne, a wealthy American playboy and
  industrialist. He is a vigilante driven by witnessing his parents'
  murder as a child — vowing to never kill, and to protect Gotham City
  from the evil that took everything from him.

 ─────────────────────────────────────────────

  › Why does he refuse to kill?

  UNMASKED
  Taking a life would make him indistinguishable from the criminals he
  fights. The no-kill rule is the one line he refuses to cross — the
  last thing separating his grief-driven mission from becoming the
  very thing he hunts.

 ─────────────────────────────────────────────

  › q
  Session ended.
```

"He", "that", and "his" all resolve correctly across turns — no context is lost, and no character name needs repeating.

---

## Architecture

UNMASKED runs two distinct pipelines: a **one-time ingestion pipeline** per character, and a **per-turn conversation pipeline** that runs on every message.

### Ingestion Pipeline *(runs once per character)*

```mermaid
flowchart TD
    A["👤 User selects a character"] --> B["📖 Wikipedia Document Loader"]
    B --> C["📄 Raw character article"]
    C --> D["✂️ Recursive Text Splitter"]
    D --> E["🧩 Small text chunks"]
    E --> F["🔢 HuggingFace Embeddings\n(all-MiniLM-L6-v2)"]
    F --> G[("🗄️ Chroma Vector DB")]

    style A fill:#1C3C3C,stroke:#fff,color:#fff
    style G fill:#4B0082,stroke:#fff,color:#fff
```

### Conversation Pipeline *(runs every turn)*

```mermaid
flowchart TD
    A["💬 User asks a question"] --> B["🧠 RunnableWithMessageHistory\nloads session history"]
    B --> C["🔄 History-Aware Retriever\nrewrites follow-up → standalone query"]
    C --> D[("🗄️ Chroma similarity search")]
    D --> E["📌 Top-3 relevant chunks"]
    E --> F["📦 Stuff Documents Chain\n(context + prompt + history)"]
    F --> G["⚡ Groq · Llama 3.1 8B Instant"]
    G --> H["✅ Grounded response"]
    H --> I["💾 Save exchange to session history"]

    style A fill:#1C3C3C,stroke:#fff,color:#fff
    style G fill:#F55036,stroke:#fff,color:#fff
    style H fill:#2E7D32,stroke:#fff,color:#fff
```

**Why the rewrite step matters:**

| Without rewriting | With history-aware rewriting |
|---|---|
| `"What about his childhood?"` → searches `"childhood"` (too vague) | `"What about his childhood?"` → rewritten to `"What was Batman's childhood like?"` |
| Retrieval misses relevant chunks | Retrieval is precise and grounded |

---

## Project Structure

```
unmasked/
├── main.py           # CLI entry point — banner, character load, chat loop
├── chain.py           # build_chain(character) — ingestion, pipeline assembly
├── prompts.py          # ChatPromptTemplate definitions — UNMASKED persona
├── memory.py           # Session store — InMemoryChatMessageHistory
├── Chroma_DB/           # Persisted vector collections, one per character
├── .env                  # GROQ_API and HF_TOKEN
└── requirements.txt
```

> **One file, one responsibility.** `chain.py` never touches CLI logic. `main.py` never touches embedding logic — making a future API version a drop-in swap of only `main.py`.

---

## How It Works

### Phase 1 — Knowledge Ingestion
1. User enters a character name.
2. `build_chain()` checks ChromaDB for an existing collection.
3. **Not found** → Wikipedia is scraped, split into chunks, embedded, and stored in ChromaDB.
4. **Found** → the existing collection loads directly, no re-scraping.

### Phase 2 — Conversation
1. `RunnableWithMessageHistory` loads the chat history for the session.
2. The **History-Aware Retriever** rewrites the question if it's a follow-up.
3. ChromaDB similarity search returns the top 3 relevant chunks.
4. Chunks + chat history + system prompt are passed to **Groq Llama 3.1**.
5. A grounded response is returned and the exchange is saved back to session history.

---

## Memory Model

Session history lives in memory for the lifetime of the running process:

```python
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

| Event | History State |
|---|---|
| Chatting within one CLI run | ✅ Persists — every prior message remembered |
| Typing `quit` | ❌ Cleared — process exits, dict is gone |
| Running `python main.py` again | 🔄 Fresh start, empty store |

> The **ChromaDB vector store** persists across runs regardless — once a character is scraped and embedded, reloading is instant on future runs.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python | Core application |
| Orchestration | LangChain | Chain composition, RAG pipeline |
| LLM Provider | Groq | Fast inference |
| Model | Llama 3.1 8B Instant | Response generation |
| Vector Store | ChromaDB | Embedding storage + similarity search |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Local, free, 384-dim vectors |
| Data Source | Wikipedia Loader | Character source material |
| Memory | In-memory dict + `InMemoryChatMessageHistory` | Session-scoped conversation memory |
| CLI | Rich | Terminal UI |

### LangChain Concepts Used

| Concept | Role in UNMASKED |
|---|---|
| `ChatPromptTemplate` | Defines the UNMASKED persona and structures system / history / human messages |
| `MessagesPlaceholder` | Injects variable-length chat history into the prompt |
| `create_stuff_documents_chain` | Stuffs retrieved chunks into `{context}` before generation |
| `create_retrieval_chain` | Combines retriever + document chain into one callable pipeline |
| `create_history_aware_retriever` | Rewrites follow-up questions into standalone queries before retrieval |
| `RunnableWithMessageHistory` | Adds multi-turn session memory to an otherwise stateless chain |

---

## Setup

```bash
git clone <repo>
cd unmasked

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Add your API keys to a `.env` file:

```env
GROQ_API=your_groq_key_here
HF_TOKEN=your_huggingface_token_here
```

---

## Usage

```bash
python main.py
```

Enter any fictional character at the prompt. UNMASKED scrapes and indexes Wikipedia on first load, then caches it for future runs.

| Input | Action |
|---|---|
| Any question | Grounded psychological analysis |
| `quit` / `exit` / `q` | End the session |
| `Ctrl+C` | Exit immediately |

---

## Current Status

> **UNMASKED V1** is a **CLI-only, single-character-per-session** application.

It focuses entirely on deep, grounded psychological conversations with full multi-turn memory and history-aware retrieval.

- ❌ No persistent chat storage
- ❌ No web UI
- ❌ No multi-character sessions

The goal of V1 is to master and demonstrate the core **LangChain conversational RAG stack**, cleanly and end to end.

### 🗺️ Roadmap Ideas
- [ ] Web UI (FastAPI + React/Streamlit)
- [ ] Persistent chat history across runs
- [ ] Multi-character comparison sessions
- [ ] Support for non-Wikipedia sources (fan wikis, scripts)

---

<div align="center">

*Every character wears a mask. UNMASKED helps you understand what's underneath.*

</div>
