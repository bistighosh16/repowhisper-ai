"""
PR Companion Page - RepoWhisper AI
Your guide to making your first open source contribution

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
    page_title="PR Companion | RepoWhisper AI",
    page_icon="🚪",
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
    
    /* Input styling */
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
    
    /* Issue Card */
    .issue-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0 1rem 0;
        border-left: 6px solid var(--sage-dark);
        box-shadow: 0 4px 20px rgba(61, 90, 60, 0.1);
    }
    
    .issue-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: var(--sage-deepest) !important;
        margin-bottom: 0.5rem;
    }
    
    .issue-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: var(--sage-medium);
    }
    
    .issue-label {
        background: linear-gradient(135deg, #F4C8D5 0%, #C8DCC2 100%);
        color: var(--sage-deepest);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid var(--sage-light);
    }
    
    .issue-state-open {
        background: #C8DCC2;
        color: #2C4028;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    .issue-state-closed {
        background: #F4B8C8;
        color: #8B3A5C;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    
    /* Guidance Header */
    .guidance-header {
        background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3);
    }
    
    .guidance-header h2 {
        color: white !important;
        margin: 0 !important;
        font-size: 2rem !important;
    }
    
    .guidance-header p {
        color: white !important;
        margin-top: 0.5rem !important;
        font-size: 1.1rem;
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
    
    pre code .k, pre code .kd, pre code .kn {
        color: #F4B8C8 !important;
        font-weight: 600 !important;
    }
    
    pre code .s, pre code .s1, pre code .s2 {
        color: #A8C4A2 !important;
    }
    
    pre code .c, pre code .c1 {
        color: #8FA88C !important;
        font-style: italic !important;
    }
    
    pre code .nf {
        color: #E8829F !important;
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
        st.markdown("### 📌 Current Repo")
        st.markdown(f"**{st.session_state['current_repo']}**")
        st.markdown("---")
    
    st.markdown("### 🚪 What is PR Companion?")
    st.markdown("""
    Your guide to making your first open source contribution!
    
    **How it works:**
    1. Find an issue you want to fix
    2. Paste the issue URL here
    3. Get AI guidance on:
       - Which files to look at
       - What to change
       - How to write your PR
    """)
    st.markdown("---")
    st.markdown("### 🎯 Find Issues At")
    st.markdown("""
    - Repo's Issues tab on GitHub
    - Filter by `good first issue` label
    - Look for `help wanted` tag
    """)
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
st.markdown('<h1 class="page-title">🚪 PR Companion</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Your guide to making your first open source contribution</p>', unsafe_allow_html=True)

# Check if repo is loaded
if 'file_tree' not in st.session_state or 'repo_url' not in st.session_state:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🚪</div>
        <h3>Load a repository first!</h3>
        <p>Head to the <strong>🗺️ Explorer</strong> page and analyze a repo.</p>
        <p>Then come back to get help with contributions! 💜</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Show current repo badge
    st.markdown(f"""
    <div class="repo-badge">
        <span class="repo-badge-label">📦 Contributing to:</span>
        <span class="repo-badge-name">{st.session_state['current_repo']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("### 🔗 Paste the Issue URL")
    st.markdown("Find an issue you want to work on, then paste its URL below!")
    
    # Example
    with st.expander("💡 How to find an issue URL"):
        st.markdown("""
        1. Go to your repo on GitHub
        2. Click the **Issues** tab
        3. Filter by `good first issue` for beginner-friendly issues
        4. Click on an issue you like
        5. Copy the URL from your browser
        
        **Example URL format:**  
        `https://github.com/owner/repo/issues/123`
        """)
    
    # Input
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        issue_url = st.text_input(
            "GitHub Issue URL",
            placeholder="https://github.com/owner/repo/issues/123",
            label_visibility="collapsed",
            key="issue_url_input"
        )
    
    with col_button:
        analyze_button = st.button("🔍 Get Guide", use_container_width=True)
    
    # ============================================================
    # ANALYSIS LOGIC
    # ============================================================
    if analyze_button and issue_url:
        try:
            reader = get_reader()
            ai = get_ai()
            
            progress = st.progress(0, text="🔍 Fetching issue details...")
            
            # Fetch issue
            progress.progress(30, text="📥 Reading issue from GitHub...")
            issue_data = reader.get_issue(issue_url)
            
            if "error" in issue_data:
                progress.empty()
                st.error(f"❌ {issue_data['error']}")
            else:
                # Prepare file tree text
                progress.progress(60, text="🗺️ Preparing context...")
                file_tree = st.session_state.get('file_tree', {})
                code_files = file_tree.get('code_files', [])
                file_tree_text = "\n".join([f"- {f['path']}" for f in code_files[:60]])
                
                # Get AI guidance
                progress.progress(80, text="🧠 AI is crafting your contribution guide...")
                result = ai.guide_contribution(
                    issue_title=issue_data['title'],
                    issue_body=issue_data['body'],
                    repo_summary=st.session_state.get('repo_analysis', ''),
                    file_tree_text=file_tree_text
                )
                
                progress.progress(100, text="✅ Guide ready!")
                progress.empty()
                
                if result['success']:
                    # Save to session state
                    st.session_state['pr_issue_data'] = issue_data
                    st.session_state['pr_guidance'] = result['content']
                else:
                    st.error(f"❌ AI Error: {result['error']}")
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
    
    elif analyze_button and not issue_url:
        st.warning("⚠️ Please paste an issue URL first!")
    
    # ============================================================
    # DISPLAY RESULTS
    # ============================================================
    if 'pr_issue_data' in st.session_state and 'pr_guidance' in st.session_state:
        st.markdown("---")
        
        issue = st.session_state['pr_issue_data']
        
        # Issue Card
        state_class = "issue-state-open" if issue['state'] == 'open' else "issue-state-closed"
        state_emoji = "🟢" if issue['state'] == 'open' else "🔴"
        
        labels_html = ""
        if issue['labels']:
            labels_html = " ".join([f'<span class="issue-label">🏷️ {label}</span>' for label in issue['labels']])
        
        st.markdown(f"""
        <div class="issue-card">
            <h2 class="issue-title">#{issue['number']}: {issue['title']}</h2>
            <div class="issue-meta">
                <span class="{state_class}">{state_emoji} {issue['state'].upper()}</span>
                <span>👤 by <strong>{issue['author']}</strong></span>
                <span>📅 {issue['created_at']}</span>
                <span>💬 {issue['comments_count']} comments</span>
            </div>
            <div>{labels_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show issue body
        with st.expander("📄 View Full Issue Description", expanded=False):
            st.markdown(issue['body'])
        
        # Link to issue
        st.markdown(f"🔗 [View Issue on GitHub →]({issue['url']})")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Guidance Header
        st.markdown("""
        <div class="guidance-header">
            <h2>🎓 Your Contribution Guide</h2>
            <p>Follow these steps to make your first PR with confidence!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show AI guidance
        cleaned_guidance = clean_markdown_output(st.session_state['pr_guidance'])
        st.markdown(cleaned_guidance)
        
        # Encouragement CTA
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6B8E6A 0%, #E8829F 100%); 
                    border-radius: 20px; padding: 2.5rem; text-align: center; 
                    box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3); margin: 2rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌟</div>
            <h3 style="color: white !important; margin-top: 0 !important; font-size: 1.8rem !important;">You've Got This!</h3>
            <p style="color: white !important; font-size: 1.15rem; margin-bottom: 0;">
                Every senior developer started with their first PR. This is YOUR moment! 💜
            </p>
            <p style="color: white !important; font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
                Made with 💜 by Vivi's RepoWhisper AI
            </p>
        </div>
        """, unsafe_allow_html=True)
