"""Entry point for the CLI application.

The primary purpose of this script is to provide a simple
command‑line interface that demonstrates how the helper
functions in ``utils/csv_tools.py`` can be used.

Typical usage::

    python -m main --file data.csv --column value

If no arguments are supplied we simply print a short help
message so the user knows how to invoke the program.
"""

import argparse
import sys
from pathlib import Path

# Import the helper functions from the utils package
# We add the project root to sys.path so ``utils`` can be resolved.
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from utils.csv_tools import read_csv, compute_average, filter_rows


def parse_args(argv):
    """Parse command line arguments.

    The CLI accepts three optional arguments.  ``--file`` specifies
    a path to a CSV file; it defaults to ``sample.csv`` for
    demonstration purposes.  ``--column`` selects the column whose
    values will be averaged.  ``--filter-value`` filters rows where
    the specified column equals this value before averaging.
    """
    parser = argparse.ArgumentParser(
        description="Compute the mean of a numeric column in a CSV file.",
        prog="python -m main",
    )
    parser.add_argument(
        "--file",
        type=str,
        default="sample.csv",
        help="Path to the CSV file to process (default: sample.csv)",
    )
    parser.add_argument(
        "--column",
        type=str,
        required=True,
        help="Name of the column to average. Column must contain numeric values.",
    )
    parser.add_argument(
        "--filter-value",
        type=str,
        default=None,
        help="Filter rows where the specified column equals this value before averaging.",
    )

    return parser.parse_args(argv)


def main(argv=None):
    """Entry point for the module."""
    argv = [] if argv is None else argv
    args = parse_args(argv)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: file '{file_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Load and optionally filter rows
    if args.filter_value is not None:
        rows = filter_rows(str(file_path), args.column, args.filter_value)
    else:
        rows = read_csv(str(file_path))

    try:
        avg = compute_average(rows, args.column)
    except ValueError as exc:
        print(f"Error computing average: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Average of column '{args.column}': {avg:.3f}")


if __name__ == "__main__":
    main(sys.argv[1:])
