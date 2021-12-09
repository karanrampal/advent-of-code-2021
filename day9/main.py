#!/usr/bin/env python3
"""Smoke Basin low points"""

import argparse
import logging
import re
from pathlib import Path

import numpy as np


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Smoke basin search")
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


def read_file(file_path: Path) -> np.ndarray:
    """Read input file
    Args:
        file_path: Path of input file
    Returns:
        read data
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                tmp = re.split(r"", line.strip())
                tmp = list(map(int, tmp[1:-1]))
                lines.append(tmp)
    except FileNotFoundError:
        logging.error("File '%s' not found!", file_path)

    return np.array(lines)


def get_neighbours(data: np.ndarray, i: int, j: int) -> np.ndarray:
    """Count the number of low points in the smoke basin
    Args:
        data: Input data
        i: X position of point
        j: Y position of point
    Returns:
        Sum of the low points
    """
    row, col = data.shape
    neighbours = []
    if i - 1 >= 0:
        neighbours.append(data[i - 1, j])
    if i + 1 < row:
        neighbours.append(data[i + 1, j])
    if j - 1 >= 0:
        neighbours.append(data[i, j - 1])
    if j + 1 < col:
        neighbours.append(data[i, j + 1])

    return np.array(neighbours)


def sum_num_low_points(data: np.ndarray) -> int:
    """Count the number of low points in the smoke basin
    Args:
        data: Input data
    Returns:
        Sum of the low points
    """
    row, col = data.shape
    sum_ = 0
    for i in range(row):
        for j in range(col):
            neighbours = get_neighbours(data, i, j)
            if (data[i, j] < neighbours).all():
                sum_ += data[i, j] + 1

    return sum_


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    ans = sum_num_low_points(data)
    assert ans == 570
    print(f"Sum of low points in the basin: {ans}")


if __name__ == "__main__":
    main()
