#!/usr/bin/env python3
"""Line intersection"""

import argparse
import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple


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


def read_file(file_path: Path) -> List[List[int]]:
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
                match = re.search(r"(\d*),(\d*) -> (\d*),(\d*)$", line.strip())
                if match:
                    lines.append([int(match.group(i)) for i in range(1, 5)])
    except FileNotFoundError:
        logging.error("File '%s' not found!", file_path)

    return lines


def count_horiz_vert_overlap(data: List[List[int]]) -> int:
    """Count the number of overlaps of the horizontal and vertical lines
    Args:
        data: Input data
    Returns:
        Count of overlap
    """
    if not data:
        logging.error("Input data is empty!")
        return -1

    graph: Dict[Tuple[int, int], int] = {}
    for pts in data:
        if pts[0] == pts[2]:
            ymin = min(pts[1], pts[3])
            ymax = max(pts[1], pts[3])
            for j in range(ymin, ymax + 1):
                val = graph.get((pts[0], j), 0)
                graph[(pts[0], j)] = val + 1
        elif pts[1] == pts[3]:
            xmin = min(pts[0], pts[2])
            xmax = max(pts[0], pts[2])
            for i in range(xmin, xmax + 1):
                val = graph.get((i, pts[1]), 0)
                graph[(i, pts[1])] = val + 1

    return sum([1 for val in graph.values() if val > 1])


def count_all_overlap(data: List[List[int]]) -> int:
    """Count all the overlaps
    Args:
        data:Input data
    Returns:
        Count of all the overlaps
    """
    if not data:
        logging.error("Input data is empty!")
        return -1

    graph: Dict[Tuple[int, int], int] = {}
    for pts in data:
        if pts[0] == pts[2]:
            ymin = min(pts[1], pts[3])
            ymax = max(pts[1], pts[3])
            for i in range(ymin, ymax + 1):
                val = graph.get((pts[0], i), 0)
                graph[(pts[0], i)] = val + 1
        elif pts[1] == pts[3]:
            xmin = min(pts[0], pts[2])
            xmax = max(pts[0], pts[2])
            for i in range(xmin, xmax + 1):
                val = graph.get((i, pts[1]), 0)
                graph[(i, pts[1])] = val + 1
        elif ((pts[0] - pts[2]) * (pts[1] - pts[3])) > 0:
            xmin = min(pts[0], pts[2])
            ymin = min(pts[1], pts[3])
            for i in range(abs(pts[0] - pts[2]) + 1):
                val = graph.get((xmin + i, ymin + i), 0)
                graph[(xmin + i, ymin + i)] = val + 1
        else:
            xmin = min(pts[0], pts[2])
            ymax = max(pts[1], pts[3])
            for i in range(abs(pts[0] - pts[2]) + 1):
                val = graph.get((xmin + i, ymax - i), 0)
                graph[(xmin + i, ymax - i)] = val + 1

    return sum([1 for val in graph.values() if val > 1])


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)
    ans = count_horiz_vert_overlap(data)
    assert ans == 5608
    print(f"Horizontal and vertical overlaps: {ans}")
    ans2 = count_all_overlap(data)
    assert ans2 == 20299
    print(f"All overlap: {ans2}")


if __name__ == "__main__":
    main()
