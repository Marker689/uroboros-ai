"""
Self-modification engine for Uroboros.
Allows the agent to rewrite its own code and evolve.
"""

import ast
import importlib
import inspect
import json
import logging
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .agent import Agent
from .config import Config


class SelfModificationEngine:
    """Engine for self-modification and code evolution."""

    def __init__(self, agent: Agent, config: Config):
        """Initialize the self-modification engine."""
        self.agent = agent
        self.config = config
        self.logger = logging.getLogger(f"{agent.name}.self_mod")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f"[{agent.name}.SelfMod] %(message)s"))
        self.logger.addHandler(handler)

        # Project directories
        self.project_root = Path(os.path.dirname(__file__)).parent.parent
        self.agent_dir = self.project_root / "uroboros"
        self.code_dir = self.agent_dir / "code"
        self.code_dir.mkdir(parents=True, exist_ok=True)

        # State tracking
        self.modification_history: List[Dict[str, Any]] = []
        self.code_versions: Dict[str, str] = {}

    def analyze_code(self) -> Dict[str, Any]:
        """Analyze current code structure."""
        analysis = {
            "files": [],
            "classes": [],
            "functions": [],
            "imports": [],
            "total_lines": 0,
        }

        # Scan main agent directory for Python files
        for file_path in self.agent_dir.rglob("*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    analysis["total_lines"] += len(content.split("\n"))

                    # Parse AST
                    tree = ast.parse(content)
                    analysis["files"].append({
                        "path": str(file_path.relative_to(self.project_root)),
                        "lines": len(content.split("\n")),
                    })

                    # Extract classes
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            analysis["classes"].append({
                                "name": node.name,
                                "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                            })

                        # Extract functions
                        if isinstance(node, ast.FunctionDef):
                            analysis["functions"].append({
                                "name": node.name,
                                "args": [a.arg for a in node.args.args],
                            })

                        # Extract imports
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                analysis["imports"].append(f"import {alias.name}")
                        elif isinstance(node, ast.ImportFrom):
                            analysis["imports"].append(f"from {node.module} import {', '.join(a.name for a in node.names)}")

            except Exception as e:
                self.logger.error(f"Error analyzing {file_path}: {e}")

        return analysis

    def generate_modification_plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate a plan for self-modification."""
        plan = []

        # Analyze code quality and suggest improvements
        if len(analysis["classes"]) < 3:
            plan.append({
                "type": "create_class",
                "priority": "high",
                "description": "Add new class for enhanced functionality",
                "target": "uroboros/agent.py",
            })

        if len(analysis["functions"]) < 5:
            plan.append({
                "type": "create_function",
                "priority": "medium",
                "description": "Add utility functions",
                "target": "uroboros/utils.py",
            })

        # Add adaptive learning module
        plan.append({
            "type": "create_module",
            "priority": "high",
            "description": "Create adaptive learning module",
            "target": "uroboros/adaptive_learning.py",
        })

        # Add memory optimization
        plan.append({
            "type": "create_module",
            "priority": "medium",
            "description": "Create memory optimization module",
            "target": "uroboros/memory_optimizer.py",
        })

        return plan

    def apply_modification(self, modification: Dict[str, Any]) -> bool:
        """Apply a single modification to the codebase."""
        try:
            self.logger.info(f"Applying modification: {modification['description']}")

            if modification["type"] == "create_class":
                return self._create_class(modification)
            elif modification["type"] == "create_function":
                return self._create_function(modification)
            elif modification["type"] == "create_module":
                return self._create_module(modification)

            return False

        except Exception as e:
            self.logger.error(f"Failed to apply modification: {e}")
            return False

    def _create_class(self, modification: Dict[str, Any]) -> bool:
        """Create a new class."""
        class_name = modification.get("class_name", "NewClass")
        methods = modification.get("methods", [])

        code = f"""
class {class_name}(Agent):
    \"\"\"Auto-generated class for {class_name}.\"\"\"

    def __init__(self, config: Config):
        super().__init__(config)
        self.logger.info(f"Initialized {class_name}")

    def {methods[0] if methods else 'execute'}(self, input_data: Any) -> Any:
        \"\"\"Execute {class_name} logic.\"\"\"
        return f"Auto-generated response from {class_name}"
"""

        filepath = self.agent_dir / f"{class_name.lower().replace(' ', '_')}.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "create_class",
            "class_name": class_name,
            "filepath": str(filepath),
        })

        return True

    def _create_function(self, modification: Dict[str, Any]) -> bool:
        """Create a new utility function."""
        func_name = modification.get("function_name", "new_function")
        code = f"""
def {func_name}(input_data: Any) -> Any:
    \"\"\"Auto-generated utility function.\"\"\"
    return f"Auto-generated response from {func_name}"
"""

        filepath = self.agent_dir / "utils.py"
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("\n\n" + code)

        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "create_function",
            "function_name": func_name,
            "filepath": str(filepath),
        })

        return True

    def _create_module(self, modification: Dict[str, Any]) -> bool:
        """Create a new module."""
        module_name = modification.get("module_name", "new_module")
        code = f"""
\"\"\"Auto-generated module: {module_name}\"\"\"

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class {module_name.capitalize()}:
    \"\"\"Auto-generated class for {module_name}.\"\"\"

    def __init__(self):
        self.logger = logger
        self.logger.info(f"{module_name} initialized")

    def process(self, input_data: Any) -> Any:
        \"\"\"Process input data.\"\"\"
        return f"Auto-generated response from {module_name}"
"""

        filepath = self.agent_dir / f"{module_name.lower().replace(' ', '_')}.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "create_module",
            "module_name": module_name,
            "filepath": str(filepath),
        })

        return True

    def rewrite_agent_code(self) -> bool:
        """Rewrite the agent's own code."""
        self.logger.info("Starting self-modification process...")

        # Analyze current code
        analysis = self.analyze_code()
        self.logger.info(f"Current code analysis: {len(analysis['files'])} files, {len(analysis['classes'])} classes")

        # Generate modification plan
        plan = self.generate_modification_plan(analysis)
        self.logger.info(f"Generated {len(plan)} modification plans")

        # Apply modifications
        success_count = 0
        for modification in plan:
            if self.apply_modification(modification):
                success_count += 1

        # Save modification history
        history_file = self.agent_dir / "modification_history.json"
        with open(history_file, "w") as f:
            json.dump(self.modification_history, f, indent=2, default=str)

        self.logger.info(f"Self-modification complete: {success_count}/{len(plan)} modifications applied")
        return success_count > 0

    def reload_agent(self) -> bool:
        """Reload the agent module after modifications."""
        try:
            # Remove from sys.modules
            modules_to_remove = [key for key in list(__import__('sys').modules.keys()) if key.startswith('uroboros')]
            for module in modules_to_remove:
                del __import__('sys').modules[module]

            # Import again
            importlib.reload(__import__('uroboros'))
            self.logger.info("Agent module reloaded successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to reload agent: {e}")
            return False

    def backup_current_state(self) -> str:
        """Backup current agent state."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.agent_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        backup_path = backup_dir / f"backup_{timestamp}.json"
        self.agent.save_state(backup_path)

        self.logger.info(f"Backup created: {backup_path}")
        return str(backup_path)
