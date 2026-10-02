import argparse
import sys
from pathlib import Path

# Import the helper functions from the utils package
# We add the project root to sys.path so ``utils`` can be resolved.
root = Path(__file__).parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from utils.csv_tools import read_csv, compute_average, filter_rows, compute_average_and_count, format_output, sort_rows
from utils.exceptions import CSVError


def parse_args(argv):
    """Parse command line arguments.

    The CLI accepts three optional arguments.  ``--file`` specifies
    a path to a CSV file; it defaults to ``sample.csv`` for
    demonstration purposes.  ``--column`` selects the column whose
    values will be averaged.  ``--filter-value`` filters rows where
    the specified column equals this value before averaging.
    ``--sort-by`` sorts the rows before averaging.  The ``--reverse``
    flag can be used with ``--sort-by`` to sort in descending order.
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
        "--output-format",
        type=str,
        choices=["csv", "json", "tsv"],
        default="csv",
        help="Output format: csv, json, or tsv.",
    )
    parser.add_argument(
        "--filter-value",
        type=str,
        default=None,
        help="Filter rows where column equals this value",
    )
    parser.add_argument(
        "--sort-by",
        type=str,
        default=None,
        help="Sort rows by this column before averaging (numeric if possible).",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Sort descending when used with --sort-by.",
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

    # Load and optionally filter or sort rows
    if args.sort_by:
        rows = sort_rows(str(file_path), args.sort_by, reverse=args.reverse)
    elif args.filter_value is not None:
        rows = filter_rows(str(file_path), args.column, args.filter_value)
    else:
        rows = read_csv(str(file_path))

    try:
        avg, count = compute_average_and_count(rows, args.column)
    except CSVError as exc:
        print(f"Error computing average: {exc}", file=sys.stderr)
        sys.exit(1)

    result_dict = {
        "column": args.column,
        "average": avg,
        "count": count,
    }
    output = format_output(result_dict, args.output_format)
    print(output)


if __name__ == "__main__":
    main(sys.argv[1:])
