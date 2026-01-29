"""
Performance analysis and comparison utilities for Sudoku solvers.
"""

import time
import statistics
from typing import List, Dict, Any, Optional
from ..solvers.base_solver import BaseSolver
from ..solvers.solver_factory import SolverFactory
from ..algorithms.enums import Algorithm
from ..utils.board_utils import BoardUtils


class PerformanceAnalyzer:
    """
    Performance analyzer for comparing different Sudoku solving algorithms.
    """
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.results: List[Dict[str, Any]] = []
    
    def compare_algorithms(self, board: List[List[int]], 
                          algorithms: Optional[List[Algorithm]] = None) -> Dict[str, Any]:
        """
        Compare performance of different algorithms on the same puzzle.
        
        Args:
            board: 9x9 Sudoku board
            algorithms: List of algorithms to compare (None for all available)
        
        Returns:
            Dictionary containing comparison results
        """
        if algorithms is None:
            algorithms = SolverFactory.get_available_algorithms()
        
        results = []
        
        for algorithm in algorithms:
            try:
                # Create solver
                solver = SolverFactory.create_solver(algorithm)
                
                # Make a copy of the board
                board_copy = BoardUtils.copy_board(board)
                
                # Time the solving process
                start_time = time.time()
                success = solver.solve(board_copy)
                end_time = time.time()
                
                # Collect results
                result = {
                    'algorithm': algorithm.value,
                    'success': success,
                    'solve_time': end_time - start_time,
                    'steps': solver.steps,
                    'evaluations': solver.evaluations,
                    'status': solver.status.value
                }
                results.append(result)
                
            except Exception as e:
                # Handle any errors during solving
                result = {
                    'algorithm': algorithm.value,
                    'success': False,
                    'solve_time': 0.0,
                    'steps': 0,
                    'evaluations': 0,
                    'status': f'Error: {str(e)}'
                }
                results.append(result)
        
        # Sort results by solve time
        results.sort(key=lambda x: x['solve_time'])
        
        return {
            'board': board,
            'results': results,
            'summary': self._generate_summary(results)
        }
    
    def benchmark_algorithms(self, puzzles: List[List[List[int]]], 
                             algorithms: Optional[List[Algorithm]] = None) -> Dict[str, Any]:
        """
        Benchmark algorithms on multiple puzzles.
        
        Args:
            puzzles: List of puzzle boards
            algorithms: List of algorithms to benchmark
        
        Returns:
            Dictionary containing benchmark results
        """
        if algorithms is None:
            algorithms = SolverFactory.get_available_algorithms()
        
        benchmark_results = {}
        
        for algorithm in algorithms:
            algorithm_results = []
            
            for i, puzzle in enumerate(puzzles):
                try:
                    solver = SolverFactory.create_solver(algorithm)
                    puzzle_copy = BoardUtils.copy_board(puzzle)
                    
                    start_time = time.time()
                    success = solver.solve(puzzle_copy)
                    end_time = time.time()
                    
                    result = {
                        'puzzle_index': i,
                        'success': success,
                        'solve_time': end_time - start_time,
                        'steps': solver.steps,
                        'evaluations': solver.evaluations
                    }
                    algorithm_results.append(result)
                    
                except Exception as e:
                    result = {
                        'puzzle_index': i,
                        'success': False,
                        'solve_time': 0.0,
                        'steps': 0,
                        'evaluations': 0,
                        'error': str(e)
                    }
                    algorithm_results.append(result)
            
            benchmark_results[algorithm.value] = {
                'results': algorithm_results,
                'statistics': self._calculate_statistics(algorithm_results)
            }
        
        return benchmark_results
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for comparison results.
        
        Args:
            results: List of algorithm results
        
        Returns:
            Summary statistics
        """
        successful_results = [r for r in results if r['success']]
        
        if not successful_results:
            return {
                'fastest_algorithm': None,
                'most_efficient_algorithm': None,
                'success_rate': 0.0,
                'average_time': 0.0,
                'average_steps': 0.0
            }
        
        # Find fastest algorithm
        fastest = min(successful_results, key=lambda x: x['solve_time'])
        
        # Find most efficient (fewest steps)
        most_efficient = min(successful_results, key=lambda x: x['steps'])
        
        # Calculate averages
        avg_time = statistics.mean([r['solve_time'] for r in successful_results])
        avg_steps = statistics.mean([r['steps'] for r in successful_results])
        
        return {
            'fastest_algorithm': fastest['algorithm'],
            'fastest_time': fastest['solve_time'],
            'most_efficient_algorithm': most_efficient['algorithm'],
            'most_efficient_steps': most_efficient['steps'],
            'success_rate': len(successful_results) / len(results) * 100,
            'average_time': avg_time,
            'average_steps': avg_steps
        }
    
    def _calculate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics for algorithm results.
        
        Args:
            results: List of results for an algorithm
        
        Returns:
            Statistical summary
        """
        successful_results = [r for r in results if r['success']]
        
        if not successful_results:
            return {
                'success_rate': 0.0,
                'average_time': 0.0,
                'min_time': 0.0,
                'max_time': 0.0,
                'std_time': 0.0,
                'average_steps': 0.0,
                'min_steps': 0.0,
                'max_steps': 0.0,
                'std_steps': 0.0
            }
        
        times = [r['solve_time'] for r in successful_results]
        steps = [r['steps'] for r in successful_results]
        
        return {
            'success_rate': len(successful_results) / len(results) * 100,
            'average_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'std_time': statistics.stdev(times) if len(times) > 1 else 0.0,
            'average_steps': statistics.mean(steps),
            'min_steps': min(steps),
            'max_steps': max(steps),
            'std_steps': statistics.stdev(steps) if len(steps) > 1 else 0.0
        }
    
    def generate_report(self, comparison_results: Dict[str, Any]) -> str:
        """
        Generate a formatted report from comparison results.
        
        Args:
            comparison_results: Results from compare_algorithms
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("Sudoku Solver Performance Comparison Report")
        report.append("=" * 50)
        report.append("")
        
        # Summary
        summary = comparison_results['summary']
        report.append("SUMMARY:")
        report.append(f"Fastest Algorithm: {summary.get('fastest_algorithm', 'N/A')}")
        report.append(f"Most Efficient: {summary.get('most_efficient_algorithm', 'N/A')}")
        report.append(f"Success Rate: {summary.get('success_rate', 0):.1f}%")
        report.append(f"Average Solve Time: {summary.get('average_time', 0):.4f}s")
        report.append(f"Average Steps: {summary.get('average_steps', 0):.1f}")
        report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS:")
        report.append("-" * 30)
        
        for result in comparison_results['results']:
            status = "✓" if result['success'] else "✗"
            report.append(f"{status} {result['algorithm']}")
            report.append(f"  Time: {result['solve_time']:.4f}s")
            report.append(f"  Steps: {result['steps']}")
            report.append(f"  Evaluations: {result['evaluations']}")
            report.append("")
        
        return "\n".join(report)
