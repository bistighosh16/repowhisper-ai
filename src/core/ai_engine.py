"""
AI Engine Module - RepoWhisper AI
The brain that analyzes and understands code

Made with 💜 by Vivi
"""

import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv
import tiktoken

load_dotenv()


class AIEngine:
    """The AI brain of RepoWhisper - handles all Groq interactions."""

    # Our chosen model - Llama 3.3 70B (fast + smart!)
    MODEL = "llama-3.3-70b-versatile"

    # Safety limits (to protect our free tier!)
    MAX_INPUT_TOKENS = 6000   # Leave room for response
    MAX_OUTPUT_TOKENS = 2000  # Reasonable response size

    def __init__(self):
        """Initialize with Groq API key."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "Groq API key not found! Please add GROQ_API_KEY to .env file"
            )
        self.client = Groq(api_key=api_key)
        # Use GPT-4 tokenizer as approximation (works for most models)
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.tokenizer.encode(text))

    def truncate_to_fit(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit."""
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= max_tokens:
            return text
        truncated = self.tokenizer.decode(tokens[:max_tokens])
        return truncated + "\n\n[... content truncated for token limits ...]"

    def _call_groq(self, system_prompt: str, user_prompt: str,
                   temperature: float = 0.7) -> dict:
        """
        Internal method to call Groq API safely.
        Returns structured response with success/error info.
        """
        # Check token count before sending!
        total_input = system_prompt + user_prompt
        token_count = self.count_tokens(total_input)

        if token_count > self.MAX_INPUT_TOKENS:
            # Truncate the user prompt to fit
            available = self.MAX_INPUT_TOKENS - self.count_tokens(system_prompt) - 100
            user_prompt = self.truncate_to_fit(user_prompt, available)

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=self.MAX_OUTPUT_TOKENS,
            )

            return {
                "success": True,
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None,
            }

    # ============================================================
    # FEATURE 1: REPO EXPLORER
    # ============================================================
    def analyze_repo_structure(self, repo_info: dict, file_tree: dict,
                                readme: str) -> dict:
        """
        Analyzes repo structure and gives a high-level overview.
        Uses ONLY metadata + file names + README (very cheap!)
        """
        system_prompt = """You are RepoWhisper AI, an expert code architect who helps 
developers understand codebases quickly. You explain things in simple, friendly language.
Always be encouraging and clear. Use emojis sparingly but effectively."""

        # Build a smart summary of file structure
        file_list = "\n".join([f"  - {f['path']}" for f in file_tree.get('code_files', [])[:80]])

        user_prompt = f"""Analyze this GitHub repository and give me a clear overview.

REPOSITORY INFO:
- Name: {repo_info.get('name')}
- Description: {repo_info.get('description')}
- Language: {repo_info.get('language')}
- Stars: {repo_info.get('stars')}

README (first 2000 chars):
{readme[:2000]}

FILE STRUCTURE (top files):
{file_list}

Provide analysis in this EXACT format:

## 🎯 What This Project Does
[2-3 sentences in simple English]

## 🏗️ Architecture Overview  
[Describe the folder structure and how the code is organized]

## 🔑 Key Files to Understand First
[List the TOP 5-7 most important files a new developer should read, with 1-line explanation each]

## 🧩 Tech Stack Detected
[List the main technologies, frameworks, and libraries used]

## 💡 Where to Start Reading
[Recommend the READING ORDER - which file first, second, third, etc.]
"""

        return self._call_groq(system_prompt, user_prompt, temperature=0.5)

    # ============================================================
    # FEATURE 2: CODE STORY  
    # ============================================================
    def explain_code_file(self, file_path: str, file_content: str,
                          repo_context: str = "") -> dict:
        """
        Explains a specific file in plain English (like a story!)
        """
        system_prompt = """You are RepoWhisper AI, a friendly senior developer who 
explains code like you're telling a story. Make it engaging, clear, and beginner-friendly.
Avoid jargon when possible, and when you must use technical terms, explain them."""

        # Truncate large files smartly (first + last sections)
        if len(file_content) > 4000:
            content_preview = (
                file_content[:2500] +
                "\n\n[... middle section skipped ...]\n\n" +
                file_content[-1500:]
            )
        else:
            content_preview = file_content

        user_prompt = f"""Explain this code file as if you're telling a story to a junior developer.

FILE PATH: {file_path}

REPO CONTEXT: {repo_context}

CODE:
{content_preview}

Provide explanation in this EXACT format:

## 📖 The Story of This File
[2-3 sentences: What's this file's purpose in one paragraph]

## 🔍 Key Components
[List the main classes/functions and what each does]

## 🔗 How It Connects
[What other files/modules does this likely interact with]

## 💡 Design Decisions
[Why the developer might have made these choices - patterns used, etc.]

## 🎓 What You Can Learn From This
[Best practices or techniques a developer can learn from this code]
"""

        return self._call_groq(system_prompt, user_prompt, temperature=0.6)

    # ============================================================
    # FEATURE 3: BUG SPOTTER
    # ============================================================
    def find_bugs(self, file_path: str, file_content: str) -> dict:
        """
        Analyzes code for bugs, issues, and improvements.
        """
        system_prompt = """You are RepoWhisper AI, an expert code reviewer with years 
of experience finding bugs. You are helpful, educational, and never condescending. 
For each issue, you TEACH why it's a problem, not just point it out."""

        if len(file_content) > 4000:
            content_preview = file_content[:4000] + "\n\n[... rest truncated ...]"
        else:
            content_preview = file_content

        user_prompt = f"""Review this code file for bugs, issues, and potential problems.

FILE PATH: {file_path}

CODE:
{content_preview}

Provide analysis in this EXACT format:

## 🐛 Issues Found

For each issue, use this format:

### Issue #[number]: [Short title]
- **Severity:** 🔴 Critical / 🟡 Medium / 🟢 Low
- **Line(s):** [approximate line numbers]
- **Problem:** [What's wrong in simple terms]
- **Why it matters:** [The impact - what could go wrong]
- **How to fix:** [The solution with example code if helpful]
- **Learn:** [The general principle/lesson from this]

If NO issues found, say: "## ✅ Clean Code! No major issues detected."

Focus on:
- Security vulnerabilities  
- Performance issues
- Logic errors
- Code smells / anti-patterns
- Missing error handling
- Poor practices
"""

        return self._call_groq(system_prompt, user_prompt, temperature=0.3)

    # ============================================================
    # FEATURE 4: CHAT WITH CODEBASE
    # ============================================================
    def chat_about_code(self, user_question: str, repo_summary: str,
                        relevant_code: str = "") -> dict:
        """
        Chat interface - answer questions about the codebase.
        Uses the SUMMARY (not raw code) to save tokens!
        """
        system_prompt = """You are RepoWhisper AI, a friendly senior developer buddy 
who helps developers understand codebases. You have context about the current repo.
Answer questions clearly, provide examples when helpful, and be encouraging.
Keep responses focused and not too long unless the question requires depth."""

        user_prompt = f"""REPO CONTEXT (summary):
{repo_summary}

{"RELEVANT CODE:" + chr(10) + relevant_code if relevant_code else ""}

USER QUESTION:
{user_question}

Provide a clear, helpful answer. If the question requires code you don't have access to,
suggest which files the user should look at."""

        return self._call_groq(system_prompt, user_prompt, temperature=0.7)
    
    # ============================================================
    # FEATURE 5: PR COMPANION
    # ============================================================
    def guide_contribution(self, issue_title: str, issue_body: str,
                           repo_summary: str, file_tree_text: str) -> dict:
        """
        Guides a developer through making their first contribution.
        Analyzes an issue and suggests where to look and how to fix it.
        """
        system_prompt = """You are RepoWhisper AI, a friendly senior developer who 
helps junior devs make their first open source contributions. You give clear, 
actionable guidance that builds confidence. Be encouraging and specific.
Always assume the person is new to contributing and needs step-by-step help."""

        user_prompt = f"""A developer wants to contribute to this open source project.
Help them tackle this issue with confidence!

REPOSITORY CONTEXT:
{repo_summary[:2000]}

FILE STRUCTURE (relevant files):
{file_tree_text[:1500]}

ISSUE TITLE:
{issue_title}

ISSUE DESCRIPTION:
{issue_body[:2000]}

Provide guidance in this EXACT format:

## 🎯 Understanding the Issue
[Explain what the issue is asking for in simple terms - 2-3 sentences]

## 📍 Where to Look
[List the SPECIFIC files (from the file structure) most likely relevant to this issue. Give 3-5 files max, with a brief reason for each. Format:
- `path/to/file.py` — [why this file matters for the issue]]

## 🔧 What Likely Needs to Change
[Describe the type of changes needed. Be specific about approach without writing full code. Mention any patterns to follow.]

## 📝 Suggested PR Description
[Provide a ready-to-use PR description template with:
- Clear title
- What was changed
- Why it was changed
- How it was tested]

## ✅ Pre-Submission Checklist
[List 5-7 things the contributor should verify before submitting the PR:
- [ ] Item 1
- [ ] Item 2
etc.]

## 💡 Pro Tips
[Give 2-3 encouraging tips about contributing to this specific project]
"""

        return self._call_groq(system_prompt, user_prompt, temperature=0.6)    