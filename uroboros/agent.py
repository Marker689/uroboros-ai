"""
Base AI Agent class for Uroboros.
"""

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from .config import Config


class Agent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, config: Config):
        """Initialize the agent with configuration."""
        self.config = config
        self.name = config.agent_name
        self.memory: List[Dict[str, Any]] = []
        self.skills: Dict[str, Any] = {}
        self.iterations = 0
        self.creation_time = datetime.now()
        self.last_update = datetime.now()
        self.logs: List[str] = []

        # Setup logging
        self.logger = logging.getLogger(f"{self.name}")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f"[{self.name}] %(message)s"))
        self.logger.addHandler(handler)

    @abstractmethod
    def think(self, input_data: Any) -> Any:
        """Process input and generate output."""
        pass

    @abstractmethod
    def learn(self, experience: Any) -> None:
        """Learn from experience."""
        pass

    def save_state(self, filepath: str) -> None:
        """Save agent state to file."""
        state = {
            "name": self.name,
            "memory": self.memory,
            "skills": self.skills,
            "iterations": self.iterations,
            "creation_time": self.creation_time.isoformat(),
            "last_update": self.last_update.isoformat(),
            "logs": self.logs[-100:],  # Keep last 100 logs
        }
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2, default=str)

    def load_state(self, filepath: str) -> None:
        """Load agent state from file."""
        with open(filepath, "r") as f:
            state = json.load(f)
        self.name = state.get("name", self.name)
        self.memory = state.get("memory", [])
        self.skills = state.get("skills", {})
        self.iterations = state.get("iterations", 0)
        self.creation_time = datetime.fromisoformat(state["creation_time"])
        self.last_update = datetime.fromisoformat(state["last_update"])
        self.logs = state.get("logs", [])

    def log(self, message: str) -> None:
        """Add a log entry."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        self.logger.info(message)

    def evolve(self) -> None:
        """Trigger evolution process."""
        self.log(f"Evolution triggered at iteration {self.iterations}")
        self.iterations += 1
        self.last_update = datetime.now()

    def __str__(self) -> str:
        """Return agent status."""
        return (
            f"{self.name}(iterations={self.iterations}, "
            f"memory_size={len(self.memory)}, "
            f"skills={len(self.skills)})"
        )
