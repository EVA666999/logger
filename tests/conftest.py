"""
Конфигурация pytest для тестов.
"""
import json
import os
import sys
import tempfile

import pytest

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def sample_log_data():
    """Тестовые данные логов."""
    return [
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "url": "/api/test1",
            "response_time": 0.1
        },
        {
            "@timestamp": "2025-06-22T13:57:32+00:00", 
            "url": "/api/test1",
            "response_time": 0.2
        },
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "url": "/api/test2", 
            "response_time": 0.3
        }
    ]


@pytest.fixture
def temp_log_file(sample_log_data):
    """Создает временный файл с логами."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        for log_entry in sample_log_data:
            f.write(json.dumps(log_entry) + '\n')
        temp_file = f.name
    
    yield temp_file
    os.unlink(temp_file) 