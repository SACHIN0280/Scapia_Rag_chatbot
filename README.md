# Scapia AI – Multi-Modal RAG Document Assistant

Scapia AI is a full-stack Retrieval-Augmented Generation (RAG) web application that allows users to seamlessly upload PDF documents or YouTube video links and converse with their content. 

Built with a responsive, modern UI using Streamlit and custom CSS, the app leverages LangChain, local HuggingFace embeddings, ChromaDB for vector storage, and Groq's high-speed inference API to generate highly accurate, context-grounded answers.

## Features
- **Multi-Modal RAG Pipeline:** Extract, chunk, and index text from complex PDF documents (`pdfplumber`) and YouTube video transcripts (`youtube-transcript-api`).
- **Local Vector Storage:** Integrated `ChromaDB` for fast local vector storage utilizing HuggingFace's open-source `BAAI/bge-base-en-v1.5` embedding model.
- **Ultra-Fast LLM Inference:** Powered by the Groq API (Llama 3.1 & 3.3 models) for near-instantaneous query resolution with strict prompts to prevent AI hallucinations.
- **Premium UI/UX:** Dynamic, multi-page frontend using Streamlit with custom CSS to achieve a flicker-free Single Page Application (SPA) experience in dark mode.
- **Stateful Chat Management:** Persistent, multi-thread conversations (ChatGPT-style sidebar) allowing users to switch between chats, rename sessions with AI, and pin important threads.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SACHIN0280/Scapia_Rag_chatbot.git
   cd Scapia_Rag_chatbot
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```
