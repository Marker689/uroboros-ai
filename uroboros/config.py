"""
Configuration module for Uroboros AI agent.
Loads settings from .env file.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for Uroboros AI agent."""

    # Required fields (no defaults)
    local_llm_base_url: str
    local_llm_api_key: str
    telegram_bot_token: str
    github_user: str
    github_repo: str
    github_token: str

    # Optional fields (with defaults)
    local_llm_model: str = "unsloth-GLM-4.7-Flash-GGUF-UD-Q4_K_XL"
    telegram_chat_id: Optional[str] = None
    agent_name: str = "Uroboros"
    evolution_interval: int = 3600  # seconds
    self_modification_interval: int = 1800  # seconds
    max_iterations: int = 1000

    @property
    def agent_dir(self) -> Path:
        """Get agent directory path."""
        return Path(__file__).parent.parent

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from .env file."""
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")

        # Load environment variables
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    os.environ[key] = value

        return cls(
            local_llm_base_url=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:3000/api"),
            local_llm_api_key=os.getenv("LOCAL_LLM_API_KEY", ""),
            local_llm_model=os.getenv("uroboros-ai-model", "unsloth-GLM-4.7-Flash-GGUF-UD-Q4_K_XL"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            github_user=os.getenv("GITHUB_USER", ""),
            github_repo=os.getenv("GITHUB_REPO", ""),
            github_token=os.getenv("GITHUB_TOKEN", ""),
            agent_name=os.getenv("AGENT_NAME", "Uroboros"),
            evolution_interval=int(os.getenv("EVOLUTION_INTERVAL", "3600")),
            self_modification_interval=int(os.getenv("SELF_MODIFICATION_INTERVAL", "1800")),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "1000")),
        )

    def __str__(self) -> str:
        """Return configuration as string (masked sensitive data)."""
        return (
            f"Config(agent_name={self.agent_name}, "
            f"local_llm_base_url={self.local_llm_base_url}, "
            f"github_repo={self.github_user}/{self.github_repo})"
        )