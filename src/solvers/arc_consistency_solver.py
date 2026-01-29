"""
Arc Consistency (AC-3) Sudoku solver implementation.
"""

import copy
from typing import List, Optional, Callable, Dict, Set, Tuple
from .base_solver import BaseSolver


class ArcConsistencySolver(BaseSolver):
    """
    Sudoku solver using Arc Consistency (AC-3) algorithm combined with backtracking.
    """
    
    def __init__(self):
        """Initialize the arc consistency solver."""
        super().__init__()
        self.domains: Dict[Tuple[int, int], Set[int]] = {}
    
    def solve(self, board: List[List[int]], 
               update_ui: Optional[Callable] = None,
               evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Solve Sudoku using Arc Consistency combined with backtracking.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if puzzle is solved, False otherwise
        """
        self.reset()
        self.domains.clear()
        self.start_timing()
        
        # First, apply AC-3
        if not self._ac3(board, update_ui, evaluation_callback):
            self.end_timing()
            self.status = self.status.FAILED
            return False
        
        # If puzzle not solved, use backtracking with the reduced domains
        if any(board[i][j] == 0 for i in range(9) for j in range(9)):
            result = self._backtrack_with_ac3(board, update_ui, evaluation_callback)
        else:
            result = True
        
        self.end_timing()
        if not result:
            self.status = self.status.FAILED
        
        return result
    
    def get_domain(self, board: List[List[int]], row: int, col: int) -> Set[int]:
        """
        Get the domain of possible values for a cell.
        
        Args:
            board: 9x9 Sudoku board
            row: Row index
            col: Column index
        
        Returns:
            Set of possible values for the cell
        """
        if board[row][col] != 0:
            return {board[row][col]}
        
        domain = set(range(1, 10))
        
        # Check row
        for j in range(9):
            if board[row][j] != 0:
                domain.discard(board[row][j])
        
        # Check column
        for i in range(9):
            if board[i][col] != 0:
                domain.discard(board[i][col])
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] != 0:
                    domain.discard(board[start_row + i][start_col + j])
        
        return domain
    
    def get_arcs(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get all arcs (constraints between cells) in the Sudoku grid.
        
        Returns:
            List of arcs representing constraints
        """
        arcs = []
        # Generate arcs for rows, columns, and boxes
        for i in range(9):
            for j in range(9):
                # Row arcs
                for k in range(9):
                    if k != j:
                        arcs.append(((i, j), (i, k)))
                # Column arcs
                for k in range(9):
                    if k != i:
                        arcs.append(((i, j), (k, j)))
                # Box arcs
                box_row, box_col = 3 * (i // 3), 3 * (j // 3)
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r, c) != (i, j):
                            arcs.append(((i, j), (r, c)))
        return arcs
    
    def revise(self, board: List[List[int]], xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
        """
        Revise the domain of xi with respect to xj.
        
        Args:
            board: 9x9 Sudoku board
            xi: First cell (row, col)
            xj: Second cell (row, col)
        
        Returns:
            True if domain was revised, False otherwise
        """
        revised = False
        i, j = xi
        if board[i][j] != 0:  # Skip if cell already has a value
            return False
        
        if (i, j) not in self.domains:
            self.domains[(i, j)] = self.get_domain(board, i, j)
        
        domain_i = self.domains[(i, j)]
        domain_j = self.get_domain(board, xj[0], xj[1])
        
        for x in list(domain_i):
            # If xi=x conflicts with all possible values in xj's domain
            if len(domain_j) == 1 and x in domain_j:
                domain_i.discard(x)
                revised = True
        
        self.domains[(i, j)] = domain_i
        return revised
    
    def _ac3(self, board: List[List[int]], 
              update_ui: Optional[Callable] = None,
              evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Implement AC-3 algorithm for arc consistency.
        
        Args:
            board: 9x9 Sudoku board
            update_ui: Optional callback for UI updates
            evaluation_callback: Optional callback for evaluation visualization
        
        Returns:
            True if arc consistency achieved, False if contradiction found
        """
        # Initialize queue with all arcs
        queue = self.get_arcs()
        
        while queue:
            self.steps += 1
            (xi, xj) = queue.pop(0)
            
            if evaluation_callback:
                evaluation_callback(xi[0], xi[1])
            
            if self.revise(board, xi, xj):
                if not self.domains[xi]:  # Domain is empty
                    return False
                
                # Add neighbors of xi back to queue
                neighbors = [(xi[0], k) for k in range(9) if k != xi[1]]  # Row neighbors
                neighbors += [(k, xi[1]) for k in range(9) if k != xi[0]]  # Column neighbors
                box_row, box_col = 3 * (xi[0] // 3), 3 * (xi[1] // 3)
                neighbors += [(r, c) for r in range(box_row, box_row + 3)
                            for c in range(box_col, box_col + 3)
                            if (r, c) != xi]  # Box neighbors
                
                for xk in neighbors:
                    if xk != xj:
                        queue.append((xk, xi))
        
        # After AC-3, try to fill in determined values
        filled = False
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0 and (i, j) in self.domains:
                    if len(self.domains[(i, j)]) == 1:
                        board[i][j] = list(self.domains[(i, j)])[0]
                        if update_ui:
                            if not update_ui(i, j, board[i][j]):
                                return False
                        filled = True
        
        # If we filled some values, run AC-3 again
        if filled:
            return self._ac3(board, update_ui, evaluation_callback)
        
        return True
    
    def _backtrack_with_ac3(self, board: List[List[int]], 
                            update_ui: Optional[Callable] = None,
                            evaluation_callback: Optional[Callable] = None) -> bool:
        """
        Backtracking with AC-3 preprocessed domains.
        
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
        domain = self.domains.get((row, col), self.get_domain(board, row, col))
        
        for num in domain:
            if self.is_valid(board, row, col, num, evaluation_callback):
                board[row][col] = num
                
                if update_ui:
                    if not update_ui(row, col, num):
                        return False
                
                # Apply AC-3 after each assignment
                old_domains = self.domains.copy()
                if self._ac3(board, update_ui, evaluation_callback):
                    if self._backtrack_with_ac3(board, update_ui, evaluation_callback):
                        return True
                
                # Restore domains if this branch fails
                self.domains = old_domains
                board[row][col] = 0
                if update_ui:
                    if not update_ui(row, col, 0):
                        return False
        
        return False
