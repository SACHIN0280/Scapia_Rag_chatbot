import json

def get_chats():
    with open("chats.json", "r") as f:
        return json.load(f)

chats = get_chats()
for k,v in chats.items():
    print(f"{k}: {v['title']} - {len(v.get('messages', []))} messages")
