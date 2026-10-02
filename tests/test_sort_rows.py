import pytest
import csv
from utils.csv_tools import sort_rows, MissingColumnError

# Helper to create temp csv file

def create_csv(tmp_path, rows, header):
    file = tmp_path / "data.csv"
    with file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return file


def test_sort_rows_numeric_ascending(tmp_path):
    rows = [["A", "10"], ["B", "5"], ["C", "15"]]
    csv_file = create_csv(tmp_path, rows, ["name", "amount"])
    sorted_rows = sort_rows(str(csv_file), "amount")
    assert [r["name"] for r in sorted_rows] == ["B", "A", "C"]


def test_sort_rows_numeric_descending(tmp_path):
    rows = [["A", "10"], ["B", "5"], ["C", "15"]]
    csv_file = create_csv(tmp_path, rows, ["name", "amount"])
    sorted_rows = sort_rows(str(csv_file), "amount", reverse=True)
    assert [r["name"] for r in sorted_rows] == ["C", "A", "B"]


def test_sort_rows_missing_column(tmp_path):
    rows = [["A", "10"]]
    csv_file = create_csv(tmp_path, rows, ["name", "quantity"])
    with pytest.raises(MissingColumnError):
        sort_rows(str(csv_file), "amount")
