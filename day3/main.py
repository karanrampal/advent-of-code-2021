#!/usr/bin/env python3
"""Binary string"""

import argparse
import logging
from pathlib import Path
from typing import List


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Binary string manipulation")
    parser.add_argument(
        "-f",
        "--file_path",
        type=Path,
        default=Path("./inputs.txt"),
        help="Path of input file",
    )
    parser.add_argument(
        "-l",
        "--log_path",
        type=Path,
        default=Path("./main.log"),
        help="Path of log file",
    )

    return parser.parse_args()


def setup_logging(log_path: Path) -> None:
    """Setup logger
    Args:
        log_path: Path of log file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, "w")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        )
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
    logger.addHandler(stream_handler)


def read_file(file_path: Path) -> List[str]:
    """Read input file
    Args:
        file_path: Path of input file
    Returns:
        Read data is returned
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                lines.append(line.strip())
    except FileNotFoundError:
        logging.warning("No such file '%s' exists!", file_path)

    return lines


def _is_max_one(data: List[str], pos: int) -> bool:
    """Check if the max value at position pos for all strings is 1
    Args:
        data: Input data
        pos: Position to search at a data point string
    Returns:
        If max value 1 or not
    """
    sum_ = sum([1 for val in data if int(val[pos])])
    return sum_ >= (len(data) / 2)


def binary_diagnostic(data: List[str]) -> int:
    """Calculate the product of gamma and epsilon values for Binary diagnostic
    Args:
        data: Input data
    Returns
        Product of decimal values of Gamma and epsilon
    """
    if not data:
        logging.error("Data is empty!")
        return -1

    num_dig = len(data[0])
    gamma, epsilon = "", ""
    for i in range(num_dig):
        if _is_max_one(data, i):
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    return int(gamma, 2) * int(epsilon, 2)


def _filter_data(data: List[str], pos: int, char: str) -> List[str]:
    """Filtering out data that match the character char at position pos
    Args:
        data: Input data
        pos: Position to search in a data point string
        search_str: Binary string of most/least common 1/0
    Returns:
        Filtered data
    """
    return [val for val in data if char == val[pos]]


def _calculate_generator_value(data: List[str], mode: str) -> str:
    """Calculate the O2 or CO2 generator value
    Args:
        data: Input data
        mode: Most/least common 1/0, possible values are o2/co2
    Returns:
        String in data which satisfies the mode criteria
    """
    pos = 0
    while len(data) > 1:
        if ((mode == "o2") and _is_max_one(data, pos)) or (
            (mode == "co2") and not _is_max_one(data, pos)
        ):
            data = _filter_data(data, pos, "1")
        else:
            data = _filter_data(data, pos, "0")
        pos += 1

    return data[0]


def life_support_rating(data: List[str]) -> int:
    """Calculate the life support rating
    Args:
        data: Input data
    Returns:
        Life support rating
    """
    if not data:
        logging.error("Data is empty!")
        return -1

    o2_val = _calculate_generator_value(data, "o2")
    co2_val = _calculate_generator_value(data, "co2")
    return int(o2_val, 2) * int(co2_val, 2)


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logging(args.log_path)

    data = read_file(args.file_path)

    res1 = binary_diagnostic(data)
    print(f"Binary Diagnostic value: {res1}")

    res2 = life_support_rating(data)
    print(f"Life support rating: {res2}")


if __name__ == "__main__":
    main()
