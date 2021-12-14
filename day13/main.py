#!/usr/bin/env python3
"""Paper folding"""

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
    parser = argparse.ArgumentParser(description="Folding transparent paper")
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


def read_file(file_path: Path) -> Tuple[np.ndarray, List[Tuple[str, int]]]:
    """Read file from file path
    Args:
        file_path: Path of input file
    Returns:
        Dots and folding operations
    """
    points, folds = [], []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                if "," in line:
                    points.append(tuple(map(int, line.strip().split(","))))
                elif "=" in line:
                    match = re.search(r"(\w+)=(\d+)", line.strip())
                    if match:
                        folds.append((match.group(1), int(match.group(2))))
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return np.array(points), folds


def fold_paper(points: np.ndarray, folds: List[Tuple[str, int]]) -> np.ndarray:
    """Fold the paper represented by the points as per the instructions in fold
    Args:
        points: The starting number of dots and their positions
        folds: Folding direction and value
    Returns:
        Paper after folding
    """
    xmax, ymax = points.max(axis=0)
    paper = np.zeros((xmax + 1, ymax + 1))
    paper[points[:, 0], points[:, 1]] = 1
    paper = paper.T
    for fold in folds:
        direction, val = fold
        if direction == "x":
            mat_rt = paper[:, val + 1 :]
            mirror_mat_rt = mat_rt[:, ::-1]
            mat_lt = paper[:, :val]
            tmp = mat_lt.shape[1] - mirror_mat_rt.shape[1]
            if tmp > 0:
                paper = mat_lt + np.pad(mirror_mat_rt, ((0, 0), (tmp, 0)))
            else:
                paper = np.pad(mat_lt, ((0, 0), (tmp, 0))) + mirror_mat_rt
        elif direction == "y":
            mat_do = paper[val + 1 :, :]
            mirror_mat_do = mat_do[::-1, :]
            mat_up = paper[:val, :]
            tmp = mat_up.shape[0] - mirror_mat_do.shape[0]
            if tmp > 0:
                paper = mat_up + np.pad(mirror_mat_do, ((tmp, 0), (0, 0)))
            else:
                paper = np.pad(mat_up, ((tmp, 0), (0, 0))) + mirror_mat_do

    return paper


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    points, folds = read_file(args.file_path)

    ans = fold_paper(points, [folds[0]])
    tmp = (ans > 0).sum()
    assert tmp == 706
    print(f"Number of dots after first fold: {tmp}")

    ans2 = fold_paper(points, folds)
    ans2 = (ans2 > 0).astype(int)
    print(ans2)
    logging.info(ans2)
    tmp = (ans2 > 0).sum()
    assert tmp == 95  # LRFJBJEH
    print(f"Number of dots after all folds: {tmp}")


if __name__ == "__main__":
    main()
