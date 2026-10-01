"""Custom exception classes for CSV related errors.

This module defines a small hierarchy of exceptions that can be raised by
:mod:`utils.csv_tools`. The goal is to provide clearer error messages that
include contextual information such as column names and file paths.
"""


class CSVError(Exception):
    """Base class for all CSV‑related errors.

    Subclasses should call ``super().__init__(message)`` with a descriptive
    message that explains what went wrong.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class MissingColumnError(CSVError):
    """Raised when a required column is absent from a CSV file.

    Parameters
    ----------
    column_name: str
        The name of the missing column.
    file_path: Optional[str]
        The path to the CSV file, if known.
    """

    def __init__(self, column_name: str, file_path: str | None = None) -> None:
        path_info = f" in file '{file_path}'" if file_path else ""
        message = f"Missing column '{column_name}'" + (f" in file '{file_path}'" if file_path else "") + "."
        super().__init__(message)
        self.column_name = column_name
        self.file_path = file_path


class EmptyDataError(CSVError):
    """Raised when a CSV file contains no rows.

    Parameters
    ----------
    file_path: Optional[str]
        The path to the CSV file, if known.
    """

    def __init__(self, file_path: str | None = None) -> None:
        path_info = f" '{file_path}'" if file_path else ""
        message = f"CSV file{path_info} is empty or contains no data."
        super().__init__(message)
        self.file_path = file_path


class NonNumericError(CSVError):
    """Raised when no numeric values are found in a numeric column.

    Parameters
    ----------
    column_name: str
        The name of the column that was expected to contain numeric data.
    file_path: Optional[str]
        The path to the CSV file, if known.
    """

    def __init__(self, column_name: str, file_path: str | None = None) -> None:
        path_info = f" in file '{file_path}'" if file_path else ""
        message = f"No numeric values found in column '{column_name}'{path_info}."
        super().__init__(message)
        self.column_name = column_name
        self.file_path = file_path
