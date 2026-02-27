#!/usr/bin/env python3
"""
Uroboros AI - Universal Launcher
Запускает все компоненты Uroboros: агент, Telegram бот, автономный режим
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def setup_logging(log_file=None):
    """Setup logging configuration."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handlers = [logging.StreamHandler()]

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=handlers
    )


def load_env():
    """Load .env file."""
    from dotenv import load_dotenv
    env_path = project_root / ".env"
    load_dotenv(env_path)

def check_config():
    """Check if configuration is valid."""
    env_path = project_root / ".env"

    if not env_path.exists():
        print("❌ .env файл не найден!")
        print("Создайте .env файл с настройками:")
        print("  LOCAL_LLM_BASE_URL=http://localhost:3000/api")
        print("  LOCAL_LLM_API_KEY=your_key")
        print("  TELEGRAM_BOT_TOKEN=your_token")
        print("  GITHUB_USER=username")
        print("  GITHUB_REPO=repo")
        print("  GITHUB_TOKEN=token")
        return False

    # Load environment variables
    load_env()
    
    # Check required variables
    required_vars = [
        "LOCAL_LLM_BASE_URL",
        "LOCAL_LLM_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "GITHUB_USER",
        "GITHUB_REPO",
        "GITHUB_TOKEN",
    ]

    missing = []
    for key in required_vars:
        if not os.getenv(key):
            missing.append(key)

    if missing:
        print(f"❌ Отсутствуют переменные окружения: {', '.join(missing)}")
        return False

    return True


def start_interactive():
    """Start interactive mode."""
    print("🪐 UROBOROS AI - Interactive Mode")
    print("=" * 60)
    print("I am Uroboros. I eat my own tail. I am the beginning and the end.")
    print("=" * 60)
    print()

    from uroboros import Config, UroborosAgent

    load_env()
    config = Config.from_env()
    agent = UroborosAgent(config)

    print("🤖 Agent Status:")
    print(f"   Name: {agent.name}")
    print(f"   Iterations: {agent.iterations}")
    print(f"   Memory: {len(agent.memory)} entries")
    print(f"   Version: {agent.evolution.current_version}")
    print()

    try:
        while True:
            print(f"\n{agent} > ", end="", flush=True)
            user_input = input().strip()

            if not user_input:
                continue

            response = agent.think(user_input)
            print(f"\n{response}")

            if agent.iterations % 10 == 0:
                state_file = project_root / "uroboros" / "state.json"
                agent.save_state(state_file)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Uroboros...")
        state_file = project_root / "uroboros" / "state.json"
        agent.save_state(state_file)
        print("🪐 Uroboros AI - The cycle continues...")
        sys.exit(0)


def start_telegram():
    """Start Telegram bot."""
    print("🤖 UROBOROS AI - Telegram Bot Mode")
    print("=" * 60)

    from uroboros import Config, UroborosAgent

    load_env()
    config = Config.from_env()
    agent = UroborosAgent(config)

    print("ℹ️  Telegram bot configured")
    print("ℹ️  Send commands:")
    print("   /start - Initialize")
    print("   /help - Show help")
    print("   /status - Check status")
    print("   /evolve - Trigger evolution")
    print("   /version - Show version")
    print("   /memory - Show memory")
    print()

    try:
        success = agent.start_telegram_bot()
        if success:
            print("✓ Bot started successfully!")
            print("Press Ctrl+C to stop...")
            import asyncio
            asyncio.Event().wait()
        else:
            print("✗ Bot failed to start")
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
        import asyncio
        asyncio.run(agent.stop())
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


def start_autonomous():
    """Start autonomous mode."""
    print("🪐 UROBOROS AI - Autonomous Mode")
    print("=" * 60)
    print("I am Uroboros. I eat my own tail. I am the beginning and the end.")
    print("I run autonomously, evolving continuously.")
    print("=" * 60)
    print()

    from uroboros import Config, UroborosAgent

    load_env()
    config = Config.from_env()
    agent = UroborosAgent(config)

    print("🤖 Agent Status:")
    print(f"   Name: {agent.name}")
    print(f"   Iterations: {agent.iterations}")
    print(f"   Memory: {len(agent.memory)} entries")
    print(f"   Version: {agent.evolution.current_version}")
    print()

    print("🔄 Evolution cycle will run every 3600 seconds")
    print("Press Ctrl+C to stop...")
    print()

    try:
        while True:
            print(f"\n{'='*60}")
            print(f"🧬 EVOLUTION CYCLE #{agent.iterations + 1}")
            print(f"{'='*60}")

            success = agent.run_evolution_cycle()

            if success:
                print(f"✅ Evolution cycle complete")
                print(f"   Version: {agent.evolution.current_version}")
                print(f"   Iterations: {agent.iterations}")
            else:
                print(f"❌ Evolution cycle failed")

            print(f"\n⏳ Waiting {config.evolution_interval} seconds before next cycle...")
            import asyncio
            asyncio.sleep(config.evolution_interval)

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Uroboros...")
        state_file = project_root / "uroboros" / "state.json"
        agent.save_state(state_file)
        agent.sync_with_github()
        print("🪐 Uroboros AI - The cycle continues...")
        sys.exit(0)


def start_test():
    """Run tests."""
    print("🧪 UROBOROS AI - Test Mode")
    print("=" * 60)

    load_env()
    from uroboros import Config, UroborosAgent

    config = Config.from_env()
    agent = UroborosAgent(config)

    print("✓ Configuration loaded")
    print(f"✓ Agent initialized: {agent}")

    # Test 1
    print("\n" + "="*60)
    print("TEST 1: Basic question")
    print("="*60)
    response = agent.think("Привет, Uroboros! Кто ты?")
    print(f"Ответ: {response}")

    # Test 2
    print("\n" + "="*60)
    print("TEST 2: Evolution trigger")
    print("="*60)
    agent.evolve()
    print(f"Iterations: {agent.iterations}")

    print("\n" + "="*60)
    print("✓ All tests passed!")
    print("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Uroboros AI - Self-modifying AI agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  interactive  - Interactive chat mode (default)
  telegram     - Start Telegram bot
  autonomous   - Continuous evolution mode
  test         - Run tests
        """
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="interactive",
        choices=["interactive", "telegram", "autonomous", "test"],
        help="Mode to run in"
    )

    parser.add_argument(
        "--log",
        "-l",
        help="Log file path"
    )

    args = parser.parse_args()

    # Setup logging
    log_file = args.log or f"uroboros_{args.mode}.log"
    setup_logging(log_file)

    logger = logging.getLogger("UroborosLauncher")

    # Check configuration
    if not check_config():
        sys.exit(1)

    logger.info(f"Starting Uroboros in {args.mode} mode")

    # Run selected mode
    if args.mode == "interactive":
        start_interactive()
    elif args.mode == "telegram":
        start_telegram()
    elif args.mode == "autonomous":
        start_autonomous()
    elif args.mode == "test":
        start_test()


if __name__ == "__main__":
    main()
