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


def count_1478_pattern(data: List[List[str]]) -> int:
    """Count the number of occurences for the patterns of 1, 4, 7 or 8
    Args:
        data: Input data
    Returns:
        Count of occurences
    """
    cnt = sum([sum([1 for x in val if len(x) in [2, 4, 3, 7]]) for val in data])

    return cnt


def sum_decode_digit(patterns: List[List[str]], digits: List[List[str]]) -> int:
    """Sum of all the digits decoded using the patterns
    Args:
        patterns: Patterns to decode and get 7 segment display patterns
        digits: Digits to be decoded
    Returns:
        Sum of the decoded digits
    """
    count = 0
    for i, pat in enumerate(patterns):
        pat1 = set(list(filter(lambda x: len(x) == 2, pat))[0])
        pat4 = set(list(filter(lambda x: len(x) == 4, pat))[0])
        pat7 = set(list(filter(lambda x: len(x) == 3, pat))[0])
        pat8 = set(list(filter(lambda x: len(x) == 7, pat))[0])
        pat3 = set(
            list(filter(lambda x, tmp=pat1: len(x) == 5 and tmp.issubset(set(x)), pat))[
                0
            ]
        )
        pat9 = pat4 | pat3
        pat2 = set(
            list(filter(lambda x, tmp=(pat8 - pat9): len(x) == 5 and tmp.issubset(set(x)), pat))[
                0
            ]
        )
        pat6 = set(
            list(
                filter(
                    lambda x, tmp=pat1: len(x) == 6 and not tmp.issubset(set(x)), pat
                )
            )[0]
        )
        pat5 = set(
            list(filter(lambda x, tmp=(pat8 - pat2): len(x) == 5 and tmp.issubset(set(x)), pat))[
                0
            ]
        )
        res = ""
        for dig in digits[i]:
            if set(dig) == pat1:
                res += "1"
            elif set(dig) == pat2:
                res += "2"
            elif set(dig) == pat3:
                res += "3"
            elif set(dig) == pat4:
                res += "4"
            elif set(dig) == pat5:
                res += "5"
            elif set(dig) == pat6:
                res += "6"
            elif set(dig) == pat7:
                res += "7"
            elif set(dig) == pat8:
                res += "8"
            elif set(dig) == pat9:
                res += "9"
            else:
                res += "0"
        count += int(res)
    return count


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    patterns, digits = read_file(args.file_path)

    ans = count_1478_pattern(digits)
    assert ans == 330
    print(f"Number of 1,4,7 or 8's: {ans}")
    ans2 = sum_decode_digit(patterns, digits)
    assert ans2 == 1010472
    print(f"Sum of all decoded output digits: {ans2}")


if __name__ == "__main__":
    main()
