#!/usr/bin/env python3
"""Submarine position"""

import argparse
import logging
from pathlib import Path
from typing import Dict, List


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
        default=Path("./inps.txt"),
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


def submarine_position(data: List[str]) -> int:
    """Calculate the position of the submarine
    Args:
        data: direction and value travelled by the submarine
    Returns:
        Positon of the submarine
    """
    if not data:
        logging.error("Data is empty!")
        return -1

    travel_dict: Dict = {}
    for line in data:
        direction, val = line.split()
        tmp = travel_dict.get(direction, 0)
        travel_dict[direction] = tmp + int(val)

    return travel_dict["forward"] * (travel_dict["down"] - travel_dict["up"])


def submarine_position_new(data: List[str]) -> int:
    """Calculate the position of the submarine
    Args:
        data: direction and value travelled by the submarine
    Returns:
        Positon of the submarine
    """
    if not data:
        logging.error("Data is empty!")
        return -1

    aim, depth, horizontal_pos = 0, 0, 0
    for line in data:
        direction, val = line.split()
        if direction == "forward":
            horizontal_pos += int(val)
            depth += aim * int(val)
        elif direction == "down":
            aim += int(val)
        else:
            aim -= int(val)

    return horizontal_pos * depth


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    logging.info("Starting ...")
    lines = read_file(args.file_path)
    print(f"Submarine position: {submarine_position(lines)}")
    print(f"New submarine position: {submarine_position_new(lines)}")
    logging.info("Finished ...")


if __name__ == "__main__":
    main()
