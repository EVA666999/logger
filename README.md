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
> <img width="477" height="158" alt="Image" src="https://github.com/user-attachments/assets/600b5b6b-1c88-49c0-9ad0-ec44e328b86e" /> 

### Отчёт с фильтрацией по дате
```bash
python main.py --file logs/example1.log --report average --date 2025-06-22
```
<img width="557" height="157" alt="Image" src="https://github.com/user-attachments/assets/c41f6e01-17e2-47ef-9e02-03e3fed466b4" />

### Анализ нескольких файлов
```bash
python main.py --file logs/example1.log logs/example2.log --report average
```
> <img width="573" height="146" alt="Image" src="https://github.com/user-attachments/assets/79590581-51db-4c7f-b054-59a3bba0ada8" />
## Запуск тестов

```bash
pytest tests/ -v --cov=main --cov=add_reports --cov-report=term-missing
```

## Структура проекта

- `main.py` - основной скрипт
- `add_reports.py` - модуль отчётов
- `tests/` - тесты (покрытие 86%)
- `logs/` - примеры лог-файлов
