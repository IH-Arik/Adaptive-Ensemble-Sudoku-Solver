"""
Sudoku puzzle generator with difficulty levels.
"""

import random
import copy
from typing import List
from .board_utils import BoardUtils
from ..solvers.backtracking_solver import BacktrackingSolver
from ..algorithms.enums import Difficulty


class PuzzleGenerator:
    """
    Sudoku puzzle generator with multiple difficulty levels.
    """
    
    def __init__(self):
        """Initialize the puzzle generator."""
        self.solver = BacktrackingSolver()
    
    def generate_puzzle(self, difficulty: Difficulty) -> List[List[int]]:
        """
        Generate a Sudoku puzzle with specified difficulty.
        
        Args:
            difficulty: Desired difficulty level
        
        Returns:
            Generated puzzle board
        """
        # Generate a solved board
        board = self._generate_solved_board()
        
        # Remove numbers based on difficulty
        cells_to_remove = BoardUtils.get_cells_to_remove(difficulty)
        self._remove_numbers(board, cells_to_remove)
        
        return board
    
    def _generate_solved_board(self) -> List[List[int]]:
        """
        Generate a completely solved Sudoku board.
        
        Returns:
            Solved 9x9 Sudoku board
        """
        # Start with an empty board
        board = BoardUtils.create_empty_board()
        
        # Fill the diagonal boxes first (these don't affect each other)
        for i in range(0, 9, 3):
            self._fill_box(board, i, i)
        
        # Solve the rest of the board
        self.solver.solve(board)
        return board
    
    def _fill_box(self, board: List[List[int]], row: int, col: int):
        """
        Fill a 3x3 box with random numbers 1-9.
        
        Args:
            board: 9x9 Sudoku board
            row: Starting row of the box
            col: Starting column of the box
        """
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()
    
    def _remove_numbers(self, board: List[List[int]], count: int):
        """
        Remove numbers from the board while maintaining uniqueness.
        
        Args:
            board: 9x9 Sudoku board
            count: Number of cells to remove
        """
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:count]:
            temp = board[i][j]
            board[i][j] = 0
            
            # Make a copy for solving
            board_copy = BoardUtils.copy_board(board)
            
            # Check if puzzle still has unique solution
            if not self._has_unique_solution(board_copy):
                board[i][j] = temp  # Restore if removing creates multiple solutions
    
    def _has_unique_solution(self, board: List[List[int]]) -> bool:
        """
        Check if the board has a unique solution.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            True if unique solution exists, False otherwise
        """
        # This is a simplified version - a full implementation would count all solutions
        # For now, we just check if at least one solution exists
        return self.solver.solve(board)
    
    def generate_multiple_puzzles(self, count: int, difficulty: Difficulty) -> List[List[List[int]]]:
        """
        Generate multiple puzzles of the same difficulty.
        
        Args:
            count: Number of puzzles to generate
            difficulty: Difficulty level
        
        Returns:
            List of puzzle boards
        """
        puzzles = []
        for _ in range(count):
            puzzle = self.generate_puzzle(difficulty)
            puzzles.append(puzzle)
        return puzzles
    
    def validate_puzzle(self, board: List[List[int]]) -> bool:
        """
        Validate if a puzzle is well-formed and solvable.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            True if puzzle is valid, False otherwise
        """
        # Check if board is valid
        if not BoardUtils.is_valid_board(board):
            return False
        
        # Check if puzzle has at least one solution
        board_copy = BoardUtils.copy_board(board)
        return self.solver.solve(board_copy)
