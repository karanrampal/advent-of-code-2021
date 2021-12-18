#!/usr/bin/env python3
"""Submarine position"""

import argparse
import logging
import re
from pathlib import Path
from typing import List, Tuple


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Calculate submarine position")
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


def read_file(file_path: Path) -> Tuple[int, int, int, int]:
    """Read file from file path
    Args:
        file_path: Path of input file
    Returns:
        read data
    """
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    try:
        with file_path.open("r") as fptr:
            line = fptr.read().strip()
            match = re.search(r"x=(\d+)..(\d+), y=(-\d+)..(-\d+)", line)
            if match:
                xmin = int(match.group(1))
                xmax = int(match.group(2))
                ymin = int(match.group(3))
                ymax = int(match.group(4))
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return xmin, xmax, ymin, ymax


def simulate(
    velocity: Tuple[int, int], target: Tuple[int, int, int, int]
) -> Tuple[bool, int]:
    """Simulate probe trajectory and return whether it goes inside target
    Args:
        velocity: Initial x, y velocity
        target: Min/Max x, y position of target area
    Returns:
        If the probe reaches target and max height reached
    """
    vel_x, vel_y = velocity
    xmin, xmax, ymin, ymax = target

    xpos, ypos = 0, 0
    step = 1000
    max_ht = 0
    reached = False
    while step:
        step -= 1
        xpos += vel_x
        ypos += vel_y
        max_ht = max(max_ht, ypos)
        if (xmin <= xpos <= xmax) and (ymin <= ypos <= ymax):
            reached = True
            break
        if (xpos > xmax) or (ypos < ymin):
            break
        vel_x -= 1 if vel_x > 0 else -1 if vel_x < 0 else 0
        vel_y -= 1

    return reached, max_ht


def run(
    target: Tuple[int, int, int, int], xrange: Tuple[int, int], yrange: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    """Run the sumulation
    Args:
        target: Min/Max x, y position of target area
    Returns:
        Max value of y height possible
    """
    xmin, xmax, ymin, ymax = target

    out = []
    max_height = 0
    for x_init in range(*xrange):
        for y_init in range(*yrange):
            reached, max_ht = simulate((x_init, y_init), (xmin, xmax, ymin, ymax))
            if reached:
                out.append((x_init, y_init))
                max_height = max(max_height, max_ht)

    return out, max_height


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)

    output, ans = run(data, (1, 500), (-500, 500))
    assert ans == 5886
    print(f"Max height reached: {ans}")
    print(f"All valid velocities: {len(output)}")


if __name__ == "__main__":
    main()
