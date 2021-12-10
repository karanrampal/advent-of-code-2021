#!/usr/bin/env python3
"""Matching paranthesis"""

import argparse
import logging
from pathlib import Path
from typing import List


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Matching paranthesis")
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


def read_file(file_path: Path) -> List[str]:
    """Read file from file path
    Args:
        file_path: Path of input file
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            lines = fptr.readlines()
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return lines


def matching_brackets(line: str) -> str:
    """Find matching brackets
    Args:
        line: Input string line
    Returns:
        Score of mismatch bracket
    """
    stack = []
    for i in line:
        if i in "{(<[":
            stack.append(i)
        elif i in "})>]":
            if stack:
                val = stack.pop()
                if val + i not in ["{}", "()", "<>", "[]"]:
                    return i
            else:
                return i

    return ""


def mismarch_score(data: List[str]) -> int:
    """Calculate the mismatch score
    Args:
        data: Input data
    Returns:
        Score of mismatch bracket
    """
    score = 0
    dict_ = {"": 0, ")": 3, "]": 57, "}": 1197, ">": 25137}
    for line in data:
        i = matching_brackets(line)
        score += dict_[i]

    return score


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    lines = read_file(args.file_path)

    ans = mismarch_score(lines)
    assert ans == 392043
    print(f"Score: {ans}")
    # ans2 = submarine_position_new(lines)
    # assert ans2 == 1698850445
    # print(f"New submarine position: {ans2}")


if __name__ == "__main__":
    main()
