import os
import re
import json
import uuid
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize embedding model using HuggingFace (runs locally, free, no API key needed)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF documents."""
    text = ""
    for pdf in pdf_docs:
        with pdfplumber.open(pdf) as pdf_reader:
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    return text

def extract_video_id(url):
    """Extract YouTube video ID from URL."""
    # handle standard youtube.com URLs
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
    # handle youtu.be URLs
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    return None

def get_youtube_transcript(url):
    """Fetch transcript from a YouTube video."""
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    try:
        transcript_list_obj = YouTubeTranscriptApi().list(video_id)
        transcript_data = list(transcript_list_obj)[0].fetch()
        transcript = ' '.join([t.text for t in transcript_data])
        return transcript
    except Exception as e:
        raise Exception(f"Failed to extract transcript: {str(e)}")

def get_text_chunks(text):
    """Split text into manageable chunks for the vector store."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, persist_directory="./chroma_db"):
    """Create a Chroma vector store from text chunks and save it locally."""
    # Create or update the vector store
    vector_store = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vector_store

def load_vector_store(persist_directory="./chroma_db"):
    """Load an existing Chroma vector store."""
    if os.path.exists(persist_directory):
        return Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return None

def load_chats(file_path="chats.json"):
    """Load chats from a local JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_chats(chats, file_path="chats.json"):
    """Save chats to a local JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=4)
