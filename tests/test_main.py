"""
Тесты для модуля main.py
"""
import os
import tempfile
from unittest.mock import patch

import pytest

from add_reports import average_report
from main import main, parse_logs


class TestParseLogs:
    """Тесты для функции parse_logs."""
    
    def test_parse_logs_basic(self, temp_log_file):
        """Тест базового парсинга логов."""
        stats = parse_logs([temp_log_file])
        
        # Проверяем что эндпоинты найдены
        assert "/api/test1" in stats
        assert "/api/test2" in stats
        
        # Проверяем количество запросов
        assert stats["/api/test1"]["count"] == 2
        assert stats["/api/test2"]["count"] == 1
    
    def test_parse_logs_with_date_filter(self, temp_log_file):
        """Тест фильтрации по дате."""
        stats = parse_logs([temp_log_file], "2025-06-22")
        
        # Должны быть найдены все записи за эту дату
        assert "/api/test1" in stats
        assert "/api/test2" in stats
    
    def test_parse_logs_invalid_json(self):
        """Тест обработки некорректного JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('{"invalid": json}\n')
            f.write(
                '{"@timestamp": "2025-06-22T13:57:32+00:00", '
                '"url": "/test", "response_time": 0.1}\n'
            )
            temp_file = f.name
        
        try:
            stats = parse_logs([temp_file])
            # Должна быть обработана только корректная запись
            assert len(stats) == 1
            assert "/test" in stats
        finally:
            os.unlink(temp_file)


class TestReports:
    """Тесты для функций отчётов."""
    
    def test_average_report(self, capsys):
        """Тест функции average_report."""
        stats = {
            "/api/test": {
                "count": 2,
                "total_time": 0.1,
                "max_time": 0.06,
                "@timestamp": []
            }
        }
        
        average_report(stats)
        captured = capsys.readouterr()
        
        # Проверяем что отчёт содержит нужную информацию
        assert "Handler" in captured.out
        assert "/api/test" in captured.out
        assert "2" in captured.out
        # 0.1 / 2 = 0.05
        assert "0.05" in captured.out


class TestMain:
    """Тесты для функции main."""
    
    @patch('main.parse_logs')
    @patch('main.average_report')
    def test_main_average_report(
        self, mock_average_report, mock_parse_logs
    ):
        """Тест main с отчётом average."""
        mock_parse_logs.return_value = {
            "/api/test": {
                "count": 1, "total_time": 0.1, "max_time": 0.1,
                "@timestamp": []
            }
        }
        
        with patch('sys.argv', [
            'main.py', '--file', 'test.log', '--report', 'average'
        ]):
            main()
        
        # Проверяем что функции вызваны с правильными параметрами
        mock_parse_logs.assert_called_once_with(
            ['test.log'], None
        )
        mock_average_report.assert_called_once()
    
    @patch('main.parse_logs')
    @patch('main.average_report')
    def test_main_with_date_filter(
        self, mock_average_report, mock_parse_logs
    ):
        """Тест main с фильтром по дате."""
        mock_parse_logs.return_value = {
            "/api/test": {
                "count": 1, "total_time": 0.1, "max_time": 0.1,
                "@timestamp": []
            }
        }
        
        with patch('sys.argv', [
            'main.py', '--file', 'test.log', '--report', 'average',
            '--date', '2025-06-22'
        ]):
            main()
        
        # Проверяем что фильтр по дате передается
        mock_parse_logs.assert_called_once_with(
            ['test.log'], '2025-06-22'
        )
        mock_average_report.assert_called_once()


if __name__ == "__main__":
    pytest.main([
        __file__, "-v", "--cov=main", "--cov=add_reports",
        "--cov-report=term-missing"
    ])