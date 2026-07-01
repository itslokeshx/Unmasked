from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
    ("human", "{text}")
])

memory_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that return repsonse to user in one line!"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{text}")
])

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer only using the provided context"),
    ("human",
     "context:\n{context}\n\nQuestion:{input}")
])

history_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Given the chat history and the latest user question, "
        "rewrite it into a standalone question. "
        "Do NOT answer the question."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Use the following pieces of retrieved context to answer the question.\n"
        "If the question is conversational, personal, or about details mentioned in the chat history (such as the user's name), "
        "rely on the chat history to answer directly. If you do not know the answer, say you do not know.\n\n"
        "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
