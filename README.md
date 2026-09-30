# My Project

A small demo project for experimenting with CSV utilities and a simple CLI powered by `utils.csv_tools`.

## 📦 Installation

```bash
# Create a virtual environment (recommended)
python -m venv .venv
.
venv\Scripts\activate   # on Windows
source .venv/bin/activate  # on macOS/Linux

# Install the project dependencies
pip install -r requirements.txt
```

The only mandatory external dependency is **pytest** for the test suite.

## 🚀 Usage

Running the CLI is straightforward. The script accepts the path to a CSV file and the column you want to compute the mean of.

```bash
# Example – compute the mean of the ``value`` column in ``data.csv``
python -m main --file data.csv --column value
```

If no file is specified the bundled `sample.csv` (located in the project root) is used.

## 🧪 Running Tests

The test suite lives in `tests/` and uses `pytest`.

```bash
# Execute the full test matrix
pytest
```

All tests are self‑contained and write temporary CSV files under the test
bucket provided by pytest’s ``tmp_path`` fixture.

## 🤝 Contributing

Feel free to fork and submit PRs.  The repository follows the standard
Python layout with a top‑level `utils/` package and an entry‑point
script in `main.py`.

---

*© 2026 My Project – MIT License*
