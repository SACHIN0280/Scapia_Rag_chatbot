import sys
from utils import load_vector_store
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

vs = load_vector_store()
retriever = vs.as_retriever(search_kwargs={"k": 15})
docs = retriever.invoke("explain the summary of this pdf in short")
context = "\n\n---\n\n".join(doc.page_content for doc in docs)

prompt_template = """You are a helpful AI assistant analyzing a user's uploaded document.
Your task is to answer the user's question based ONLY on the provided context chunks.

RULES:
- Base your answer ONLY on the context below. Do not use outside knowledge.
- If the user asks for a summary, just write a summary of the provided context.
- If the context doesn't contain the answer to a specific question, say exactly "I couldn't find this in the uploaded documents."
- Be concise.

Context:
{context}

Question: {question}

Answer:"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1)
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"context": context, "question": "explain the summary of this pdf in short"}))
