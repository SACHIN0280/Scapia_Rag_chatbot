import json

with open("chats.json", "r") as f:
    chats = json.load(f)

current_chat_id = "58a55b85-e696-491e-bf21-2c78c382d227"
active_chat = chats.get(current_chat_id)
messages = active_chat.get("messages", [])
prompt = "hello test"
messages.append({"role": "user", "content": prompt})

if len(messages) == 1 and active_chat["title"] == "New Chat":
    print("INSIDE IF BLOCK!")
else:
    print(f"FAILED. len={len(messages)}, title={active_chat['title']}")

