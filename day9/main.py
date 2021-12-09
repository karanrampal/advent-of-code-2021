#!/usr/bin/env python3
"""Smoke Basin low points"""

import argparse
import logging
import re
from pathlib import Path
from typing import List, Tuple

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


def get_neighbours(data: np.ndarray, i: int, j: int) -> Tuple[List[int], List[int]]:
    """Count the number of low points in the smoke basin
    Args:
        data: Input data
        i: X position of point
        j: Y position of point
    Returns:
        Sum of the low points
    """
    row, col = data.shape
    row_list, col_list = [], []
    if i - 1 >= 0:
        row_list.append(i - 1)
        col_list.append(j)
    if i + 1 < row:
        row_list.append(i + 1)
        col_list.append(j)
    if j - 1 >= 0:
        row_list.append(i)
        col_list.append(j - 1)
    if j + 1 < col:
        row_list.append(i)
        col_list.append(j + 1)

    return row_list, col_list


def get_low_points(data: np.ndarray) -> Tuple[List[int], List[int]]:
    """Get the number of low points in the smoke basin
    Args:
        data: Input data
    Returns:
        The low points
    """
    row, col = data.shape
    rows_list, cols_list = [], []
    for i in range(row):
        for j in range(col):
            r_list, c_list = get_neighbours(data, i, j)
            if (data[i, j] < data[r_list, c_list]).all():
                rows_list.append(i)
                cols_list.append(j)

    return rows_list, cols_list


def sum_num_low_points(data: np.ndarray) -> int:
    """Sum of risk of the low points
    Args:
        data: input data
    Returns:
        Sum of the risk scores
    """
    row_list, col_list = get_low_points(data)
    return (data[row_list, col_list]).sum() + len(row_list)


def get_basin_sizes(data: np.ndarray) -> List[int]:
    """Get sizes of the basins
    Args:
        data: Input data
    Returns:
        Sizes of each basin
    """
    visited = np.zeros_like(data)
    rows_list, cols_list = get_low_points(data)
    size_list = []
    for point in zip(rows_list, cols_list):
        stack = [point]
        size_ = 0
        while stack:
            i, j = stack.pop(0)
            if not visited[i, j]:
                visited[i, j] = 1
                size_ += 1
            r_list, c_list = get_neighbours(data, i, j)
            for sub in zip(r_list, c_list):
                if (data[point] < data[sub] < 9) and not visited[sub]:
                    stack.append(sub)
        size_list.append(size_)

    return size_list


def prod_basin_sizes(data: np.ndarray) -> int:
    """Product of biggest 3 basin sizes
    Args:
        data: Input data
    Returns:
        Product of top 3 basin sizes
    """
    size_list = get_basin_sizes(data)
    tmp = sorted(size_list, reverse=True)[:3]
    return np.prod(tmp)


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    ans = sum_num_low_points(data)
    assert ans == 570
    print(f"Sum of low points in the basin: {ans}")
    ans2 = prod_basin_sizes(data)
    assert ans2 == 899392
    print(f"Product of 3 largest basins: {ans2}")


if __name__ == "__main__":
    main()
