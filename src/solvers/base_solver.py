"""
Base Sudoku solver class with common functionality.
"""

import time
from typing import List, Tuple, Optional, Callable
from ..algorithms.enums import Algorithm, SolverStatus


class BaseSolver:
    """
    Base class for Sudoku solvers providing common functionality.
    """
    
    def __init__(self):
        """Initialize the base solver."""
        self.steps = 0
        self.evaluations = 0
        self.status = SolverStatus.READY
        self.start_time = None
        self.end_time = None
        
    def reset(self):
        """Reset solver statistics."""
        self.steps = 0
        self.evaluations = 0
        self.status = SolverStatus.READY
        self.start_time = None
        self.end_time = None
    
    def start_timing(self):
        """Start timing the solving process."""
        self.start_time = time.time()
        self.status = SolverStatus.SOLVING
    
    def end_timing(self):
        """End timing the solving process."""
        self.end_time = time.time()
        if self.status == SolverStatus.SOLVING:
            self.status = SolverStatus.COMPLETED
    
    def get_solve_time(self) -> float:
        """Get the time taken to solve the puzzle."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def is_valid(self, board: List[List[int]], row: int, col: int, num: int, 
                 evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Check if placing num at board[row][col] is valid.
        
        Args:
            board: 9x9 Sudoku board
            row: Row index
            col: Column index
            num: Number to place
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if placement is valid, False otherwise
        """
        if evaluation_callback:
            evaluation_callback(row, col)
        
        self.evaluations += 1
        
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def find_empty(self, board: List[List[int]], 
                   evaluation_callback: Optional[Callable] = None) -> Optional[Tuple[int, int]]:
        """
        Find the first empty cell in the board.
        
        Args:
            board: 9x9 Sudoku board
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            Tuple of (row, col) if empty cell found, None otherwise
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if evaluation_callback:
                        evaluation_callback(i, j)
                    return (i, j)
        return None
    
    def is_solved(self, board: List[List[int]]) -> bool:
        """
        Check if the puzzle is solved.
        
        Args:
            board: 9x9 Sudoku board
        
        Returns:
            True if solved, False otherwise
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False
        return True
    
    def get_statistics(self) -> dict:
        """
        Get solver statistics.
        
        Returns:
            Dictionary containing solver statistics
        """
        return {
            'algorithm': self.__class__.__name__,
            'steps': self.steps,
            'evaluations': self.evaluations,
            'solve_time': self.get_solve_time(),
            'status': self.status.value
        }
