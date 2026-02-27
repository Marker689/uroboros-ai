"""
Evolution engine for Uroboros.
Handles iterative improvement and versioning.
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .agent import Agent
from .config import Config


class EvolutionEngine:
    """Engine for agent evolution and versioning."""

    def __init__(self, agent: Agent, config: Config):
        """Initialize the evolution engine."""
        self.agent = agent
        self.config = config
        self.logger = logging.getLogger(f"{agent.name}.evolution")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f"[{agent.name}.Evolution] %(message)s"))
        self.logger.addHandler(handler)

        # Project directories
        self.project_root = Path(os.path.dirname(__file__)).parent.parent
        self.agent_dir = self.project_root / "uroboros"
        self.evolution_dir = self.agent_dir / "evolution"
        self.evolution_dir.mkdir(parents=True, exist_ok=True)

        # State tracking
        self.evolution_log: List[Dict[str, Any]] = []
        self.current_version = "1.0.0"
        self.version_history: List[str] = []

    def create_version(self, version: Optional[str] = None) -> str:
        """Create a new version of the agent."""
        if version is None:
            version = self._increment_version(self.current_version)

        self.logger.info(f"Creating version {version}")

        # Backup current state
        backup_path = self._create_backup()

        # Save evolution log
        self._save_evolution_log()

        # Update version
        self.current_version = version
        self.version_history.append(version)

        # Create version tag
        self._create_git_tag(version)

        self.logger.info(f"Version {version} created successfully")
        return version

    def _increment_version(self, current_version: str) -> str:
        """Increment version number."""
        major, minor, patch = current_version.split(".")
        return f"{major}.{minor}.{int(patch) + 1}"

    def _create_backup(self) -> str:
        """Create a backup of the agent state."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.evolution_dir / f"backup_{timestamp}.json"

        state = {
            "version": self.current_version,
            "agent_name": self.agent.name,
            "iterations": self.agent.iterations,
            "memory_count": len(self.agent.memory),
            "skills_count": len(self.agent.skills),
            "timestamp": datetime.now().isoformat(),
        }

        with open(backup_file, "w") as f:
            json.dump(state, f, indent=2)

        return str(backup_file)

    def _save_evolution_log(self) -> None:
        """Save evolution log to file."""
        log_file = self.evolution_dir / "evolution_log.json"
        with open(log_file, "w") as f:
            json.dump(self.evolution_log, f, indent=2, default=str)

    def _create_git_tag(self, version: str) -> bool:
        """Create a git tag for the version."""
        try:
            subprocess.run(
                ["git", "tag", f"v{version}"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            self.logger.info(f"Git tag v{version} created")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create git tag: {e}")
            return False

    def commit_evolution(self, message: str) -> bool:
        """Commit evolution changes to git."""
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"[Evolution] {message}"],
                cwd=self.project_root,
                capture_output=True,
                check=True,
            )
            self.logger.info(f"Evolution committed: {message}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to commit evolution: {e}")
            return False

    def log_evolution(self, event_type: str, description: str) -> None:
        """Log an evolution event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "description": description,
            "version": self.current_version,
        }
        self.evolution_log.append(event)
        self.logger.info(f"[{event_type}] {description}")

    def get_evolution_summary(self) -> Dict[str, Any]:
        """Get summary of evolution history."""
        return {
            "current_version": self.current_version,
            "version_history": self.version_history,
            "evolution_count": len(self.evolution_log),
            "last_evolution": self.evolution_log[-1] if self.evolution_log else None,
        }

    def evolve(self, improvement_plan: Optional[List[str]] = None) -> bool:
        """Execute evolution cycle."""
        self.logger.info("Starting evolution cycle...")

        # Log evolution start
        self.log_evolution("evolution_start", "Evolution cycle initiated")

        # Apply improvements
        if improvement_plan:
            for improvement in improvement_plan:
                self.log_evolution("improvement", improvement)
                # Here you would integrate with the self-modification engine

        # Create new version
        new_version = self.create_version()
        self.log_evolution("version_created", f"Version {new_version} created")

        # Commit changes
        self.commit_evolution(f"Evolution to version {new_version}")

        self.logger.info("Evolution cycle complete")
        return True

    def check_evolution_conditions(self) -> bool:
        """Check if evolution conditions are met."""
        # Check iteration count
        if self.agent.iterations >= self.config.max_iterations:
            return True

        # Check time since last evolution
        time_since_last = (datetime.now() - self.agent.last_update).total_seconds()
        if time_since_last >= self.config.evolution_interval:
            return True

        return False
