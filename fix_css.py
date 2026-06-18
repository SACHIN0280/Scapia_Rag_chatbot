with open("app.py", "r") as f:
    code = f.read()

# Blocks to remove:
landing_hide_sidebar = '    st.markdown("""<style>[data-testid="stSidebar"] { display: none !important; }</style>""", unsafe_allow_html=True)\n    \n'
landing_css_block = '''    <style>
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
    div[data-testid=\'stHorizontalBlock\'] > div:nth-child(2) .stButton > button { background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid=\'stHorizontalBlock\'] > div:nth-child(2) .stButton > button:hover { background: #2563eb !important; border-color: #1d4ed8 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important; }
    div[data-testid=\'stHorizontalBlock\'] > div:nth-child(3) .stButton > button { background: transparent !important; border: 1px solid #3b82f6 !important; color: #3b82f6 !important; font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; } 
    div[data-testid=\'stHorizontalBlock\'] > div:nth-child(3) .stButton > button:hover { background: rgba(59,130,246,0.1) !important; transform: translateY(-2px) !important; }
    </style>

'''

source_css_block = '''    <style>
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
    </style>
    
'''

source_btn = '    st.markdown("<style>div.stButton > button { background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important; padding: 12px 30px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; }\\ndiv.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important; background: #2563eb !important; color: white !important; border-color: #1d4ed8 !important; }</style>", unsafe_allow_html=True)\n    \n'

chat_css_block = '''    <style>
    /* Chat Specific CSS */
    [data-testid="stSidebar"] {
        display: flex !important;
        background: #111827 !important;
        border-right: 1px solid #1f2937 !important;
        min-width: 280px !important;
        max-width: 280px !important;
        transform: translateX(0px) !important;
        visibility: visible !important;
        padding-bottom: 70px !important;
    }
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    
    /* File Uploader */
    [data-testid="stFileUploader"] { background: #1f2937 !important; border: 1px dashed #374151 !important; border-radius: 12px !important; padding: 12px !important; }
    [data-testid="stFileUploader"] p { color: #9ca3af !important; font-size: 13px !important; }
    [data-testid="stFileUploaderDropzoneIcon"] { display: none !important; }
    [data-testid="stFileUploader"] button { width: auto !important; background: #374151 !important; padding: 4px 12px !important; font-size: 12px !important; color: white !important; margin-top: 10px !important; }

    /* Text Input */
    .stTextInput > div > div > input {
        background: #1f2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        color: #f3f4f6 !important;
        font-size: 13px !important;
        padding: 10px !important;
    }
    .stTextInput > div > div > input:focus { border-color: #6366f1 !important; box-shadow: none !important; }
    .stTextInput label { display: none !important; }

    /* Chat Messages */
    [data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 10px 15px !important; }
    [data-testid="stChatMessageContent"] { font-size: 15px !important; line-height: 1.6 !important; color: #f8fafc !important; }
    .stChatMessageAvatar { display: none !important; }

    /* User Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { flex-direction: row-reverse !important; display: flex !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
        background: #312e81 !important; /* Deep Indigo Bubble */
        border: 1px solid #3730a3 !important;
        border-radius: 16px 16px 4px 16px !important;
        padding: 12px 18px !important;
        max-width: 70% !important;
        color: #f8fafc !important;
        margin-left: auto !important;
    }

    /* Assistant Bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
        background: transparent !important;
        border: none !important;
        padding: 12px 0 !important;
        max-width: 750px !important;
        margin: 0 auto !important;
    }

    /* Chat Input Bar */
    [data-testid="stBottom"] { background: transparent !important; }
    [data-testid="stBottom"] > div { background: transparent !important; }
    [data-testid="stBottomBlockContainer"] { background: transparent !important; display: flex !important; justify-content: center !important; }
    [data-testid="stChatInput"] { background: transparent !important; padding: 20px !important; width: 100% !important; max-width: 750px !important; margin: 0 auto !important; transform: translateX(-65px) !important; }
    [data-testid="stChatInput"] > div {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important;
        padding: 6px 10px !important;
        width: 100% !important;
    }
    [data-testid="stChatInput"] textarea { color: #f8fafc !important; font-size: 15px !important; background: transparent !important; }
    [data-testid="stChatInput"] button { background: #6366f1 !important; border-radius: 12px !important; }
    
    /* Expander */
    [data-testid="stExpander"] { background: #1e293b !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
    [data-testid="stExpander"] summary { color: #94a3b8 !important; }

    /* Top Nav */
    .chat-nav { display:flex; align-items:center; justify-content:space-between; padding:14px 24px; border-bottom:1px solid #1e293b; background:#0F172A; }
    .chat-nav-logo { display:flex; align-items:center; gap:9px; font-size:15px; font-weight:700; color:#f8fafc; }
    .chat-nav-logo-icon { width:28px; height:28px; background:linear-gradient(135deg,#6366f1,#8b5cf6); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:14px; }
    </style>

'''

