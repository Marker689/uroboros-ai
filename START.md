# Как запустить Uroboros

## Команда:

```bash
python3 start.py autonomous
```

## Что делает:

При старте агент сразу переписывает свой код, а потом каждые 30 минут делает это снова. Всё видно в консоли.

## В фоне:

```bash
nohup python3 start.py autonomous > uroboros.log 2>&1 &
```

## .env настройки:

```env
LOCAL_LLM_BASE_URL=http://localhost:3000/api
LOCAL_LLM_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
GITHUB_USER=username
GITHUB_REPO=uroboros-ai
GITHUB_TOKEN=token
```
