from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

store = {}

def get_session_history(session_id):

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

session_id = "chat1"

history = [
    HumanMessage("Hi my name is loki"),
    AIMessage("Greetings, Loki, I'm here to assist you with any questions or tasks you may have."),
    HumanMessage("From now your name is jarvis"),
    AIMessage("I'm at your service, master."),
    HumanMessage("My fav color is black and i love virat kohli")
]
