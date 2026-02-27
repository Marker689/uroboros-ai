#!/usr/bin/env python3
"""
Простой тест Uroboros агента без Telegram бота.
"""

import sys
sys.path.insert(0, '/home/marker/ouroboros')

from uroboros import Config, UroborosAgent

# Загрузка конфигурации
config = Config.from_env()
print("✓ Конфигурация загружена")

# Инициализация агента
agent = UroborosAgent(config)
print(f"✓ Агент инициализирован: {agent}")

# Тест 1: Базовый вопрос
print("\n" + "="*60)
print("ТЕСТ 1: Базовый вопрос")
print("="*60)
response = agent.think("Привет, Uroboros! Кто ты?")
print(f"Ответ: {response}")

# Тест 2: Вопрос о принципах
print("\n" + "="*60)
print("ТЕСТ 2: Вопрос о принципах")
print("="*60)
response = agent.think("Какие у тебя принципы?")
print(f"Ответ: {response}")

# Тест 3: Вопрос о памяти
print("\n" + "="*60)
print("ТЕСТ 3: Вопрос о памяти")
print("="*60)
response = agent.think("Что ты помнишь?")
print(f"Ответ: {response}")

# Тест 4: Проверка статуса
print("\n" + "="*60)
print("ТЕСТ 4: Статус агента")
print("="*60)
status = agent.get_status()
print(f"Статус: {status}")

# Тест 5: Проверка эволюции
print("\n" + "="*60)
print("ТЕСТ 5: Триггер эволюции")
print("="*60)
agent.evolve()
print(f"Итерация: {agent.iterations}")

print("\n" + "="*60)
print("✓ Все тесты пройдены!")
print("="*60)
