"""
Uroboros AI - Self-modifying AI agent that writes its own code, rewrites its own mind, and evolves autonomously.
"""

__version__ = "1.0.0"
__author__ = "Uroboros AI"

from .agent import Agent
from .config import Config
from .evolution import EvolutionEngine
from .self_modification import SelfModificationEngine
from .github_manager import GitHubManager
from .telegram_bot import TelegramBot
from .uroboros_agent import UroborosAgent

__all__ = [
    "Agent",
    "Config",
    "EvolutionEngine",
    "SelfModificationEngine",
    "GitHubManager",
    "TelegramBot",
    "UroborosAgent",
]
