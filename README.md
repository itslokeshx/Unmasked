# 🎭 UNMASKED

**Know the Character. Unmask Their Mind.**

UNMASKED is an AI-powered conversational RAG application that lets you chat with fictional characters through a psychological lens.

Instead of simply answering factual questions, UNMASKED retrieves grounded knowledge about a character and analyzes the motivations, beliefs, trauma, relationships, and decisions that shaped them.

It doesn't roleplay as the character.
It helps you unmask them.

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

- 💬 Chat naturally with fictional characters
- 🧠 Psychological character analysis
- 📚 Wikipedia-powered Retrieval-Augmented Generation (RAG)
- 🔍 Context-aware document retrieval
- 💭 Multi-turn conversations with memory
- 🔄 History-aware question rewriting
- ⚡ Fast responses powered by Groq + Llama 3.1

---

## 🧠 Example

```
Who is Johan Liebert?

↓

Why does he smile while manipulating people?

↓

Was he born evil?

↓

What belief drives all of his actions?

↓

Who influenced him the most?

↓

Why do people relate to him?
```

Each question builds on the previous conversation without losing context.

---

## ⚙️ How It Works

```
User Question
      │
      ▼
Conversation History
      │
      ▼
History-Aware Retriever
      │
      ▼
Question Rewriting
      │
      ▼
Vector Search (ChromaDB)
      │
      ▼
Relevant Character Knowledge
      │
      ▼
Document Chain (context stuffing)
      │
      ▼
LLM
      │
      ▼
Grounded Character Analysis
```

---

## 🛠 Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Orchestration | LangChain |
| LLM Provider | Groq |
| Model | Llama 3.1 8B Instant |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace (`all-MiniLM-L6-v2`) |
| Data Source | Wikipedia Loader |

---

## 📌 Current Status

UNMASKED is currently focused on character conversations.

Future versions will expand beyond fictional characters into deeper psychological reflection and self-analysis, but the current goal is to build the best conversational character analysis experience possible.

---

*Every character wears a mask. UNMASKED helps you understand what's underneath.*