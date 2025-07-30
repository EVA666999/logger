import json
import argparse
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any

from add_reports import average_report


def parse_logs(
    file_paths: List[str], filter_date: str = None
) -> Dict[str, Dict[str, Any]]:

    """Парсит лог-файлы и собирает статистику по эндпоинтам."""
    stats = defaultdict(
        lambda: {"count": 0, "total_time": 0, "max_time": 0, "@timestamp": []}
    ) 

    for path in file_paths:
        with open(path, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    endpoint = data.get("url")
                    response_time = data.get("response_time")
                    date = data.get("@timestamp")
                    correct_date_format = datetime.strptime(
                        date, "%Y-%m-%dT%H:%M:%S+00:00"
                    ).date()

                    if endpoint:
                        if filter_date:
                            try:
                                filter_date_obj = datetime.strptime(
                                    filter_date, "%Y-%m-%d"
                                ).date()
                                if correct_date_format != filter_date_obj:
                                    continue
                            except ValueError:
                                continue
                        
                        stats[endpoint]["count"] += 1
                        stats[endpoint]["total_time"] += response_time
                        try:
                            stats[endpoint]["@timestamp"].append(
                                correct_date_format
                            )
                        except (ValueError):
                            continue
                except json.JSONDecodeError:
                    continue
    return stats


def main() -> None:
    """Основная функция программы."""
    parser = argparse.ArgumentParser(description="Обработка логов")
    parser.add_argument(
        "--file", nargs="+", required=True, help="Путь к лог-файлам"
    )
    parser.add_argument(
        "--date", required=False,
        help="Фильтрация логов по дате (формат: 2025-06-22)"
    )
    parser.add_argument(
        "--report", required=True,
        choices=["average", "date"],
        help="Название отчёта"
    )
    args = parser.parse_args()

    stats = parse_logs(args.file, args.date)
    
    if args.report == "average":
        average_report(stats)
    elif args.report == "date":
        average_report(stats)


if __name__ == "__main__":
    main()
