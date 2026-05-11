#!/usr/bin/env python
"""
Quick guide for running the benchmark and understanding output.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bidirectional_dijkstra import BidirectionalDijkstra
from algorithms.johnsons_algorithm import JohnsonsAlgorithm
from algorithms.jump_point_search import JumpPointSearch
from algorithms.graph_utils import GraphGenerator
from benchmarks.metrics import AlgorithmBenchmark


def quick_demo():
    """Quick demonstration of all three algorithms."""
    
    print("\n" + "="*70)
    print("SHORTEST PATH ALGORITHMS - QUICK DEMO")
    print("="*70)
    
    # Create a test graph
    print("\n[Step 1] Creating test graph...")
    graph = GraphGenerator.create_weighted_graph(50, 0.15, seed=42)
    print(f"  ✓ Generated graph: 50 vertices, {sum(len(n) for n in graph.values())} edges")
    
    # Create test pairs
    print("\n[Step 2] Generating test pairs...")
    test_pairs = [(0, 49), (10, 40), (20, 30), (5, 45), (15, 35)]
    print(f"  ✓ Generated {len(test_pairs)} test pairs")
    
    # Run benchmark
    print("\n[Step 3] Running benchmark...")
    benchmark = AlgorithmBenchmark()
    
    # Bidirectional Dijkstra
    print("\n  Testing Bidirectional Dijkstra...")
    bd = BidirectionalDijkstra(graph)
    bd_result = benchmark.benchmark_algorithm("Bidirectional Dijkstra", bd, test_pairs, 50)
    
    # Johnson's
    print("  Testing Johnson's Algorithm...")
    johnson = JohnsonsAlgorithm(graph)
    joh_result = benchmark.benchmark_algorithm("Johnson's Algorithm", johnson, test_pairs, 50)
    
    # JPS
    print("  Testing Jump Point Search...")
    jps = JumpPointSearch(graph)
    jps_result = benchmark.benchmark_algorithm("Jump Point Search", jps, test_pairs, 50)
    
    # Display results
    print("\n[Step 4] Results Summary")
    print("-" * 70)
    
    algorithms = [bd_result, joh_result, jps_result]
    
    for result in algorithms:
        print(f"\n{result['algorithm']}:")
        print(f"  Paths found: {result['paths_found']}/{result['test_cases']}")
        if result.get('avg_time'):
            print(f"  Avg time: {result['avg_time']*1000:.3f}ms")
            print(f"  Total time: {result['total_time']*1000:.3f}ms")
        if result.get('avg_operations'):
            print(f"  Avg operations: {result['avg_operations']:.0f}")
    
    # Comparative analysis
    print("\n" + "="*70)
    print("COMPARATIVE ANALYSIS")
    print("="*70)
    
    fastest = min(algorithms, key=lambda x: x.get('avg_time', float('inf')))
    print(f"\n✓ Fastest: {fastest['algorithm']}")
    print(f"  Average time: {fastest['avg_time']*1000:.3f}ms")
    
    if any('avg_operations' in r for r in algorithms):
        most_efficient = min([r for r in algorithms if 'avg_operations' in r],
                            key=lambda x: x['avg_operations'])
        print(f"\n✓ Most efficient (operations): {most_efficient['algorithm']}")
        print(f"  Average operations: {most_efficient['avg_operations']:.0f}")
    
    print("\n" + "="*70)
    print("FULL REPORT")
    print("="*70)
    print(benchmark.generate_report())


def stress_test():
    """Stress test with larger graphs."""
    
    print("\n" + "="*70)
    print("STRESS TEST - LARGER GRAPHS")
    print("="*70)
    
    benchmark = AlgorithmBenchmark()
    
    configurations = [
        {"name": "Medium (100 vertices)", "vertices": 100, "density": 0.1},
        {"name": "Large (200 vertices)", "vertices": 200, "density": 0.05},
    ]
    
    for config in configurations:
        print(f"\n[Test] {config['name']}")
        print(f"  Density: {config['density']}")
        
        graph = GraphGenerator.create_weighted_graph(
            config['vertices'],
            config['density'],
            seed=42
        )
        
        test_pairs = [(i, (i + config['vertices']//2) % config['vertices']) 
                     for i in range(0, config['vertices'], 10)][:5]
        
        # Test each algorithm
        print(f"  Running Bidirectional Dijkstra...")
        bd = BidirectionalDijkstra(graph)
        benchmark.benchmark_algorithm(
            f"BiDijkstra_{config['name']}", bd, test_pairs, config['vertices']
        )
        
        print(f"  Running Johnson's Algorithm...")
        johnson = JohnsonsAlgorithm(graph)
        benchmark.benchmark_algorithm(
            f"Johnson_{config['name']}", johnson, test_pairs, config['vertices']
        )
        
        print(f"  Running Jump Point Search...")
        jps = JumpPointSearch(graph)
        benchmark.benchmark_algorithm(
            f"JPS_{config['name']}", jps, test_pairs, config['vertices']
        )
    
    print("\n" + "="*70)
    print("STRESS TEST REPORT")
    print("="*70)
    print(benchmark.generate_report())


def grid_test():
    """Test Jump Point Search advantage on grids."""
    
    print("\n" + "="*70)
    print("GRID-BASED PATHFINDING TEST")
    print("="*70)
    print("(Jump Point Search should shine here)")
    print()
    
    # Create grid graphs
    grid_sizes = [
        (10, 10),
        (15, 15),
        (20, 20),
    ]
    
    benchmark = AlgorithmBenchmark()
    
    for rows, cols in grid_sizes:
        size = rows * cols
        print(f"[Test] {rows}×{cols} grid ({size} vertices)")
        
        grid = GraphGenerator.create_grid_graph(rows, cols)
        
        # Generate test pairs (corners and centers)
        test_pairs = [
            (0, size - 1),                    # TL to BR
            (cols - 1, size - cols),          # TR to BL
            (size // 2, size // 2 + cols),    # Center paths
        ]
        
        # Bidirectional Dijkstra
        print(f"  BiDijkstra...")
        bd = BidirectionalDijkstra(grid)
        benchmark.benchmark_algorithm(
            f"BiDijkstra_{rows}x{cols}", bd, test_pairs, size
        )
        
        # Jump Point Search (with Manhattan heuristic)
        def manhattan(u, v):
            u_r, u_c = u // cols, u % cols
            v_r, v_c = v // cols, v % cols
            return abs(u_r - v_r) + abs(u_c - v_c)
        
        print(f"  Jump Point Search...")
        jps = JumpPointSearch(grid, heuristic=manhattan)
        benchmark.benchmark_algorithm(
            f"JPS_{rows}x{cols}", jps, test_pairs, size
        )
    
    print("\n" + "="*70)
    print("GRID TEST REPORT")
    print("="*70)
    print(benchmark.generate_report())
    
    print("\n[Note] JPS should show significant speedup on grids!")
    print("Typical speedup: 5-20x faster than Dijkstra variants")


def main():
    """Main execution."""
    
    import time
    
    print("\n" + "="*70)
    print("CSE 317 PROJECT - SHORTEST PATH ALGORITHMS")
    print("Benchmarking Framework")
    print("="*70)
    
    print("\nAvailable tests:")
    print("1. Quick Demo (5-10 seconds)")
    print("2. Stress Test (30-60 seconds)")
    print("3. Grid Test (20-40 seconds)")
    print("4. All Tests")
    
    choice = input("\nSelect test (1-4, or 'q' to quit): ").strip().lower()
    
    start_time = time.time()
    
    if choice == '1':
        quick_demo()
    elif choice == '2':
        stress_test()
    elif choice == '3':
        grid_test()
    elif choice == '4':
        quick_demo()
        stress_test()
        grid_test()
    elif choice == 'q':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Running quick demo...")
        quick_demo()
    
    elapsed = time.time() - start_time
    print(f"\n[Done] Total time: {elapsed:.1f} seconds")
    print("="*70)


if __name__ == "__main__":
    main()
