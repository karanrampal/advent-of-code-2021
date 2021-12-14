#!/usr/bin/env python3
"""Polymer template"""

import argparse
import logging
from collections import Counter, defaultdict
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
    Returns:
        Starting Sequence and operations to be performed
    """
    operations: Dict[str, str] = {}
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                tmp = line.strip()
                if "->" in tmp:
                    i, j = tmp.split(" -> ")
                    operations[i] = j
                elif tmp:
                    seq = tmp
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return seq, operations


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


def merge(left: str, right: str, operations: Dict[str, str]) -> str:
    """Merge step of divide and conquer
    Args:
        left: Left sub sequence
        right: Right sub sequence
        operations: Insertion operations to perform
    Returns:
        Merged sequence
    """
    return left + operations[left[-1] + right[0]] + right


def divide_conquer(seq: str, operations: Dict[str, str]) -> str:
    """Divide step of divide and conquer
    Args:
        seq: Starting sequence
        operations: Insertion operations to perform
    Returns:
        Merged sequence
    """
    num = len(seq)
    if num == 1:
        return seq

    mid = num // 2
    left = divide_conquer(seq[:mid], operations)
    right = divide_conquer(seq[mid:], operations)

    return merge(left, right, operations)


def polymerize_fast(seq: str, operations: Dict[str, str], steps: int) -> int:
    """Fast version of PCR using dictionary
    Args:
        seq: Starting sequence
        operations: Insertion operations to perform
        steps: Number of steps in the PCR
    Returns:
        Final sequence pairs counts
    """
    # Create a dictionary from initial seq
    buffer: Dict[str, int] = defaultdict(int)
    for i in range(len(seq) - 1):
        buffer[seq[i : i + 2]] += 1

    # Run the PCR for steps
    for _ in range(steps):
        new_buffer: Dict[str, int] = defaultdict(int)
        for key, val in buffer.items():
            tmp = operations[key]
            new_buffer[key[0] + tmp] += 1 * val
            new_buffer[tmp + key[1]] += 1 * val
        buffer = new_buffer

    # Calculate the counts of each letter
    counter: Dict[str, int] = defaultdict(int)
    for key, val in buffer.items():
        counter[key[0]] += val
        counter[key[1]] += val

    # Find max/min of the counter
    cmin = cmax = counter["N"] // 2
    for val in counter.values():
        val = int((val / 2) + 0.5)
        cmax = max(val, cmax)
        cmin = min(val, cmin)

    return cmax - cmin


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    seq, operations = read_file(args.file_path)

    steps = 10
    ans = polymerization_reaction(seq, operations, steps=steps)
    assert ans == 2712
    print(f"Difference of max and min char count for {steps} steps: {ans}")

    seq_cp = seq
    for _ in range(steps):
        seq_cp = divide_conquer(seq_cp, operations)
    ctr = Counter(seq_cp).most_common()
    ans2 = ctr[0][1] - ctr[-1][1]
    assert ans2 == 2712
    assert ans2 == ans
    print(
        f"Difference of max and min char count for {steps} steps (divide & conquer): {ans2}"
    )

    steps = 40
    out = polymerize_fast(seq, operations, steps)
    assert out == 8336623059567
    print(f"Difference of max and min char count for {steps} steps (fast): {out}")


if __name__ == "__main__":
    main()
