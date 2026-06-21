import streamlit as st
import uuid
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import (
    get_pdf_text,
    get_youtube_transcript,
    get_text_chunks,
    get_vector_store,
    load_vector_store,
    load_chats,
    save_chats
)

st.set_page_config(
    page_title="Scapia AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "view" not in st.session_state:
    st.session_state.view = "landing"
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Llama 3.1 (Flash)"

# Chat State Initialization
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
if "current_chat_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
    else:
        new_id = str(uuid.uuid4())
        st.session_state.chats = {new_id: {"title": "New Chat", "messages": [], "pinned": False}}
        st.session_state.current_chat_id = new_id
        save_chats(st.session_state.chats)


# ── Global CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
/* Mask the unstyled flash on every rerun: start invisible, fade in once CSS paints */
[data-testid="stAppViewContainer"] {
    animation: fadeInApp 0.18s ease-in forwards;
    opacity: 0;
}
@keyframes fadeInApp { to { opacity: 1; } }

/* Reset & Fonts */
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0F172A !important;
    background-image: 
        linear-gradient(rgba(147, 197, 253, 0.1) 1px, transparent 1px), 
        linear-gradient(90deg, rgba(147, 197, 253, 0.1) 1px, transparent 1px) !important;
    background-size: 64px 64px !important;
    color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
.stAppDeployButton { display: none !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 auto; }

/* Hide expand_more icons completely, but keep SVG for chat input arrow */
.material-symbols-rounded { display: none !important; }

/* Buttons */
.stButton > button {
    border: none !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

.stButton > button:hover { transform: translateY(-1px) !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* Landing page primary/secondary CTA buttons — styled globally up-front
   instead of injected mid-layout, so there's no unstyled flash window */
.hero-cta-primary .stButton > button {
    background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important;
    font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important;
    padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;
}
.hero-cta-primary .stButton > button:hover {
    background: #2563eb !important; border-color: #1d4ed8 !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important;
}
.hero-cta-secondary .stButton > button {
    background: transparent !important; border: 1px solid #3b82f6 !important; color: #3b82f6 !important;
    font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;
}
.hero-cta-secondary .stButton > button:hover { background: rgba(59,130,246,0.1) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

</style>
""", unsafe_allow_html=True)


view = st.session_state.view
dynamic_css = ""

if view == "landing":
    dynamic_css = """
    [data-testid="stSidebar"] { display: none !important; }
    /* Landing Specific Styles */
    .nav { display:flex; align-items:center; justify-content:space-between; padding:20px 48px; position:relative; z-index:10; }
    .nav-logo { display:flex; align-items:center; gap:10px; font-size:18px; font-weight:700; color:#fff; }
    .nav-logo-icon { width:34px; height:34px; background:linear-gradient(135deg,#6366f1,#8b5cf6); border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:17px; }

    .hero-container { position:relative; overflow:hidden; padding-bottom:40px; }
    
    /* Background Glowing Orbs */
    .bg-orb-1 { position:absolute; top:-10%; left:-10%; width:400px; height:400px; background:radial-gradient(circle, rgba(99,102,241,0.15) 0%, rgba(15,23,42,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }
    .bg-orb-2 { position:absolute; top:20%; right:-10%; width:500px; height:500px; background:radial-gradient(circle, rgba(168,85,247,0.15) 0%, rgba(15,23,42,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }
    .bg-orb-3 { position:absolute; bottom:0%; left:30%; width:600px; height:600px; background:radial-gradient(circle, rgba(99,102,241,0.1) 0%, rgba(15,23,42,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }

    .hero { text-align:center; padding:80px 24px 40px; max-width:800px; margin:0 auto; position:relative; z-index:10; }
    .hero-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(99,102,241,0.15); border:1px solid rgba(99,102,241,0.3); color:#818cf8; font-size:12px; font-weight:600; padding:6px 14px; border-radius:20px; margin-bottom:24px; }
    
    .hero-title { font-size:56px; font-weight:800; line-height:1.15; color:#f8fafc; letter-spacing:-1.5px; margin-bottom:18px; }
    .hero-title span { background:linear-gradient(to right, #818cf8, #c084fc, #f472b6); -webkit-background-clip: text; color: transparent; display:inline-block; padding-bottom:8px;}
    
    .hero-sub { font-size:18px; color:#94a3b8; line-height:1.6; max-width:560px; margin:0 auto 32px; }
    .hero-note { font-size:12px; color:#64748b; margin-top:16px; text-align:center; }

    .stats-row { display:flex; justify-content:center; gap:60px; margin:60px auto 80px; flex-wrap:wrap; position:relative; z-index:10; border-top:1px solid rgba(99,102,241,0.15); border-bottom:1px solid rgba(99,102,241,0.15); background:rgba(30,41,59,0.3); padding:40px 20px; }
    .stat { text-align:left; display:flex; gap:16px; align-items:center; }
    .stat-icon { color:#818cf8; font-size:24px; }
    .stat-num { font-size:28px; font-weight:800; color:#f8fafc; font-family: monospace; }
    .stat-label { font-size:12px; color:#94a3b8; margin-top:2px; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;}

    .section-head { text-align:center; margin: 40px auto 50px; position:relative; z-index:10; }
    .section-title { font-size:32px; font-weight:800; color:#f8fafc; letter-spacing:-0.5px; }
    .section-sub { font-size:16px; color:#94a3b8; margin-top:8px; }

    .steps-row { display:flex; gap:24px; max-width:1000px; margin:0 auto 80px; padding:0 24px; flex-wrap:wrap; justify-content:center; position:relative; z-index:10; }
    .step-card { background:rgba(30,41,59,0.4); border:1px solid rgba(99,102,241,0.15); border-radius:24px; padding:32px 24px; flex:1; min-width:280px; max-width:320px; text-align:center; backdrop-filter:blur(12px); transition:transform 0.3s, border-color 0.3s; }
    .step-card:hover { transform:translateY(-4px); border-color:rgba(99,102,241,0.4); }
    .step-icon { font-size:36px; margin-bottom:16px; display:inline-block; padding:12px; background:rgba(15,23,42,0.5); border-radius:16px; border:1px solid rgba(255,255,255,0.05); }
    .step-title { font-size:18px; font-weight:700; color:#f8fafc; margin-bottom:10px; }
    .step-text { font-size:14px; color:#94a3b8; line-height:1.6; }

    /* Button specific styles placed here to avoid FOUC */
    div[data-testid='stHorizontalBlock'] > div:nth-child(2) .stButton > button { background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid='stHorizontalBlock'] > div:nth-child(2) .stButton > button:hover { background: #2563eb !important; border-color: #1d4ed8 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important; }
    div[data-testid='stHorizontalBlock'] > div:nth-child(3) .stButton > button { background: transparent !important; border: 1px solid #3b82f6 !important; color: #3b82f6 !important; font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid='stHorizontalBlock'] > div:nth-child(3) .stButton > button:hover { background: rgba(59,130,246,0.1) !important; transform: translateY(-2px) !important; }
    """
elif view == "source_selection":
    dynamic_css = """
    /* Hide specific elements */
    [data-testid="stSidebar"] { display: none !important; }
    
    .nav { padding: 20px 40px; display: flex; align-items: center; justify-content: space-between; position: relative; z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .nav-logo { font-size: 20px; font-weight: 800; color: #f8fafc; letter-spacing: -0.5px; display: flex; align-items: center; gap: 12px; }
    .nav-logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
    
    .source-container { max-width: 900px; margin: 60px auto; padding: 0 20px; text-align: center; }
    .source-title { font-size: 32px; font-weight: 800; color: #f8fafc; margin-bottom: 12px; }
    .source-sub { font-size: 16px; color: #94a3b8; margin-bottom: 40px; }
    
    /* Box styles */
    .source-box { background: rgba(30,41,59,0.5); border: 1px solid rgba(99,102,241,0.2); border-radius: 12px; padding: 12px 16px; text-align: left; height: 100%; backdrop-filter: blur(12px); transition: transform 0.3s, border-color 0.3s; }
    .source-box:hover { transform: translateY(-4px); border-color: rgba(99,102,241,0.5); }
    .source-box-title { font-size: 13px; font-weight: 700; color: #f8fafc; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
    
    /* Hide specific elements & Shrink Uploader */
    [data-testid="stFileUploader"] { background: rgba(15,23,42,0.4) !important; border: 1px dashed rgba(99,102,241,0.3) !important; border-radius: 8px !important; cursor: pointer !important; min-height: 40px !important; margin-bottom: 0 !important; }
    [data-testid="stFileUploader"] section { cursor: pointer !important; padding: 8px 10px !important; min-height: 40px !important; }
    [data-testid="stFileUploader"] button { display: none !important; }
    [data-testid="stFileUploader"] small { font-size: 10px !important; }
    .stTextInput > div > div > input { background: rgba(15,23,42,0.4) !important; border: 1px solid rgba(99,102,241,0.3) !important; color: #f8fafc !important; font-size: 12px !important; padding: 6px 10px !important; border-radius: 8px !important; }
    div.stButton > button { background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important; padding: 12px 30px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; }
div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important; background: #2563eb !important; color: white !important; border-color: #1d4ed8 !important; }
    """
elif view == "chat":
    dynamic_css = """
    /* Global Adjustments */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0B1121 !important;
        background-image: none !important;
    }
    
    [data-testid="stMain"] { background: #0B1121 !important; }

    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {
        display: flex !important;
        background: #0B1121 !important;
        border-right: 1px solid #1f2937 !important;
        min-width: 250px !important;
        max-width: 250px !important;
        transform: translateX(0px) !important;
        visibility: visible !important;
        padding-top: 10px !important;
    }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }

    .sidebar-menu-item {
        padding: 10px 16px;
        margin: 4px 16px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s;
        text-decoration: none;
        cursor: pointer;
    }
    .sidebar-menu-item:hover { background: #1e293b; color: #f8fafc; }
    .sidebar-menu-item.active { background: rgba(16, 185, 129, 0.1); color: #10b981; }

    /* Top Bar */
    .top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        margin-bottom: 20px;
    }
    
    .search-box {
        display: flex;
        align-items: center;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 6px 12px;
        width: 400px;
        color: #94a3b8;
        font-size: 13px;
    }
    .search-box input {
        background: transparent;
        border: none;
        color: #f8fafc;
        width: 100%;
        outline: none;
        margin-left: 8px;
    }
    
    /* Panels */
    .dashboard-panel {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        height: 75vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
    }
    .panel-header {
        font-size: 15px;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .panel-header span.icons { color: #64748b; letter-spacing: 4px; font-weight: normal; }

    /* PDF Preview */
    iframe.pdf-iframe {
        width: 100%;
        height: 100%;
        border: none;
        border-radius: 8px;
        background: #1e293b;
    }
    .pdf-placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        color: #64748b;
        font-size: 14px;
        background: #1e293b;
        border-radius: 8px;
        border: 1px dashed #334155;
    }

    /* Chat Messages Container */
    .chat-history {
        flex: 1;
        overflow-y: auto;
        padding-right: 10px;
        padding-bottom: 80px; /* space for input */
    }

    /* Chat Messages overrides */
    [data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 12px 0 !important; }
    .stChatMessageAvatar { display: none !important; }

    /* User Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { flex-direction: column !important; align-items: flex-start !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px 12px 12px 4px !important;
        padding: 12px 16px !important;
        max-width: 90% !important;
        color: #f8fafc !important;
        font-size: 14px !important;
    }

    /* Assistant Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { flex-direction: column !important; align-items: flex-start !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
        background: rgba(16, 185, 129, 0.05) !important;
        border: 1px solid rgba(16, 185, 129, 0.1) !important;
        border-radius: 12px 12px 12px 4px !important;
        padding: 12px 16px !important;
        max-width: 90% !important;
        color: #e2e8f0 !important;
        font-size: 14px !important;
    }

    /* Avatar Overrides in HTML */
    .chat-avatar-user { width: 28px; height: 28px; border-radius: 50%; object-fit: cover; }
    .chat-avatar-ai { width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #10b981, #059669); color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }
    .chat-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .chat-name { font-size: 13px; font-weight: 600; color: #f8fafc; }

    /* Hide native chat input elements partially to inline them inside the right panel */
    [data-testid="stChatInput"] { 
        position: absolute !important;
        bottom: 20px !important;
        left: 20px !important;
        right: 20px !important;
        width: calc(100% - 40px) !important;
        background: transparent !important; 
        padding: 0 !important;
        margin: 0 !important;
        transform: none !important;
    }
    [data-testid="stChatInput"] > div {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 4px 8px !important;
    }
    [data-testid="stChatInput"] textarea { color: #f8fafc !important; font-size: 14px !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* Logo area */
    .logo-area { display: flex; align-items: center; gap: 10px; padding: 10px 20px; margin-bottom: 20px; font-size: 18px; font-weight: 700; color: #f8fafc; }
    .logo-icon { width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #10b981, #059669); color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; }
    """

st.markdown(f"""
<style>
{dynamic_css}
</style>
""", unsafe_allow_html=True)


# ── LANDING PAGE ───────────────────────────────────────────────
def render_landing():
    # Force sidebar closed on landing
    st.markdown("""
<div class="nav">
<div class="nav-logo"><div class="nav-logo-icon">🧠</div> Scapia AI</div>
</div>

<div class="hero-container">
<div class="bg-orb-1"></div>
<div class="bg-orb-2"></div>
<div class="bg-orb-3"></div>

<div class="hero">
<div class="hero-badge">✨ AI-Powered Document Chat</div>
<div class="hero-title">Turn your notes into<br><span>answers you can trust.</span></div>
<div class="hero-sub">Upload any PDF or paste a YouTube link. Ask questions and get answers grounded strictly in your own material — no hallucinations, no guesswork.</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Injecting Streamlit buttons seamlessly into the layout
    col1, col2, col3, col4 = st.columns([1, 0.4, 0.4, 1])
    with col2:
        if st.button("Get Started Free →", use_container_width=True):
            st.session_state.view = "source_selection"
            st.rerun()
    with col3:
        if st.button("Try Demo 🎮", use_container_width=True):
            st.session_state.view = "source_selection"
            st.rerun()

    st.markdown("""
<div class="hero-note">No credit card required · Free forever plan available</div>

<div class="stats-row">
<div class="stat"><div class="stat-icon">🎓</div><div><div class="stat-num">17,300+</div><div class="stat-label">Students</div></div></div>
<div class="stat"><div class="stat-icon">⚡</div><div><div class="stat-num">1M+</div><div class="stat-label">Questions</div></div></div>
<div class="stat"><div class="stat-icon">⭐</div><div><div class="stat-num">4.8/5</div><div class="stat-label">User Rating</div></div></div>
<div class="stat"><div class="stat-icon">🚀</div><div><div class="stat-num">∞</div><div class="stat-label">More Fun</div></div></div>
</div>

<div class="section-head">
<div class="section-title">How It Works</div>
<div class="section-sub">Three simple steps to chat with your material</div>
</div>

<div class="steps-row">
<div class="step-card">
<div class="step-icon">📄</div>
<div class="step-title">Upload Your Content</div>
<div class="step-text">Upload a PDF or paste a YouTube link — Scapia AI analyzes and indexes it instantly.</div>
</div>
<div class="step-card">
<div class="step-icon">🔍</div>
<div class="step-title">Ask Anything</div>
<div class="step-text">Type any question. The AI retrieves only the relevant chunks from your material.</div>
</div>
<div class="step-card">
<div class="step-icon">✅</div>
<div class="step-title">Get Grounded Answers</div>
<div class="step-text">Every answer is quoted and sourced from your actual document — never made up.</div>
</div>
</div>

<div style="text-align:center; padding:40px 24px; color:#475569; font-size:12px; border-top:1px solid rgba(255,255,255,0.05);">
© 2026 Scapia AI · Built with Streamlit + Groq
</div>
""", unsafe_allow_html=True)


# ── CHAT VIEW ──────────────────────────────────────────────────
def get_conversational_chain(vector_store, model_choice, chat_messages):
    if "Flash" in model_choice:
        model_id = "llama-3.1-8b-instant"
        style_instruction = "Keep your answer extremely concise, fast, and straight to the point (1-3 sentences max)."
    else:
        model_id = "llama-3.3-70b-versatile"
        style_instruction = "Provide a deep, comprehensive, and highly detailed analysis. Use structured paragraphs, bullet points, and quotes from the text where applicable."
        
    llm = ChatGroq(model=model_id, temperature=0.1)

    prompt_template = f"""You are a precise document analysis assistant. Your ONLY job is to answer questions strictly from the provided context.

RULES:
1. Answer ONLY from the context below. Never use external knowledge.
2. If the user asks for a general summary or overview, summarize the provided context to the best of your ability.
3. If the answer is completely missing from the context and cannot be inferred, say exactly: "I couldn't find this in the uploaded documents."
4. Auto-correct obvious phonetic typos in the context (e.g. if the context is a YouTube transcript and says 'langin' or 'langraph', correct it to 'LangChain' and 'LangGraph' in your answer).
5. {style_instruction}

Chat History (for reference to understand pronouns like "it" or "again"):
{{chat_history}}

Context:
{{context}}

Question: {{question}}

Answer (strictly from context):"""

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])
    retriever = vector_store.as_retriever(search_kwargs={"k": 15})

    def format_docs(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    def run_chain(question):
        history_str = ""
        search_query = question
        
        # Build memory and rewrite query to resolve references
        if len(chat_messages) > 1:
            history_msgs = chat_messages[-5:-1]
            history_str = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in history_msgs])
            rewrite_prompt = f"Given the chat history below, rewrite the user's latest query into a standalone query that resolves references like 'it' or 'again'. Maintain the specific intent of the user's latest query (e.g., if they ask to 'explain it', rewrite it to 'explain [topic]'). Do NOT answer the query, just output the rewritten standalone query string and nothing else.\n\nChat History:\n{history_str}\n\nLatest Query: {question}\n\nStandalone Query:"
            try:
                search_query = llm.invoke(rewrite_prompt).content.strip()
            except Exception:
                pass
                
        docs = retriever.invoke(search_query)
        context = format_docs(docs)
        chain = PROMPT | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": search_query, "chat_history": history_str})
        return answer, docs

    return run_chain

def render_source_selection():
    st.markdown("""
    <div class="nav">
        <div class="nav-logo"><div class="nav-logo-icon">🧠</div> Scapia AI</div>
    </div>
    
    <div class="source-container">
        <div class="source-title">Add Your Knowledge Base</div>
        <div class="source-sub">Upload a document or paste a YouTube link to start chatting.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="max-width: 450px; margin: 0 auto;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.markdown('<div class="source-box"><div class="source-box-title">📄 Upload PDF</div>', unsafe_allow_html=True)
        pdf_docs = st.file_uploader("", accept_multiple_files=True, type=["pdf"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="source-box"><div class="source-box-title">🎥 YouTube Link</div>', unsafe_allow_html=True)
        youtube_url = st.text_input("", placeholder="https://youtube.com/...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
    col_space1, col_btn, col_space3 = st.columns([1, 1, 1])
    with col_btn:
        if st.button("Process Documents", use_container_width=True):
            with st.spinner("Processing..."):
                raw_text = ""
                if pdf_docs:
                    raw_text += get_pdf_text(pdf_docs) + "\n\n"
                    import base64
                    # Save the first PDF as base64 for previewing
                    st.session_state.pdf_base64 = base64.b64encode(pdf_docs[0].getvalue()).decode("utf-8")
                    st.session_state.pdf_name = pdf_docs[0].name
                if youtube_url:
                    try:
                        raw_text += get_youtube_transcript(youtube_url) + "\n\n"
                    except Exception as e:
                        st.error(f"YouTube error: {e}")
                if not raw_text.strip():
                    st.warning("Upload a PDF or enter a YouTube URL first.")
                else:
                    chunks = get_text_chunks(raw_text)
                    get_vector_store(chunks)
                    st.session_state.view = "chat"
                    st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_chat():
    # Top Bar (Main Area Header)
    st.markdown('''
    <div class="top-bar">
        <div class="search-box">
            <span>🔍</span>
            <input type="text" placeholder="Search">
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #1e293b; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 16px;">🔔</div>
            <img src="https://ui-avatars.com/api/?name=User&background=0D8ABC&color=fff" style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid #334155;">
        </div>
    </div>
    ''', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('''
        <div class="logo-area">
            <div class="logo-icon">S</div>
            Scapia AI
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <a href="#" class="sidebar-menu-item active"><span>📊</span> Dashboard</a>
        <a href="#" class="sidebar-menu-item"><span>🗂️</span> Projects</a>
        <a href="#" class="sidebar-menu-item"><span>📄</span> Documents</a>
        <a href="#" class="sidebar-menu-item"><span>▶️</span> YouTube</a>
        <a href="#" class="sidebar-menu-item"><span>⏱️</span> History</a>
        <a href="#" class="sidebar-menu-item" style="margin-top: 100px;"><span>⚙️</span> Settings</a>
        ''', unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: #1f2937; margin: 20px 16px;'>", unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("＋ New Chat", use_container_width=True):
                new_id = str(uuid.uuid4())
                st.session_state.chats[new_id] = {"title": "New Chat", "messages": [], "pinned": False}
                st.session_state.current_chat_id = new_id
                save_chats(st.session_state.chats)
                st.rerun()
        with col_btn2:
            if st.button("📄 Add Docs", use_container_width=True):
                st.session_state.view = "source_selection"
                st.rerun()
                
        st.selectbox("Model", ["Llama 3.1 (Flash)", "Llama 3.3 (Thinking)"], key="model_choice")

    # Main Layout: 2 Columns
    col1, col2 = st.columns([1.1, 1])
    
    with col1:
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div>Document Preview</div><span class="icons">...</span></div>', unsafe_allow_html=True)
        
        if "pdf_base64" in st.session_state and st.session_state.pdf_base64:
            pdf_data = st.session_state.pdf_base64
            st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_data}#toolbar=0&navpanes=0&scrollbar=0" class="pdf-iframe"></iframe>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="pdf-placeholder">No Document Uploaded</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header"><div>Scapia AI Assistant</div><span class="icons">...</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        
        active_chat = st.session_state.chats.get(st.session_state.current_chat_id)
        if not active_chat:
            st.error("Chat not found.")
            st.stop()
            
        messages = active_chat.get("messages", [])

        if not messages:
            st.markdown('''
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;color:#64748b;padding-top:40px;">
                <div>Upload a document, then ask away.</div>
            </div>
            ''', unsafe_allow_html=True)

        for message in messages:
            if message["role"] == "user":
                st.markdown(f'''
                <div class="user-msg-container">
                    <img src="https://ui-avatars.com/api/?name=User&background=0D8ABC&color=fff" class="user-avatar">
                    <div style="width: 100%;">
                        <div class="msg-header">User</div>
                        <div class="msg-content">{message["content"]}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="ai-msg-container">
                    <div class="ai-avatar">S</div>
                    <div style="width: 100%;">
                        <div class="msg-header" style="color: #10b981;">Scapia AI</div>
                        <div class="ai-msg-content">{message["content"]}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True) # End chat history
        st.markdown('</div>', unsafe_allow_html=True) # End dashboard-panel

    if prompt := st.chat_input("Message Scapia AI..."):
        messages.append({"role": "user", "content": prompt})
        save_chats(st.session_state.chats)
        st.rerun()

    # Handle Assistant Response if last message is from user
    if messages and messages[-1]["role"] == "user":
        
        if len(messages) == 1 and active_chat["title"] == "New Chat":
            first_msg = messages[0]["content"]
            try:
                title_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
                title_prompt = f"Generate a short 2-4 word title summarizing this query. Output ONLY the title, no quotes, no extra text:\n\n{first_msg}"
                generated_title = title_llm.invoke(title_prompt).content.strip().strip('"')
                new_title = generated_title if generated_title else first_msg[:30]
            except Exception as e:
                new_title = first_msg[:30] + ("..." if len(first_msg) > 30 else "")
            
            chats_copy = dict(st.session_state.chats)
            chats_copy[st.session_state.current_chat_id]["title"] = new_title
            st.session_state.chats = chats_copy
            save_chats(st.session_state.chats)

        vs = load_vector_store()
        if not vs:
            answer = "Please upload and process a document first using the sidebar."
            messages.append({"role": "assistant", "content": answer})
            save_chats(st.session_state.chats)
            st.rerun()
        else:
            with st.spinner("Thinking..."):
                run_chain = get_conversational_chain(vs, st.session_state.model_choice, messages)
                prompt_text = messages[-1]["content"]
                answer, sources = run_chain(prompt_text)
            
            messages.append({"role": "assistant", "content": answer})
            save_chats(st.session_state.chats)
            st.rerun()

# ── Router ─────────────────────────────────────────────────────
if st.session_state.view == "landing":
    render_landing()
elif st.session_state.view == "source_selection":
    render_source_selection()
else:
    render_chat()