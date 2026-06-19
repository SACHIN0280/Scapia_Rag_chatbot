import json

with open("chats.json", "r") as f:
    chats = json.load(f)

for cid, cdata in chats.items():
    print(f"Chat: {cdata['title']}")
    print(f"Messages count: {len(cdata.get('messages', []))}")
    if cdata.get('messages'):
        print(f"First message: {cdata['messages'][0]['content'][:30]}")
    print("---")
