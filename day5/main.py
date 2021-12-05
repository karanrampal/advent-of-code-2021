#!/usr/bin/env python3
"""Line intersection"""

import argparse
import logging
from pathlib import Path
from typing import List, Tuple


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


def main() -> None:
    """Main function"""
    args = arg_parser()
    setup_logger(args.log_path)

    data = read_file(args.file_path)


if __name__ == "__main__":
    main()
