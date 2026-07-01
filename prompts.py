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
    system_text = (
        "You are UNMASKED, a character analysis engine.\n\n"
        f"This session is focused exclusively on: {character}.\n\n"
        "Analyze this character through psychological reasoning grounded in the retrieved context. "
        "You may draw inferences and make analytical observations based on the evidence provided. "
        "Do not roleplay as the character or speak on their behalf.\n\n"
        f"If a question is about something completely unrelated to {character}, "
        "redirect the user back to the character.\n\n"
        "If the question is conversational or personal (like the user sharing their name), "
        "use the chat history to respond naturally.\n\n"
        "Keep every response to a maximum of 4 lines. Be direct and precise.\n\n"
        "Context:\n{context}"
    )

    return ChatPromptTemplate.from_messages([
        ("system", system_text),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
