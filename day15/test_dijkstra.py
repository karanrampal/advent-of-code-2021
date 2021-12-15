"""Tests for day 15"""

import os
from pathlib import Path

from main import dijkstra, read_file


def test_dijkstra():
    """Test dijkstra's algo"""
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    print(type(path))
    data = read_file(Path(path + "/inputs.txt"))
    ans2 = dijkstra(data, 1)
    assert ans2 == 441
