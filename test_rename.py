import json
from langchain_groq import ChatGroq

prompt = "what is rag"

title_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
title_prompt = f"Generate a short 2-4 word title summarizing this query. Output ONLY the title, no quotes, no extra text:\n\n{prompt}"
try:
    generated_title = title_llm.invoke(title_prompt).content.strip().strip('"')
    print("SUCCESS:", generated_title)
except Exception as e:
    print("ERROR:", e)
