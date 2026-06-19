import json

with open("chats.json", "r") as f:
    chats = json.load(f)

for cid, cdata in chats.items():
    if cdata["title"] == "New Chat" and len(cdata.get("messages", [])) > 0:
        print(f"Modifying chat {cid}")
        prompt = cdata["messages"][0]["content"]
        cdata["title"] = prompt[:30]

with open("chats.json", "w") as f:
    json.dump(chats, f, indent=4)
