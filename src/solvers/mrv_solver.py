"""
Minimum Remaining Values (MRV) Sudoku solver implementation.
"""

from typing import List, Optional, Callable
from .base_solver import BaseSolver


class MRVSolver(BaseSolver):
    """
    Sudoku solver using Minimum Remaining Values heuristic.
    """
    
    def solve(self, board: List[List[int]], 
               update_ui: Optional[Callable] = None,
               evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Solve Sudoku using MRV heuristic.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if puzzle is solved, False otherwise
        """
        self.reset()
        self.start_timing()
        
        result = self._mrv_search(board, update_ui, evaluation_callback)
        
        self.end_timing()
        if not result:
            self.status = self.status.FAILED
        
        return result
    
    def _get_legal_values(self, board: List[List[int]], row: int, col: int,
                         evaluation_callback: Optional[Callable] = None) -> List[int]:
        """
        Get legal values for a specific cell.
        
        Args:
            board: 9x9 Sudoku board
            row: Row index
            col: Column index
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            List of legal values for the cell
        """
        legal = []
        for num in range(1, 10):
            if self.is_valid(board, row, col, num, evaluation_callback):
                legal.append(num)
        return legal
    
    def _find_mrv(self, board: List[List[int]], 
                  evaluation_callback: Optional[Callable] = None) -> Optional[tuple]:
        """
        Find cell with minimum remaining values.
        
        Args:
            board: 9x9 Sudoku board
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            Tuple of (row, col, legal_values) for MRV cell, None if no empty cells
        """
        min_remaining = 10
        min_pos = None
        
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    if evaluation_callback:
                        evaluation_callback(i, j)
                    
                    legal_values = self._get_legal_values(board, i, j, evaluation_callback)
                    if len(legal_values) < min_remaining:
                        min_remaining = len(legal_values)
                        min_pos = (i, j, legal_values)
                    
                    # If we find a cell with no legal values, fail fast
                    if min_remaining == 0:
                        return min_pos
        
        return min_pos
    
    def _mrv_search(self, board: List[List[int]], 
                    update_ui: Optional[Callable] = None,
                    evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Search using MRV heuristic.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if puzzle is solved, False otherwise
        """
        self.steps += 1
        
        # Find cell with minimum remaining values
        mrv = self._find_mrv(board, evaluation_callback)
        if not mrv:
            return True  # No empty cells
        
        row, col, legal_values = mrv
        
        # If no legal values for a cell, this branch fails
        if not legal_values:
            return False
        
        for num in legal_values:
            board[row][col] = num
            
            # Update UI
            if update_ui:
                if not update_ui(row, col, num):
                    return False
            
            if self._mrv_search(board, update_ui, evaluation_callback):
                return True
            
            board[row][col] = 0
            if update_ui:
                if not update_ui(row, col, 0):
                    return False
        
        return False
