#!/usr/bin/env python3
"""Dumbo octopuses"""

import argparse
import logging
import re
from pathlib import Path
from typing import List, Tuple

import numpy as np


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Octopus energy level simulator")
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
    """Setup logger
    Args:
        log_path: Path of log file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode="w")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        )
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
        logger.addHandler(stream_handler)


def read_file(file_path: Path) -> np.ndarray:
    """Read file from file path
    Args:
        file_path: Path of input file
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                tmp = list(map(int, re.split(r"", line.strip())[1:-1]))
                lines.append(tmp)
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return np.array(lines)


def get_neighbours(data: np.ndarray, i: int, j: int) -> List[Tuple[int, int]]:
    """Get 8 neighbours of a point in a 2D matrix
    Args:
        data: Input data
        i: x-point around which to get neighbours
        j: y-point around which to get neighbours
    Returns:
        Neighbours
    """
    rows, cols = data.shape
    min_i = max(0, i - 1)
    max_i = min(rows, i + 2)
    min_j = max(0, j - 1)
    max_j = min(cols, j + 2)
    neighbours = []
    for xval in range(min_i, max_i):
        for yval in range(min_j, max_j):
            if (xval, yval) != (i, j):
                neighbours.append((xval, yval))

    return neighbours


def octopus_energy_level(data: np.ndarray) -> Tuple[int, np.ndarray]:
    """Simulate the octopus energy levels
    Args:
        data: Input data
    Returns:
        Count of number of flashes
    """
    count = 0
    data += 1
    xval, yval = np.nonzero(data > 9)
    while len(xval):
        count += len(xval)
        for i, j in zip(xval, yval):
            data[i, j] = 0
            neigh = get_neighbours(data, i, j)
            for val in neigh:
                data[val] += 1 if 0 < data[val] <= 9 else 0
        xval, yval = np.nonzero(data > 9)

    return count, data


def count_flashes(data, num: int = 100) -> int:
    """Simulate flashes for num steps
    Args:
        data: Input dtat
        num: Number of steps
    Returns:
        Count of flashes for num steps
    """
    count = 0
    for _ in range(num):
        cnt, data = octopus_energy_level(data)
        count += cnt

    return count


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    lines = read_file(args.file_path)

    ans = count_flashes(lines)
    # assert ans == 392043
    print(f"Score: {ans}")


if __name__ == "__main__":
    main()
