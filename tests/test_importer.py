from weewx_meteohub.importer import Importer
from unittest.mock import patch, mock_open
from datetime import datetime
import pytest


def test_count_lines():
    with patch(
        "builtins.open",
        mock_open(
            read_data="20071101145756 rain0 0 0 2764\n20071101145830 thb0 218 46 10 1024 3 1024\n20071101145943 th0 132 82 10"  # noqa: E501
        ),
    ) as input_file:
        importer = Importer(input_file, "../out.txt")
        assert importer.count_lines() == 3


@pytest.mark.parametrize(
    "number, output",
    [
        (1, 0),
        (2, 0),
        (5, 5),
        (7, 5),
        (15, 15),
        (27, 25),
        (59, 55),
    ],  # noqa: E501
)
def test_roundto5(number, output):
    with patch(
        "builtins.open", mock_open(read_data="20071101145756 rain0 0 0 2764")
    ) as input_file:
        importer = Importer(input_file, "../out.txt")
        assert importer.roundto5(number) == output


def test_get_start_date():
    with patch(
        "builtins.open", mock_open(read_data="20071101145756 rain0 0 0 2764")
    ) as input_file:
        importer = Importer(input_file, "../out.txt")
        importer.sort()
        assert (
            importer.get_start_date().strftime("%Y%m%d%H%M%S")
            == "20071101145756"
        )


@pytest.mark.parametrize(
    "date, start, end",
    [
        ("20071101145756", "20071101145500", "20071101150000"),
        ("20110901003317", "20110901003000", "20110901003500"),
        ("20220901001717", "20220901001500", "20220901002000"),
        (None, "20071101145500", "20071101150000"),
    ],
)
def test_get_interval(date, start, end):
    with patch(
        "builtins.open", mock_open(read_data="20071101145756 rain0 0 0 2764")
    ) as input_file:
        importer = Importer(input_file, "../out.txt")
        if date:
            date = datetime.strptime(date, "%Y%m%d%H%M%S")
        importer.sort()

        interval_start, interval_end = importer.get_interval(date)

        assert interval_start.strftime("%Y%m%d%H%M%S") == start
        assert interval_end.strftime("%Y%m%d%H%M%S") == end
