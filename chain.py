import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory

from prompts import rag_prompt, history_prompt, qa_prompt
from memory import get_session_history, session_id

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_TOKEN")

GROQ_API = os.environ["GROQ_API_KEY"]

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1, max_tokens=1024, api_key=GROQ_API)

parser = StrOutputParser()

chain = llm | parser

hg_embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

Vector_DB = Chroma(
    collection_name="Batman_DB",
    embedding_function=hg_embedding,
    persist_directory="Chroma_DB"
)

retriever = Vector_DB.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

document_chain = create_stuff_documents_chain(
    llm,
    rag_prompt
)

retrieval_chain = create_retrieval_chain(
    retriever,
    document_chain
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, history_prompt
)

convo_document_chain = create_stuff_documents_chain(llm, qa_prompt)
convo_retrieval_chain = create_retrieval_chain(history_aware_retriever, convo_document_chain)

conversation_chain = RunnableWithMessageHistory(
    convo_retrieval_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"
)
