# Запуск автономного Uroboros агента

## Способ 1: Прямой запуск в фоне

```bash
nohup python3 autonomous_agent.py > uroboros.log 2>&1 &
```

## Способ 2: С логированием в файл

```bash
python3 autonomous_agent.py 2>&1 | tee uroboros.log
```

## Способ 3: С таймаутом (если зависнет)

```bash
timeout 3600 python3 autonomous_agent.py
```

## Проверка статуса

```bash
# Посмотреть логи
tail -f uroboros.log

# Проверить процесс
ps aux | grep autonomous_agent

# Посмотреть состояние агента
python3 -c "from uroboros import Config, UroborosAgent; c=Config.from_env(); a=UroborosAgent(c); print(a)"
```

## Остановка

```bash
# Найти PID
ps aux | grep autonomous_agent

# Убить процесс
kill <PID>

# Или принудительно
kill -9 <PID>
```

## Параметры эволюции

Измените в `.env`:
- `EVOLUTION_INTERVAL` - интервал между эволюциями (секунды)
- `SELF_MODIFICATION_INTERVAL` - интервал самопереписывания (секунды)
- `MAX_ITERATIONS` - максимальное количество итераций
