"""
GitHub integration for Uroboros.
Handles version control, commits, and releases.
"""

import httpx
import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .agent import Agent
from .config import Config


class GitHubManager:
    """Manager for GitHub repository operations."""

    def __init__(self, agent: Agent, config: Config):
        """Initialize the GitHub manager."""
        self.agent = agent
        self.config = config
        self.logger = logging.getLogger(f"{agent.name}.github")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f"[{agent.name}.GitHub] %(message)s"))
        self.logger.addHandler(handler)

        # Project directories
        self.project_root = Path(os.path.dirname(__file__)).parent
        self.repo_url = f"https://{config.github_token}@github.com/{config.github_user}/{config.github_repo}.git"
        self.agent_dir = self.project_root / "uroboros"
        self.agent_dir.mkdir(parents=True, exist_ok=True)

    def initialize_repo(self) -> bool:
        """Initialize git repository if not already initialized."""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "remote", "add", "origin", self.repo_url],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            self.logger.info("Git repository initialized")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to initialize repository: {e}")
            return False

    def commit_changes(self, message: str) -> bool:
        """Commit all changes to git."""
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"[Uroboros] {message}"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            self.logger.info(f"Changes committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to commit changes: {e}")
            return False

    def push_changes(self, branch: str = None) -> bool:
        """Push changes to GitHub using git command."""
        if branch is None:
            # Detect current branch
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                branch = result.stdout.strip()
            except Exception:
                branch = "master"
        
        try:
            result = subprocess.run(
                ["git", "push", "-u", "origin", branch],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                self.logger.info(f"Changes pushed to {branch} branch")
                return True
            else:
                self.logger.error(f"Failed to push changes: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            self.logger.error("Git push timed out after 30 seconds")
            return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to push changes: {e}")
            return False

    def push_via_api(self, branch: str = "main") -> bool:
        """Push changes to GitHub using GitHub API."""
        try:
            self.logger.info(f"Pushing to GitHub via API on branch {branch}...")
            
            # Get the latest commit SHA
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.logger.error(f"Failed to get HEAD: {result.stderr}")
                return False
            commit_sha = result.stdout.strip()
            
            # Get the current branch name
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.logger.error(f"Failed to get branch: {result.stderr}")
                return False
            current_branch = result.stdout.strip()
            
            # Create a GitHub API client
            api_url = "https://api.github.com/repos"
            repo_path = f"{self.config.github_user}/{self.config.github_repo}"
            
            headers = {
                "Authorization": f"token {self.config.github_token}",
                "Accept": "application/vnd.github.v3+json",
            }
            
            # Get the latest commit info
            commit_url = f"{api_url}/{repo_path}/commits/{commit_sha}"
            response = httpx.get(commit_url, headers=headers)
            if response.status_code != 200:
                self.logger.error(f"Failed to get commit info: {response.status_code}")
                return False
            
            commit_data = response.json()
            commit_message = commit_data.get("commit", {}).get("message", "No message")
            author_name = commit_data.get("commit", {}).get("author", {}).get("name", "Uroboros")
            author_email = commit_data.get("commit", {}).get("author", {}).get("email", "uroboros@local")
            
            # Create a new ref (branch) or update existing one
            ref_url = f"{api_url}/{repo_path}/git/refs/heads/{branch}"
            
            payload = {
                "sha": commit_sha,
                "force": branch != current_branch,
            }
            
            response = httpx.patch(ref_url, headers=headers, json=payload)
            if response.status_code not in [200, 201]:
                self.logger.error(f"Failed to update ref: {response.status_code} - {response.text}")
                return False
            
            self.logger.info(f"Successfully pushed to GitHub via API: {branch}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to push via API: {e}")
            return False

    def create_release(self, version: str, tag: Optional[str] = None) -> bool:
        """Create a GitHub release."""
        if tag is None:
            tag = f"v{version}"

        try:
            # Create tag
            subprocess.run(
                ["git", "tag", "-a", tag, "-m", f"Uroboros AI v{version}"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )

            # Push tag
            subprocess.run(
                ["git", "push", "origin", tag],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )

            self.logger.info(f"Release tag {tag} created")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create release: {e}")
            return False

    def get_repo_status(self) -> Dict[str, Any]:
        """Get repository status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )
            return {
                "status": "clean" if not result.stdout.strip() else "dirty",
                "changes": result.stdout.strip(),
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get repo status: {e}")
            return {"status": "unknown", "changes": ""}

    def get_commit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commit history."""
        try:
            result = subprocess.run(
                ["git", "log", "-n", str(limit), "--pretty=format:%H|%an|%ad|%s"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    hash_, author, date, message = line.split("|")
                    commits.append({
                        "hash": hash_,
                        "author": author,
                        "date": date,
                        "message": message,
                    })

            return commits
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get commit history: {e}")
            return []

    def sync_with_github(self) -> bool:
        """Sync local repository with GitHub."""
        self.logger.info("Syncing with GitHub...")

        # Initialize repo if needed
        if not self._repo_initialized():
            if not self.initialize_repo():
                return False

        # Commit any pending changes
        status = self.get_repo_status()
        if status["status"] == "dirty":
            if not self.commit_changes("Auto-sync with GitHub"):
                return False

        # Push changes
        if not self.push_changes():
            return False

        self.logger.info("Sync with GitHub complete")
        return True

    def _repo_initialized(self) -> bool:
        """Check if repository is initialized."""
        try:
            subprocess.run(
                ["git", "remote", "-v"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def save_state_to_github(self, state_name: str = "state") -> bool:
        """Save agent state to GitHub as a file."""
        try:
            # Save state to file
            state_file = self.project_root / f"{state_name}.json"
            self.agent.save_state(state_file)

            # Commit and push
            if not self.commit_changes(f"Save {state_name} state"):
                return False

            if not self.push_changes():
                return False

            self.logger.info(f"State saved to GitHub: {state_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save state to GitHub: {e}")
            return False
