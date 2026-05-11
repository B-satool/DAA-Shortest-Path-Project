#!/usr/bin/env python
"""Debug script to test each graph generation function."""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithms.bidirectional_dijkstra import BidirectionalDijkstra
from algorithms.a_star_algorithm import AStarSearch
from algorithms.bellman_ford import BellmanFord
from algorithms.jump_point_search import JumpPointSearch
from algorithms.graph_utils import GraphGenerator, TestCaseGenerator

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("ERROR: matplotlib not available")
    sys.exit(1)

print("Testing graph generation functions one by one...\n")

# Test 1: Runtime vs Size
print("=" * 80)
print("TEST 1: generate_runtime_vs_size_graph()")
print("=" * 80)

try:
    sizes = [20, 40, 60, 80, 100, 150, 200]
    bi_dijkstra_times = []
    a_star_times = []
    bf_times = []
    
    for size in sizes:
        print(f"Testing size V={size}...")
        graph = GraphGenerator.create_weighted_graph(size, 0.08, max_weight=100, seed=42)
        test_pairs = TestCaseGenerator.generate_test_pairs(size, min(10, size//5), seed=42)
        
        # BiDijkstra
        bd = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bd.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bi_dijkstra_times.append(avg_time)
        
        # A*
        a_star = AStarSearch(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            a_star.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        a_star_times.append(avg_time)
        
        # Bellman-Ford
        bf = BellmanFord(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bf.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bf_times.append(avg_time)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, bi_dijkstra_times, marker='o', label='BiDijkstra', linewidth=2, markersize=8)
    ax.plot(sizes, a_star_times, marker='s', label='A*', linewidth=2, markersize=8)
    ax.plot(sizes, bf_times, marker='^', label='Bellman-Ford', linewidth=2, markersize=8)
    ax.set_xlabel('Graph Size (Vertices)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Runtime (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Runtime vs Graph Size (Sparse Graphs: ~8% Density)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    output_path = os.path.join(os.path.dirname(__file__), 'tests', 'debug_runtime_vs_size.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Successfully generated: {output_path}\n")
except Exception as e:
    print(f"✗ ERROR in TEST 1:\n{type(e).__name__}: {e}\n")
    import traceback
    traceback.print_exc()

# Test 2: Runtime vs Density
print("=" * 80)
print("TEST 2: generate_runtime_vs_density_graph()")
print("=" * 80)

try:
    densities = [0.05, 0.10, 0.15, 0.25, 0.35, 0.50, 0.70]
    size = 100
    bi_dijkstra_times = []
    a_star_times = []
    bf_times = []
    
    for density in densities:
        print(f"Testing density {density*100:.0f}%...")
        graph = GraphGenerator.create_weighted_graph(size, density, max_weight=100, seed=42)
        test_pairs = TestCaseGenerator.generate_test_pairs(size, 10, seed=42)
        
        # BiDijkstra
        bd = BidirectionalDijkstra(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bd.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bi_dijkstra_times.append(avg_time)
        
        # A*
        a_star = AStarSearch(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            a_star.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        a_star_times.append(avg_time)
        
        # Bellman-Ford
        bf = BellmanFord(graph)
        times = []
        for s, d in test_pairs:
            start = time.time()
            bf.find_shortest_path(s, d)
            times.append(time.time() - start)
        avg_time = sum(times) / len(times) * 1000
        bf_times.append(avg_time)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(densities, bi_dijkstra_times, marker='o', label='BiDijkstra', linewidth=2, markersize=8)
    ax.semilogy(densities, a_star_times, marker='s', label='A*', linewidth=2, markersize=8)
    ax.semilogy(densities, bf_times, marker='^', label='Bellman-Ford', linewidth=2, markersize=8)
    ax.set_xlabel('Graph Density', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Runtime (ms, log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Runtime vs Graph Density (100 vertices)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, which='both')
    
    output_path = os.path.join(os.path.dirname(__file__), 'tests', 'debug_runtime_vs_density.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ Successfully generated: {output_path}\n")
except Exception as e:
    print(f"✗ ERROR in TEST 2:\n{type(e).__name__}: {e}\n")
    import traceback
    traceback.print_exc()

print("=" * 80)
print("Debug script completed!")
print("=" * 80)
