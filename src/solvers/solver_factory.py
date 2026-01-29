"""
Factory class for creating different Sudoku solvers.
"""

from typing import Dict, Type
from .base_solver import BaseSolver
from .backtracking_solver import BacktrackingSolver
from .mrv_solver import MRVSolver
from .arc_consistency_solver import ArcConsistencySolver
from ..algorithms.enums import Algorithm


class SolverFactory:
    """
    Factory class for creating Sudoku solver instances.
    """
    
    _solvers: Dict[Algorithm, Type[BaseSolver]] = {
        Algorithm.BACKTRACKING: BacktrackingSolver,
        Algorithm.MRV: MRVSolver,
        Algorithm.ARC_CONSISTENCY: ArcConsistencySolver,
        # Add more solvers as they are implemented
        # Algorithm.DFS: DFSSolver,
        # Algorithm.BFS: BFSSolver,
        # Algorithm.HEURISTIC: HeuristicSolver,
        # Algorithm.FORWARD_CHECKING: ForwardCheckingSolver,
    }
    
    @classmethod
    def create_solver(cls, algorithm: Algorithm) -> BaseSolver:
        """
        Create a solver instance based on the specified algorithm.
        
        Args:
            algorithm: The algorithm to use
        
        Returns:
            Solver instance
        
        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in cls._solvers:
            raise ValueError(f"Algorithm {algorithm.value} is not supported. "
                           f"Supported algorithms: {[algo.value for algo in cls._solvers.keys()]}")
        
        solver_class = cls._solvers[algorithm]
        return solver_class()
    
    @classmethod
    def get_available_algorithms(cls) -> list:
        """
        Get list of available algorithms.
        
        Returns:
            List of available algorithms
        """
        return list(cls._solvers.keys())
    
    @classmethod
    def register_solver(cls, algorithm: Algorithm, solver_class: Type[BaseSolver]):
        """
        Register a new solver class.
        
        Args:
            algorithm: Algorithm enum
            solver_class: Solver class
        """
        cls._solvers[algorithm] = solver_class
    
    @classmethod
    def get_solver_info(cls) -> Dict[str, str]:
        """
        Get information about available solvers.
        
        Returns:
            Dictionary with algorithm names as keys and descriptions as values
        """
        return {
            Algorithm.BACKTRACKING.value: "Classic backtracking algorithm with recursive search",
            Algorithm.MRV.value: "Minimum Remaining Values heuristic for optimized variable selection",
            Algorithm.ARC_CONSISTENCY.value: "AC-3 algorithm with arc consistency and backtracking",
            # Add descriptions for other algorithms as they are implemented
        }
