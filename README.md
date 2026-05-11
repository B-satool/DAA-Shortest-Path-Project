# CSE 317: Shortest Path Algorithms Project

## Overview
This project implements and analyzes three shortest path algorithms:
1. **Bidirectional Dijkstra**
2. **Johnson's Algorithm**
3. **Jump Point Search (JPS)**

## Project Structure

```
DAA-Project/
├── algorithms/              # Algorithm implementations
│   ├── bidirectional_dijkstra.py    # Bidirectional Dijkstra
│   ├── johnsons_algorithm.py        # Johnson's Algorithm
│   ├── jump_point_search.py         # Jump Point Search
│   ├── graph_utils.py               # Graph generation and utilities
│   └── __init__.py
├── benchmarks/              # Performance benchmarking
│   ├── metrics.py                   # Metrics collection and reporting
│   └── __init__.py
├── tests/                   # Test suite and benchmarks
│   ├── test_benchmark.py            # Main benchmark runner
│   └── __init__.py
├── docs/
│   └── COMPLEXITY_ANALYSIS.md       # Detailed complexity analysis
└── README.md
```

## Quick Start

### Running Tests

```bash
python tests/test_benchmark.py
```

This will:
1. Run a simple verification test on all three algorithms
2. Execute comprehensive benchmarks on various graph sizes and densities
3. Generate performance reports and CSV output

### Output

- Console report with detailed metrics and comparative analysis
- CSV file (`benchmark_results.csv`) with exportable results

## Algorithm Descriptions

### 1. Bidirectional Dijkstra
- **Approach**: Runs Dijkstra simultaneously from source and destination
- **Advantage**: Often finds shortest path faster by meeting in the middle
- **Best for**: Dense graphs, small to medium-sized graphs
- **Key metrics tracked**: Operations, heap operations, comparisons

### 2. Johnson's Algorithm
- **Approach**: Combines Bellman-Ford for reweighting with Dijkstra
- **Advantage**: Efficient for all-pairs shortest paths on sparse graphs
- **Best for**: Sparse graphs requiring all-pairs or multiple queries
- **Key metrics tracked**: Relaxations, Dijkstra calls, comparisons

### 3. Jump Point Search (JPS)
- **Approach**: A* variant that identifies and jumps over forced neighbors
- **Advantage**: Significantly faster on uniform-cost graphs
- **Best for**: Grid-like graphs, pathfinding with heuristics
- **Key metrics tracked**: Jump points found, operations, comparisons

## Complexity Analysis

See [COMPLEXITY_ANALYSIS.md](docs/COMPLEXITY_ANALYSIS.md) for detailed theoretical and empirical complexity analysis.

### Summary

| Algorithm | Time Complexity | Space Complexity | Best Case | Worst Case |
|-----------|-----------------|------------------|-----------|-----------|
| Bidirectional Dijkstra | O((V+E) log V) | O(V) | O((V+E) log V) | O((V+E) log V) |
| Johnson's Algorithm | O(V²log V + VE) | O(V²) | O(V²log V + VE) | O(V³) |
| Jump Point Search | O(V+E) | O(V) | O(V) | O(V+E) |

## Metrics Collected

For each algorithm, we measure:
- **Execution Time**: Total, average, min, max, standard deviation
- **Operations Count**: Number of graph traversals
- **Comparisons**: Number of distance comparisons
- **Paths Found**: Success rate for test cases
- **Algorithm-Specific Metrics**:
  - Bidirectional: Heap operations
  - Johnson's: Relaxations, Dijkstra calls
  - JPS: Jump points identified

## Test Cases

Benchmarks include:
- Small sparse graphs (20 vertices, 15% density)
- Small dense graphs (20 vertices, 60% density)
- Medium sparse graphs (100 vertices, 5% density)
- Medium dense graphs (100 vertices, 30% density)
- Large sparse graphs (300 vertices, 2% density)

Each configuration tests 15-25 random source-destination pairs.

## Results and Analysis

After running the benchmark, consult:
1. **Console Output**: Real-time performance metrics and comparative analysis
2. **benchmark_results.csv**: Machine-readable results for spreadsheet analysis
3. **Performance Report**: Detailed statistics including fastest algorithm, most efficient operations, etc.

## Key Findings

The benchmark reveals:
- **Bidirectional Dijkstra**: Best for single-pair shortest paths on medium graphs
- **Johnson's Algorithm**: Optimal for all-pairs problems on sparse graphs
- **Jump Point Search**: Superior performance on grid-like structures with good heuristics

## Implementation Notes

### Graph Representation
- Adjacency list: `Dict[int, List[Tuple[int, int]]]`
- Graph[u] = [(v, weight), ...] for each edge u→v

### Edge Weights
- Must be positive (non-negative for most algorithms)
- Johnson's Algorithm can handle negative weights (no negative cycles)

### Algorithm Properties

**Bidirectional Dijkstra**
- Terminates when searches meet
- Requires reverse graph lookups for true bidirectionality
- Better with undirected graphs

**Johnson's Algorithm**
- Handles all-pairs computation
- Uses Bellman-Ford for reweighting
- Detects and rejects negative cycles

**Jump Point Search**
- Heuristic-based optimization
- Particularly efficient on grids and lattice graphs
- Can be further optimized with preprocessing

## References

- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
- Johnson, D. B. (1977). "Efficient algorithms for shortest paths in sparse networks"
- Anya, A. et al. (2012). "Jump Point Search: Fast and practical pathfinding"

## Team Members

- Arhum Ali Kaleem (29288)
- Ammar Khan (29296)
- Sumaiya Batool (29295)
- Fatima Irfan (29294)
- Zainab Irfan Ansari (29091)

---

For detailed complexity analysis and empirical results, see the project documentation and benchmark outputs.
