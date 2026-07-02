"""
Bug Spotter Page - RepoWhisper AI
AI-powered code review that finds bugs AND teaches you

Made with 💜 by Vivi
"""

import streamlit as st
import sys
import os
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.github_reader import GitHubReader
from src.core.ai_engine import AIEngine

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Bug Spotter | RepoWhisper AI",
    page_icon="🐛",
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
        --critical: #C0392B;
        --medium: #E67E22;
        --low: #27AE60;
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
    
    /* Search & filter */
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
    
    /* Scan Header */
    .scan-header {
        background: linear-gradient(135deg, #C85A7E 0%, #3D5A3C 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0 1rem 0;
        color: white;
        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3);
    }
    
    .scan-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 1.8rem !important;
    }
    
    .scan-header .file-path {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Severity Summary Cards */
    .severity-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(61, 90, 60, 0.1);
        border: 2px solid var(--sage-light);
        transition: all 0.3s ease;
    }
    
    .severity-card:hover {
        transform: translateY(-3px);
    }
    
    .severity-count {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
    }
    
    .severity-critical .severity-count { color: var(--critical); }
    .severity-medium .severity-count { color: var(--medium); }
    .severity-low .severity-count { color: var(--low); }
    
    .severity-label {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: var(--sage-dark);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Clean code celebration */
    .clean-code {
        background: linear-gradient(135deg, #C8DCC2 0%, #A8C4A2 100%);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(107, 142, 106, 0.3);
    }
    
    .clean-code-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }
    
    .clean-code h2 {
        color: var(--sage-deepest) !important;
        font-size: 2.5rem !important;
    }
    
    .clean-code p {
        color: var(--sage-deepest);
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* Inline code */
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
.stDeployButton {display: none;}

/* Hide header background but keep toggle button visible */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

/* Sidebar toggle button - sage and pink theme */
[data-testid="stSidebarCollapsedControl"] {
    background: linear-gradient(135deg, #3D5A3C, #C85A7E) !important;
    border: 1px solid #A8C4A2 !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 15px rgba(61, 90, 60, 0.4);
    z-index: 999999 !important;
}

[data-testid="stSidebarCollapsedControl"]:hover {
    background: linear-gradient(135deg, #C85A7E, #3D5A3C) !important;
    box-shadow: 0 6px 25px rgba(200, 90, 126, 0.6);
}

[data-testid="stSidebarCollapsedControl"] button {
    color: white !important;
}
        
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER: Count severities from AI output
# ============================================================
def clean_markdown_output(text: str) -> str:
    """
    Fix nested code blocks in AI output.
    Removes indentation from code blocks inside bullet points
    so they render properly in Streamlit.
    """
    lines = text.split('\n')
    cleaned_lines = []
    in_code_block = False
    code_block_indent = 0
    
    for line in lines:
        stripped = line.lstrip()
        
        # Detect start of code block
        if stripped.startswith('```'):
            if not in_code_block:
                # Starting a code block - record its indent
                code_block_indent = len(line) - len(stripped)
                in_code_block = True
                # Remove indentation from the opening ```
                cleaned_lines.append(stripped)
            else:
                # Ending a code block
                in_code_block = False
                cleaned_lines.append(stripped)
        elif in_code_block:
            # Inside code block - remove the base indentation
            if line.startswith(' ' * code_block_indent):
                cleaned_lines.append(line[code_block_indent:])
            else:
                cleaned_lines.append(line)
        else:
            # Regular line - keep as is
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def count_severities(analysis_text: str) -> dict:
    """Count how many issues of each severity level."""
    critical = len(re.findall(r'🔴\s*Critical', analysis_text, re.IGNORECASE))
    medium = len(re.findall(r'🟡\s*Medium', analysis_text, re.IGNORECASE))
    low = len(re.findall(r'🟢\s*Low', analysis_text, re.IGNORECASE))
    return {
        "critical": critical,
        "medium": medium,
        "low": low,
        "total": critical + medium + low
    }

def is_clean_code(analysis_text: str) -> bool:
    """Check if AI reported no issues."""
    clean_indicators = [
        "clean code",
        "no major issues",
        "no issues detected",
        "no bugs found"
    ]
    text_lower = analysis_text.lower()
    return any(indicator in text_lower for indicator in clean_indicators)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🌿 RepoWhisper AI")
    st.markdown("*The tool that helps you keep your job*")
    st.markdown("---")
    
    if "current_repo" in st.session_state:
        st.markdown("### 📌 Currently Scanning")
        st.markdown(f"**{st.session_state['current_repo']}**")
        st.markdown("---")
    
    st.markdown("### 🎯 Severity Guide")
    st.markdown("""
    - 🔴 **Critical** — Fix immediately!  
      Security, crashes, data loss
    - 🟡 **Medium** — Fix soon  
      Performance, logic issues
    - 🟢 **Low** — Consider fixing  
      Style, minor improvements
    """)
    st.markdown("---")
    st.markdown("### 💡 Pro Tip")
    st.markdown("*Always fix Critical issues before deploying!*")
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
# MAIN CONTENT
# ============================================================

# Page Title
st.markdown('<h1 class="page-title">🐛 Bug Spotter</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">AI code review that finds bugs AND teaches you why they matter</p>', unsafe_allow_html=True)

# Check if repo is loaded
if 'file_tree' not in st.session_state or 'repo_url' not in st.session_state:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <h3>No repository loaded yet!</h3>
        <p>Head to the <strong>🗺️ Explorer</strong> page first to analyze a repository.</p>
        <p>Once loaded, come back here to hunt for bugs! 🐛</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show current repo badge
    st.markdown(f"""
    <div class="repo-badge">
        <span class="repo-badge-label">📦 Scanning:</span>
        <span class="repo-badge-name">{st.session_state['current_repo']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Get file list
    file_tree = st.session_state['file_tree']
    code_files = file_tree.get('code_files', [])
    all_file_paths = [f['path'] for f in code_files]
    
    # File count
    st.markdown(f'<div class="file-count">📁 {len(all_file_paths)} code files available for scanning</div>', unsafe_allow_html=True)
    
    # SEARCH + SELECT UX
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input(
            "🔍 Search for a file to scan",
            placeholder="Type to filter... (e.g., 'auth', 'api', 'database')",
            key="bug_file_search"
        )
    
    with col_filter:
        extensions = sorted(set([
            "." + f.split(".")[-1] for f in all_file_paths if "." in f
        ]))
        extension_filter = st.selectbox(
            "Filter by type",
            options=["All types"] + extensions,
            key="bug_ext_filter"
        )
    
    # Apply filters
    filtered_files = all_file_paths
    
    if search_query:
        filtered_files = [f for f in filtered_files if search_query.lower() in f.lower()]
    
    if extension_filter != "All types":
        filtered_files = [f for f in filtered_files if f.endswith(extension_filter)]
    
    if search_query or extension_filter != "All types":
        st.markdown(f"*Showing {len(filtered_files)} of {len(all_file_paths)} files*")
    
    # File selector
    if filtered_files:
        selected_file = st.selectbox(
            "📄 Choose a file to scan for bugs",
            options=filtered_files,
            key="bug_selected_file"
        )
        
        # Scan button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            scan_button = st.button("🔍 Scan for Bugs", use_container_width=True)
        
        # ============================================================
        # BUG SCAN LOGIC
        # ============================================================
        if scan_button:
            try:
                reader = get_reader()
                ai = get_ai()
                
                progress = st.progress(0, text="📄 Fetching file content...")
                
                # Fetch file
                progress.progress(30, text="📄 Reading file from GitHub...")
                file_content = reader.get_file_content(
                    st.session_state['repo_url'],
                    selected_file
                )
                
                if file_content.startswith("Error:") or file_content.startswith("Invalid"):
                    st.error(f"❌ {file_content}")
                elif file_content == "Binary file - cannot display as text":
                    st.warning("⚠️ This is a binary file and cannot be analyzed.")
                else:
                    # AI Analysis
                    progress.progress(70, text="🧠 AI is hunting for bugs...")
                    result = ai.find_bugs(
                        file_path=selected_file,
                        file_content=file_content
                    )
                    
                    progress.progress(100, text="✅ Scan complete!")
                    progress.empty()
                    
                    if result['success']:
                        st.session_state['last_scan_file'] = selected_file
                        st.session_state['last_scan_content'] = result['content']
                        st.session_state['last_scan_code'] = file_content
                    else:
                        st.error(f"❌ AI Error: {result['error']}")
            
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        
        # ============================================================
        # DISPLAY SCAN RESULTS
        # ============================================================
        if 'last_scan_content' in st.session_state:
            analysis = st.session_state['last_scan_content']
            
            # Scan header
            st.markdown(f"""
            <div class="scan-header">
                <h2>🐛 Bug Scan Results</h2>
                <div class="file-path">{st.session_state['last_scan_file']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Check if code is clean
            if is_clean_code(analysis):
                st.markdown("""
                <div class="clean-code">
                    <div class="clean-code-icon">✨</div>
                    <h2>Clean Code!</h2>
                    <p>No major issues detected. This file looks great! 🎉</p>
                    <p style="font-size: 1rem; opacity: 0.8;">Keep up the amazing work! 💜</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Show severity summary
                severities = count_severities(analysis)
                
                if severities['total'] > 0:
                    st.markdown("### 📊 Scan Summary")
                    col_c, col_m, col_l, col_t = st.columns(4)
                    
                    with col_c:
                        st.markdown(f"""
                        <div class="severity-card severity-critical">
                            <div class="severity-label">🔴 Critical</div>
                            <div class="severity-count">{severities['critical']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_m:
                        st.markdown(f"""
                        <div class="severity-card severity-medium">
                            <div class="severity-label">🟡 Medium</div>
                            <div class="severity-count">{severities['medium']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_l:
                        st.markdown(f"""
                        <div class="severity-card severity-low">
                            <div class="severity-label">🟢 Low</div>
                            <div class="severity-count">{severities['low']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_t:
                        st.markdown(f"""
                        <div class="severity-card">
                            <div class="severity-label">📊 Total</div>
                            <div class="severity-count" style="color: var(--sage-deepest);">{severities['total']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # Show full analysis (cleaned!)
                st.markdown("### 🔍 Detailed Analysis")
                cleaned_analysis = clean_markdown_output(analysis)
                st.markdown(cleaned_analysis)
            
            # Show original code
            with st.expander("💻 View Original Source Code", expanded=False):
                file_ext = st.session_state['last_scan_file'].split('.')[-1]
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
                st.code(st.session_state['last_scan_code'], language=lang)
            
            # Next steps CTA
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%); 
                        border-radius: 20px; padding: 2rem; text-align: center; 
                        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3); margin: 2rem 0;">
                <h3 style="color: white !important; margin-top: 0 !important;">🎯 What's Next?</h3>
                <p style="color: white !important; font-size: 1.1rem; margin-bottom: 0;">
                    Understand the file better with <strong>📖 Code Story</strong>, 
                    or ask questions in <strong>💬 Chat</strong>! ✨
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <h3>No files match your search!</h3>
            <p>Try a different keyword or clear the filter.</p>
        </div>
        """, unsafe_allow_html=True)
