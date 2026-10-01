"""Unit tests for CSV helper functions.

The tests exercise :func:`utils.csv_tools.read_csv` and
:func:`utils.csv_tools.compute_average`.  They use the
pytest ``tmp_path`` fixture to create a temporary CSV file so the
tests remain self‑contained and do not depend on any external data.

All tests are deterministic and make no external network calls.

"""

import csv
from pathlib import Path
from typing import Dict

import pytest

from utils.csv_tools import read_csv, compute_average
from utils.exceptions import MissingColumnError, NonNumericError


def write_csv(path: Path, rows: list[Dict[str, str]]) -> None:
    """Write the given *rows* to *path* as a CSV file.

    ``rows`` must be a list of dictionaries whose keys form the header
    row.  The function writes values in the order of the first row
    keys.
    """
    if not rows:
        raise ValueError("Cannot write an empty list of rows")
    header = rows[0].keys()
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(header))
        writer.writeheader()
        writer.writerows(rows)


class TestReadCSV:
    def test_reads_header_and_rows(self, tmp_path: Path) -> None:
        """The CSV is read back as a list of dictionaries."""
        data = {
            "id": "1",
            "name": "Alice",
            "value": "10.5",
        }
        csv_file = tmp_path / "sample.csv"
        write_csv(csv_file, [data])

        rows = read_csv(str(csv_file))
        assert rows == [data]

    def test_fieldnames_order(self, tmp_path: Path) -> None:
        """The order of fields in the CSV does not affect the output."""
        rows = [
            {"b": "2", "a": "1"},
            {"b": "4", "a": "3"},
        ]
        csv_file = tmp_path / "order.csv"
        write_csv(csv_file, rows)

        parsed = read_csv(str(csv_file))
        assert parsed == rows


class TestComputeAverage:
    def test_basic_average(self) -> None:
        rows = [{"value": "2"}, {"value": "4"}, {"value": "6"}]
        assert compute_average(rows, "value") == 4.0

    def test_ignores_non_numeric(self) -> None:
        rows = [{"value": "1"}, {"value": "NaN"}, {"value": "3"}]
        assert compute_average(rows, "value") == 2.0

    def test_missing_column_raises(self) -> None:
        rows = [{"value": "1"}, {"other": "2"}]
        with pytest.raises(MissingColumnError, match="Missing column 'value'"):
            compute_average(rows, "value")

    def test_no_numeric_throws(self) -> None:
        rows = [{"value": "abc"}, {"value": ""}]
        with pytest.raises(NonNumericError, match="No numeric values found"):
            compute_average(rows, "value")

# End of file.