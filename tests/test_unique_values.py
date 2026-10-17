import csv
import pytest

from utils.csv_tools import unique_values, MissingColumnError


# Helper to create temp csv file

def create_csv(tmp_path, rows, header):
    file = tmp_path / "data.csv"
    with file.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return file


def test_unique_values_basic(tmp_path):
    rows = [["A", "10"], ["B", "5"], ["A", "20"]]
    csv_file = create_csv(tmp_path, rows, ["name", "amount"])
    unique = unique_values(str(csv_file), "name")
    assert unique == ["A", "B"]


def test_unique_values_missing_column(tmp_path):
    rows = [["A", "10"]]
    csv_file = create_csv(tmp_path, rows, ["name", "amount"])
    with pytest.raises(MissingColumnError):
        unique_values(str(csv_file), "nonexistent")


def test_unique_values_order(tmp_path):
    rows = [["C", "1"], ["B", "2"], ["C", "3"], ["A", "4"], ["B", "5"]]
    csv_file = create_csv(tmp_path, rows, ["name", "amount"])
    unique = unique_values(str(csv_file), "name")
    assert unique == ["C", "B", "A"]
