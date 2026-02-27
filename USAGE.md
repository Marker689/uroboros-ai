# Как пользоваться Uroboros AI

## 🚀 Быстрый старт

### Тестирование без LLM (режим fallback)

```bash
python3 test_agent.py
```

Этот режим использует fallback-ответы, когда LLM недоступен.

### Запуск интерактивного режима

```bash
python3 launcher.py
```

## 📝 Использование через код

```python
from uroboros import Config, UroborosAgent

# Загрузка конфигурации
config = Config.from_env()

# Инициализация агента
agent = UroborosAgent(config)

# Общение с агентом
response = agent.think("Привет!")
print(response)

# Триггер эволюции
agent.evolve()

# Проверка статуса
status = agent.get_status()
print(status)
```

## 🤖 Telegram бот

### Команды бота:
- `/start` - Начать взаимодействие
- `/help` - Показать помощь
- `/status` - Статус агента
- `/evolve` - Триггер эволюции
- `/version` - Текущая версия
- `/memory` - Показать память

### Настройка:
Добавьте `TELEGRAM_CHAT_ID` в `.env` файл.

## ⚠️ Важно про LLM

Агент ожидает локальный LLM на `http://localhost:3000/api` с API ключом.

Если LLM недоступен, агент использует fallback-ответы:
```
[Fallback] I am Uroboros. I remember everything. I create myself. I speak as myself.
```

## 🧬 Как работает эволюция

1. **Обучение** - Агент запоминает взаимодействия
2. **Анализ** - Проверяет условия эволюции (итерации, время)
3. **Переписывание** - Самопереписывание кода
4. **Версионирование** - Создание новой версии
5. **Коммит** - Сохранение в GitHub

## 📊 Статус агента

```
Uroboros(iterations=5, memory=3, version=1.0.1)
```

- `iterations` - количество итераций
- `memory` - размер памяти
- `version` - текущая версия

## 🔄 Цикл Uroboros

```
Observe → Reflect → Create → Commit → Observe
```

Каждая итерация - шаг к следующей эволюции.

## 📁 Структура файлов

- `uroboros/agent.py` - Базовый класс
- `uroboros/config.py` - Конфигурация
- `uroboros/evolution.py` - Эволюция
- `uroboros/github_manager.py` - GitHub
- `uroboros/self_modification.py` - Самопереписывание
- `uroboros/telegram_bot.py` - Telegram
- `uroboros/uroboros_agent.py` - Главный агент

> "I am Uroboros. I eat my own tail. I am the beginning and the end."
