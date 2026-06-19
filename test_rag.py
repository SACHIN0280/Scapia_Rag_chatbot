from utils import load_vector_store
import sys

vs = load_vector_store()
if not vs:
    print("No vector store found.")
    sys.exit(0)

retriever = vs.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke("explain the summary of this pdf in short")

print(f"Retrieved {len(docs)} documents.")
for i, doc in enumerate(docs):
    print(f"\n--- Doc {i+1} ---")
    print(doc.page_content[:200] + "...")
