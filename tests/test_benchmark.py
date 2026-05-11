"""
Comprehensive test suite and main benchmark runner for shortest path algorithms.
Tests: Bidirectional Dijkstra, A* Search, Jump Point Search, Bellman-Ford
Generates empirical complexity graphs and comparative analysis.
"""

import sys
import os
import json
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bidirectional_dijkstra import BidirectionalDijkstra
from algorithms.a_star_algorithm import AStarSearch
from algorithms.bellman_ford import BellmanFord
from algorithms.jump_point_search import JumpPointSearch
from algorithms.graph_utils import GraphGenerator, GraphValidator, TestCaseGenerator
from benchmarks.metrics import AlgorithmBenchmark

# Try to import matplotlib for graph generation
try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Graphs will not be generated.")


def generate_runtime_vs_size_graph():
    """Generate graph showing runtime vs graph size for all algorithms (sparse graphs)."""
    print("\n" + "="*80)
    print("GENERATING: Runtime vs Graph Size (Sparse Graphs)")
    print("="*80)
    
    if not MATPLOTLIB_AVAILABLE:
        print("Skipping graph generation (matplotlib not available)")
        return {}
    
    sizes = [20, 40, 60, 80, 100, 150, 200]
    bi_dijkstra_times = []
    a_star_times = []
    bf_times = []
    
    for size in sizes:
        print(f"\nTesting size V={size}...")
        
        # Generate sparse graph (density ~5-10%)
        graph = GraphGenerator.create_weighted_graph(size, 0.08, max_weight=100, seed=42)
        
        # Generate test pairs
        test_pairs = TestCaseGenerator.generate_test_pairs(size, min(10, size//5), seed=42)
        
        # Test BiDijkstra
        bi_dijkstra = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bi_dijkstra.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000  # Convert to ms
        bi_dijkstra_times.append(avg_time)
        print(f"  BiDijkstra: {avg_time:.4f} ms")
        
        # Test A*
        a_star = AStarSearch(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            a_star.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        a_star_times.append(avg_time)
        print(f"  A*: {avg_time:.4f} ms")
        
        # Test Bellman-Ford
        bf = BellmanFord(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bf.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bf_times.append(avg_time)
        print(f"  Bellman-Ford: {avg_time:.4f} ms")
        
        # Test JPS (on grid if applicable, else dummy)
        jps = JumpPointSearch(graph)
        times = []
        for s, d in test_pairs[:5]:  # Only a few tests for JPS
            start = time.time()
            try:
                jps.find_shortest_path(s, d)
                times.append(time.time() - start)
            except:
                pass
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(sizes, bi_dijkstra_times, marker='o', label='BiDijkstra', linewidth=2, markersize=8)
    ax.plot(sizes, a_star_times, marker='s', label='A*', linewidth=2, markersize=8)
    ax.plot(sizes, bf_times, marker='^', label='Bellman-Ford', linewidth=2, markersize=8)
    
    ax.set_xlabel('Graph Size (Vertices)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Runtime (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Runtime vs Graph Size (Sparse Graphs: ~8% Density)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'runtime_vs_size.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return {
        'sizes': sizes,
        'bi_dijkstra': bi_dijkstra_times,
        'a_star': a_star_times,
        'bellman_ford': bf_times
    }


def generate_runtime_vs_density_graph():
    """Generate graph showing runtime vs graph density."""
    print("\n" + "="*80)
    print("GENERATING: Runtime vs Graph Density")
    print("="*80)
    
    if not MATPLOTLIB_AVAILABLE:
        print("Skipping graph generation (matplotlib not available)")
        return {}
    
    densities = [0.05, 0.10, 0.15, 0.25, 0.35, 0.50, 0.70]
    size = 100
    bi_dijkstra_times = []
    a_star_times = []
    bf_times = []
    
    for density in densities:
        print(f"\nTesting density {density*100:.0f}%...")
        
        # Generate graph with specified density
        graph = GraphGenerator.create_weighted_graph(size, density, max_weight=100, seed=42)
        
        # Generate test pairs
        test_pairs = TestCaseGenerator.generate_test_pairs(size, 10, seed=42)
        
        # Test BiDijkstra
        bi_dijkstra = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bi_dijkstra.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bi_dijkstra_times.append(avg_time)
        print(f"  BiDijkstra: {avg_time:.4f} ms")
        
        # Test A*
        a_star = AStarSearch(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            a_star.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        a_star_times.append(avg_time)
        print(f"  A*: {avg_time:.4f} ms")
        
        # Test Bellman-Ford
        bf = BellmanFord(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bf.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bf_times.append(avg_time)
        print(f"  Bellman-Ford: {avg_time:.4f} ms")
    
    # Create plot with log scale
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.semilogy(densities, bi_dijkstra_times, marker='o', label='BiDijkstra', 
                linewidth=2, markersize=8, base=10)
    ax.semilogy(densities, a_star_times, marker='s', label='A*', 
                linewidth=2, markersize=8, base=10)
    ax.semilogy(densities, bf_times, marker='^', label='Bellman-Ford', 
                linewidth=2, markersize=8, base=10)
    
    ax.set_xlabel('Graph Density (proportion of edges)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Runtime (ms, log scale)', fontsize=12, fontweight='bold')
    ax.set_title(f'Runtime vs Graph Density (100 vertices)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which='both')
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'runtime_vs_density.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return {
        'densities': densities,
        'bi_dijkstra': bi_dijkstra_times,
        'a_star': a_star_times,
        'bellman_ford': bf_times
    }


def generate_algorithms_comparison_graph():
    """Generate side-by-side comparison of all algorithms on sparse graphs."""
    print("\n" + "="*80)
    print("GENERATING: Algorithms Comparison on Sparse Graphs")
    print("="*80)
    
    if not MATPLOTLIB_AVAILABLE:
        print("Skipping graph generation (matplotlib not available)")
        return {}
    
    sizes = [50, 100, 150, 200, 300]
    bi_dijkstra_times = []
    a_star_times = []
    bf_times = []
    jps_times = []
    
    for size in sizes:
        print(f"\nTesting size V={size}...")
        
        # Generate sparse graph
        graph = GraphGenerator.create_weighted_graph(size, 0.05, max_weight=100, seed=42)
        
        # Generate test pairs
        test_pairs = TestCaseGenerator.generate_test_pairs(size, min(8, size//10), seed=42)
        
        # Test BiDijkstra
        bi_dijkstra = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bi_dijkstra.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bi_dijkstra_times.append(avg_time)
        print(f"  BiDijkstra: {avg_time:.4f} ms")
        
        # Test A*
        a_star = AStarSearch(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            a_star.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        a_star_times.append(avg_time)
        print(f"  A*: {avg_time:.4f} ms")
        
        # Test Bellman-Ford
        bf = BellmanFord(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bf.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bf_times.append(avg_time)
        print(f"  Bellman-Ford: {avg_time:.4f} ms")
        
        # Test JPS
        jps = JumpPointSearch(graph)
        times = []
        for s, d in test_pairs[:3]:
            start = time.time()
            try:
                jps.find_shortest_path(s, d)
                times.append(time.time() - start)
            except:
                pass
        if times:
            avg_time = sum(times) / len(times) * 1000
            jps_times.append(avg_time)
        else:
            jps_times.append(None)
        print(f"  JPS: {jps_times[-1]:.4f} ms" if jps_times[-1] else "  JPS: N/A")
    
    # Create plot with log scale
    fig, ax = plt.subplots(figsize=(11, 7))
    
    ax.loglog(sizes, bi_dijkstra_times, marker='o', label='BiDijkstra', 
              linewidth=2.5, markersize=9, base=10)
    ax.loglog(sizes, a_star_times, marker='s', label="A*", 
              linewidth=2.5, markersize=9, base=10)
    ax.loglog(sizes, bf_times, marker='^', label='Bellman-Ford', 
              linewidth=2.5, markersize=9, base=10)
    if jps_times and any(jps_times):
        jps_filtered = [t for t in jps_times if t is not None]
        if jps_filtered:
            ax.loglog(sizes[:len(jps_filtered)], jps_filtered, marker='d', label='JPS', 
                     linewidth=2.5, markersize=9, base=10)
    
    ax.set_xlabel('Graph Size (Vertices, log scale)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Runtime (ms, log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Algorithm Comparison: Sparse Graphs (5% Density)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, which='both')
    
    # Add complexity annotations
    ax.text(0.98, 0.05, 'BiDijkstra: O(V log V)\nA*: O((V+E)log V)\nBF: O(VE)\nJPS: O((V+E)log V)*', 
            transform=ax.transAxes, fontsize=10, verticalalignment='bottom',
            horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    # Add note about JPS on general graphs
    ax.text(0.98, 0.15, '*JPS is O(V) on grids only.\nOn general graphs, it behaves like A*.', 
            transform=ax.transAxes, fontsize=8, verticalalignment='bottom',
            horizontalalignment='right', style='italic', color='red')
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'algorithms_comparison.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return {
        'sizes': sizes,
        'bi_dijkstra': bi_dijkstra_times,
        'a_star': a_star_times,
        'bellman_ford': bf_times,
        'jps': jps_times
    }


def generate_complexity_analysis_graphs():
    """Generate empirical vs theoretical complexity analysis graphs."""
    print("\n" + "="*80)
    print("GENERATING: Empirical vs Theoretical Complexity Analysis")
    print("="*80)
    
    if not MATPLOTLIB_AVAILABLE:
        print("Skipping graph generation (matplotlib not available)")
        return {}
    
    sizes = [20, 40, 60, 80, 100, 150, 200]
    empirical = []
    theoretical_v_log_v = []
    theoretical_v2_log_v = []
    
    for size in sizes:
        # Generate sparse graph
        graph = GraphGenerator.create_weighted_graph(size, 0.08, max_weight=100, seed=42)
        
        # Measure empirical time
        test_pairs = TestCaseGenerator.generate_test_pairs(size, 5, seed=42)
        bi_dijkstra = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bi_dijkstra.find_shortest_path(s, d)
            times.append(time.time() - start)
        empirical_seconds = sum(times) / len(times)
        empirical.append(empirical_seconds)
        
        # Compute theoretical bounds (in operations, not time)
        import math
        v_log_v = size * math.log(size) if size > 0 else 1
        v2_log_v = (size ** 2) * math.log(size) if size > 0 else 1
        
        # Store as raw values - scale will be determined by fitting
        theoretical_v_log_v.append(v_log_v)
        theoretical_v2_log_v.append(v2_log_v)
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linear scale plot
    ax1.plot(sizes, empirical, marker='o', label='Empirical (BiDijkstra)', 
             linewidth=2.5, markersize=8, color='blue')
    ax1.plot(sizes, theoretical_v_log_v, '--', label='V log V (Sparse)', 
             linewidth=2, color='red', alpha=0.7)
    ax1.set_xlabel('Graph Size (Vertices)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Runtime (microseconds)', fontsize=11, fontweight='bold')
    ax1.set_title('Empirical vs Theoretical: Linear Scale', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Log scale plot
    ax2.loglog(sizes, empirical, marker='o', label='Empirical (BiDijkstra)', 
               linewidth=2.5, markersize=8, color='blue', base=10)
    ax2.loglog(sizes, theoretical_v_log_v, '--', label='V log V (scaled)', 
               linewidth=2, color='red', alpha=0.7, base=10)
    ax2.loglog(sizes, theoretical_v2_log_v, ':', label='V^2 log V (dense)', 
               linewidth=2, color='green', alpha=0.7, base=10)
    ax2.set_xlabel('Graph Size (Vertices, log scale)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Runtime (microseconds, log scale)', fontsize=11, fontweight='bold')
    ax2.set_title('Empirical vs Theoretical: Log Scale', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.suptitle('Complexity Analysis: BiDijkstra on Sparse Graphs', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), 'complexity_analysis.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {output_path}")
    plt.close()
    
    return {
        'sizes': sizes,
        'empirical': empirical,
        'v_log_v': theoretical_v_log_v,
        'v2_log_v': theoretical_v2_log_v
    }


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
        
        # Test A* Search
        print("Testing A* Search...")
        a_star = AStarSearch(graph)
        benchmark.benchmark_algorithm(
            f"AStar_{config['name']}",
            a_star,
            test_pairs,
            config['vertices']
        )
        
        # Test Bellman-Ford
        print("Testing Bellman-Ford...")
        bf = BellmanFord(graph)
        benchmark.benchmark_algorithm(
            f"BellmanFord_{config['name']}",
            bf,
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
    
    # Test A* Search
    print("A* Search (with zero heuristic):")
    a_star = AStarSearch(graph)
    distance, path = a_star.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Path: {path}")
    print(f"  Operations: {a_star.operations_count}\n")
    
    # Test Bellman-Ford
    print("Bellman-Ford:")
    bf = BellmanFord(graph)
    distance, path = bf.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Path: {path}")
    print(f"  Operations: {bf.operations_count}\n")
    
    # Test Jump Point Search
    print("Jump Point Search:")
    jps = JumpPointSearch(graph)
    distance, path = jps.find_shortest_path(source, destination)
    print(f"  Distance: {distance}")
    print(f"  Path: {path}")
    print(f"  Operations: {jps.operations_count}\n")
    
    print("[OK] All algorithms completed successfully!\n")


if __name__ == "__main__":
    # Run simple test first
    run_simple_test()
    
    # Run comprehensive benchmark
    print("\n" + "="*80)
    print("COMPREHENSIVE BENCHMARK")
    print("="*80 + "\n")
    run_comprehensive_benchmark()
    
    # Generate empirical complexity graphs
    print("\n" + "="*80)
    print("GENERATING EMPIRICAL COMPLEXITY GRAPHS")
    print("="*80)
    
    if MATPLOTLIB_AVAILABLE:
        print("\nGenerating 4 analysis graphs...")
        
        # Generate all graphs
        graph_data = {}
        
        graph_data['runtime_vs_size'] = generate_runtime_vs_size_graph()
        graph_data['runtime_vs_density'] = generate_runtime_vs_density_graph()
        graph_data['comparison'] = generate_algorithms_comparison_graph()
        graph_data['complexity'] = generate_complexity_analysis_graphs()
        
        # Save graph data to JSON
        output_file = os.path.join(os.path.dirname(__file__), "graph_data.json")
        with open(output_file, 'w') as f:
            # Convert graph_data to JSON-serializable format
            json_data = {}
            for key, data in graph_data.items():
                json_data[key] = {k: v for k, v in data.items() if k != 'sizes' and k != 'densities'}
            json.dump(json_data, f, indent=2)
        
        print(f"\n[OK] Graph data saved to: {output_file}")
        print("\n" + "="*80)
        print("GRAPH GENERATION COMPLETE")
        print("="*80)
        print("\nGenerated graphs:")
        print("  1. runtime_vs_size.png - Algorithm performance vs graph size")
        print("  2. runtime_vs_density.png - Algorithm performance vs graph density")
        print("  3. algorithms_comparison.png - All algorithms compared on sparse graphs")
        print("  4. complexity_analysis.png - Empirical vs theoretical complexity")
        print("\nAll graphs saved in: tests/")
    else:
        print("\nMatplotlib not available - skipping graph generation")
        print("Install with: pip install matplotlib")

