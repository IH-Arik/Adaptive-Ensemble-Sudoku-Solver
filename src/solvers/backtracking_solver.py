"""
Backtracking Sudoku solver implementation.
"""

import copy
from typing import List, Optional, Callable
from .base_solver import BaseSolver


class BacktrackingSolver(BaseSolver):
    """
    Classic backtracking Sudoku solver.
    """
    
    def solve(self, board: List[List[int]], 
               update_ui: Optional[Callable] = None,
               evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Solve Sudoku using backtracking algorithm.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if puzzle is solved, False otherwise
        """
        self.reset()
        self.start_timing()
        
        result = self._backtrack(board, update_ui, evaluation_callback)
        
        self.end_timing()
        if not result:
            self.status = self.status.FAILED
        
        return result
    
    def _backtrack(self, board: List[List[int]], 
                   update_ui: Optional[Callable] = None,
                   evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Recursive backtracking algorithm.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if puzzle is solved, False otherwise
        """
        self.steps += 1
        empty = self.find_empty(board, evaluation_callback)
        if not empty:
            return True
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(board, row, col, num, evaluation_callback):
                board[row][col] = num
                
                # Update UI if callback provided
                if update_ui:
                    if not update_ui(row, col, num):
                        return False
                
                if self._backtrack(board, update_ui, evaluation_callback):
                    return True
                
                board[row][col] = 0
                if update_ui:
                    if not update_ui(row, col, 0):
                        return False
        
        return False
