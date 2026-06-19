import uuid
import json

chats = {
    "test_id": {"title": "New Chat", "messages": [], "pinned": False}
}

active_chat = chats["test_id"]
messages = active_chat["messages"]
prompt = "what is a vector db"
messages.append({"role": "user", "content": prompt})

if len(messages) == 1 and active_chat["title"] == "New Chat":
    try:
        raise Exception("Simulated Groq Failure")
    except Exception:
        new_title = prompt[:30]
        
    chats_copy = dict(chats)
    chats_copy["test_id"]["title"] = new_title
    chats = chats_copy

print(f"Result title: {chats['test_id']['title']}")
