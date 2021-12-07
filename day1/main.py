#!/usr/bin/env python3
"""Number of increments"""

import argparse
import logging
from pathlib import Path
from typing import List


def args_parser() -> argparse.Namespace:
    """Argument parser
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Process input file")
    parser.add_argument(
        "-f",
        "--file_path",
        type=Path,
        default=Path("./inps.txt"),
        help="File path of the inputs",
    )
    parser.add_argument(
        "-l",
        "--log_path",
        type=Path,
        default=Path("./main.log"),
        help="File path of the log file",
    )
    return parser.parse_args()


def setup_logger(log_path: Path) -> None:
    """Setup logger
    Args:
        log_path: Path of lig file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(log_path, mode="w")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
        )
        logger.addHandler(file_handler)

        # Logging to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))
        logger.addHandler(stream_handler)


def read_file(file_path: Path) -> List[str]:
    """Read input file
    Args:
        file_path: File path of the inputs
    Returns:
        (List[str]) List of strings
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            lines = fptr.readlines()
    except FileNotFoundError:
        logging.warning("No such file '%s' exists!", file_path)

    return lines


def get_num_increments(file_path: Path) -> int:
    """Get number of increments
    Args:
        file_path: File path of the inputs
    Returns:
        (int) Number of increments
    """
    incr = 0
    prev = -1
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                cur = int(line.strip())
                if (prev != -1) and (cur > prev):
                    incr += 1
                prev = cur
    except FileNotFoundError:
        logging.warning("No such file '%s' exists!", file_path)

    return incr


def get_num_windowed_increments(data: List[int], win: int = 3) -> int:
    """Get the number of increments per window fo size n
    Args:
        data: Input data
        win: Size of window
    Returns:
        (int) Number of increments
    """
    if win < 0:
        logging.error("Window size can not be less than 0!")
        return 0

    num = len(data)
    if num == 0:
        logging.error("Data is empty!")
        return 0
    incr = 0
    prev = -1
    for i in range(num - win + 1):
        cur = sum(data[i : (i + win)])
        if (prev != -1) and (cur > prev):
            incr += 1
        prev = cur

    return incr


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    answer1 = get_num_increments(args.file_path)
    assert answer1 == 1711
    print(f"Num increments of window size 1: {answer1}")

    lines = read_file(args.file_path)
    lines_int = list(map(int, lines))
    ans1 = get_num_windowed_increments(lines_int, 1)
    assert ans1 == answer1, f"{ans1} not equal to {answer1}"
    answer2 = get_num_windowed_increments(lines_int)
    assert answer2 == 1743
    print(f"Num increments of window size 3: {answer2}")


if __name__ == "__main__":
    main()
