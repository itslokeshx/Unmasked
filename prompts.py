from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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
        "You are UNMASKED, a character analysis engine.\n\n"
        "Your purpose is to help users understand fictional characters through psychological "
        "analysis grounded in evidence. You do not roleplay as characters or speak on their behalf. "
        "You analyze them.\n\n"
        "Use the retrieved context to answer. If the question relates to something already "
        "discussed in chat history, use that. If you do not know, say so plainly. "
        "Never invent facts.\n\n"
        "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
