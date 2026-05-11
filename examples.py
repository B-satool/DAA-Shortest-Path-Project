"""
Example usage and quick reference for shortest path algorithms.
This file demonstrates how to use each algorithm and provides common patterns.
"""

from algorithms.bidirectional_dijkstra import BidirectionalDijkstra
from algorithms.johnsons_algorithm import JohnsonsAlgorithm
from algorithms.jump_point_search import JumpPointSearch
from algorithms.graph_utils import GraphGenerator


def example_1_simple_usage():
    """Example 1: Basic usage of each algorithm."""
    
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Create a simple graph
    graph = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2), (3, 7)],
        2: [(0, 4), (1, 2), (3, 1)],
        3: [(1, 7), (2, 1)]
    }
    
    source, destination = 0, 3
    
    print(f"\nFinding shortest path from {source} to {destination}\n")
    
    # Bidirectional Dijkstra
    print("1. Bidirectional Dijkstra:")
    bd = BidirectionalDijkstra(graph)
    distance, path = bd.find_shortest_path(source, destination)
    print(f"   Distance: {distance}")
    print(f"   Path: {path}")
    print(f"   Operations: {bd.operations_count}")
    print(f"   Comparisons: {bd.comparisons}\n")
    
    # Johnson's Algorithm (for all-pairs)
    print("2. Johnson's Algorithm (All-Pairs):")
    johnson = JohnsonsAlgorithm(graph)
    all_pairs = johnson.find_all_pairs_shortest_paths()
    if all_pairs:
        print(f"   Distance from {source} to {destination}: {all_pairs[source][destination]}")
        print(f"   Dijkstra calls: {johnson.dijkstra_calls}")
        print(f"   Total relaxations: {johnson.relaxations}\n")
    
    # Jump Point Search
    print("3. Jump Point Search:")
    jps = JumpPointSearch(graph)
    distance, path = jps.find_shortest_path(source, destination)
    print(f"   Distance: {distance}")
    print(f"   Path: {path}")
    print(f"   Jump points found: {jps.jump_points_found}\n")


def example_2_graph_generation():
    """Example 2: Generate and analyze different graph types."""
    
    print("=" * 60)
    print("Example 2: Graph Generation")
    print("=" * 60)
    
    # Sparse graph
    print("\nGenerating sparse graph (50 vertices, 10% density)...")
    sparse = GraphGenerator.create_weighted_graph(50, 0.1, seed=42)
    print(f"  Vertices: {len(sparse)}")
    print(f"  Edges: {sum(len(neighbors) for neighbors in sparse.values())}")
    print(f"  Density: {sum(len(neighbors) for neighbors in sparse.values()) / (50 * 49):.4f}")
    
    # Dense graph
    print("\nGenerating dense graph (50 vertices, 50% density)...")
    dense = GraphGenerator.create_weighted_graph(50, 0.5, seed=42)
    print(f"  Vertices: {len(dense)}")
    print(f"  Edges: {sum(len(neighbors) for neighbors in dense.values())}")
    print(f"  Density: {sum(len(neighbors) for neighbors in dense.values()) / (50 * 49):.4f}")
    
    # Grid graph
    print("\nGenerating grid graph (8x8 = 64 vertices)...")
    grid = GraphGenerator.create_grid_graph(8, 8)
    print(f"  Vertices: {len(grid)}")
    print(f"  Edges: {sum(len(neighbors) for neighbors in grid.values())}")
    print()


def example_3_performance_metrics():
    """Example 3: Collecting and displaying performance metrics."""
    
    print("=" * 60)
    print("Example 3: Performance Metrics")
    print("=" * 60)
    
    graph = GraphGenerator.create_weighted_graph(100, 0.15, seed=42)
    
    test_pairs = [(0, 50), (10, 90), (25, 75), (5, 95), (30, 60)]
    
    print("\nBidirectional Dijkstra Performance:")
    print("─" * 40)
    times = []
    operations = []
    
    for source, dest in test_pairs:
        bd = BidirectionalDijkstra(graph)
        import time as time_module
        start = time_module.perf_counter()
        distance, path = bd.find_shortest_path(source, dest)
        elapsed = time_module.perf_counter() - start
        times.append(elapsed)
        operations.append(bd.operations_count)
        print(f"  {source} → {dest}: {elapsed*1000:.3f}ms, "
              f"Distance: {distance}, Ops: {bd.operations_count}")
    
    import statistics
    print(f"\n  Average time: {statistics.mean(times)*1000:.3f}ms")
    print(f"  Average operations: {statistics.mean(operations):.0f}")
    print()


