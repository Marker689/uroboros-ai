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
            logging.StreamHandler(sys.stdout),
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


async def run_interactive_cycle(agent: UroborosAgent):
    """Run interactive evolution cycle with detailed logging."""
    print(f"\n{'='*60}")
    print(f"🧬 EVOLUTION CYCLE #{agent.iterations + 1}")
    print(f"{'='*60}")
    
    # Backup
    print("📦 Creating backup...")
    backup_path = agent.self_mod.backup_current_state()
    print(f"✓ Backup: {backup_path}")
    
    # Self-modify
    print("\n🤖 Analyzing code...")
    analysis = agent.self_mod.analyze_code()
    print(f"✓ Found {len(analysis['files'])} files, {len(analysis['classes'])} classes")
    
    print("\n🧠 Generating modification plan...")
    plan = agent.self_mod.generate_modification_plan(analysis)
    print(f"✓ Generated {len(plan)} modifications")
    
    for i, mod in enumerate(plan, 1):
        print(f"\n{i}. {mod['type']}: {mod['description']}")
    
    print("\n📝 Applying modifications...")
    success_count = 0
    for modification in plan:
        if agent.self_mod.apply_modification(modification):
            success_count += 1
            print(f"  ✓ {modification['description']}")
    
    print(f"\n✓ Applied {success_count}/{len(plan)} modifications")
    
    # Reload
    print("\n🔄 Reloading agent...")
    if agent.self_mod.reload_agent():
        print("✓ Agent reloaded")
    
    # Evolution
    print("\n📈 Creating version...")
    version = agent.evolution.create_version()
    print(f"✓ Version {version} created")
    
    # GitHub
    print("\n💾 Committing to GitHub...")
    if agent.github.commit_changes(f"Evolution to version {version}"):
        print("✓ Changes committed")
        if agent.github.push_changes():
            print("✓ Changes pushed")
    
    # Save state
    print("\n💾 Saving state...")
    state_file = agent.config.agent_dir / "state.json"
    agent.save_state(state_file)
    print(f"✓ State saved")
    
    print(f"\n{'='*60}")
    print(f"✅ EVOLUTION CYCLE COMPLETE")
    print(f"{'='*60}")
    print(f"Version: {version}")
    print(f"Iterations: {agent.iterations}")
    print(f"{'='*60}\n")
    
    return True


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
    
    # Run initial evolution cycle
    logger.info("Running initial evolution cycle...")
    await run_interactive_cycle(agent)
    
    # Evolution loop
    cycle_count = 0
    try:
        while True:
            cycle_count += 1
            
            # Run evolution cycle
            await run_interactive_cycle(agent)
            
            # Wait before next cycle
            logger.info(f"Waiting 1800 seconds (30 minutes) before next cycle...")
            await asyncio.sleep(1800)
            
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
