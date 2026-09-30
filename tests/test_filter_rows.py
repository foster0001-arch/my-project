import pytest
from utils.csv_tools import filter_rows
from pathlib import Path
import csv


def write_csv(path, rows):
    """Write rows to a CSV file for testing."""
    if not rows:
        raise ValueError("Rows must not be empty")
    header = rows[0].keys()
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(header))
        writer.writeheader()
        writer.writerows(rows)


class TestFilterRows:
    def test_basic_filter(self, tmp_path):
        rows = [
            {"id": "1", "color": "red", "value": "10"},
            {"id": "2", "color": "blue", "value": "20"},
            {"id": "3", "color": "red", "value": "30"},
        ]
        csv_file = tmp_path / "input.csv"
        write_csv(csv_file, rows)

        result = filter_rows(str(csv_file), "color", "red")
        assert result == [rows[0], rows[2]]

    def test_no_match(self, tmp_path):
        rows = [{"name": "Alice", "age": "25"}, {"name": "Bob", "age": "30"}]
        csv_file = tmp_path / "input.csv"
        write_csv(csv_file, rows)
        result = filter_rows(str(csv_file), "name", "Carol")
        assert result == []

    def test_nonexistent_column(self, tmp_path):
        rows = [{"x": "1"}, {"x": "2"}]
        csv_file = tmp_path / "input.csv"
        write_csv(csv_file, rows)
        # Should return empty list when column missing in all rows
        result = filter_rows(str(csv_file), "y", "something")
        assert result == []

    def test_multiple_matches(self, tmp_path):
        rows = [{"k": "a"}, {"k": "a"}, {"k": "b"}]
        csv_file = tmp_path / "input.csv"
        write_csv(csv_file, rows)
        result = filter_rows(str(csv_file), "k", "a")
        assert result == rows[:2]
