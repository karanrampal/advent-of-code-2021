"""Bingo board"""

from typing import List

import numpy as np


class BingoBoard:
    """5x5 Bingo Boards"""

    def __init__(self, data: List[List[int]]) -> None:
        """Initialize a bingo board with data
        Args:
            data: 5x5 data to initialize the board
        """
        assert len(data) == 5, "Num rows of bingo board should be 5!"
        assert len(data[0]) == 5, "Num cols of bingo board should be 5!"

        self.board = np.array(data)
        self.ticks = np.zeros((5, 5), dtype=bool)

    def __str__(self) -> str:
        """Print an object
        Returns:
            board to print out
        """
        return self.board.__str__()

    def cross_out(self, val: int) -> None:
        """Cross out a value from the board
        Args:
            val: Value to cross out if exists on board
        """
        mask = self.board == val
        if mask.any():
            self.ticks[mask] = True

    def check(self) -> bool:
        """Check if bingo"""
        row_sum = self.ticks.sum(axis=0)
        if (row_sum == 5).any():
            return True
        col_sum = self.ticks.sum(axis=1)
        if (col_sum == 5).any():
            return True

        return False

    def score(self) -> int:
        """Score of the board
        Returns:
            Sum of all the non ticked numbers on the board
        """
        return self.board[~self.ticks].sum()
