"""
Модуль для добавления отчётов в лог-файлы.
"""

from typing import Dict
from tabulate import tabulate


def average_report(stats: Dict[str, Dict[str, float]]) -> None:
    """Выводит отчёт по среднему времени."""
    table = []
    for endpoint, values in stats.items():
        avg = values["total_time"] / values["count"]
        table.append([endpoint, values['count'], round(avg, 3)])

    headers = ["Handler", "total_time", "avg_response_time"]
    print(tabulate(table, headers=headers, tablefmt="github"))