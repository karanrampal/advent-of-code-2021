#!/usr/bin/env python3
"""Line intersection"""

import argparse
import logging
from pathlib import Path
from typing import List


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Line intersection")
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


def count_lanternfishes(days: int, data: List[int]) -> int:
    """Count the number of lanternfishes after given number of days
    Args:
        days: Number of days to simulate
        data: Input data
    Returns:
        Count of the number of lanter fishes
    """
    for _ in range(days):
        num_zeros = data.count(0)
        data += [9] * num_zeros
        data = [val - 1 if val > 0 else 6 for val in data]

    return len(data)


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    ans = count_lanternfishes(80, data)
    print(f"Number of lanternfishes: {ans}")


if __name__ == "__main__":
    main()
