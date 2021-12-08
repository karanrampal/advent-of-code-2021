#!/usr/bin/env python3
"""Seven segment search"""

import argparse
import logging
from pathlib import Path
from typing import List, Tuple


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Seven segment search")
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


def read_file(file_path: Path) -> Tuple[List[List[str]], List[List[str]]]:
    """Read input file
    Args:
        file_path: Path of input file
    Returns:
        read data
    """
    patterns, digits = [], []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                pat, dig = line.strip().split("|")
                patterns.append(pat.strip().split())
                digits.append(dig.strip().split())
    except FileNotFoundError:
        logging.error("File '%s' not found!", file_path)

    return patterns, digits


def count_1478_pattern(data):
    """Count the number of occurences for the patterns of 1, 4, 7 or 8
    Args:
        data: Input data
    Returns:
        Count of occurences
    """
    count = 0
    for val in data:
        count += sum([1 for x in val if len(x) in [2, 4, 3, 7]])

    return count


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    _, digits = read_file(args.file_path)

    ans = count_1478_pattern(digits)
    assert ans == 330
    print(f"Number of 1,4,7 or 8's: {ans}")


if __name__ == "__main__":
    main()
