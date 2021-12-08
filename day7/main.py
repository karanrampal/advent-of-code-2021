#!/usr/bin/env python3
"""Horizontal position estimator"""

import argparse
import logging
import statistics
import sys
from pathlib import Path
from typing import List


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Horizontal position estimator")
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


def setup_logger(log_path: Path) -> None:
    """Setup Logger
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


def read_file(file_path: Path) -> List[int]:
    """Read input file
    Args:
        file_path: Path of input file
    Returns:
        read data
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            lines = list(map(int, fptr.read().strip().split(",")))
    except FileNotFoundError:
        logging.error("File '%s' not found!", file_path)

    return lines


def min_horizontal_change(data: List[int]) -> int:
    """Caculate the minimum change to align horizontal positions
    Args:
        data: Inpu data
    Returns
        Sum of the distances to min point
    """
    med = statistics.median(data)
    return int(sum([abs(i - med) for i in data]))


def min_horizontal_change_2(data: List[int]) -> int:
    """Caculate the minimum change to align horizontal positions given that the
    crabs move in arithmetic progression.
    Args:
        data: Inpu data
    Returns
        Sum of the distances to min point
    """
    min_fuel = sys.maxsize
    min_val = min(data)
    max_val = max(data)
    for j in range(min_val, max_val):
        sum_ = 0
        for i in data:
            dist = abs(i - j)
            sum_ += dist * (dist + 1) // 2
        if sum_ < min_fuel:
            min_fuel = sum_

    return min_fuel


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    ans = min_horizontal_change(data)
    print(f"Min fuel: {ans}")
    assert ans == 336120
    ans2 = min_horizontal_change_2(data)
    assert ans2 == 96864235
    print(f"Min fuel: {ans2}")


if __name__ == "__main__":
    main()
