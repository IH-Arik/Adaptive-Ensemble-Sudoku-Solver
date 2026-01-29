"""
Configuration settings for the Adaptive Ensemble Sudoku Solver.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class SolverConfig:
    """Configuration for individual solvers."""
    
    # Performance settings
    max_steps: int = 1000000
    timeout_seconds: float = 60.0
    
    # Visualization settings
    enable_visualization: bool = True
    step_delay: float = 0.05
    evaluation_delay: float = 0.025
    
    # Logging settings
    log_steps: bool = True
    log_evaluations: bool = True
    log_time: bool = True


@dataclass
class GUIConfig:
    """Configuration for GUI components."""
    
    # Window settings
    window_title: str = "Adaptive Ensemble Sudoku Solver"
    window_width: int = 1000
    window_height: int = 750
    min_width: int = 900
    min_height: int = 700
    
    # Grid settings
    cell_size: int = 55
    grid_padding: int = 10
    
    # Colors
    background_color: str = "#f5f5f5"
    cell_background: str = "white"
    original_cell_color: str = "#e0e0e0"
    original_cell_text: str = "#000080"
    highlight_color: str = "#ffeb99"
    evaluation_color: str = "#e6f7ff"
    solution_color: str = "#e6fffb"
    
    # Fonts
    cell_font: tuple = ("Helvetica", 16, "bold")
    header_font: tuple = ("Helvetica", 20, "bold")
    normal_font: tuple = ("Helvetica", 11)
    stats_font: tuple = ("Helvetica", 10)


@dataclass
class PuzzleConfig:
    """Configuration for puzzle generation."""
    
    # Difficulty settings
    default_difficulty: str = "MEDIUM"
    ensure_unique_solution: bool = True
    
    # Generation settings
    max_generation_attempts: int = 100
    validation_enabled: bool = True


@dataclass
class EvaluationConfig:
    """Configuration for performance evaluation."""
    
    # Benchmark settings
    benchmark_puzzles_count: int = 100
    benchmark_difficulties: list = None
    
    # Comparison settings
    compare_all_algorithms: bool = True
    statistical_significance: bool = True
    
    # Output settings
    generate_reports: bool = True
    save_results: bool = True
    results_directory: str = "results"
    
    def __post_init__(self):
        if self.benchmark_difficulties is None:
            self.benchmark_difficulties = ["Easy", "Medium", "Hard", "Very Hard"]


@dataclass
class ProjectConfig:
    """Overall project configuration."""
    
    # Project info
    project_name: str = "Adaptive Ensemble Sudoku Solver"
    version: str = "1.0.0"
    description: str = "An Adaptive and Intelligent Ensemble Framework for Efficient Sudoku Solving"
    
    # Paths
    root_dir: str = os.getcwd()
    src_dir: str = "src"
    data_dir: str = "data"
    results_dir: str = "results"
    logs_dir: str = "logs"
    
    # Sub-configurations
    solver: SolverConfig = SolverConfig()
    gui: GUIConfig = GUIConfig()
    puzzle: PuzzleConfig = PuzzleConfig()
    evaluation: EvaluationConfig = EvaluationConfig()
    
    def __post_init__(self):
        # Create absolute paths
        self.src_dir = os.path.join(self.root_dir, self.src_dir)
        self.data_dir = os.path.join(self.root_dir, self.data_dir)
        self.results_dir = os.path.join(self.root_dir, self.results_dir)
        self.logs_dir = os.path.join(self.root_dir, self.logs_dir)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'project': {
                'name': self.project_name,
                'version': self.version,
                'description': self.description
            },
            'solver': {
                'max_steps': self.solver.max_steps,
                'timeout_seconds': self.solver.timeout_seconds,
                'enable_visualization': self.solver.enable_visualization,
                'step_delay': self.solver.step_delay
            },
            'gui': {
                'window_width': self.gui.window_width,
                'window_height': self.gui.window_height,
                'cell_size': self.gui.cell_size
            },
            'puzzle': {
                'default_difficulty': self.puzzle.default_difficulty,
                'ensure_unique_solution': self.puzzle.ensure_unique_solution
            },
            'evaluation': {
                'benchmark_puzzles_count': self.evaluation.benchmark_puzzles_count,
                'generate_reports': self.evaluation.generate_reports,
                'save_results': self.evaluation.save_results
            }
        }


# Global configuration instance
config = ProjectConfig()