chat_sidebar_btn = '        st.markdown("<style>.stButton > button { margin-bottom: 8px; }</style>", unsafe_allow_html=True)\n        \n'

chat_float_css = '''    st.markdown("""
    <style>
    /* Floating Selectbox right side of Chat Input */
    [data-testid="stSelectbox"] {
        position: fixed;
        bottom: 82px; 
        right: max(calc(50vw - 675px), 0px);
        width: 200px !important;
        z-index: 99999;
    }
    
    /* Dark pill styling */
    [data-testid="stSelectbox"] > div > div {
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        min-height: 32px !important;
        padding: 0 4px !important;
        cursor: pointer !important;
    }
    
    /* Hide the typing cursor so it feels like a button */
    [data-testid="stSelectbox"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }
    
    /* Small text */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 12px !important;
        color: #f8fafc !important;
    }
    [data-testid="stSelectbox"] label { display: none !important; }
    
    /* Normal padding */
    [data-testid="stChatInput"] textarea {
        padding-right: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
'''

# Delete all inline CSS blocks
code = code.replace(landing_hide_sidebar, "")
code = code.replace(landing_css_block, "")
code = code.replace(source_css_block, "")
code = code.replace(source_btn, "")
code = code.replace(chat_css_block, "")
code = code.replace(chat_sidebar_btn, "")
code = code.replace(chat_float_css, "")

# Build dynamic CSS strings without the <style> tags (stripping them out)
landing_css_raw = landing_css_block.replace("    <style>\n", "").replace("    </style>\n\n", "").strip()
source_css_raw = source_css_block.replace("    <style>\n", "").replace("    </style>\n    \n", "").strip()
chat_css_raw = chat_css_block.replace("    <style>\n", "").replace("    </style>\n\n", "").strip()
float_css_raw = chat_float_css.replace('    st.markdown("""\n    <style>\n', '').replace('    </style>\n    """, unsafe_allow_html=True)\n    \n', '').strip()

source_btn_raw = "div.stButton > button { background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important; font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important; padding: 12px 30px !important; font-size: 16px !important; border-radius: 8px !important; transition: all 0.2s ease !important; }\ndiv.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important; background: #2563eb !important; color: white !important; border-color: #1d4ed8 !important; }"

sidebar_btn_raw = ".stButton > button { margin-bottom: 8px; }"

dynamic_global_injection = f'''
view = st.session_state.view
dynamic_css = ""

if view == "landing":
    dynamic_css = """
    [data-testid="stSidebar"] {{ display: none !important; }}
    {landing_css_raw}
    """
elif view == "source_selection":
    dynamic_css = """
    {source_css_raw}
    {source_btn_raw}
    """
elif view == "chat":
    dynamic_css = """
    {chat_css_raw}
    {sidebar_btn_raw}
    {float_css_raw}
    """

st.markdown(f"""
<style>
{{dynamic_css}}
</style>
""", unsafe_allow_html=True)
'''

# Find end of original global CSS block
global_end = '    transition: all 0.2s !important;\n}\n\n.stButton > button:hover { transform: translateY(-1px) !important; }\n.stButton > button:active { transform: scale(0.98) !important; }\n\n/* Landing page primary/secondary CTA buttons — styled globally up-front\n   instead of injected mid-layout, so there\'s no unstyled flash window */\n.hero-cta-primary .stButton > button {\n    background: #3b82f6 !important; border: 1px solid #2563eb !important; color: white !important;\n    font-weight: 600 !important; box-shadow: 0 4px 14px rgba(59,130,246,0.4) !important;\n    padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;\n}\n.hero-cta-primary .stButton > button:hover {\n    background: #2563eb !important; border-color: #1d4ed8 !important;\n    box-shadow: 0 6px 20px rgba(59,130,246,0.6) !important;\n}\n.hero-cta-secondary .stButton > button {\n    background: transparent !important; border: 1px solid #3b82f6 !important; color: #3b82f6 !important;\n    font-weight: 600 !important; padding: 14px 20px !important; font-size: 16px !important; border-radius: 8px !important;\n}\n.hero-cta-secondary .stButton > button:hover { background: rgba(59,130,246,0.1) !important; }\n\n/* Scrollbar */\n::-webkit-scrollbar { width: 6px; }\n::-webkit-scrollbar-track { background: #0F172A; }\n::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }\n::-webkit-scrollbar-thumb:hover { background: #475569; }\n\n</style>\n""", unsafe_allow_html=True)\n'

code = code.replace(global_end, global_end + "\n" + dynamic_global_injection)

with open("app.py", "w") as f:
    f.write(code)

print("CSS refactored.")
