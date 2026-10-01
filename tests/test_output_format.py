import json
import pytest

from utils.csv_tools import format_output


def test_json_format():
    result = {"column": "amount", "average": 20.0, "count": 3}
    output = format_output(result, "json")
    # json output should be a valid JSON string
    data = json.loads(output)
    assert data == result


def test_csv_format():
    result = {"column": "amount", "average": 20.0, "count": 3}
    output = format_output(result, "csv")
    assert output == "Average of column 'amount': 20.000"


def test_tsv_format():
    result = {"column": "amount", "average": 20.0, "count": 3}
    output = format_output(result, "tsv")
    expected = "column\taverage\tcount\namount\t20.0\t3"
    assert output == expected
