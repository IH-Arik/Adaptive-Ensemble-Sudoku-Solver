"""
Enumerations for Sudoku solving algorithms and difficulty levels.
"""

from enum import Enum


class Algorithm(Enum):
    """Enumeration of available Sudoku solving algorithms."""
    BACKTRACKING = "Backtracking"
    DFS = "Depth-First Search"
    BFS = "Breadth-First Search"
    HEURISTIC = "Heuristic Search"
    MRV = "Minimum Remaining Values"
    FORWARD_CHECKING = "Forward Checking"
    ARC_CONSISTENCY = "Arc Consistency"


class Difficulty(Enum):
    """Enumeration of puzzle difficulty levels."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    VERY_HARD = "Very Hard"


class SolverStatus(Enum):
    """Enumeration for solver status."""
    READY = "Ready"
    SOLVING = "Solving"
    PAUSED = "Paused"
    STOPPED = "Stopped"
    COMPLETED = "Completed"
    FAILED = "Failed"
