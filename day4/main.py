#!/usr/bin/env python3
"""Bingo"""

import argparse
import logging
from pathlib import Path
from typing import List, Tuple

from bingo_board import BingoBoard


def arg_parser() -> argparse.Namespace:
    """Parse CLI arguments"""
    parser = argparse.ArgumentParser(description="Bingo game simulator")
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


def read_file(file_path: Path) -> List[str]:
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
                lines.append(line.strip())
    except FileNotFoundError:
        logging.error("File '%s' not found!", file_path)

    return lines


def setup_game(data: List[str]) -> Tuple[List[int], List[BingoBoard]]:
    """Setup the boards and the bingo onput numbers
    Args:
        data: Input data to create a bingo game
    Returns:
        Numers to call out and the list of boards
    """
    numbers = list(map(int, data[0].split(sep=",")))
    boards = []
    tmp = []
    for line in data[2:]:
        if line:
            tmp.append(list(map(int, line.split())))
        else:
            boards.append(BingoBoard(tmp))
            tmp = []

    return numbers, boards


def play(numbers: List[int], boards: List[BingoBoard]) -> List[Tuple[int, int]]:
    """Play a game of bingo and pick the boards that win in a list
    Args:
        data: Input data to create a bingo game
    Returns:
        List of boards and their corresponding scores
    """
    wins = []
    already_won = set()
    num_boards = len(boards)
    for num in numbers:
        for i, board in enumerate(boards):
            board.cross_out(num)
            if board.check() and i not in already_won:
                already_won.add(i)
                scr = board.score() * num
                wins.append((i, scr))
        if len(already_won) == num_boards:
            break

    return wins


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    nums, boards = setup_game(data)
    scores = play(nums, boards)
    assert scores[0][1] == 28082
    assert scores[-1][1] == 8224
    print(f"SCore to win: {scores[0][1]}")
    print(f"SCore to lose: {scores[-1][1]}")


if __name__ == "__main__":
    main()
