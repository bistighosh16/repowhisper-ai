"""
Chat Page - RepoWhisper AI
Your personal senior dev buddy for any codebase

Made with 💜 by Vivi
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.github_reader import GitHubReader
from src.core.ai_engine import AIEngine

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Chat | RepoWhisper AI",
    page_icon="💬",
    layout="wide",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --sage-light: #A8C4A2;
        --sage-medium: #6B8E6A;
        --sage-dark: #3D5A3C;
        --sage-deepest: #2C4028;
        --pink-light: #F4B8C8;
        --pink-medium: #E8829F;
        --pink-dark: #C85A7E;
        --cream: #FAF7F2;
        --charcoal: #1F2E1F;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FAF7F2 0%, #F0E8DC 100%);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #D4E0CE 0%, #E8C8D2 100%);
        border-right: 3px solid var(--sage-dark);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--sage-deepest) !important;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
        font-weight: 700 !important;
    }
    
    p, span, div, li {
        font-family: 'Inter', sans-serif;
        color: #2C3E2D;
    }
    
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3D5A3C 0%, #C85A7E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
    }
    
    .page-subtitle {
        font-size: 1.15rem;
        color: var(--sage-dark);
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Repo Badge */
    .repo-badge {
        background: linear-gradient(135deg, #C8DCC2 0%, #F4C8D5 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 5px solid var(--sage-dark);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .repo-badge-label {
        color: var(--sage-deepest);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .repo-badge-name {
        color: var(--pink-dark);
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Chat message styling */
    div[data-testid="stChatMessage"] {
        background: white;
        border-radius: 15px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid var(--sage-light);
        box-shadow: 0 2px 10px rgba(61, 90, 60, 0.08);
    }
    
    /* User message specific */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #F4C8D5 0%, #FFE5EC 100%);
        border-left: 4px solid var(--pink-dark);
    }
    
    /* Assistant message specific */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, #E8F0E5 0%, #F5FAF3 100%);
        border-left: 4px solid var(--sage-dark);
    }
    
    /* Chat input area */
    .stChatInput {
        border-radius: 15px !important;
    }
    
        div[data-testid="stChatInput"] {
        background: white !important;
        border: 2px solid var(--sage-light) !important;
        border-radius: 15px !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--pink-medium) !important;
        box-shadow: 0 0 0 3px rgba(232, 130, 159, 0.2) !important;
    }
    
    /* Fix invisible text in chat input */
    div[data-testid="stChatInput"] textarea {
        color: #2C4028 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background: white !important;
    }
    
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8FA88C !important;
        font-style: italic !important;
    }
    
    /* Send button styling */
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, var(--sage-dark) 0%, var(--pink-dark) 100%) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.05) !important;
    }
            
                /* Fix the chat input container background */
    section[data-testid="stBottom"] {
        background: linear-gradient(135deg, #FAF7F2 0%, #F0E8DC 100%) !important;
    }
    
    section[data-testid="stBottom"] > div {
        background: transparent !important;
    }
    
    div[data-testid="stChatInput"] {
        background: white !important;
        border: 2px solid var(--sage-light) !important;
        border-radius: 15px !important;
        padding: 0.25rem !important;
    }
    
    /* Fix invisible text in chat input */
    div[data-testid="stChatInput"] textarea {
        color: #2C4028 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background: white !important;
    }
    
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #8FA88C !important;
        font-style: italic !important;
    }
    
    /* Send button styling */
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, var(--sage-dark) 0%, var(--pink-dark) 100%) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    div[data-testid="stChatInput"] button:hover {
        transform: scale(1.05) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--sage-dark) 0%, var(--pink-dark) 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(200, 90, 126, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(200, 90, 126, 0.5);
    }
    
    /* Suggested questions */
    .suggestion-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        border: 2px solid var(--sage-light);
        margin-bottom: 0.75rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--sage-deepest);
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .suggestion-card:hover {
        border-color: var(--pink-medium);
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(200, 90, 126, 0.15);
    }
    
    /* Inline code */
    code {
        background: linear-gradient(135deg, #F4C8D5 0%, #C8DCC2 100%) !important;
        color: #2C4028 !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.92em !important;
        font-weight: 600 !important;
        border: 1px solid #A8C4A2 !important;
    }
    
    /* Code Blocks */
    pre {
        background: #1F2E1F !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 2px solid #A8C4A2 !important;
        overflow-x: auto !important;
    }
    
    pre code {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.9em !important;
        line-height: 1.7 !important;
    }
    
    pre code span,
    pre code .token {
        color: #F5F0E8 !important;
    }
    
    pre code .k, pre code .kd, pre code .kn, pre code .kc {
        color: #F4B8C8 !important;
        font-weight: 600 !important;
    }
    
    pre code .s, pre code .s1, pre code .s2 {
        color: #A8C4A2 !important;
    }
    
    pre code .c, pre code .c1, pre code .cm {
        color: #8FA88C !important;
        font-style: italic !important;
    }
    
    pre code .nf, pre code .fm {
        color: #E8829F !important;
    }
    
    pre code .nc, pre code .nn {
        color: #FAF7F2 !important;
        font-weight: 600 !important;
    }
    
    pre code .m, pre code .mi, pre code .mf {
        color: #F4C8D5 !important;
    }
    
    pre code .nb {
        color: #C8DCC2 !important;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        background: white;
        border-radius: 20px;
        border: 2px dashed var(--sage-light);
        margin-top: 2rem;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state h3 {
        color: var(--sage-deepest) !important;
    }
    
    .empty-state p {
        color: var(--sage-medium);
        font-size: 1.1rem;
    }
    
    /* Welcome banner for chat */
    .chat-welcome {
        background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3);
        margin-bottom: 2rem;
    }
    
    .chat-welcome h3 {
        color: white !important;
        margin-top: 0 !important;
        font-size: 1.8rem !important;
    }
    
    .chat-welcome p {
        color: white !important;
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER: Clean AI markdown output
# ============================================================
def clean_markdown_output(text: str) -> str:
    """Fix nested code blocks in AI output."""
    lines = text.split('\n')
    cleaned_lines = []
    in_code_block = False
    code_block_indent = 0
    
    for line in lines:
        stripped = line.lstrip()
        
        if stripped.startswith('```'):
            if not in_code_block:
                code_block_indent = len(line) - len(stripped)
                in_code_block = True
                cleaned_lines.append(stripped)
            else:
                in_code_block = False
                cleaned_lines.append(stripped)
        elif in_code_block:
            if line.startswith(' ' * code_block_indent):
                cleaned_lines.append(line[code_block_indent:])
            else:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🌿 RepoWhisper AI")
    st.markdown("*The tool that helps you keep your job*")
    st.markdown("---")
    
    if "current_repo" in st.session_state:
        st.markdown("### 📌 Chatting About")
        st.markdown(f"**{st.session_state['current_repo']}**")
        st.markdown("---")
    
    st.markdown("### 💡 Try Asking")
    st.markdown("""
    - What does this project do?
    - How does the authentication work?
    - Where is the database connection?
    - Which file should I read first?
    - Explain the folder structure
    - What design patterns are used?
    """)
    st.markdown("---")
    
    # Clear chat button in sidebar
    if "chat_messages" in st.session_state and len(st.session_state["chat_messages"]) > 0:
        if st.button("🗑️ Clear Chat History", key="clear_chat_sidebar"):
            st.session_state["chat_messages"] = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("*Made with 💜 by Vivi*")

# ============================================================
# INITIALIZE MODULES
# ============================================================
@st.cache_resource
def get_reader():
    return GitHubReader()

@st.cache_resource
def get_ai():
    return AIEngine()

# ============================================================
# INITIALIZE CHAT MESSAGES
# ============================================================
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

# ============================================================
# MAIN CONTENT
# ============================================================

# Page Title
st.markdown('<h1 class="page-title">💬 Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Your personal senior dev buddy — ask anything about the codebase</p>', unsafe_allow_html=True)

# Check if repo is loaded
if 'repo_analysis' not in st.session_state or 'repo_url' not in st.session_state:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💬</div>
        <h3>Load a repository first!</h3>
        <p>Head to the <strong>🗺️ Explorer</strong> page and analyze a repo.</p>
        <p>Then come back here to chat with your senior dev buddy! 💜</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show current repo badge
    st.markdown(f"""
    <div class="repo-badge">
        <span class="repo-badge-label">📦 Chatting about:</span>
        <span class="repo-badge-name">{st.session_state['current_repo']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message if no chat history
    if len(st.session_state["chat_messages"]) == 0:
        st.markdown("""
        <div class="chat-welcome">
            <h3>👋 Hey there!</h3>
            <p>I've read through the codebase and I'm ready to help. Ask me anything!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggested questions
        st.markdown("### 💡 Not sure what to ask? Try these:")
        
        suggested_questions = [
            "What does this project do in simple terms?",
            "What are the most important files I should read first?",
            "Explain the overall architecture",
            "What technologies and frameworks are used?",
            "How would I contribute to this project?",
        ]
        
        col1, col2 = st.columns(2)
        for i, q in enumerate(suggested_questions):
            with col1 if i % 2 == 0 else col2:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    # Add as user message and trigger response
                    st.session_state["chat_messages"].append({
                        "role": "user",
                        "content": q
                    })
                    st.rerun()
    
    # Display chat history
    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                cleaned = clean_markdown_output(message["content"])
                st.markdown(cleaned)
            else:
                st.markdown(message["content"])
    
    # Check if last message is from user and needs a response
    if (len(st.session_state["chat_messages"]) > 0 and 
        st.session_state["chat_messages"][-1]["role"] == "user"):
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                try:
                    ai = get_ai()
                    
                    # Build context from repo analysis
                    repo_summary = st.session_state.get('repo_analysis', '')
                    
                    # Get the last user question
                    user_question = st.session_state["chat_messages"][-1]["content"]
                    
                    # Get AI response
                    result = ai.chat_about_code(
                        user_question=user_question,
                        repo_summary=repo_summary,
                        relevant_code=""
                    )
                    
                    if result['success']:
                        response = result['content']
                        cleaned_response = clean_markdown_output(response)
                        st.markdown(cleaned_response)
                        
                        # Save to chat history
                        st.session_state["chat_messages"].append({
                            "role": "assistant",
                            "content": response
                        })
                    else:
                        error_msg = f"❌ Sorry, I encountered an error: {result['error']}"
                        st.markdown(error_msg)
                        st.session_state["chat_messages"].append({
                            "role": "assistant",
                            "content": error_msg
                        })
                
                except Exception as e:
                    error_msg = f"❌ Unexpected error: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state["chat_messages"].append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Chat input at the bottom
    user_input = st.chat_input("Ask me anything about this codebase... 💬")
    
    if user_input:
        # Add user message to history
        st.session_state["chat_messages"].append({
            "role": "user",
            "content": user_input
        })
        st.rerun()