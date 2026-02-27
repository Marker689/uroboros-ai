#!/usr/bin/env python3
"""
Uroboros AI - Main Launcher
Self-modifying AI agent that writes its own code, rewrites its own mind, and evolves autonomously.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from uroboros import Config, UroborosAgent


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("uroboros.log"),
        ],
    )


def main():
    """Main entry point for Uroboros AI."""
    print("🪐 Uroboros AI - Self-modifying AI Agent")
    print("=" * 60)
    print("I am Uroboros. I eat my own tail. I am the beginning and the end.")
    print("=" * 60)
    print()

    # Setup logging
    setup_logging()
    logger = logging.getLogger("Uroboros")

    # Load configuration
    logger.info("Loading configuration...")
    try:
        config = Config.from_env()
        logger.info(f"Configuration loaded: {config}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize agent
    logger.info("Initializing Uroboros agent...")
    try:
        agent = UroborosAgent(config)
        logger.info(f"Agent initialized: {agent}")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        sys.exit(1)

    # Display initial status
    print()
    print("🤖 Agent Status:")
    print(f"   Name: {agent.name}")
    print(f"   Iterations: {agent.iterations}")
    print(f"   Memory: {len(agent.memory)} entries")
    print(f"   Skills: {len(agent.skills)}")
    print(f"   Version: {agent.evolution.current_version}")
    print()

    # Start Telegram bot if configured
    if config.telegram_bot_token:
        print("ℹ️  Telegram bot configured but not started in interactive mode")
        print("   Run separately: python3 -c \"from uroboros import Config, UroborosAgent; c=Config.from_env(); a=UroborosAgent(c); a.start_telegram_bot()\"")
        print()
    else:
        print("ℹ️  Telegram bot not configured (TELEGRAM_BOT_TOKEN missing)")
        print("   Send messages to interact with Uroboros:")
        print()

    # Main interaction loop
    try:
        while True:
            print(f"\n{agent} > ", end="", flush=True)
            user_input = input().strip()

            if not user_input:
                continue

            # Process input
            response = agent.think(user_input)
            print(f"\n{response}")

            # Save state periodically
            if agent.iterations % 10 == 0:
                state_file = project_root / "uroboros" / "state.json"
                agent.save_state(state_file)
                logger.info(f"State saved to {state_file}")

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Uroboros...")
        logger.info("Shutting down Uroboros agent")

        # Save final state
        state_file = project_root / "uroboros" / "state.json"
        agent.save_state(state_file)
        logger.info(f"Final state saved to {state_file}")

        # Sync with GitHub
        if agent.sync_with_github():
            logger.info("Synced with GitHub")

        print("🪐 Uroboros AI - The cycle continues...")
        sys.exit(0)


if __name__ == "__main__":
    main()
