#!/usr/bin/env python3
"""Shortest path in a rectangle, Dynamic programming"""

import argparse
import heapq
import logging
import sys
from pathlib import Path
from typing import List, Tuple

import numpy as np


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Dynamic programming")
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


def read_file(file_path: Path) -> np.ndarray:
    """Read file from file path
    Args:
        file_path: Path of input file
    Returns:
        Starting Sequence and operations to be performed
    """
    data = []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                data.append(list(map(int, line.strip())))
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return np.array(data)


def neighbors(
    xpos: int, ypos: int, height: int, width: int, scale: int
) -> List[Tuple[int, int]]:
    """Get neighbours of the matrix given the expansion scale
    Args:
        xpos: X position of point
        j: Column position of point
        height: Height of the 2D matrix
        width: Width of the 2D matrix
        scale: Expansion scale for the matrix
    Returns:
        List of neighbour positions
    """
    out = [(xpos - 1, ypos), (xpos + 1, ypos), (xpos, ypos - 1), (xpos, ypos + 1)]
    return [
        (i, j) for i, j in out if 0 <= i < (width * scale) and 0 <= j < (height * scale)
    ]


def cost(data: np.ndarray, xpos: int, ypos: int) -> int:
    """Get the entry cost for a point
    Args:
        data: Input matrix tile
        xpos: x position of point
        ypos: y position of point
    Returns:
        Cost
    """
    height, width = data.shape
    val = data[ypos % height, xpos % width]
    val = val + xpos // width + ypos // height
    val = 1 + (val - 1) % 9
    return val


def dijkstra(data: np.ndarray, scale: int) -> int:
    """Dijkstra's algorithm to find the min cost of traversing the graph
    Args:
        data: Input 2D matrix tile
        scale: Expand the tile in both directions
    Returns:
        Min cost
    """
    height, width = data.shape
    distances = {(0, 0): 0}
    min_heap = [(0, (0, 0))]
    while min_heap:
        total, (i, j) = heapq.heappop(min_heap)
        if total <= distances[(i, j)]:
            for neigh in neighbors(i, j, height, width, scale):
                distance = total + cost(data, *neigh)
                if distance < distances.get(neigh, sys.maxsize):
                    distances[neigh] = distance
                    heapq.heappush(min_heap, (distance, neigh))

    return distances[(width * scale - 1, height * scale - 1)]


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    ans = dijkstra(data, 1)
    assert ans == 441
    print(f"Min risk: {ans}")

    scale = 5
    ans2 = dijkstra(data, scale)
    assert ans2 == 2849
    print(f"Min risk at scale of {scale}: {ans2}")


if __name__ == "__main__":
    main()
