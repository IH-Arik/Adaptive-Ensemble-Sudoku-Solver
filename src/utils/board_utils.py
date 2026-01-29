"""
Utility functions for Sudoku board operations.
"""

import copy
import random
from typing import List, Tuple, Optional
from ..algorithms.enums import Difficulty


class BoardUtils:
    """
    Utility class for Sudoku board operations.
    """
    
    @staticmethod
    def create_empty_board() -> List[List[int]]:
        """
        Create an empty 9x9 Sudoku board.
        
        Returns:
            Empty 9x9 board filled with zeros
        """
        return [[0 for _ in range(9)] for _ in range(9)]
    
    @staticmethod
    def copy_board(board: List[List[int]]) -> List[List[int]]:
        """
        Create a deep copy of a Sudoku board.
        
        Args:
            board: Source board
        
        Returns:
            Deep copy of the board
        """
        return copy.deepcopy(board)
    
    @staticmethod
    def board_to_string(board: List[List[int]]) -> str:
        """
        Convert board to string representation.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            String representation of the board
        """
        lines = []
        for i, row in enumerate(board):
            line = ""
            for j, val in enumerate(row):
                line += str(val) if val != 0 else "."
                if j % 3 == 2 and j < 8:
                    line += "|"
            lines.append(line)
            if i % 3 == 2 and i < 8:
                lines.append("-" * 11)
        return "\n".join(lines)
    
    @staticmethod
    def string_to_board(board_string: str) -> List[List[int]]:
        """
        Convert string representation to board.
        
        Args:
            board_string: String representation of the board
        
        Returns:
            9x9 Sudoku board
        """
        board = []
        lines = board_string.strip().split('\n')
        for line in lines:
            if line.startswith('-'):
                continue
            row = []
            for char in line:
                if char == '|':
                    continue
                elif char == '.':
                    row.append(0)
                elif char.isdigit():
                    row.append(int(char))
            if row:
                board.append(row)
        return board
    
    @staticmethod
    def is_valid_board(board: List[List[int]]) -> bool:
        """
        Check if a board is valid (no rule violations).
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            True if board is valid, False otherwise
        """
        # Check dimensions
        if len(board) != 9 or any(len(row) != 9 for row in board):
            return False
        
        # Check values
        for i in range(9):
            for j in range(9):
                val = board[i][j]
                if not (0 <= val <= 9):
                    return False
                if val != 0:
                    # Check row
                    if board[i].count(val) > 1:
                        return False
                    # Check column
                    if [board[k][j] for k in range(9)].count(val) > 1:
                        return False
                    # Check box
                    box_row, box_col = 3 * (i // 3), 3 * (j // 3)
                    box_values = []
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if board[r][c] == val:
                                box_values.append(val)
                    if len(box_values) > 1:
                        return False
        return True
    
    @staticmethod
    def count_empty_cells(board: List[List[int]]) -> int:
        """
        Count the number of empty cells in the board.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            Number of empty cells
        """
        return sum(1 for row in board for val in row if val == 0)
    
    @staticmethod
    def get_filled_cells(board: List[List[int]]) -> List[Tuple[int, int, int]]:
        """
        Get all filled cells with their values.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            List of tuples (row, col, value) for filled cells
        """
        filled = []
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    filled.append((i, j, board[i][j]))
        return filled
    
    @staticmethod
    def get_empty_cells(board: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Get all empty cells.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            List of tuples (row, col) for empty cells
        """
        empty = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    empty.append((i, j))
        return empty
    
    @staticmethod
    def calculate_difficulty(board: List[List[int]]) -> Difficulty:
        """
        Calculate puzzle difficulty based on number of empty cells.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            Difficulty level
        """
        empty_count = BoardUtils.count_empty_cells(board)
        
        if empty_count <= 40:
            return Difficulty.EASY
        elif empty_count <= 52:
            return Difficulty.MEDIUM
        elif empty_count <= 59:
            return Difficulty.HARD
        else:
            return Difficulty.VERY_HARD
    
    @staticmethod
    def get_cells_to_remove(difficulty: Difficulty) -> int:
        """
        Get number of cells to remove for given difficulty.
        
        Args:
            difficulty: Difficulty level
        
        Returns:
            Number of cells to remove
        """
        if difficulty == Difficulty.EASY:
            return random.randint(40, 45)
        elif difficulty == Difficulty.MEDIUM:
            return random.randint(46, 52)
        elif difficulty == Difficulty.HARD:
            return random.randint(53, 59)
        else:  # VERY_HARD
            return random.randint(60, 64)
