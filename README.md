# CSV Filter & Average CLI

A simple command‑line utility for reading a CSV file, filtering rows and
calculating the arithmetic mean of a numeric column. It supports multiple
output formats (CSV, JSON, TSV) and robust error handling.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Usage

```bash
python -m main --file <csv> --column <column>
```

Optional flags:

- `--filter-value` to filter rows where the column equals the given value.
- `--output-format {csv,json,tsv}` – default is `csv`.

## Examples

### Basic usage

```bash
python -m main --file test.csv --column amount
```

Output:
```
Average of column 'amount': 20.000
```

### With filtering

```bash
python -m main --file data.csv --column price --filter-value 100
```

### JSON output

```bash
python -m main --file test.csv --column amount --output-format json
```

Output:
```
{"column":"amount","average":20.0,"count":3}
```

### TSV output

```bash
python -m main --file test.csv --column amount --output-format tsv
```

Output:
```
column	average	count
amount	20.0	3
```

### Error handling

```bash
python -m main --file test.csv --column nonexistent
```

Output:
```
Error computing average: Missing column 'nonexistent'.
```

## Edge cases

- Empty CSV file – raises `EmptyDataError`.
- Header row with no data rows – same error.
- `NaN` values – ignored; no error.
- Mixed numeric/non‑numeric values – non‑numeric rows are skipped; non‑error.
- Missing column – `MissingColumnError` is shown.

## Exit codes

- `0` – success.
- `1` – any error.

## Testing

```bash
pytest
pytest -v
```
