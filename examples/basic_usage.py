"""
Basic usage example for the Adaptive Ensemble Sudoku Solver.
"""

import utils.session
from src import SolverFactory, PuzzleGenerator, PerformanceAnalyzer
from src.algorithms import Algorithm, Difficulty
from src.utils import BoardUtils


def main():
    """
    Basic usage example demonstrating the Sudoku solver framework.
    """
    print("Adaptive Ensemble Sudoku Solver - Basic Usage Example")
    print("=" * 60)
    
    # Generate a puzzle
    print("\n1. Generating a Medium difficulty puzzle...")
    generator = PuzzleGenerator()
    puzzle = generator.generate_puzzle(Difficulty.MEDIUM)
    
    print("Generated puzzle:")
    print(BoardUtils.board_to_string(puzzle))
    print(f"Empty cells: {BoardUtils.count_empty_cells(puzzle)}")
    
    # Solve with different algorithms
    algorithms = [Algorithm.BACKTRACKING, Algorithm.MRV, Algorithm.ARC_CONSISTENCY]
    
    print(f"\n2. Solving with {len(algorithms)} algorithms...")
    
    results = []
    for algorithm in algorithms:
        print(f"\nSolving with {algorithm.value}...")
        
        # Create solver
        solver = SolverFactory.create_solver(algorithm)
        
        # Make a copy of the puzzle to preserve original
        board_to_solve = [row[:] for row in puzzle]
        
        # Solve the puzzle
        success = solver.solve(board_to_solve)
        
        if success:
            print(f"✓ Solved in {solver.get_solve_time():.4f} seconds")
            print(f"  Steps: {solver.steps}")
            print(f"  Evaluations: {solver.evaluations}")
            results.append({
                'algorithm': algorithm.value,
                'success': True,
                'time': solver.get_solve_time(),
                'steps': solver.steps,
                'evaluations': solver.evaluations
            })
        else:
            print(f"✗ Failed to solve")
            results.append({
                'algorithm': algorithm.value,
                'success': False,
                'time': 0.0,
                'steps': 0,
                'evaluations': 0
            })
    
    # Performance comparison
    print(f"\n3. Performance Comparison:")
    print("-" * 40)
    
    successful_results = [r for r in results if r['success']]
    if successful_results:
        # Sort by time
        successful_results.sort(key=lambda x: x['time'])
        
        print("Algorithm Rankings (by solve time):")
        for i, result in enumerate(successful_results, 1):
            print(f"{i}. {result['algorithm']}: {result['time']:.4f}s "
                  f"({result['steps']} steps, {result['evaluations']} evals)")
        
        fastest = successful_results[0]
        most_efficient = min(successful_results, key=lambda x: x['steps'])
        
        print(f"\nFastest: {fastest['algorithm']} ({fastest['time']:.4f}s)")
        print(f"Most Efficient: {most_efficient['algorithm']} ({most_efficient['steps']} steps)")
    else:
        print("No algorithm successfully solved the puzzle")
    
    # Advanced comparison using PerformanceAnalyzer
    print(f"\n4. Advanced Performance Analysis:")
    print("-" * 40)
    
    analyzer = PerformanceAnalyzer()
    comparison_results = analyzer.compare_algorithms(puzzle, algorithms)
    
    # Generate detailed report
    report = analyzer.generate_report(comparison_results)
    print(report)
    
    # Generate multiple puzzles for benchmarking
    print(f"\n5. Benchmarking on multiple puzzles...")
    print("-" * 40)
    
    test_puzzles = []
    for difficulty in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]:
        for _ in range(3):  # 3 puzzles per difficulty
            test_puzzles.append(generator.generate_puzzle(difficulty))
    
    benchmark_results = analyzer.benchmark_algorithms(test_puzzles, algorithms)
    
    print("Benchmark Summary:")
    for algorithm, data in benchmark_results.items():
        stats = data['statistics']
        print(f"\n{algorithm}:")
        print(f"  Success Rate: {stats['success_rate']:.1f}%")
        print(f"  Average Time: {stats['average_time']:.4f}s ± {stats['std_time']:.4f}s")
        print(f"  Average Steps: {stats['average_steps']:.1f} ± {stats['std_steps']:.1f}")
        print(f"  Min/Max Time: {stats['min_time']:.4f}s / {stats['max_time']:.4f}s")
    
    print(f"\n6. Puzzle Generation Demo:")
    print("-" * 40)
    
    for difficulty in [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD, Difficulty.VERY_HARD]:
        test_puzzle = generator.generate_puzzle(difficulty)
        empty_cells = BoardUtils.count_empty_cells(test_puzzle)
        print(f"{difficulty.value}: {empty_cells} empty cells")
    
    print(f"\nExample completed successfully!")
    print("Explore the framework for more advanced features and custom algorithms.")


if __name__ == "__main__":
    main()
