from chain import conversation_chain, session_id

response = conversation_chain.invoke(
    {
        "input": "whats your and my name"
    },
    config={
        "configurable": {
            "session_id": session_id
        }
    }
)

print(response["answer"])
