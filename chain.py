import os
import uuid
import time
import warnings
import logging

os.environ["TQDM_DISABLE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("chromadb").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

import wikipedia
import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory

from prompts import history_prompt, make_qa_prompt
from memory import get_session_history

wikipedia.set_user_agent("Unmasked/1.0 (Character Analysis Tool; Python)")

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")

GROQ_API = os.environ["GROQ_API_KEY"]

MAX_RETRIES = 3


def load_from_wikipedia(character):
    for attempt in range(MAX_RETRIES):
        try:
            loader = WikipediaLoader(query=character, load_max_docs=5)
            docs = loader.load()
            if docs:
                return docs
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
    raise RuntimeError(
        f"Could not fetch Wikipedia data for '{character}'. "
        "Check your internet connection and try again."
    )


def build_chain(character):
    collection_name = character.lower().replace(" ", "_") + "_db"

    client = chromadb.PersistentClient(path="Chroma_DB")
    existing = {c.name.lower(): c.name for c in client.list_collections()}

    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if collection_name not in existing:
        docs = load_from_wikipedia(character)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name=collection_name,
            persist_directory="Chroma_DB"
        )
        ingested = True
    else:
        collection_name = existing[collection_name]
        db = Chroma(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory="Chroma_DB"
        )
        ingested = False

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=1024,
        api_key=GROQ_API,
        request_timeout=30
    )

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    history_aware_retriever = create_history_aware_retriever(llm, retriever, history_prompt)
    document_chain = create_stuff_documents_chain(llm, make_qa_prompt(character))
    retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    session_id = str(uuid.uuid4())[:8]

    conversation_chain = RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversation_chain, session_id, ingested
