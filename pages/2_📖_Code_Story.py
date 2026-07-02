"""
Code Story Page - RepoWhisper AI
AI narrates any code file as a beautiful story

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
    page_title="Code Story | RepoWhisper AI",
    page_icon="📖",
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
    
    /* Search Input */
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid var(--sage-light);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--charcoal);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--pink-medium);
        box-shadow: 0 0 0 3px rgba(232, 130, 159, 0.2);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid var(--sage-light);
        border-radius: 12px;
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
    
    /* File count badge */
    .file-count {
        background: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        display: inline-block;
        color: var(--sage-dark);
        font-weight: 600;
        border: 1px solid var(--sage-light);
        margin-bottom: 1rem;
    }
    
    /* Story container */
    .story-header {
        background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0 1rem 0;
        color: white;
        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3);
    }
    
    .story-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.8rem !important;
    }
    
    .story-header .file-path {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
            
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
        st.markdown("### 📌 Currently Reading")
        st.markdown(f"**{st.session_state['current_repo']}**")
        st.markdown("---")
    
    st.markdown("### 💡 How To Use")
    st.markdown("""
    1. Load a repo in **🗺️ Explorer** first
    2. Search or pick a file below
    3. Click **Explain This File**
    4. Read the beautiful story! 📖
    """)
    st.markdown("---")
    st.markdown("### 🎓 Pro Tip")
    st.markdown("*Start with entry point files like `main.py`, `app.py`, or `__init__.py`!*")
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
# INITIALIZE MODULES
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
st.markdown('<h1 class="page-title">📖 Code Story</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Let AI narrate any code file as an engaging story</p>', unsafe_allow_html=True)

# Check if repo is loaded
if 'file_tree' not in st.session_state or 'repo_url' not in st.session_state:
    # Empty state - no repo loaded
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📚</div>
        <h3>No repository loaded yet!</h3>
        <p>Head to the <strong>🗺️ Explorer</strong> page first to analyze a repository.</p>
        <p>Once loaded, come back here to hear the story of any file! ✨</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show current repo badge
    st.markdown(f"""
    <div class="repo-badge">
        <span class="repo-badge-label">📦 Reading from:</span>
        <span class="repo-badge-name">{st.session_state['current_repo']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Get file list
    file_tree = st.session_state['file_tree']
    code_files = file_tree.get('code_files', [])
    all_file_paths = [f['path'] for f in code_files]
    
    # File count
    st.markdown(f'<div class="file-count">📁 {len(all_file_paths)} code files available</div>', unsafe_allow_html=True)
    
    # SEARCH + SELECT UX
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input(
            "🔍 Search for a file",
            placeholder="Type to filter... (e.g., 'button', 'theme', 'main')",
            key="file_search"
        )
    
    with col_filter:
        # Extract file extensions for filter
        extensions = sorted(set([
            "." + f.split(".")[-1] for f in all_file_paths if "." in f
        ]))
        extension_filter = st.selectbox(
            "Filter by type",
            options=["All types"] + extensions,
            key="ext_filter"
        )
    
    # Apply filters
    filtered_files = all_file_paths
    
    if search_query:
        filtered_files = [f for f in filtered_files if search_query.lower() in f.lower()]
    
    if extension_filter != "All types":
        filtered_files = [f for f in filtered_files if f.endswith(extension_filter)]
    
    # Show filtered count
    if search_query or extension_filter != "All types":
        st.markdown(f"*Showing {len(filtered_files)} of {len(all_file_paths)} files*")
    
    # File selector
    if filtered_files:
        selected_file = st.selectbox(
            "📄 Choose a file to explore",
            options=filtered_files,
            key="selected_file"
        )
        
        # Explain button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            explain_button = st.button("✨ Explain This File", use_container_width=True)
        
        # ============================================================
        # AI EXPLANATION LOGIC
        # ============================================================
        if explain_button:
            try:
                reader = get_reader()
                ai = get_ai()
                
                progress = st.progress(0, text="📄 Fetching file content...")
                
                # Fetch file content
                progress.progress(30, text="📄 Reading file from GitHub...")
                file_content = reader.get_file_content(
                    st.session_state['repo_url'],
                    selected_file
                )
                
                if file_content.startswith("Error:") or file_content.startswith("Invalid"):
                    st.error(f"❌ {file_content}")
                elif file_content == "Binary file - cannot display as text":
                    st.warning("⚠️ This is a binary file and cannot be analyzed as text.")
                else:
                    # Get repo context for better analysis
                    progress.progress(60, text="🧠 AI is reading and understanding...")
                    repo_context = st.session_state.get('repo_analysis', '')[:1500]
                    
                    # Get AI explanation
                    progress.progress(80, text="✨ Crafting the story...")
                    result = ai.explain_code_file(
                        file_path=selected_file,
                        file_content=file_content,
                        repo_context=repo_context
                    )
                    
                    progress.progress(100, text="✅ Story ready!")
                    progress.empty()
                    
                    if result['success']:
                        # Save to session state for reference
                        st.session_state[f'story_{selected_file}'] = result['content']
                        st.session_state['last_story_file'] = selected_file
                        st.session_state['last_story_content'] = result['content']
                        st.session_state['last_story_code'] = file_content
                    else:
                        st.error(f"❌ AI Error: {result['error']}")
            
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        
        # ============================================================
        # DISPLAY STORY (if exists)
        # ============================================================
        if 'last_story_content' in st.session_state:
            st.markdown(f"""
            <div class="story-header">
                <h2>📖 The Story of...</h2>
                <div class="file-path">{st.session_state['last_story_file']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show the AI narration (cleaned!)
            cleaned_story = clean_markdown_output(st.session_state['last_story_content'])
            st.markdown(cleaned_story)
            
            # Show original code in expander
            with st.expander("💻 View Original Source Code", expanded=False):
                # Determine language from extension
                file_ext = st.session_state['last_story_file'].split('.')[-1]
                lang_map = {
                    'py': 'python', 'js': 'javascript', 'ts': 'typescript',
                    'jsx': 'jsx', 'tsx': 'tsx', 'java': 'java',
                    'cpp': 'cpp', 'c': 'c', 'cs': 'csharp',
                    'go': 'go', 'rs': 'rust', 'rb': 'ruby',
                    'php': 'php', 'swift': 'swift', 'kt': 'kotlin',
                    'html': 'html', 'css': 'css', 'sql': 'sql',
                    'yaml': 'yaml', 'yml': 'yaml', 'json': 'json',
                    'md': 'markdown', 'sh': 'bash',
                }
                lang = lang_map.get(file_ext, 'text')
                st.code(st.session_state['last_story_code'], language=lang)
            
            # Next steps CTA
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%); 
                        border-radius: 20px; padding: 2rem; text-align: center; 
                        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3); margin: 2rem 0;">
                <h3 style="color: white !important; margin-top: 0 !important;">🎯 What's Next?</h3>
                <p style="color: white !important; font-size: 1.1rem; margin-bottom: 0;">
                    Check for bugs in this file with <strong>🐛 Bug Spotter</strong>, 
                    or explore another file above! ✨
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # No files match filter
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <h3>No files match your search!</h3>
            <p>Try a different keyword or clear the filter.</p>
        </div>
        """, unsafe_allow_html=True)
