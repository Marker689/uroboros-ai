#!/usr/bin/env python3
"""
Тест Telegram бота Uroboros
"""

import asyncio
import sys
sys.path.insert(0, '/home/marker/ouroboros')

from uroboros import Config, UroborosAgent

# Загрузка конфигурации
config = Config.from_env()
print(f"✓ Конфигурация загружена")
print(f"  Bot token: {config.telegram_bot_token[:10]}...")

# Инициализация агента
agent = UroborosAgent(config)
print(f"✓ Агент инициализирован")

# Запуск Telegram бота
print("\n🤖 Запуск Telegram бота...")
print("Отправьте команды в Telegram:")
print("  /start - Начать")
print("  /help - Помощь")
print("  /status - Статус")
print("  /evolve - Эволюция")
print("  /version - Версия")
print("  /memory - Память")
print()

async def main():
    try:
        success = await agent.start_telegram_bot()
        if success:
            print("✓ Бот запущен успешно!")
            print("Нажмите Ctrl+C для остановки...")
            await asyncio.Event().wait()  # Блокируем выполнение
        else:
            print("✗ Бот не запустился")
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
        await agent.stop()
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(main())
