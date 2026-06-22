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

# ── INITIALIZATION ─────────────────────────────────────────────
url_view = st.query_params.get("view", "landing")
if "view" not in st.session_state:
    st.session_state.view = url_view
    st.session_state._last_url_view = url_view
elif st.session_state.get("_last_url_view") != url_view:
    # Detected browser back/forward navigation
    st.session_state.view = url_view
    st.session_state._last_url_view = url_view
if "view_history" not in st.session_state:
    st.session_state.view_history = []
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Llama 3.1 (Flash)"

# Initialize or Load Chats
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
if "current_chat_id" not in st.session_state:
    saved_chat_id = st.query_params.get("chat_id")
    if saved_chat_id and saved_chat_id in st.session_state.chats:
        st.session_state.current_chat_id = saved_chat_id
    elif st.session_state.chats:
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
    background-color: #FAF9F5 !important;
    background-image: none !important;
    color: #2D2B27;
    font-family: 'Söhne', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif !important;
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
    color: #2D2B27 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    background: #EEECE2 !important;
}

.stButton > button:hover { transform: translateY(-1px) !important; background: #E5E2D6 !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* Landing page primary/secondary CTA buttons */
.hero-cta-primary .stButton > button {
    background: #DA7756 !important; border: 1px solid #C96A4B !important; color: white !important;
    font-weight: 600 !important; box-shadow: 0 4px 14px rgba(218,119,86,0.3) !important;
    padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;
}
.hero-cta-primary .stButton > button:hover {
    background: #C96A4B !important; border-color: #B85E40 !important;
    box-shadow: 0 6px 20px rgba(218,119,86,0.5) !important;
}
.hero-cta-secondary .stButton > button {
    background: transparent !important; border: 1px solid #DA7756 !important; color: #DA7756 !important;
    font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;
}
.hero-cta-secondary .stButton > button:hover { background: rgba(218,119,86,0.08) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #FAF9F5; }
::-webkit-scrollbar-thumb { background: #D5D1C8; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #B8B4AB; }

</style>
""", unsafe_allow_html=True)


view = st.session_state.view
dynamic_css = ""

if view == "landing":
    dynamic_css = """
    [data-testid="stSidebar"] { display: none !important; }
    /* Landing Specific Styles */
    .nav { display:flex; align-items:center; justify-content:space-between; padding:20px 48px; position:relative; z-index:10; }
    .nav-logo { display:flex; align-items:center; gap:10px; font-size:18px; font-weight:700; color:#2D2B27; }
    .nav-logo-icon { width:34px; height:34px; background:linear-gradient(135deg,#DA7756,#C96A4B); border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:17px; }

    .hero-container { position:relative; overflow:hidden; padding-bottom:40px; }
    
    /* Background Glowing Orbs */
    .bg-orb-1 { position:absolute; top:-10%; left:-10%; width:400px; height:400px; background:radial-gradient(circle, rgba(218,119,86,0.08) 0%, rgba(250,249,245,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }
    .bg-orb-2 { position:absolute; top:20%; right:-10%; width:500px; height:500px; background:radial-gradient(circle, rgba(183,148,115,0.08) 0%, rgba(250,249,245,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }
    .bg-orb-3 { position:absolute; bottom:0%; left:30%; width:600px; height:600px; background:radial-gradient(circle, rgba(218,119,86,0.06) 0%, rgba(250,249,245,0) 70%); border-radius:50%; pointer-events:none; z-index:0; }

    .hero { text-align:center; padding:80px 24px 40px; max-width:800px; margin:0 auto; position:relative; z-index:10; }
    .hero-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(218,119,86,0.1); border:1px solid rgba(218,119,86,0.25); color:#DA7756; font-size:12px; font-weight:600; padding:6px 14px; border-radius:20px; margin-bottom:24px; }
    
    .hero-title { font-size:56px; font-weight:800; line-height:1.15; color:#2D2B27; letter-spacing:-1.5px; margin-bottom:18px; }
    .hero-title span { background:linear-gradient(to right, #DA7756, #C96A4B, #B85E40); -webkit-background-clip: text; color: transparent; display:inline-block; padding-bottom:8px;}
    
    .hero-sub { font-size:18px; color:#6B6560; line-height:1.6; max-width:560px; margin:0 auto 32px; }
    .hero-note { font-size:12px; color:#9B9590; margin-top:16px; text-align:center; }

    .stats-row { display:flex; justify-content:center; gap:60px; margin:60px auto 80px; flex-wrap:wrap; position:relative; z-index:10; border-top:1px solid rgba(218,119,86,0.15); border-bottom:1px solid rgba(218,119,86,0.15); background:rgba(238,236,226,0.4); padding:40px 20px; }
    .stat { text-align:left; display:flex; gap:16px; align-items:center; }
    .stat-icon { color:#DA7756; font-size:24px; }
    .stat-num { font-size:28px; font-weight:800; color:#2D2B27; font-family: monospace; }
    .stat-label { font-size:12px; color:#6B6560; margin-top:2px; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;}

    .section-head { text-align:center; margin: 40px auto 50px; position:relative; z-index:10; }
    .section-title { font-size:32px; font-weight:800; color:#2D2B27; letter-spacing:-0.5px; }
    .section-sub { font-size:16px; color:#6B6560; margin-top:8px; }

    .steps-row { display:flex; gap:24px; max-width:1000px; margin:0 auto 80px; padding:0 24px; flex-wrap:wrap; justify-content:center; position:relative; z-index:10; }
    .step-card { background:#EEECE2; border:1px solid rgba(218,119,86,0.15); border-radius:24px; padding:32px 24px; flex:1; min-width:280px; max-width:320px; text-align:center; transition:transform 0.3s, border-color 0.3s; }
    .step-card:hover { transform:translateY(-4px); border-color:rgba(218,119,86,0.4); }
    .step-icon { font-size:36px; margin-bottom:16px; display:inline-block; padding:12px; background:#FAF9F5; border-radius:16px; border:1px solid rgba(0,0,0,0.05); }
    .step-title { font-size:18px; font-weight:700; color:#2D2B27; margin-bottom:10px; }
    .step-text { font-size:14px; color:#6B6560; line-height:1.6; }

    /* Button specific styles placed here to avoid FOUC */
    div[data-testid='stHorizontalBlock'] > div:nth-child(2) .stButton > button { background: #DA7756 !important; border: 1px solid #C96A4B !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(218,119,86,0.3) !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid='stHorizontalBlock'] > div:nth-child(2) .stButton > button:hover { background: #C96A4B !important; border-color: #B85E40 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(218,119,86,0.5) !important; }
    div[data-testid='stHorizontalBlock'] > div:nth-child(3) .stButton > button { background: transparent !important; border: 1px solid #DA7756 !important; color: #DA7756 !important; font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid='stHorizontalBlock'] > div:nth-child(3) .stButton > button:hover { background: rgba(218,119,86,0.08) !important; transform: translateY(-2px) !important; }
    """
elif view == "source_selection":
    dynamic_css = """
    /* Hide specific elements */
    [data-testid="stSidebar"] { display: none !important; }
    
    .nav { padding: 20px 40px; display: flex; align-items: center; justify-content: space-between; position: relative; z-index: 100; border-bottom: 1px solid rgba(0,0,0,0.06); }
    .nav-logo { font-size: 20px; font-weight: 800; color: #2D2B27; letter-spacing: -0.5px; display: flex; align-items: center; gap: 12px; }
    .nav-logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #DA7756, #C96A4B); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
    
    .source-container { max-width: 900px; margin: 60px auto; padding: 0 20px; text-align: center; }
    .source-title { font-size: 32px; font-weight: 800; color: #2D2B27; margin-bottom: 12px; }
    .source-sub { font-size: 16px; color: #6B6560; margin-bottom: 40px; }
    
    /* Box styles */
    .source-box { background: #EEECE2; border: 1px solid rgba(218,119,86,0.15); border-radius: 12px; padding: 12px 16px; text-align: left; height: 100%; transition: transform 0.3s, border-color 0.3s; }
    .source-box:hover { transform: translateY(-4px); border-color: rgba(218,119,86,0.4); }
    .source-box-title { font-size: 13px; font-weight: 700; color: #2D2B27; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
    
    /* Hide specific elements & Shrink Uploader */
    [data-testid="stFileUploader"] { background: #EEECE2 !important; border: 1px dashed rgba(218,119,86,0.3) !important; border-radius: 8px !important; cursor: pointer !important; min-height: 40px !important; margin-bottom: 0 !important; }
    [data-testid="stFileUploader"] section { cursor: pointer !important; padding: 8px 10px !important; min-height: 40px !important; }
    [data-testid="stFileUploader"] button { display: none !important; }
    [data-testid="stFileUploader"] small { font-size: 10px !important; color: #6B6560 !important; }
    .stTextInput > div > div > input { background: #EEECE2 !important; border: 1px solid rgba(218,119,86,0.2) !important; color: #2D2B27 !important; font-size: 12px !important; padding: 6px 10px !important; border-radius: 8px !important; }
    div.stButton > button { background: #DA7756 !important; border: 1px solid #C96A4B !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(218,119,86,0.3) !important; padding: 12px 30px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; }
div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(218,119,86,0.5) !important; background: #C96A4B !important; color: white !important; border-color: #B85E40 !important; }
    """
elif view == "chat":
    dynamic_css = """
    /* Global Adjustments */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #FAF9F5 !important;
        background-image: none !important;
    }
    
    [data-testid="stMain"] { background: #FAF9F5 !important; }

    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {
        display: flex !important;
        background: #F0EDE5 !important;
        border-right: 1px solid #E5E2D6 !important;
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
        color: #6B6560;
        font-size: 14px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.2s;
        text-decoration: none;
        cursor: pointer;
    }
    .sidebar-menu-item:hover { background: #E5E2D6; color: #2D2B27; }
    .sidebar-menu-item.active { background: rgba(218,119,86,0.1); color: #DA7756; }

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
        background: #EEECE2;
        border: 1px solid #D5D1C8;
        border-radius: 8px;
        padding: 6px 12px;
        width: 400px;
        color: #6B6560;
        font-size: 13px;
    }
    .search-box input {
        background: transparent;
        border: none;
        color: #2D2B27;
        width: 100%;
        outline: none;
        margin-left: 8px;
    }
    
    /* Logo area */
    .logo-area { display: flex; align-items: center; gap: 10px; padding: 10px 20px; margin-bottom: 16px; font-size: 18px; font-weight: 700; color: #2D2B27; }
    .logo-icon { width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #DA7756, #C96A4B); color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; }

    /* Chat Messages overrides */
    /* Hide the avatars entirely */
    [data-testid="stChatMessage"] > div:first-child,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatMessage"] img { display: none !important; }

    [data-testid="stChatMessage"] { 
        background: transparent !important; 
        border: none !important; 
        padding: 10px 0 !important; 
        display: flex !important;
        flex-direction: row !important;
        width: 100% !important;
    }

    [data-testid="stChatMessage"]:has(.user-msg-marker) { justify-content: flex-end !important; }
    [data-testid="stChatMessage"]:has(.user-msg-marker) [data-testid="stChatMessageContent"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 8px 0 !important;
        max-width: 70% !important;
        color: #2D2B27 !important;
        font-size: 14.5px !important;
        flex: 0 1 auto !important;
        margin: 0 16px !important;
    }

    [data-testid="stChatMessage"]:has(.assistant-msg-marker) { justify-content: flex-start !important; }
    [data-testid="stChatMessage"]:has(.assistant-msg-marker) [data-testid="stChatMessageContent"] {
        background: transparent !important;
        border: none !important;
        padding: 4px 0 !important;
        max-width: 95% !important;
        color: #2D2B27 !important;
        font-size: 14.5px !important;
        line-height: 1.7 !important;
        flex: 0 1 auto !important;
        margin: 0 16px !important;
    }

    /* Chat Input */
    [data-testid="stBottom"] { background: transparent !important; }
    [data-testid="stBottom"] > div { background: transparent !important; }
    [data-testid="stBottomBlockContainer"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        background: transparent !important;
        padding: 0 20px !important;
        flex-wrap: nowrap !important;
    }
    /* Collapse all Streamlit wrapper divs inside the bottom container */
    [data-testid="stBottomBlockContainer"] > div {
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: 0 !important;
    }
    [data-testid="stBottomBlockContainer"] > div:has([data-testid="stChatInput"]) {
        flex: 0 0 500px !important;
        max-width: 500px !important;
    }
    [data-testid="stBottomBlockContainer"] > div:has([data-testid="stSelectbox"]) {
        flex: 0 0 160px !important;
        max-width: 160px !important;
    }
    /* Also collapse the iframe wrapper from components.html to zero */
    [data-testid="stBottomBlockContainer"] > div:has(iframe) {
        flex: 0 0 0px !important;
        width: 0px !important;
        max-width: 0px !important;
        overflow: hidden !important;
    }
    [data-testid="stChatInput"] { width: 100% !important; padding: 16px 0 24px !important; }
    [data-testid="stChatInput"] > div {
        background: #ffffff !important;
        border: 1px solid #D5D1C8 !important;
        border-radius: 14px !important;
        padding: 4px 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }
    /* Kill navy on every inner element */
    [data-testid="stChatInput"] * {
        background-color: #ffffff !important;
        color: #2D2B27 !important;
    }
    [data-testid="stChatInput"] > div > *,
    [data-testid="stChatInput"] > div > * > * {
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #2D2B27 !important;
        font-size: 14.5px !important;
        background: #ffffff !important;
        -webkit-text-fill-color: #2D2B27 !important;
        caret-color: #2D2B27 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9B9590 !important;
        -webkit-text-fill-color: #9B9590 !important;
    }

    /* Selectbox beside Chat Input (moved by JS into bottom container) */
    .sb-moved [data-testid="stSelectbox"],
    [data-testid="stSelectbox"] {
        position: static !important;
        width: 160px !important;
        flex-shrink: 0 !important;
        z-index: auto !important;
        transform: none !important;
        bottom: auto !important;
        left: auto !important;
        align-self: center !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background: #EEECE2 !important;
        border: 1px solid #D5D1C8 !important;
        border-radius: 8px !important;
        min-height: 32px !important;
        padding: 0 4px !important;
        cursor: pointer !important;
    }
    [data-testid="stSelectbox"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 12px !important;
        color: #2D2B27 !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSelectbox"] div[data-baseweb="select"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: #2D2B27 !important;
        -webkit-text-fill-color: #2D2B27 !important;
    }
    [data-testid="stSelectbox"] svg {
        fill: #6B6560 !important;
        color: #6B6560 !important;
    }
    [data-testid="stSelectbox"] label { display: none !important; }
    [data-testid="stChatInput"] textarea { color: #2D2B27 !important; font-size: 14.5px !important; background: transparent !important; -webkit-text-fill-color: #2D2B27 !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: #9B9590 !important; -webkit-text-fill-color: #9B9590 !important; }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #D5D1C8; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #B8B4AB; }

    /* Logo area */
    .logo-area { display: flex; align-items: center; gap: 10px; padding: 10px 20px; margin-bottom: 20px; font-size: 18px; font-weight: 700; color: #2D2B27; }
    .logo-icon { width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #DA7756, #C96A4B); color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; }

    /* Back Button Top Left */
    .back-btn-container {
        position: absolute;
        top: 24px;
        left: 24px;
        z-index: 1000;
    }
    .back-btn-container .stButton > button {
        background: #2D2B27 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        width: auto !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.2s !important;
    }
    .back-btn-container .stButton > button:hover {
        background: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2) !important;
    }

    /* ── Sidebar Button Overrides ── */
    [data-testid="stSidebar"] .stButton > button {
        background: #E5E2D6 !important;
        color: #2D2B27 !important;
        border: 1px solid #D5D1C8 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #DAD7CB !important;
        border-color: #C5C1B8 !important;
    }
    /* Primary (active chat) button in sidebar */
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[data-testid*="primary"] {
        background: #DA7756 !important;
        color: #ffffff !important;
        border: 1px solid #C96A4B !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: #C96A4B !important;
    }

    /* ── Popover (three-dot menu) ── */
    [data-testid="stPopover"] > div:first-child > button {
        background: transparent !important;
        border: 1px solid #D5D1C8 !important;
        color: #6B6560 !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        min-height: 32px !important;
    }
    [data-testid="stPopover"] > div:first-child > button:hover {
        background: #E5E2D6 !important;
        color: #2D2B27 !important;
    }
    /* Popover dropdown panel */
    [data-testid="stPopoverBody"],
    div[data-baseweb="popover"] > div {
        background: #FAF9F5 !important;
        border: 1px solid #D5D1C8 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    [data-testid="stPopoverBody"] .stButton > button,
    div[data-baseweb="popover"] .stButton > button {
        background: #FAF9F5 !important;
        color: #2D2B27 !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
    }
    [data-testid="stPopoverBody"] .stButton > button:hover,
    div[data-baseweb="popover"] .stButton > button:hover {
        background: #EEECE2 !important;
    }

    /* ── Selectbox Dropdown Menu (baseweb) ── */
    ul[role="listbox"] {
        background: #FAF9F5 !important;
        border: 1px solid #D5D1C8 !important;
        border-radius: 8px !important;
    }
    ul[role="listbox"] li {
        color: #2D2B27 !important;
        background: transparent !important;
    }
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"] {
        background: #EEECE2 !important;
    }

    /* ── Chat Input Send Button ── */
    [data-testid="stChatInput"] button {
        background: #DA7756 !important;
        border: none !important;
        border-radius: 8px !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #ffffff !important;
        color: #ffffff !important;
        display: block !important;
    }
    [data-testid="stChatInput"] button:hover {
        background: #C96A4B !important;
    }

    /* ── Streamlit Spinner / Loading ── */
    .stSpinner > div { color: #DA7756 !important; }

    /* ── Markdown text colors ── */
    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4 {
        color: #2D2B27 !important;
    }
    [data-testid="stMain"] a { color: #DA7756 !important; }

    /* ── Streamlit alerts / info / success / error ── */
    [data-testid="stAlert"] {
        background: #EEECE2 !important;
        border: 1px solid #D5D1C8 !important;
        color: #2D2B27 !important;
        border-radius: 8px !important;
    }

    /* ── Sidebar text colors ── */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #2D2B27 !important;
    }
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
            st.session_state.view_history.append(st.session_state.view)
            st.session_state.view = "source_selection"
            st.rerun()
    with col3:
        if st.button("Try Demo 🎮", use_container_width=True):
            st.session_state.view_history.append(st.session_state.view)
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
1.⁠ ⁠Answer ONLY from the context below. Never use external knowledge.
2.⁠ ⁠If the user asks for a general summary or overview, summarize the provided context to the best of your ability.
3.⁠ ⁠If the answer is completely missing from the context and cannot be inferred, say exactly: "I couldn't find this in the uploaded documents."
4.⁠ ⁠Auto-correct obvious phonetic typos in the context (e.g. if the context is a YouTube transcript and says 'langin' or 'langraph', correct it to 'LangChain' and 'LangGraph' in your answer).
5.⁠ ⁠{style_instruction}

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

    # Back button
    if st.session_state.view_history:
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Back"):
            st.session_state.view = st.session_state.view_history.pop()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
                    st.session_state.view_history.append(st.session_state.view)
                    st.session_state.view = "chat"
                    st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_chat():
    with st.sidebar:
        st.markdown('''
        <div class="logo-area">
            <div class="logo-icon">S</div>
            Scapia AI
        </div>
        ''', unsafe_allow_html=True)

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
                st.session_state.view_history.append(st.session_state.view)
                st.session_state.view = "source_selection"
                st.rerun()

        st.markdown("<hr style='border-color: #E5E2D6; margin: 16px 4px;'>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px;font-weight:700;color:#9B9590;margin:0 4px 8px;letter-spacing:.06em;'>CHATS</div>", unsafe_allow_html=True)

        chats_items = list(st.session_state.chats.items())
        pinned = [(k, v) for k, v in chats_items if v.get("pinned", False) and not v.get("archived", False)]
        unpinned = [(k, v) for k, v in chats_items if not v.get("pinned", False) and not v.get("archived", False)]
        archived_chats = [(k, v) for k, v in chats_items if v.get("archived", False)]

        for c_id, c_data in pinned + unpinned:
            col1, col2 = st.columns([5, 1])
            icon = "📌 " if c_data.get("pinned") else "💬 "
            btn_type = "primary" if c_id == st.session_state.current_chat_id else "secondary"
            with col1:
                if st.button(icon + c_data.get("title", "Chat"), key=f"btn_{c_id}", type=btn_type, use_container_width=True):
                    st.session_state.current_chat_id = c_id
                    st.rerun()
            with col2:
                with st.popover("⋮", use_container_width=True):
                    if st.button("Archive", key=f"arc_{c_id}", use_container_width=True):
                        st.session_state.chats[c_id]["archived"] = True
                        save_chats(st.session_state.chats)
                        if st.session_state.current_chat_id == c_id:
                            remaining = [k for k, v in st.session_state.chats.items() if not v.get("archived", False)]
                            if remaining: st.session_state.current_chat_id = remaining[0]
                            else:
                                new_id = str(uuid.uuid4())
                                st.session_state.chats[new_id] = {"title": "New Chat", "messages": [], "pinned": False}
                                st.session_state.current_chat_id = new_id
                                save_chats(st.session_state.chats)
                        st.rerun()
                    if st.button("Delete", key=f"del_{c_id}", use_container_width=True):
                        del st.session_state.chats[c_id]
                        save_chats(st.session_state.chats)
                        if st.session_state.current_chat_id == c_id:
                            remaining = [k for k, v in st.session_state.chats.items() if not v.get("archived", False)]
                            if remaining: st.session_state.current_chat_id = remaining[0]
                            else:
                                new_id = str(uuid.uuid4())
                                st.session_state.chats[new_id] = {"title": "New Chat", "messages": [], "pinned": False}
                                st.session_state.current_chat_id = new_id
                                save_chats(st.session_state.chats)
                        st.rerun()

        if archived_chats:
            st.markdown("<div style='font-size:11px;font-weight:700;color:#9B9590;margin:16px 4px 8px;letter-spacing:.06em;'>ARCHIVED</div>", unsafe_allow_html=True)
            for c_id, c_data in archived_chats:
                col1, col2 = st.columns([5, 1])
                btn_type = "primary" if c_id == st.session_state.current_chat_id else "secondary"
                with col1:
                    if st.button("📦 " + c_data.get("title", "Chat"), key=f"btn_{c_id}", type=btn_type, use_container_width=True):
                        st.session_state.current_chat_id = c_id
                        st.rerun()
                with col2:
                    with st.popover("⋮", use_container_width=True):
                        if st.button("Unarchive", key=f"unarc_{c_id}", use_container_width=True):
                            st.session_state.chats[c_id]["archived"] = False
                            save_chats(st.session_state.chats)
                            st.rerun()
                        if st.button("Delete", key=f"del_{c_id}", use_container_width=True):
                            del st.session_state.chats[c_id]
                            save_chats(st.session_state.chats)
                            if st.session_state.current_chat_id == c_id:
                                remaining = [k for k, v in st.session_state.chats.items() if not v.get("archived", False)]
                                if remaining: st.session_state.current_chat_id = remaining[0]
                                else:
                                    new_id = str(uuid.uuid4())
                                    st.session_state.chats[new_id] = {"title": "New Chat", "messages": [], "pinned": False}
                                    st.session_state.current_chat_id = new_id
                                    save_chats(st.session_state.chats)
                            st.rerun()

        st.markdown("<hr style='border-color: #E5E2D6; margin: 16px 4px;'>", unsafe_allow_html=True)

    active_chat = st.session_state.chats.get(st.session_state.current_chat_id)
    if not active_chat:
        st.error("Chat not found.")
        st.stop()

    messages = active_chat.get("messages", [])

    if not messages:
        st.markdown('''
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;text-align:center;">
            <div style="font-size:32px;font-weight:700;color:#2D2B27;margin-bottom:8px;">What would you like to know?</div>
            <div style="font-size:14px;color:#9B9590;">Upload a document in the sidebar, then ask away.</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div style="max-width: 700px; margin: 0 auto; padding: 0 24px 100px 24px;">', unsafe_allow_html=True)
    for message in messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown('<div class="user-msg-marker" style="display:none;"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="assistant-msg-marker" style="display:none;"></div>', unsafe_allow_html=True)
            st.markdown(message["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.selectbox("", ["Llama 3.1 (Flash)", "Llama 3.3 (Thinking)"], key="model_choice", label_visibility="collapsed")

    # JS: move the selectbox into the bottom container so they sit side-by-side
    import streamlit.components.v1 as components
    components.html("""
    <script>
    function moveSelectbox() {
        const doc = window.parent.document;
        const bottom = doc.querySelector('[data-testid="stBottomBlockContainer"]');
        if (!bottom) return;

        // Find selectbox NOT already inside the bottom bar
        const allSB = doc.querySelectorAll('[data-testid="stSelectbox"]');
        let sb = null;
        allSB.forEach(el => { if (!bottom.contains(el)) sb = el; });
        if (!sb) return;

        // Remove any old selectbox already in the bottom bar
        bottom.querySelectorAll('[data-testid="stSelectbox"]').forEach(old => old.remove());

        // Append directly into the bottom container
        bottom.appendChild(sb);
        sb.style.cssText = 'flex: 0 0 160px !important; width: 160px !important; max-width: 160px !important; align-self: center !important;';
    }
    setTimeout(moveSelectbox, 200);
    setTimeout(moveSelectbox, 800);
    setTimeout(moveSelectbox, 2000);
    setTimeout(moveSelectbox, 4000);
    </script>
    """, height=0)

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
# Keep URL query parameters in sync with session state so refreshes open the same page
st.query_params.view = st.session_state.view
st.session_state._last_url_view = st.session_state.view
if "current_chat_id" in st.session_state and st.session_state.current_chat_id:
    st.query_params.chat_id = st.session_state.current_chat_id

if st.session_state.view == "landing":
    render_landing()
elif st.session_state.view == "source_selection":
    render_source_selection()
else:
    render_chat()