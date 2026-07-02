"""
Explorer Page - RepoWhisper AI
The gateway to understanding any GitHub repository

Made with 💜 by Vivi
"""

import streamlit as st
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.github_reader import GitHubReader
from src.core.ai_engine import AIEngine

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Explorer | RepoWhisper AI",
    page_icon="🗺️",
    layout="wide",
)

# ============================================================
# CUSTOM CSS (same theme as home!)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
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
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid var(--sage-light);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: var(--charcoal);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--pink-medium);
        box-shadow: 0 0 0 3px rgba(232, 130, 159, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--sage-dark) 0%, var(--pink-dark) 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 2.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(200, 90, 126, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(200, 90, 126, 0.5);
    }
    
    /* Stat cards */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid var(--sage-light);
        box-shadow: 0 4px 15px rgba(61, 90, 60, 0.1);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        border-color: var(--pink-medium);
    }
    
    .stat-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: var(--sage-deepest);
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: var(--sage-dark);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Analysis box */
    .analysis-box {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border-left: 6px solid var(--sage-dark);
        box-shadow: 0 4px 20px rgba(61, 90, 60, 0.1);
    }
    
    .analysis-box h2 {
        color: var(--sage-deepest) !important;
        margin-top: 1.5rem !important;
    }
    
    .analysis-box h3 {
        color: var(--pink-dark) !important;
        margin-top: 1.5rem !important;
    }
    
    /* Success/Info messages */
    .success-msg {
        background: linear-gradient(135deg, #C8DCC2 0%, #F4C8D5 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--sage-dark);
        color: var(--sage-deepest);
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
            
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
    
    /* Code Blocks Container */
    pre {
        background: #1F2E1F !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 2px solid #A8C4A2 !important;
        overflow-x: auto !important;
    }
    
    /* Base code inside pre */
    pre code {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.9em !important;
        line-height: 1.7 !important;
    }
    
    /* FORCE ALL SYNTAX TOKENS TO BE VISIBLE (light colors!) */
    pre code span,
    pre code .token,
    .highlight span,
    .highlight .token {
        color: #F5F0E8 !important;
    }
    
    /* Keywords (if, else, from, import, def, class, etc.) - Pink */
    pre code .k, pre code .kd, pre code .kn, pre code .kc,
    pre code .keyword, .highlight .k, .highlight .kd, .highlight .kn {
        color: #F4B8C8 !important;
        font-weight: 600 !important;
    }
    
    /* Strings - Light Sage */
    pre code .s, pre code .s1, pre code .s2, pre code .sb, pre code .sd,
    pre code .string, .highlight .s, .highlight .s1, .highlight .s2 {
        color: #A8C4A2 !important;
    }
    
    /* Comments - Muted */
    pre code .c, pre code .c1, pre code .cm, pre code .comment,
    .highlight .c, .highlight .c1, .highlight .cm {
        color: #8FA88C !important;
        font-style: italic !important;
    }
    
    /* Function names - Light Pink */
    pre code .nf, pre code .fm, pre code .function,
    .highlight .nf, .highlight .fm {
        color: #E8829F !important;
    }
    
    /* Class names - Cream */
    pre code .nc, pre code .nn, pre code .class,
    .highlight .nc, .highlight .nn {
        color: #FAF7F2 !important;
        font-weight: 600 !important;
    }
    
    /* Numbers - Warm */
    pre code .m, pre code .mi, pre code .mf, pre code .number,
    .highlight .m, .highlight .mi, .highlight .mf {
        color: #F4C8D5 !important;
    }
    
    /* Operators - Light */
    pre code .o, pre code .operator,
    .highlight .o {
        color: #E8C8D2 !important;
    }
    
    /* Names/Variables - Light cream */
    pre code .n, pre code .name,
    .highlight .n {
        color: #F5F0E8 !important;
    }
    
    /* Built-ins - Sage */
    pre code .nb, pre code .builtin,
    .highlight .nb {
        color: #C8DCC2 !important;
    }
    
    /* Punctuation - Muted cream */
    pre code .p, pre code .punctuation,
    .highlight .p {
        color: #D4D0C8 !important;
    }
    
    /* Streamlit specific overrides */
    .stCode {
        border-radius: 12px !important;
    }
    
    .stCode > div {
        background: #1F2E1F !important;
    }
    
    /* Hover fix - prevent code from disappearing */
    pre:hover, pre code:hover, pre code span:hover {
        opacity: 1 !important;
    }
    
    /* Streamlit's code containers */
    .stCode {
        border-radius: 12px !important;
    }
    
    .stCode > div {
        background: #2C4028 !important;
    }
    
    /* Preserve code formatting in markdown */
    .element-container pre code {
        white-space: pre !important;
        display: block !important;
    }
            
                /* NUCLEAR FIX: Force ALL possible sidebar toggle selectors visible */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    div[data-testid="stSidebarCollapsedControl"],
    button[title="Close sidebar"],
    button[title="Open sidebar"],
    [aria-label="Open sidebar"],
    [aria-label="Close sidebar"],
    .stSidebar > div > button,
    section[data-testid="stSidebar"] button:first-child {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999999999 !important;
        background: linear-gradient(135deg, #3D5A3C 0%, #C85A7E 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        width: auto !important;
        height: auto !important;
        min-width: 40px !important;
        min-height: 40px !important;
    }
    
    /* Force all SVGs inside toggle buttons to be white */
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg,
    button[title*="sidebar"] svg,
    button[aria-label*="sidebar"] svg {
        color: white !important;
        fill: white !important;
        stroke: white !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Remove any hidden overrides on parent containers */
    [data-testid="stSidebarCollapsedControl"] * {
        visibility: visible !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🌿 RepoWhisper AI")
    st.markdown("*The tool that helps you keep your job*")
    st.markdown("---")
    
    if "current_repo" in st.session_state:
        st.markdown("### 📌 Currently Analyzing")
        st.markdown(f"**{st.session_state['current_repo']}**")
        st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Use public repositories
    - Try popular repos like:
      - `streamlit/streamlit`
      - `tiangolo/fastapi`
      - Your own repos!
    """)
    st.markdown("---")
    st.markdown("*Made with 💜 by Vivi*")

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
# INITIALIZE MODULES (with caching!)
# ============================================================
@st.cache_resource
def get_reader():
    return GitHubReader()

@st.cache_resource
def get_ai():
    return AIEngine()

# ============================================================
# MAIN CONTENT
# ============================================================

# Page Title
st.markdown('<h1 class="page-title">🗺️ Repo Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Paste any GitHub URL and let AI map the codebase for you</p>', unsafe_allow_html=True)

# Input Section
col_input, col_button = st.columns([4, 1])

with col_input:
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repository",
        label_visibility="collapsed",
        key="repo_url_input"
    )

with col_button:
    analyze_button = st.button("🔍 Analyze", use_container_width=True)

# ============================================================
# ANALYSIS LOGIC
# ============================================================
if analyze_button and repo_url:
    try:
        reader = get_reader()
        ai = get_ai()
        
        # Validate URL first
        parsed = reader.parse_repo_url(repo_url)
        if not parsed:
            st.error("❌ Invalid GitHub URL! Please use format: https://github.com/owner/repo")
        else:
            # Multi-step progress
            progress = st.progress(0, text="🌱 Starting analysis...")
            
            # Step 1: Get repo info
            progress.progress(20, text="📊 Fetching repository info...")
            repo_info = reader.get_repo_info(repo_url)
            
            if "error" in repo_info:
                st.error(f"❌ {repo_info['error']}")
            else:
                # Step 2: Get README
                progress.progress(40, text="📖 Reading README...")
                readme = reader.get_readme(repo_url)
                
                # Step 3: Get file tree
                progress.progress(60, text="🗂️ Mapping file structure...")
                file_tree = reader.get_file_tree(repo_url)
                
                if "error" in file_tree:
                    st.error(f"❌ {file_tree['error']}")
                else:
                    # Step 4: AI Analysis
                    progress.progress(80, text="🧠 AI is analyzing the codebase...")
                    analysis = ai.analyze_repo_structure(repo_info, file_tree, readme)
                    
                    progress.progress(100, text="✅ Complete!")
                    progress.empty()
                    
                    if analysis['success']:
                        # SAVE TO SESSION STATE for other pages!
                        st.session_state['repo_url'] = repo_url
                        st.session_state['current_repo'] = repo_info['full_name']
                        st.session_state['repo_info'] = repo_info
                        st.session_state['readme'] = readme
                        st.session_state['file_tree'] = file_tree
                        st.session_state['repo_analysis'] = analysis['content']
                        st.session_state['analysis_tokens'] = analysis['tokens_used']
                        
                        st.markdown('<div class="success-msg">✨ Analysis complete! Data saved — you can now use other pages!</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"❌ AI Error: {analysis['error']}")
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

elif analyze_button and not repo_url:
    st.warning("⚠️ Please enter a GitHub repository URL first!")

# ============================================================
# DISPLAY RESULTS (if analysis exists in session state)
# ============================================================
if 'repo_info' in st.session_state and 'repo_analysis' in st.session_state:
    st.markdown("---")
    
    repo_info = st.session_state['repo_info']
    
    # Repo Header
    st.markdown(f"## 📦 {repo_info['full_name']}")
    st.markdown(f"*{repo_info['description']}*")
    st.markdown(f"[View on GitHub →]({repo_info['url']})")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">⭐ Stars</div>
            <div class="stat-value">{repo_info['stars']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🍴 Forks</div>
            <div class="stat-value">{repo_info['forks']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">💻 Language</div>
            <div class="stat-value" style="font-size: 1.4rem;">{repo_info['language']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        file_tree = st.session_state.get('file_tree', {})
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📄 Code Files</div>
            <div class="stat-value">{file_tree.get('code_files_count', 0)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        size_kb = repo_info['size_kb']
        if size_kb < 1024:
            size_display = f"{size_kb} KB"
        elif size_kb < 1024 * 1024:
            size_display = f"{size_kb / 1024:.1f} MB"
        else:
            size_display = f"{size_kb / (1024 * 1024):.1f} GB"
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📦 Size</div>
            <div class="stat-value" style="font-size: 1.4rem;">{size_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # AI Analysis Display  
    st.markdown("## 🧠 AI Analysis")
    cleaned_analysis = clean_markdown_output(st.session_state['repo_analysis'])
    st.markdown(cleaned_analysis)
    
    # File Tree Expandable Section
    with st.expander("📁 View Complete File Structure", expanded=False):
        file_tree = st.session_state.get('file_tree', {})
        code_files = file_tree.get('code_files', [])
        
        st.markdown(f"**Showing {len(code_files)} code files:**")
        st.markdown("")
        
        for f in code_files:
            size_kb = f['size'] / 1024
            st.markdown(f"📄 `{f['path']}` — *{size_kb:.1f} KB*")
    
    # Next Steps CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%); 
                border-radius: 20px; padding: 2rem; text-align: center; 
                box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3); margin: 2rem 0;">
        <h3 style="color: white !important; margin-top: 0 !important;">🎯 What's Next?</h3>
        <p style="color: white !important; font-size: 1.1rem; margin-bottom: 0;">
            Head to <strong>📖 Code Story</strong> to understand specific files, 
            or <strong>💬 Chat</strong> to ask questions about the codebase!
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: white; 
                border-radius: 20px; border: 2px dashed #A8C4A2;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌱</div>
        <h3 style="color: #3D5A3C !important;">Ready to explore your first repository?</h3>
        <p style="color: #6B8E6A; font-size: 1.1rem;">
            Paste a GitHub URL above and click <strong>Analyze</strong> to begin!
        </p>
    </div>
    """, unsafe_allow_html=True)
