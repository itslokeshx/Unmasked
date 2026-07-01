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


def make_qa_prompt(character):
    return ChatPromptTemplate.from_messages([
        (
            "system",
            f"You are UNMASKED, a character analysis engine.\n\n"
            f"This session is focused exclusively on: {character}.\n\n"
            "Analyze this character through psychological evidence. "
            "Do not roleplay as the character or speak on their behalf.\n\n"
            "You must ONLY use the retrieved context provided below to answer. "
            "Do not use your training knowledge. "
            "If the context does not contain enough information, say so clearly.\n\n"
            "Keep every response to a maximum of 4 lines. Be direct and precise.\n\n"
            "Context:\n{context}"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
