# UNMASKED V1

**Know the character. Unmask their mind.**

UNMASKED is an AI-powered conversational RAG application that helps users explore and understand fictional characters through grounded, context-aware conversations.

Unlike traditional AI chatbots that rely solely on a language model's internal knowledge, UNMASKED retrieves information from a dedicated knowledge base before generating every response. This keeps conversations factual, consistent, and closely tied to the character's established story rather than producing hallucinated or generic answers.

The current version focuses on **character analysis**, enabling users to ask natural follow-up questions and progressively uncover a character's motivations, beliefs, personality, relationships, trauma, decision-making, and overall psychological development.

It does not roleplay as the character. It helps you unmask them.

---

## Table of Contents

1. [What is UNMASKED](#what-is-unmasked)
2. [Example Conversation](#example-conversation)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [How It Works](#how-it-works)
6. [Memory Model](#memory-model)
7. [Tech Stack](#tech-stack)
8. [LangChain Concepts Used](#langchain-concepts-used)
9. [Setup](#setup)
10. [Usage](#usage)
11. [Current Status](#current-status)

---

## What is UNMASKED

Every great character hides something beneath the surface.

Batman isn't just a vigilante.
Johan Liebert isn't just a villain.
Walter White isn't just a chemistry teacher.

UNMASKED lets you have natural conversations about these characters while using Retrieval-Augmented Generation (RAG) to provide grounded, context-aware psychological analysis instead of hallucinated answers.

For example, instead of simply answering *"Who is Batman?"*, users can continue the conversation with questions like:

- Why does Batman refuse to kill?
- What shaped his moral code?
- Was he always this way?
- How did the death of his parents influence his identity?
- What separates Bruce Wayne from Batman?

UNMASKED maintains conversational context across multiple turns so follow-up questions feel natural without repeatedly mentioning the character's name. A history-aware retrieval pipeline rewrites ambiguous questions into standalone queries before searching the vector database, ensuring accurate document retrieval and grounded responses.

---

## Example Conversation

```
$ python main.py

╭──────────────────────────────────╮
│        U N M A S K E D          │
│  Know the character. Unmask      │
│         their mind.              │
╰──────────────────────────────────╯

Who do you want to unmask: Johan Liebert

  Scraped and indexed Wikipedia for Johan Liebert.
  Type quit to end the session.

You: Who is Johan Liebert?
UNMASKED  Johan is not a villain in the traditional sense...

You: Why does he smile while manipulating people?
UNMASKED  Because the smile is the only face that was never taken from him...

You: Was he born evil?
UNMASKED  No. That is the entire point of Monster...

You: quit
  Session ended.
```

Each question builds on the previous conversation without losing context. "he", "that", and "his" all resolve correctly because of session memory and history-aware retrieval.

---

## Architecture

```
              User selects a character
                      │
                      ▼
           Wikipedia Document Loader
                      │
                      ▼
              Raw Character Article
                      │
                      ▼
          Recursive Text Splitter
                      │
                      ▼
             Small Text Chunks
                      │
                      ▼
          HuggingFace Embeddings
                      │
                      ▼
              Chroma Vector DB
════════════════════════════════════════

              User asks a question
                      │
                      ▼
      RunnableWithMessageHistory
                      │
                      ▼
        History Aware Retriever
                      │
                      ▼
      Rewrite Follow-up Question
                      │
                      ▼
          Chroma Similarity Search
                      │
                      ▼
          Top Relevant Chunks
                      │
                      ▼
        Stuff Document Chain
                      │
                      ▼
        Prompt + Context + History
                      │
                      ▼
             Groq Llama 3.1
                      │
                      ▼
             Final AI Response
                      │
                      ▼
          Save Conversation History
```

---

## Project Structure

```
unmasked/
├── main.py           # CLI entry point — banner, character load, chat loop
├── chain.py          # build_chain(character) — ingestion, pipeline assembly
├── prompts.py        # ChatPromptTemplate definitions — UNMASKED persona
├── memory.py         # Session store — InMemoryChatMessageHistory
├── Chroma_DB/        # Persisted vector collections, one per character
├── .env              # GROQ_API and HF_TOKEN
└── requirements.txt
```

One file, one responsibility. `chain.py` never touches CLI logic. `main.py` never touches embedding logic. This separation makes a future API version a drop-in swap of only `main.py`.

---

## How It Works

### Phase 1 — Knowledge Ingestion (once per character)

1. User enters a character name.
2. `build_chain` checks ChromaDB for an existing collection.
3. If not found: Wikipedia is scraped, documents are split into chunks, embedded with HuggingFace, and stored in ChromaDB.
4. If found: the existing collection is loaded directly — no re-scraping.

### Phase 2 — Conversation

```
User types a question
        │
        ▼
RunnableWithMessageHistory loads chat history for session
        │
        ▼
History-Aware Retriever rewrites the question if it's a follow-up
        │
        ▼
ChromaDB similarity search → top 3 relevant chunks
        │
        ▼
Chunks + chat history + system prompt passed to Groq Llama 3.1
        │
        ▼
Grounded response returned
        │
        ▼
Exchange saved back to session history
```

**Why question rewriting?**

Without it:

```
Who is Batman?
→ What about his childhood?
```

The retriever searches "childhood" — too vague. With history-aware rewriting:

```
What about his childhood?
→ What was Batman's childhood like?
```

Retrieval becomes accurate.

---

## Memory Model

Session history is held in-memory for the lifetime of the running process.

```python
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

| Event | History State |
|---|---|
| Chatting within one CLI run | Persists — every prior message remembered |
| Typing `quit` | Cleared — process exits, dict is gone |
| Running `python main.py` again | Fresh start, empty store |

The ChromaDB vector store persists across runs regardless. Once a character is scraped and embedded, reloading is instant on future runs.

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
| Memory | In-memory dict + InMemoryChatMessageHistory | Session-scoped conversation memory |
| CLI | Rich | Terminal UI |

---

## LangChain Concepts Used

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
source venv/bin/activate

pip install -r requirements.txt
```

Add your API keys to `.env`:

```
GROQ_API=your_groq_key_here
HF_TOKEN=your_huggingface_token_here
```

---

## Usage

```bash
python main.py
```

Enter any fictional character at the prompt. UNMASKED will scrape and index Wikipedia on first load, then cache it for future runs.

**Commands during chat:**

| Input | Action |
|---|---|
| Any question | Grounded psychological analysis |
| `quit` / `exit` / `q` | End the session |
| `Ctrl+C` | Exit immediately |

---

## Current Status

UNMASKED V1 is a CLI-only, single-character-per-session application.

It focuses entirely on deep, grounded psychological conversations with full multi-turn memory and history-aware retrieval. There is no persistent storage, no web UI, and no multi-character sessions in this version.

The goal of V1 is to master and demonstrate the core LangChain conversational RAG stack cleanly, end to end.

---

*Every character wears a mask. UNMASKED helps you understand what's underneath.*
