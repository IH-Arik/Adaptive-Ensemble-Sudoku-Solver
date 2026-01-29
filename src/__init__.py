"""
Adaptive Ensemble Sudoku Solver

An Adaptive and Intelligent Ensemble Framework for Efficient Sudoku Solving
integrating classical Constraint Satisfaction Problem (CSP) techniques.
"""

__version__ = "1.0.0"
__author__ = "Research Team"
__email__ = "research@example.com"

from .algorithms.enums import Algorithm, Difficulty, SolverStatus
from .solvers.solver_factory import SolverFactory
from .solvers.base_solver import BaseSolver
from .utils.board_utils import BoardUtils
from .utils.puzzle_generator import PuzzleGenerator
from .evaluation.performance_analyzer import PerformanceAnalyzer
from .utils.config import config

__all__ = [
    "Algorithm",
    "Difficulty", 
    "SolverStatus",
    "SolverFactory",
    "BaseSolver",
    "BoardUtils",
    "PuzzleGenerator",
    "PerformanceAnalyzer",
    "config"
]
