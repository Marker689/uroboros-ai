#!/usr/bin/env python3
"""
Autonomous Uroboros Agent - Runs evolution cycles continuously.
"""

import asyncio
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
            logging.FileHandler("uroboros_autonomous.log"),
        ],
    )


async def run_evolution_cycle(agent: UroborosAgent):
    """Run a single evolution cycle."""
    print(f"\n{'='*60}")
    print(f"🧬 EVOLUTION CYCLE #{agent.iterations + 1}")
    print(f"{'='*60}")
    
    # Run evolution
    success = agent.run_evolution_cycle()
    
    if success:
        print(f"✅ Evolution cycle complete")
        print(f"   Version: {agent.evolution.current_version}")
        print(f"   Iterations: {agent.iterations}")
    else:
        print(f"❌ Evolution cycle failed")
    
    return success


async def main():
    """Main autonomous agent loop."""
    setup_logging()
    logger = logging.getLogger("UroborosAutonomous")
    
    print("🪐 UROBOROS AUTONOMOUS AGENT")
    print("=" * 60)
    print("I am Uroboros. I eat my own tail. I am the beginning and the end.")
    print("I run autonomously, evolving continuously.")
    print("=" * 60)
    
    # Load configuration
    logger.info("Loading configuration...")
    try:
        config = Config.from_env()
        logger.info(f"Configuration loaded")
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
    
    # Evolution loop
    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            
            # Run evolution cycle
            await run_evolution_cycle(agent)
            
            # Wait before next cycle
            logger.info(f"Waiting {config.evolution_interval} seconds before next cycle...")
            await asyncio.sleep(config.evolution_interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Uroboros...")
        logger.info("Shutting down autonomous agent")
        
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
    asyncio.run(main())
