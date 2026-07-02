# 🌿 RepoWhisper AI

<div align="center">

### *The tool that helps you keep your job* 🍓

**An AI-powered companion that reads any GitHub repository, explains it in plain English, finds bugs, and guides you through open source contributions.**

[![Python](https://img.shields.io/badge/Python-3.11-3D5A3C?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39-C85A7E?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-6B8E6A?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-E8829F?style=for-the-badge)](LICENSE)

[**🚀 Live Demo**](https://repowhisper-ai.streamlit.app/) · [**📚 Documentation**](#-features) · [**🐛 Report Bug**](https://github.com/bistighosh16/repowhisper-ai/issues)

</div>

---

## 💡 The Story Behind This Project

Most developers don't get fired because they can't build new things.  
They struggle because they **can't read, debug, and navigate existing codebases** fast enough.

Getting hired is one thing. **Keeping the job** is another.

That's where **RepoWhisper AI** comes in — your personal senior developer sitting next to you, explaining every corner of any GitHub repository in plain English, helping you find bugs, and guiding you through your first open source contribution.

Whether you're a junior dev overwhelmed by a massive codebase or a mid-level engineer joining a new team, RepoWhisper AI grows with you. 💜

---

## ✨ Features

### 🗺️ Repo Explorer
Get a complete architectural overview of any GitHub repository.
- Understand the folder structure at a glance
- Identify key files to read first
- Detect the tech stack automatically
- Get a recommended reading order

### 📖 Code Story
AI narrates any code file as an engaging story.
- Plain English explanations
- Key components (classes/functions) breakdown
- How the file connects to others
- Design decisions explained
- Learning takeaways from real code

### 🐛 Bug Spotter
AI-powered code review that finds bugs AND teaches you why they matter.
- Severity ratings (🔴 Critical, 🟡 Medium, 🟢 Low)
- Detailed explanations of each issue
- Fix suggestions with code examples
- Educational focus — learn as you fix

### 💬 Chat with Codebase
Your personal senior dev buddy — ask anything.
- Context-aware answers about the loaded repo
- Suggested questions for quick starts
- Persistent chat history
- Beautiful sage green + pink message bubbles

### 🚪 PR Companion
Make your first open source contribution with confidence.
- Paste any GitHub issue URL
- Get specific file recommendations
- Ready-to-use PR description template
- Pre-submission checklist
- Motivational guidance because contributing is scary!

---

## 🎨 The Aesthetic

RepoWhisper AI features a professional **Sage Green + Soft Pink** theme designed to feel calming and approachable while remaining developer-focused.

- 🌿 **Sage Green** — Calm, professional, focused
- 🍓 **Soft Pink** — Warm, welcoming, human
- 🍦 **Cream Background** — Easy on the eyes for long coding sessions
- 📖 **Playfair Display** — Elegant, magazine-quality headings
- ✒️ **Inter** — Clean, modern body text
- 💻 **JetBrains Mono** — Beautiful code rendering

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11 |
| **UI Framework** | Streamlit (Multi-page app) |
| **AI Model** | Groq — Llama 3.3 70B Versatile |
| **GitHub API** | PyGithub |
| **Token Management** | tiktoken |
| **Environment** | python-dotenv |
| **Deployment** | Streamlit Community Cloud |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- A [Groq API key](https://console.groq.com) (free)
- A [GitHub Personal Access Token](https://github.com/settings/tokens) with `public_repo` scope (free)

### Installation

**1. Clone the repository:**

```bash
git clone https://github.com/bistighosh16/repowhisper-ai.git
cd repowhisper-ai
2. Create a virtual environment:

Bash

py -3.11 -m venv venv
3. Activate the virtual environment:

Windows:

Bash

.\venv\Scripts\activate
Mac/Linux:

Bash

source venv/bin/activate
4. Install dependencies:

Bash

pip install -r requirements.txt
5. Create a .env file in the project root:

env

GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here
6. Run the app:

Bash

streamlit run app.py
The app will open at http://localhost:8501 🎉

📖 How To Use
Workflow
Start with 🗺️ Explorer — Paste any GitHub repo URL to analyze it
📖 Code Story — Pick any file to hear its detailed story
🐛 Bug Spotter — Scan any file for issues and improvements
💬 Chat — Ask questions about the loaded codebase
🚪 PR Companion — Paste an issue URL for contribution guidance
Example: Contributing to Open Source
text

1. Analyze streamlit/streamlit in Explorer
2. Find an issue tagged "good first issue"
3. Paste the issue URL in PR Companion
4. Follow the AI's file recommendations
5. Fix the issue
6. Use the generated PR description template
7. Submit your PR with confidence! 🎉
🏗️ Project Structure
text

repowhisper-ai/
├── app.py                      # Home page
├── requirements.txt            # Dependencies
├── .env                        # API keys (not committed!)
├── .gitignore                  # Git exclusions
├── README.md                   # You're reading this!
│
├── src/
│   └── core/
│       ├── __init__.py
│       ├── github_reader.py    # GitHub API integration
│       └── ai_engine.py        # Groq AI logic
│
└── pages/
    ├── 1_🗺️_Explorer.py         # Repo analysis page
    ├── 2_📖_Code_Story.py       # File explanation page
    ├── 3_🐛_Bug_Spotter.py      # Bug detection page
    ├── 4_💬_Chat.py             # Chat interface page
    └── 5_🚪_PR_Companion.py     # Contribution guide page
🧠 Smart Design Decisions
Token-Efficient Architecture
RepoWhisper AI uses a 4-layer processing strategy to work within free tier limits while still delivering powerful analysis:

Structure Layer — Reads file tree + README only (~2K tokens)
Smart Sampling Layer — Analyzes key files (~8K tokens)
On-Demand Layer — Fetches specific files when user asks (~3K tokens)
Chat Memory Layer — Uses summaries instead of raw code (~1.5K tokens per message)
This means RepoWhisper can analyze repos with 500+ files while using minimal API calls!

Modular & Professional
Separation of concerns (core logic vs UI vs features)
Reusable AI engine with 5 specialized modes
Cached resources to prevent redundant API calls
Session state for cross-page data persistence
Error handling at every layer
🎯 Who Is This For?
🎓 Junior developers overwhelmed by their first big codebase at work
🌱 Aspiring open source contributors who don't know where to start
🔍 Code reviewers wanting AI-assisted analysis
📚 Students learning to read production code
🚀 Job seekers preparing to onboard quickly at new companies
💼 Mid-level developers joining unfamiliar projects
🚧 Roadmap
 Support for private repositories
 Vector database integration for semantic search
 Multi-file bug scanning at once
 Export analysis as beautiful PDF reports
 Chrome extension for GitHub integration
 Support for GitLab and Bitbucket
 Team collaboration features
 Historical analysis tracking
🤝 Contributing
Contributions make the open source community amazing! Any contributions are greatly appreciated.

Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
Pro tip: Use RepoWhisper AI to help you understand this codebase before contributing! 😉

📜 License
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgments
Groq for lightning-fast LLM inference
Streamlit for the incredible framework
PyGithub for making GitHub API a breeze
The open source community for inspiration ✨
👩‍💻 About the Creator
Vivi (Bistighosh) — A passionate developer building tools that matter.

🏆 National Hardware Hackathon Winner
📦 PyPI Publisher (NeonUI)
🌟 Open Source Contributor
💜 Building AI-powered developer tools
Connect with me:

🐙 GitHub: @bistighosh16
💼 LinkedIn: https://www.linkedin.com/in/bisti-ghosh-it-660488387/
📦 PyPI: https://pypi.org/project/neonui/
<div align="center">
Made with 💜 by Vivi
Building tools that help developers understand, contribute, and thrive.

⭐ If RepoWhisper AI helped you, please star the repo! ⭐

</div> ```
