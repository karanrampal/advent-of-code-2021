#!/usr/bin/env python3
"""Graph search"""

import argparse
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Union


def args_parser() -> argparse.Namespace:
    """Parse CLI arguments
    Returns:
        argument parser
    """
    parser = argparse.ArgumentParser(description="Find all the paths in a graph")
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


def read_file(file_path: Path) -> List[List[str]]:
    """Read file from file path
    Args:
        file_path: Path of input file
    """
    lines = []
    try:
        with file_path.open("r") as fptr:
            for line in fptr:
                lines.append(line.strip().split("-"))
    except FileNotFoundError:
        logging.warning("No such file exists '%s'!", file_path)

    return lines


def create_graph(data: List[List[str]]) -> Dict[str, List[str]]:
    """Create a graph
    Args:
        data: Input data in the form of [["src", "target"] ... ]
    Returns:
        Graph
    """
    graph = defaultdict(list)
    for line in data:
        graph[line[0]].append(line[1])
        graph[line[1]].append(line[0])

    return graph


def _dfs(
    graph: Dict[str, List[str]],
    node: str,
    cur_path: str,
    paths: List[str],
    allow_once: bool,
) -> Union[str, None]:
    """Depth first search helper
    Args:
        graph: All the nodes and edges
        node: Current node
        cur_path: Current path in string
        paths: All the valid paths
        allow_once: Allow one small cave
    Returns:
        Current comma separated path or empty string
    """
    if node == "end":
        return cur_path + ",end"
    elif node.islower():
        if node in cur_path:
            if allow_once:
                return ""
            else:
                allow_once = True
    for child in graph[node]:
        if child != "start":
            val = _dfs(graph, child, cur_path + "," + node, paths, allow_once)
            if val:
                paths.append(val)

    return None


def dfs(graph: Dict[str, List[str]], mode: bool) -> List[str]:
    """Depth first search
    Args:
        graph: All the nodes and edges
        mode: Allow one small cave or not
    Returns:
        All the valid paths
    """
    paths: List[str] = []
    for child in graph["start"]:
        if mode:
            _dfs(graph, child, "start", paths, False)
        else:
            _dfs(graph, child, "start", paths, True)

    return paths


def main() -> None:
    """Main function"""
    args = args_parser()
    setup_logger(args.log_path)

    lines = read_file(args.file_path)

    graph = create_graph(lines)
    paths = dfs(graph, mode=False)
    assert len(paths) == 3761
    print(f"Number of valid paths: {len(paths)}")

    paths = dfs(graph, mode=True)
    assert len(paths) == 99138
    print(f"Number of valid paths when one small cave is allowed: {len(paths)}")


if __name__ == "__main__":
    main()
