"""
RepoWhisper AI - Home Page
The tool that helps you keep your job 🌿

Made with 💜 by Vivi
"""

import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="RepoWhisper AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS - Sage Green + Pink Professional Theme
# ============================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    
    /* Root Colors - DEEPER Sage Green + Pink Palette */
    :root {
        --sage-light: #A8C4A2;
        --sage-medium: #6B8E6A;
        --sage-dark: #3D5A3C;
        --sage-deepest: #2C4028;
        --pink-light: #F4B8C8;
        --pink-medium: #E8829F;
        --pink-dark: #C85A7E;
        --pink-deepest: #8B3A5C;
        --cream: #FAF7F2;
        --cream-warm: #F5EDE0;
        --charcoal: #1F2E1F;
        --text-body: #2C3E2D;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #FAF7F2 0%, #F0E8DC 100%);
    }
    
    /* Sidebar Styling - Darker for contrast */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #D4E0CE 0%, #E8C8D2 100%);
        border-right: 3px solid var(--sage-dark);
    }

    
    section[data-testid="stSidebar"] * {
        color: var(--sage-deepest) !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--sage-deepest) !important;
        font-weight: 700 !important;
    }
    
    /* All Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
        font-weight: 700 !important;
    }
    
    /* Body Text - MUCH darker for readability */
    p, span, div, li {
        font-family: 'Inter', sans-serif;
        color: var(--text-body);
    }
    
    /* Hero Title */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3D5A3C 0%, #C85A7E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        color: var(--sage-dark);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 500;
        font-style: italic;
    }
    
    /* Feature Cards - White with clear borders */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(61, 90, 60, 0.15);
        border: 2px solid var(--sage-light);
        transition: all 0.3s ease;
        height: 100%;
        min-height: 260px;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(200, 90, 126, 0.25);
        border-color: var(--pink-medium);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--sage-deepest);
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        font-family: 'Inter', sans-serif;
        color: #3D4A3D;
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Info Boxes - DEEPER background, DARK text */
    .info-box {
        background: linear-gradient(135deg, #F4C8D5 0%, #C8DCC2 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border-left: 6px solid var(--sage-dark);
        box-shadow: 0 4px 15px rgba(61, 90, 60, 0.1);
    }
    
    .info-box h3 {
        color: var(--sage-deepest) !important;
        margin-top: 0 !important;
        font-weight: 700 !important;
    }
    
    .info-box p {
        color: var(--charcoal) !important;
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 500;
        margin-bottom: 0;
    }
    
    .info-box strong {
        color: var(--pink-deepest);
        font-weight: 700;
    }
    
    /* CTA Box - Extra emphasis */
    .cta-box {
        background: linear-gradient(135deg, #E8829F 0%, #6B8E6A 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 30px rgba(200, 90, 126, 0.3);
    }
    
    .cta-box h3 {
        color: white !important;
        margin-top: 0 !important;
        font-size: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .cta-box p {
        color: white !important;
        font-size: 1.15rem;
        font-weight: 500;
        margin-bottom: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .cta-box strong {
        color: #FFE5EC;
        font-weight: 700;
    }
    
    /* Made with love footer */
    .made-with-love {
        text-align: center;
        color: var(--sage-dark);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        margin-top: 3rem;
        padding: 1.5rem;
        font-weight: 500;
        border-top: 2px dashed var(--sage-light);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--sage-dark) 0%, var(--pink-dark) 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(200, 90, 126, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(200, 90, 126, 0.5);
    }
    
    /* Section Headers */
    .stMarkdown h2 {
        color: var(--sage-deepest) !important;
        font-size: 2.2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
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
    st.markdown("### 📚 Navigation")
    st.markdown("👈 Use the pages above to explore features!")
    st.markdown("---")
    st.markdown("### 💡 How to Use")
    st.markdown("""
    1. Start with **🗺️ Explorer** to load a repo
    2. Use **📖 Code Story** to understand files
    3. Try **🐛 Bug Spotter** to find issues
    4. **💬 Chat** with your codebase
    5. Get help with **🚪 PR Companion**
    """)
    st.markdown("---")
    st.markdown("*Made with 💜 by Vivi*")

# ============================================================
# MAIN CONTENT
# ============================================================

# Hero Section
st.markdown('<h1 class="hero-title">RepoWhisper AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">🌿 The tool that helps you keep your job 🍓</p>', unsafe_allow_html=True)

# Info Box
st.markdown("""
<div class="info-box">
    <h3 style="margin-top: 0;">👋 Welcome, developer!</h3>
    <p style="margin-bottom: 0; color: #1F2E1F;">
        Ever felt lost staring at a massive codebase? You're not alone! 
        RepoWhisper AI helps you <b style="color: #C85A7E;">understand</b>, 
        <b style="color: #C85A7E;">navigate</b>, and 
        <b style="color: #C85A7E;">contribute</b> 
        to any GitHub repository — like having a senior developer sitting next to you.
    </p>
</div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("## ✨ What Can RepoWhisper Do?")
st.markdown("")

# Row 1
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <div class="feature-title">Repo Explorer</div>
        <p class="feature-desc">
            Get a complete architectural overview of any GitHub repository. 
            Understand the structure, key files, and where to start reading.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📖</div>
        <div class="feature-title">Code Story</div>
        <p class="feature-desc">
            AI narrates any code file as a story. Understand what each 
            function does, how components connect, and why decisions were made.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🐛</div>
        <div class="feature-title">Bug Spotter</div>
        <p class="feature-desc">
            AI-powered code review that finds bugs, security issues, and 
            anti-patterns. Learn WHY each issue matters and how to fix it.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Row 2
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Chat with Codebase</div>
        <p class="feature-desc">
            Your personal senior dev buddy. Ask any question about the code, 
            get context-aware answers, and learn as you go.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚪</div>
        <div class="feature-title">PR Companion</div>
        <p class="feature-desc">
            Make your first open source contribution with confidence. 
            Get guided from issue to pull request, step by step.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌿</div>
        <div class="feature-title">Made for Devs</div>
        <p class="feature-desc">
            Built by a developer, for developers. Whether you're a junior 
            or mid-level dev, RepoWhisper grows with you.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Call to Action
st.markdown("""
<div class="cta-box">
    <h3>🚀 Ready to Start?</h3>
    <p>Head to the <strong>🗺️ Explorer</strong> page in the sidebar to analyze your first repository!</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="made-with-love">
    Made with 💜 by Vivi | RepoWhisper AI © 2024
</div>
""", unsafe_allow_html=True)
