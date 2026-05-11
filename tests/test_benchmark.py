"""
Comprehensive test suite and main benchmark runner for shortest path algorithms.
Tests: Bidirectional Dijkstra, Johnson's Algorithm, Jump Point Search
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bidirectional_dijkstra import BidirectionalDijkstra
from algorithms.johnsons_algorithm import JohnsonsAlgorithm
from algorithms.jump_point_search import JumpPointSearch
from algorithms.graph_utils import GraphGenerator, GraphValidator, TestCaseGenerator
from benchmarks.metrics import AlgorithmBenchmark


def run_comprehensive_benchmark():
    """Run comprehensive benchmark across multiple graph sizes and types."""
    
    benchmark = AlgorithmBenchmark()
    
    # Test configurations
    test_configs = [
        {"name": "Small Sparse", "vertices": 20, "density": 0.15, "test_pairs": 15},
        {"name": "Small Dense", "vertices": 20, "density": 0.6, "test_pairs": 15},
        {"name": "Medium Sparse", "vertices": 100, "density": 0.05, "test_pairs": 20},
        {"name": "Medium Dense", "vertices": 100, "density": 0.3, "test_pairs": 20},
        {"name": "Large Sparse", "vertices": 300, "density": 0.02, "test_pairs": 25},
    ]
    
    print("Starting Comprehensive Algorithm Benchmark...\n")
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"Testing: {config['name']}")
        print(f"Vertices: {config['vertices']}, Density: {config['density']}")
        print(f"{'='*60}\n")
        
        # Generate graph
        print("Generating graph...")
        graph = GraphGenerator.create_weighted_graph(
            config['vertices'],
            config['density'],
            max_weight=100,
            seed=42
        )
        
        # Validate graph
        if not GraphValidator.is_valid_graph(graph):
            print("ERROR: Invalid graph generated!")
            continue
        
        stats = GraphValidator.get_graph_stats(graph)
        print(f"Graph Stats: {stats['vertices']} vertices, {stats['edges']} edges")
        print(f"Density: {stats['density']:.4f}, Avg Degree: {stats['avg_degree']:.2f}\n")
        
        # Generate test pairs
        test_pairs = TestCaseGenerator.generate_test_pairs(
            config['vertices'],
            config['test_pairs'],
            seed=42
        )
        
        # Test Bidirectional Dijkstra
        print("Testing Bidirectional Dijkstra...")
        bi_dijkstra = BidirectionalDijkstra(graph)
        benchmark.benchmark_algorithm(
            f"BiDijkstra_{config['name']}",
            bi_dijkstra,
            test_pairs,
            config['vertices']
        )
        
        # Test Johnson's Algorithm
        print("Testing Johnson's Algorithm...")
        johnson = JohnsonsAlgorithm(graph)
        benchmark.benchmark_algorithm(
            f"Johnson_{config['name']}",
            johnson,
            test_pairs,
            config['vertices']
        )
        
        # Test Jump Point Search
        print("Testing Jump Point Search...")
        jps = JumpPointSearch(graph)
        benchmark.benchmark_algorithm(
            f"JPS_{config['name']}",
            jps,
            test_pairs,
            config['vertices']
        )
        
        print(f"Completed {config['name']}\n")
    
    # Print comprehensive report
    report = benchmark.generate_report()
    print(report)
    
    # Export results
    output_file = os.path.join(
        os.path.dirname(__file__),
        "benchmark_results.csv"
    )
    benchmark.export_to_csv(output_file)
    
    return benchmark


def run_simple_test():
    """Run a simple test to verify algorithms work correctly."""
    
    print("Running Simple Verification Test...\n")
    
    # Create a small test graph
    #   0 - 1 - 2
    #   |   |   |
    #   3 - 4 - 5
    
    graph = {
        0: [(1, 1), (3, 4)],
        1: [(0, 1), (2, 2), (4, 5)],
        2: [(1, 2), (5, 1)],
        3: [(0, 4), (4, 2)],
        4: [(3, 2), (1, 5), (5, 1)],
        5: [(4, 1), (2, 1)]
    }
    
    source, destination = 0, 5
    
    print(f"Graph: 6 vertices, testing shortest path from {source} to {destination}\n")
    
    # Test Bidirectional Dijkstra
    print("Bidirectional Dijkstra:")
    bi_dijkstra = BidirectionalDijkstra(graph)
    distance, path = bi_dijkstra.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Path: {path}")
    print(f"  Operations: {bi_dijkstra.operations_count}\n")
    
    # Test Johnson's Algorithm
    print("Johnson's Algorithm:")
    johnson = JohnsonsAlgorithm(graph)
    distance, path = johnson.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Operations: {johnson.operations_count}\n")
    
    # Test Jump Point Search
    print("Jump Point Search:")
    jps = JumpPointSearch(graph)
    distance, path = jps.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Path: {path}")
    print(f"  Operations: {jps.operations_count}\n")
    
    print("✓ All algorithms completed successfully!\n")


if __name__ == "__main__":
    # Run simple test first
    run_simple_test()
    
    # Run comprehensive benchmark
    print("\n" + "="*80)
    print("COMPREHENSIVE BENCHMARK")
    print("="*80 + "\n")
    run_comprehensive_benchmark()
