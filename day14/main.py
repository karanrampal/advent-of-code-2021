#!/usr/bin/env python3
"""Polymer template"""

import argparse
import logging
from collections import Counter
from pathlib import Path
from typing import Dict, Tuple


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Polymer template")
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


def read_file(file_path: Path) -> Tuple[str, Dict[str, str]]:
    """Read file from file path
    Args:
        file_path: Path of input file
    """
    inserts: Dict[str, str] = {}
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                tmp = line.strip()
                if "->" in tmp:
                    i, j = tmp.split(" -> ")
                    inserts[i] = j
                elif tmp:
                    seq = tmp
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return seq, inserts


def polymerization_reaction(seq: str, operations: Dict[str, str], steps: int) -> int:
    """Simulate a polymerization chain reaction
    Args:
        seq: Starting sequence
        operations: Insertion operations to perform
        steps: Number of steps in the chain reaction
    Returns:
        Difference of max and min char count
    """
    for _ in range(steps):
        new_seq = ""
        for i in range(len(seq) - 1):
            val = operations.get(seq[i : i + 2], "")
            new_seq += seq[i] + val if val else ""
        seq = new_seq + seq[-1]

    ctr = Counter(seq).most_common()
    return ctr[0][1] - ctr[-1][1]


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    seq, inserts = read_file(args.file_path)

    ans = polymerization_reaction(seq, inserts, steps=10)
    print(f"Difference of max and min char count: {ans}")


if __name__ == "__main__":
    main()
