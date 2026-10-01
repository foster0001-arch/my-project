"""Utility functions for working with CSV files.

The module exposes two straightforward helpers:

* ``read_csv`` – read a CSV file into a list of dictionaries.
* ``compute_average`` – calculate the mean of a numeric column.

These helpers are intentionally lightweight so they can be used
by other scripts or extended in the future.
"""

import csv
import statistics
import math
from pathlib import Path
from utils.exceptions import CSVError, MissingColumnError, NonNumericError, EmptyDataError
from typing import Dict, Iterable, List


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of rows.

    Parameters
    ----------
    file_path:
        Path to the CSV file.  The file is opened in universal
        newline mode to support Windows, Unix, and Mac line ending
        conventions.

    Returns
    -------
    list[dict[str, str]]
        Each row is represented as a dictionary mapping column
        names to their string values.
    """
    with Path(file_path).open("r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            raise EmptyDataError(file_path)
        return rows


def _to_float(value: str):
    """Attempt to convert a string to float.

    ``None`` or empty strings are considered missing values and
    cause ``ValueError`` to be raised to let the caller decide
    how to handle them.
    """
    try:
        val = float(value)
        if math.isnan(val):
            raise ValueError(f"Cannot convert '{value}' to float")
        return val
    except Exception as exc:
        raise ValueError(f"Cannot convert '{value}' to float") from exc


def compute_average(rows: Iterable[Dict[str, str]], column_name: str) -> float:
    """Compute the arithmetic mean of values in ``column_name``.

    Parameters
    ----------
    rows:
        Iterable of dictionaries produced by :func:`read_csv`.
    column_name:
        Name of the column to average.

    Returns
    -------
    float
        The mean of the numeric values.

    Raises
    ------
    ValueError
        If the column is missing in any row, or if no numeric
        values are found.
    """
    values = []
    for i, row in enumerate(rows, start=1):
        try:
            val = _to_float(row[column_name])
        except KeyError as exc:
            raise MissingColumnError(column_name) from exc
        except ValueError:
            # Skip non‑numeric or missing values
            continue
        values.append(val)

    if not values:
        raise NonNumericError(column_name)
    return statistics.mean(values)

# ---------------------------------------------------------------------------
# Output formatting helpers and average+count
# ---------------------------------------------------------------------------
import json


def format_output(result: dict, format_type: str) -> str:
    """Return a formatted string for *result*.

    Parameters
    ----------
    result:
        Dict containing ``column``, ``average`` and ``count``.
    format_type:
        One of ``"csv"``, ``"json"`` or ``"tsv"``.
    """
    if format_type == "csv":
        return f"Average of column '{result['column']}': {result['average']:.3f}"
    elif format_type == "json":
        return json.dumps(result, separators=(",", ": "))
    elif format_type == "tsv":
        return ("column\taverage\tcount\n" +
                f"{result['column']}\t{result['average']}\t{result['count']}")
    else:
        raise ValueError(f"Unsupported format type: {format_type}")


def compute_average_and_count(rows: Iterable[Dict[str, str]], column_name: str):
    """Compute average and count of numeric values in *column_name*.
    """
    values = []
    for row in rows:
        try:
            val = _to_float(row[column_name])
        except KeyError as exc:
            raise MissingColumnError(column_name) from exc
        except ValueError:
            continue
        values.append(val)
    if not values:
        raise NonNumericError(column_name)
    return statistics.mean(values), len(values)



def filter_rows(csv_path: str, column: str, value: str):
    """Return only rows from *csv_path* where *column* equals *value*.

    Parameters
    ----------
    csv_path:
        Path to the CSV file.
    column:
        Column name to filter on.
    value:
        The string value rows must match.

    Returns
    -------
    list[dict[str, str]]
        A list of row dictionaries that satisfied the predicate.
    """
    rows = read_csv(csv_path)
    return [row for row in rows if row.get(column) == value]


__all__ = ["read_csv", "compute_average", "filter_rows"]