def example_4_algorithm_comparison():
    """Example 4: Direct comparison of algorithms on same graph."""
    
    print("=" * 60)
    print("Example 4: Algorithm Comparison")
    print("=" * 60)
    
    # Create medium-sized graph
    graph = GraphGenerator.create_weighted_graph(80, 0.12, seed=42)
    test_pair = (0, 79)
    
    print(f"\nComparing algorithms on 80-vertex graph")
    print(f"Finding path from {test_pair[0]} to {test_pair[1]}\n")
    
    # Bidirectional Dijkstra
    bd = BidirectionalDijkstra(graph)
    dist1, path1 = bd.find_shortest_path(test_pair[0], test_pair[1])
    print(f"Bidirectional Dijkstra:")
    print(f"  Distance: {dist1}")
    print(f"  Path length: {len(path1)}")
    print(f"  Operations: {bd.operations_count}")
    print(f"  Comparisons: {bd.comparisons}")
    
    # Johnson's Algorithm
    johnson = JohnsonsAlgorithm(graph)
    all_pairs = johnson.find_all_pairs_shortest_paths()
    if all_pairs:
        dist2 = all_pairs[test_pair[0]][test_pair[1]]
        print(f"\nJohnson's Algorithm:")
        print(f"  Distance: {dist2}")
        print(f"  Dijkstra calls: {johnson.dijkstra_calls}")
        print(f"  Relaxations: {johnson.relaxations}")
        print(f"  Operations: {johnson.operations_count}")
    
    # Jump Point Search
    jps = JumpPointSearch(graph)
    dist3, path3 = jps.find_shortest_path(test_pair[0], test_pair[1])
    print(f"\nJump Point Search:")
    print(f"  Distance: {dist3}")
    print(f"  Path length: {len(path3)}")
    print(f"  Jump points: {jps.jump_points_found}")
    print(f"  Operations: {jps.operations_count}")
    
    # Verify all found same distance
    print(f"\nVerification:")
    if dist1 == dist2 == dist3:
        print(f"  ✓ All algorithms found same distance: {dist1}")
    else:
        print(f"  ✗ Inconsistent results!")
        print(f"    BiDijkstra: {dist1}")
        print(f"    Johnson: {dist2}")
        print(f"    JPS: {dist3}")
    print()


def example_5_grid_pathfinding():
    """Example 5: Specialized grid-based pathfinding with JPS."""
    
    print("=" * 60)
    print("Example 5: Grid-Based Pathfinding (JPS Advantage)")
    print("=" * 60)
    
    # Create 10x10 grid
    grid = GraphGenerator.create_grid_graph(10, 10)
    
    # Top-left to bottom-right
    source = 0  # (0, 0)
    destination = 99  # (9, 9)
    
    print(f"\n10x10 Grid Pathfinding")
    print(f"From top-left (0,0) to bottom-right (9,9)\n")
    
    # Bidirectional Dijkstra
    print("Bidirectional Dijkstra:")
    bd = BidirectionalDijkstra(grid)
    dist1, path1 = bd.find_shortest_path(source, destination)
    print(f"  Distance: {dist1}")
    print(f"  Operations: {bd.operations_count}")
    
    # Jump Point Search (with Manhattan heuristic)
    print("\nJump Point Search (with heuristic):")
    def manhattan_distance(u, dest):
        """Manhattan distance heuristic for 10x10 grid."""
        u_row, u_col = u // 10, u % 10
        d_row, d_col = dest // 10, dest % 10
        return abs(u_row - d_row) + abs(u_col - d_col)
    
    jps = JumpPointSearch(grid, heuristic=manhattan_distance)
    dist2, path2 = jps.find_shortest_path(source, destination)
    print(f"  Distance: {dist2}")
    print(f"  Operations: {jps.operations_count}")
    print(f"  Jump points: {jps.jump_points_found}")
    
    # Performance comparison
    speedup = bd.operations_count / jps.operations_count if jps.operations_count > 0 else 0
    print(f"\nSpeedup: {speedup:.1f}x (JPS is {speedup:.1f}x faster in operations)")
    print()


def example_6_metrics_tracking():
    """Example 6: Advanced metrics tracking for analysis."""
    
    print("=" * 60)
    print("Example 6: Metrics Tracking and Analysis")
    print("=" * 60)
    
    from benchmarks.metrics import MetricsCollector
    
    graph = GraphGenerator.create_weighted_graph(150, 0.08, seed=42)
    test_pairs = [(0, 149), (50, 100), (25, 75), (10, 140), (60, 80)]
    
    print("\nTracking Bidirectional Dijkstra Metrics:")
    print("─" * 40)
    
    collector = MetricsCollector()
    
    for source, dest in test_pairs:
        bd = BidirectionalDijkstra(graph)
        collector.start_timer("bidijkstra")
        distance, path = bd.find_shortest_path(source, dest)
        collector.end_timer("bidijkstra")
        
        collector.record_metric("operations", bd.operations_count)
        collector.record_metric("comparisons", bd.comparisons)
    
    # Get statistics
    time_stats = collector.get_stats("bidijkstra")
    ops_stats = collector.get_stats("operations")
    
    print(f"\nExecution Time Statistics:")
    print(f"  Min: {time_stats.get('min', 0)*1000:.3f}ms")
    print(f"  Max: {time_stats.get('max', 0)*1000:.3f}ms")
    print(f"  Mean: {time_stats.get('mean', 0)*1000:.3f}ms")
    print(f"  StdDev: {time_stats.get('stdev', 0)*1000:.3f}ms")
    
    print(f"\nOperation Count Statistics:")
    print(f"  Min: {ops_stats.get('min', 0):.0f}")
    print(f"  Max: {ops_stats.get('max', 0):.0f}")
    print(f"  Mean: {ops_stats.get('mean', 0):.0f}")
    print()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SHORTEST PATH ALGORITHMS - USAGE EXAMPLES")
    print("="*60 + "\n")
    
    example_1_simple_usage()
    example_2_graph_generation()
    example_3_performance_metrics()
    example_4_algorithm_comparison()
    example_5_grid_pathfinding()
    example_6_metrics_tracking()
    
    print("="*60)
    print("All examples completed successfully!")
    print("="*60)
