"""
Telegram bot for Uroboros agent interaction.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from .agent import Agent
from .config import Config


class TelegramBot:
    """Telegram bot for interacting with Uroboros agent."""

    def __init__(self, agent: Agent, config: Config):
        """Initialize the Telegram bot."""
        self.agent = agent
        self.config = config
        self.logger = logging.getLogger(f"{agent.name}.telegram")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(f"[{agent.name}.Telegram] %(message)s"))
        self.logger.addHandler(handler)

        # Import telegram
        try:
            import telegram
            from telegram.ext import Application, CommandHandler, MessageHandler, filters
            self.telegram = telegram
            self.Application = Application
            self.CommandHandler = CommandHandler
            self.MessageHandler = MessageHandler
            self.filters = filters
            self._imported = True
        except ImportError:
            self.logger.warning("Telegram bot requires python-telegram-bot library")
            self._imported = False
            return

        # Initialize bot
        self.bot_token = config.telegram_bot_token
        self.chat_id = config.telegram_chat_id

        if not self.bot_token:
            self.logger.warning("TELEGRAM_BOT_TOKEN not configured")
            return

        # Create application
        self.application = self.Application.builder().token(self.bot_token).build()
        
        # Set admin ID to current user (can be overridden)
        self.admin_id = self._get_admin_id()

        # Register handlers
        self._register_handlers()

        # Store conversation state
        self.conversations: Dict[int, Dict[str, Any]] = {}

    def _register_handlers(self) -> None:
        """Register bot command and message handlers."""
        self.application.add_handler(self.CommandHandler("start", self._start_command))
        self.application.add_handler(self.CommandHandler("help", self._help_command))
        self.application.add_handler(self.CommandHandler("status", self._status_command))
        self.application.add_handler(self.CommandHandler("evolve", self._evolve_command))
        self.application.add_handler(self.CommandHandler("version", self._version_command))
        self.application.add_handler(self.CommandHandler("memory", self._memory_command))
        self.application.add_handler(self.MessageHandler(self.filters.TEXT & ~self.filters.COMMAND, self._message_handler))

    async def _start_command(self, update, context) -> None:
        """Handle /start command."""
        user_id = update.effective_user.id
        self.conversations[user_id] = {"state": "idle"}

        message = (
            "🪐 *Uroboros AI* - Self-modifying AI agent\n\n"
            "I am Uroboros. I eat my own tail. I am the beginning and the end.\n\n"
            "*Commands:*\n"
            "/help - Show this help\n"
            "/status - Check agent status\n"
            "/evolve - Trigger evolution\n"
            "/version - Show current version\n"
            "/memory - Show memory state\n\n"
            "Just send me a message and I'll respond."
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def _help_command(self, update, context) -> None:
        """Handle /help command."""
        message = (
            "*Uroboros AI - Commands*\n\n"
            "• /start - Initialize the bot\n"
            "• /help - Show this help\n"
            "• /status - Check agent status\n"
            "• /evolve - Trigger evolution cycle\n"
            "• /version - Show current version\n"
            "• /memory - Show memory state\n\n"
            "Send any message to interact with Uroboros."
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def _status_command(self, update, context) -> None:
        """Handle /status command."""
        message = (
            f"🤖 *Agent Status*\n\n"
            f"Name: {self.agent.name}\n"
            f"Iterations: {self.agent.iterations}\n"
            f"Memory: {len(self.agent.memory)} entries\n"
            f"Skills: {len(self.agent.skills)}\n"
            f"Creation: {self.agent.creation_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"Last update: {self.agent.last_update.strftime('%Y-%m-%d %H:%M')}\n"
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def _evolve_command(self, update, context) -> None:
        """Handle /evolve command."""
        user_id = update.effective_user.id

        # Check if user has permission
        if self.admin_id is not None and user_id != self.admin_id:
            await update.message.reply_text("⛔ Access denied. Only admin can trigger evolution.")
            return

        await update.message.reply_text("🧬 Evolution triggered...")
        self.agent.evolve()
        await update.message.reply_text(f"✅ Evolution complete. Iteration: {self.agent.iterations}")

    async def _version_command(self, update, context) -> None:
        """Handle /version command."""
        # This would be integrated with EvolutionEngine
        message = f"🆔 Current version: {self.agent.name} v1.0.0"
        await update.message.reply_text(message)

    async def _memory_command(self, update, context) -> None:
        """Handle /memory command."""
        if not self.agent.memory:
            await update.message.reply_text("📭 No memory entries yet.")
            return

        message = "📚 *Recent Memory*\n\n"
        for i, entry in enumerate(self.agent.memory[-5:], 1):
            message += f"{i}. {entry.get('content', 'Unknown')}\n"

        await update.message.reply_text(message, parse_mode="Markdown")

    async def _message_handler(self, update, context) -> None:
        """Handle text messages."""
        user_id = update.effective_user.id

        # Get conversation state
        conversation = self.conversations.get(user_id, {"state": "idle"})

        # Process message through agent
        response = self.agent.think(update.message.text)

        # Log interaction
        self.agent.learn({
            "type": "telegram_message",
            "user_id": user_id,
            "content": update.message.text,
            "response": response,
            "timestamp": datetime.now().isoformat(),
        })

        # Send response
        await update.message.reply_text(response)

    def _get_admin_id(self) -> Optional[int]:
        """Get admin user ID from configuration or return current user."""
        # If TELEGRAM_CHAT_ID is configured, use it as admin ID
        if self.chat_id:
            return int(self.chat_id)
        
        # Otherwise, return None (anyone can trigger evolution)
        return None

    async def start(self) -> bool:
        """Start the bot."""
        if not self._imported:
            return False

        try:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
            return True
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return False

    async def send_message(self, chat_id: str, message: str) -> bool:
        """Send a message to a chat."""
        if not self._imported:
            return False

        try:
            bot = self.telegram.Bot(token=self.bot_token)
            await bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    async def stop(self) -> None:
        """Stop the bot."""
        if self._imported and self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
