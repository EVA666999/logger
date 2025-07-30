# Logger Analyzer

Скрипт для анализа лог-файлов API запросов.

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### Базовый отчёт
```bash
python main.py --file logs/example1.log --report average
```
https://github.com/EVA666999/logger/issues/1#issuecomment-3135183862

### Отчёт с фильтрацией по дате
```bash
python main.py --file logs/example1.log --report average --date 2025-06-22
```
![Пример работы](https://i.imgur.com/example2.png)

### Анализ нескольких файлов
```bash
python main.py --file logs/example1.log logs/example2.log --report average
```
![Пример работы](https://i.imgur.com/example3.png)

## Запуск тестов

```bash
pytest tests/ -v --cov=main --cov=add_reports --cov-report=term-missing
```

## Структура проекта

- `main.py` - основной скрипт
- `add_reports.py` - модуль отчётов
- `tests/` - тесты (покрытие 86%)
- `logs/` - примеры лог-файлов
