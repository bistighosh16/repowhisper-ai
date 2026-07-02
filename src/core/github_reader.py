"""
GitHub Reader Module - RepoWhisper AI
Handles all interactions with GitHub API

Made with 💜 by Vivi
"""

import os
import re
from typing import Optional
from github import Github, GithubException
from dotenv import load_dotenv

# Load our environment variables (.env file)
load_dotenv()


class GitHubReader:
    """Handles reading and parsing GitHub repositories."""

    # Files/folders we ALWAYS ignore (useless for understanding code!)
    IGNORED_PATTERNS = [
        'node_modules', '__pycache__', '.git', 'venv', 'env',
        '.venv', 'dist', 'build', '.next', '.nuxt', 'target',
        '.pytest_cache', '.mypy_cache', '.tox', 'coverage',
        '.DS_Store', 'Thumbs.db', '.idea', '.vscode',
    ]

    # File extensions we CARE about (actual code files!)
    CODE_EXTENSIONS = [
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp',
        '.c', '.cs', '.go', '.rs', '.rb', '.php', '.swift',
        '.kt', '.scala', '.r', '.sh', '.sql', '.html', '.css',
        '.vue', '.svelte', '.yaml', '.yml', '.json', '.toml',
        '.md', '.txt',
    ]

    def __init__(self):
        """Initialize with GitHub token from .env file."""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError(
                "GitHub token not found! Please add GITHUB_TOKEN to .env file"
            )
        self.github = Github(token)

    def parse_repo_url(self, url: str) -> Optional[tuple]:
        """
        Extract owner and repo name from a GitHub URL.
        
        Examples:
          https://github.com/tiangolo/fastapi -> ('tiangolo', 'fastapi')
          github.com/streamlit/streamlit -> ('streamlit', 'streamlit')
        """
        # Pattern to match GitHub URLs (with or without https://)
        pattern = r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\s]+?)(?:\.git)?/?$"
        match = re.match(pattern, url.strip())

        if match:
            owner = match.group(1)
            repo = match.group(2)
            return (owner, repo)
        return None

    def get_repo_info(self, url: str) -> dict:
        """
        Get basic information about a repository.
        Returns metadata like stars, language, description, etc.
        """
        parsed = self.parse_repo_url(url)
        if not parsed:
            return {"error": "Invalid GitHub URL format"}

        owner, repo_name = parsed

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")

            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description or "No description available",
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language or "Not specified",
                "size_kb": repo.size,
                "created_at": repo.created_at.strftime("%Y-%m-%d"),
                "updated_at": repo.updated_at.strftime("%Y-%m-%d"),
                "url": repo.html_url,
                "owner": owner,
                "repo_name": repo_name,
            }
        except GithubException as e:
            return {"error": f"GitHub API Error: {e.data.get('message', str(e))}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def get_readme(self, url: str) -> str:
        """Fetch the README file content of the repository."""
        parsed = self.parse_repo_url(url)
        if not parsed:
            return "Invalid repository URL"

        owner, repo_name = parsed

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            readme = repo.get_readme()
            return readme.decoded_content.decode('utf-8')
        except GithubException:
            return "No README found in this repository"
        except Exception as e:
            return f"Error fetching README: {str(e)}"

    def should_ignore(self, path: str) -> bool:
        """Check if a file/folder should be ignored."""
        path_lower = path.lower()
        for pattern in self.IGNORED_PATTERNS:
            if pattern in path_lower:
                return True
        return False

    def is_code_file(self, path: str) -> bool:
        """Check if file is a code file we care about."""
        for ext in self.CODE_EXTENSIONS:
            if path.lower().endswith(ext):
                return True
        return False

    def get_file_tree(self, url: str, max_files: int = 200) -> dict:
        """
        Get the complete file tree of the repository.
        Returns a filtered list of important files.
        """
        parsed = self.parse_repo_url(url)
        if not parsed:
            return {"error": "Invalid repository URL"}

        owner, repo_name = parsed

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")

            # Get the entire tree recursively
            tree = repo.get_git_tree(repo.default_branch, recursive=True)

            all_files = []
            code_files = []

            for item in tree.tree:
                if item.type == "blob":  # It's a file (not folder)
                    path = item.path

                    # Skip ignored patterns
                    if self.should_ignore(path):
                        continue

                    all_files.append({
                        "path": path,
                        "size": item.size or 0,
                    })

                    if self.is_code_file(path):
                        code_files.append({
                            "path": path,
                            "size": item.size or 0,
                        })

                    # Safety limit
                    if len(all_files) >= max_files:
                        break

            return {
                "total_files": len(all_files),
                "code_files_count": len(code_files),
                "all_files": all_files,
                "code_files": code_files,
                "truncated": len(all_files) >= max_files,
            }

        except GithubException as e:
            return {"error": f"GitHub API Error: {e.data.get('message', str(e))}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def get_file_content(self, url: str, file_path: str) -> str:
        """
        Fetch content of a specific file from the repository.
        """
        parsed = self.parse_repo_url(url)
        if not parsed:
            return "Invalid repository URL"

        owner, repo_name = parsed

        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            file_content = repo.get_contents(file_path)

            # Decode the content (GitHub returns it base64 encoded)
            if file_content.size > 1000000:  # 1MB safety limit
                return "File too large to read (>1MB)"

            return file_content.decoded_content.decode('utf-8')

        except GithubException as e:
            return f"Error: {e.data.get('message', str(e))}"
        except UnicodeDecodeError:
            return "Binary file - cannot display as text"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    def get_issue(self, issue_url: str) -> dict:
        """
        Fetch a GitHub issue by its URL.
        Example URL: https://github.com/owner/repo/issues/123
        """
        import re
        
        # Parse issue URL
        pattern = r"github\.com/([^/]+)/([^/]+)/issues/(\d+)"
        match = re.search(pattern, issue_url.strip())
        
        if not match:
            return {"error": "Invalid GitHub issue URL. Format: https://github.com/owner/repo/issues/NUMBER"}
        
        owner = match.group(1)
        repo_name = match.group(2)
        issue_number = int(match.group(3))
        
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            issue = repo.get_issue(number=issue_number)
            
            return {
                "success": True,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "No description provided",
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "author": issue.user.login,
                "created_at": issue.created_at.strftime("%Y-%m-%d"),
                "comments_count": issue.comments,
                "url": issue.html_url,
                "repo_owner": owner,
                "repo_name": repo_name,
            }
        
        except GithubException as e:
            return {"error": f"GitHub API Error: {e.data.get('message', str(e))}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}            