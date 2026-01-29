# Adaptive Ensemble Sudoku Solver

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Research](https://img.shields.io/badge/status-research-orange.svg)](https://github.com/IH-Arik/Adaptive-Ensemble-Sudoku-Solver)

## Overview

This repository contains the implementation of **Adaptive Ensemble Sudoku Solver**, an intelligent framework that integrates classical Constraint Satisfaction Problem (CSP) techniques for efficient Sudoku solving. The project combines multiple algorithms including backtracking, heuristic search, and consistency methods to provide optimal solving performance.

## Key Features

- **Multiple Solving Algorithms**: Backtracking, Depth-First Search, Breadth-First Search, Heuristic Search, MRV, Forward Checking, Arc Consistency
- **Adaptive Framework**: Intelligent algorithm selection based on puzzle characteristics
- **Performance Analysis**: Comprehensive benchmarking and comparison tools
- **Interactive GUI**: Modern interface with real-time visualization
- **Puzzle Generation**: Automatic generation with difficulty levels
- **Statistical Analysis**: Detailed performance metrics and reporting

## Project Structure

```
Adaptive-Ensemble-Sudoku-Solver/
├── src/                          # Source code
│   ├── algorithms/               # Algorithm enumerations
│   │   └── enums.py             # Algorithm and difficulty enums
│   ├── solvers/                  # Solver implementations
│   │   ├── base_solver.py       # Base solver class
│   │   ├── backtracking_solver.py # Backtracking algorithm
│   │   ├── mrv_solver.py        # MRV heuristic solver
│   │   ├── arc_consistency_solver.py # AC-3 algorithm
│   │   └── solver_factory.py    # Factory for creating solvers
│   ├── utils/                    # Utility functions
│   │   ├── board_utils.py       # Board manipulation utilities
│   │   ├── puzzle_generator.py  # Puzzle generation
│   │   └── config.py            # Configuration management
│   ├── evaluation/               # Performance analysis
│   │   └── performance_analyzer.py # Benchmarking tools
│   └── gui/                      # GUI components (original implementation)
├── notebooks/                    # Research notebooks
│   └── game.py                  # Original implementation with GUI
├── examples/                     # Usage examples
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── configs/                      # Configuration files
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/IH-Arik/Adaptive-Ensemble-Sudoku-Solver.git
cd Adaptive-Ensemble-Sudoku-Solver

# Install dependencies
pip install -r requirements.txt

# Install the package (optional)
pip install -e .
```

### Basic Usage

```python
from src import SolverFactory, PuzzleGenerator, PerformanceAnalyzer
from src.algorithms import Algorithm, Difficulty

# Create a puzzle
generator = PuzzleGenerator()
puzzle = generator.generate_puzzle(Difficulty.MEDIUM)

# Solve with different algorithms
factory = SolverFactory()
solver = factory.create_solver(Algorithm.BACKTRACKING)

# Copy the puzzle to preserve original
board_to_solve = [row[:] for row in puzzle]

# Solve the puzzle
success = solver.solve(board_to_solve)

if success:
    print(f"Puzzle solved in {solver.get_solve_time():.4f} seconds")
    print(f"Steps: {solver.steps}, Evaluations: {solver.evaluations}")
else:
    print("Could not solve the puzzle")
```

### Performance Comparison

```python
# Compare multiple algorithms
analyzer = PerformanceAnalyzer()
results = analyzer.compare_algorithms(puzzle)

# Generate report
report = analyzer.generate_report(results)
print(report)
```

## Supported Algorithms

### Classical Algorithms

1. **Backtracking**: Classic recursive backtracking with constraint propagation
2. **Depth-First Search (DFS)**: Iterative DFS implementation with stack-based exploration
3. **Breadth-First Search (BFS)**: BFS with queue-based state exploration

### Heuristic Algorithms

4. **Heuristic Search**: Frequency-based heuristic for optimal number selection
5. **Minimum Remaining Values (MRV)**: Variable ordering heuristic for efficient search

### Consistency Algorithms

6. **Forward Checking**: Local consistency checking with domain reduction
7. **Arc Consistency (AC-3)**: Global arc consistency with backtracking

### Algorithm Performance

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Backtracking | O(9^n) | O(n) | General puzzles |
| DFS | O(9^n) | O(n²) | Deep search trees |
| BFS | O(9^n) | O(9^n) | Shallow solutions |
| Heuristic | O(9^n) | O(n) | Speed optimization |
| MRV | O(9^n) | O(n) | Complex puzzles |
| Forward Checking | O(9^n) | O(n²) | Constraint propagation |
| AC-3 | O(9³) | O(n²) | Highly constrained puzzles |

## Puzzle Generation

The framework supports automatic puzzle generation with four difficulty levels:

- **Easy**: 40-45 empty cells
- **Medium**: 46-52 empty cells  
- **Hard**: 53-59 empty cells
- **Very Hard**: 60-64 empty cells

All generated puzzles are guaranteed to have unique solutions.

## Performance Analysis

### Benchmarking Features

- **Multi-algorithm Comparison**: Compare performance across all algorithms
- **Statistical Analysis**: Mean, standard deviation, confidence intervals
- **Success Rate Analysis**: Reliability metrics across puzzle sets
- **Performance Profiling**: Time, steps, and evaluation metrics

### Example Benchmark

```python
# Generate test puzzles
puzzles = [generator.generate_puzzle(Difficulty.MEDIUM) for _ in range(50)]

# Run benchmark
benchmark_results = analyzer.benchmark_algorithms(puzzles)

# Analyze results
for algorithm, stats in benchmark_results.items():
    print(f"{algorithm}:")
    print(f"  Success Rate: {stats['statistics']['success_rate']:.1f}%")
    print(f"  Average Time: {stats['statistics']['average_time']:.4f}s")
    print(f"  Average Steps: {stats['statistics']['average_steps']:.1f}")
```

## Configuration

The framework uses a centralized configuration system:

```python
from src.utils import config

# Access configuration
print(config.solver.max_steps)        # 1000000
print(config.gui.cell_size)           # 55
print(config.evaluation.benchmark_puzzles_count)  # 100

# Modify configuration
config.solver.step_delay = 0.1
config.gui.window_width = 1200
```

### Key Configuration Options

```python
# Solver configuration
config.solver.max_steps = 1000000
config.solver.timeout_seconds = 60.0
config.solver.enable_visualization = True

# GUI configuration  
config.gui.cell_size = 55
config.gui.window_width = 1000
config.gui.window_height = 750

# Evaluation configuration
config.evaluation.benchmark_puzzles_count = 100
config.evaluation.generate_reports = True
config.evaluation.save_results = True
```

## Research Applications

This framework is designed for research in:

- **Constraint Satisfaction Problems**: Classical CSP research
- **Algorithm Analysis**: Performance comparison and optimization
- **Heuristic Development**: New heuristic design and testing
- **Educational Tools**: Teaching AI and algorithms
- **Performance Engineering**: Optimization techniques

## Advanced Features

### Ensemble Methods

The framework supports ensemble approaches for improved performance:

```python
# Create ensemble of best performers
ensemble_algorithms = [Algorithm.MRV, Algorithm.ARC_CONSISTENCY, Algorithm.BACKTRACKING]

# Solve with ensemble voting
results = []
for algo in ensemble_algorithms:
    solver = factory.create_solver(algo)
    board_copy = [row[:] for row in puzzle]
    if solver.solve(board_copy):
        results.append((algo, solver.get_solve_time(), solver.steps))

# Select best result
best_result = min(results, key=lambda x: x[1])
print(f"Best: {best_result[0].value} in {best_result[1]:.4f}s")
```

### Custom Algorithm Development

```python
from src.solvers.base_solver import BaseSolver
from src.algorithms.enums import Algorithm

class CustomSolver(BaseSolver):
    def solve(self, board, update_ui=None, evaluation_callback=None):
        # Implement your custom algorithm
        pass

# Register with factory
SolverFactory.register_solver(Algorithm.CUSTOM, CustomSolver)
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Code Style

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Citation

If you use this code in your research, please cite:

```bibtex
@software{adaptive_ensemble_sudoku_2024,
  title={Adaptive Ensemble Sudoku Solver: An Intelligent Framework for Efficient Sudoku Solving},
  author={Research Team},
  year={2024},
  url={https://github.com/IH-Arik/Adaptive-Ensemble-Sudoku-Solver}
}
```

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Contribution Areas

- **New Algorithms**: Implement additional solving algorithms
- **Performance Optimization**: Improve existing algorithm efficiency
- **GUI Enhancements**: Improve user interface and visualization
- **Documentation**: Enhance documentation and examples
- **Benchmarks**: Add comprehensive benchmark suites

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Constraint Satisfaction Problem research community
- Algorithm optimization researchers
- Open-source contributors
- Educational institutions supporting AI research

## Contact

For questions or collaborations:
- Email: ittesafarik@gmail.com
- GitHub Issues: [Create an issue](https://github.com/IH-Arik/Adaptive-Ensemble-Sudoku-Solver/issues)

---

**Note**: This repository contains the implementation code for research purposes. The research paper describing the methodology and results is currently under review for publication.
