# CSE 317: Shortest Path Algorithms Project

## Overview
This project implements and analyzes four shortest path algorithms:
1. **Bidirectional Dijkstra** - O(V log V) bidirectional search
2. **A* Search** - O((V+E)log V) heuristic-guided search
3. **Jump Point Search (JPS)** - O(√V) grid-optimized pathfinding
4. **Bellman-Ford** - O(VE) relaxation-based algorithm

## Project Structure

```
DAA-Project/
├── algorithms/              # Algorithm implementations
│   ├── bidirectional_dijkstra.py    # Bidirectional Dijkstra
│   ├── a_star_algorithm.py          # A* Search with heuristics
│   ├── jump_point_search.py         # Jump Point Search
│   ├── bellman_ford.py              # Bellman-Ford algorithm
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
├── create_presentation.py           # Presentation generation script
└── README.md
```

## Quick Start

### Running Tests

```bash
python tests/test_benchmark.py
```

This will:
1. Run a simple verification test on all four algorithms
2. Execute comprehensive benchmarks on various graph sizes and densities
3. Generate performance reports and CSV output
4. Create performance comparison graphs (if matplotlib available)

### Output

- Console report with detailed metrics and comparative analysis
- CSV file (`benchmark_results.csv`) with exportable results
- PNG graphs showing performance comparisons
- Updated presentations with full analysis

## Algorithm Descriptions

### 1. Bidirectional Dijkstra
- **Approach**: Runs Dijkstra simultaneously from source and destination
- **Advantage**: Often finds shortest path faster by meeting in the middle
- **Best for**: Dense graphs, small to medium-sized graphs
- **Key metrics tracked**: Operations, heap operations, comparisons

### 2. A* Search
- **Approach**: Combines actual cost g(n) and heuristic estimate h(n) for guided search
- **Advantage**: 14-45% fewer operations than BiDijkstra with good heuristic
- **Best for**: Graphs where good distance heuristics exist
- **Key metrics tracked**: Nodes opened, nodes closed, comparisons

### 3. Jump Point Search (JPS)
- **Approach**: A* variant that identifies and jumps over forced neighbors
- **Advantage**: 10-40× faster on true grid graphs
- **Best for**: Grid-like graphs, pathfinding with heuristics
- **Key metrics tracked**: Jump points found, operations, comparisons

### 4. Bellman-Ford
- **Approach**: Relax all edges V-1 times to find shortest paths
- **Advantage**: Handles negative edge weights and detects negative cycles
- **Best for**: Graphs with negative weights, cycle detection required
- **Key metrics tracked**: Relaxations, comparisons, operations

## Complexity Analysis

See [COMPLEXITY_ANALYSIS.md](docs/COMPLEXITY_ANALYSIS.md) for detailed theoretical and empirical complexity analysis.

### Summary

| Algorithm | Time Complexity | Space Complexity | Best for |
|-----------|-----------------|------------------|----------|
| Bidirectional Dijkstra | O((V+E) log V) | O(V) | Medium graphs, single-pair queries |
| A* Search | O((V+E) log V) | O(V) | Graphs with good heuristics |
| Jump Point Search | O(√V) grids | O(V) | Grid-based pathfinding |
| Bellman-Ford | O(VE) | O(V) | Negative weights, cycle detection |

## Metrics Collected

For each algorithm, we measure:
- **Execution Time**: Total, average, min, max, standard deviation
- **Operations Count**: Number of graph traversals
- **Comparisons**: Number of distance comparisons
- **Paths Found**: Success rate for test cases
- **Algorithm-Specific Metrics**:
  - Bidirectional Dijkstra: Heap operations
  - A* Search: Nodes opened, nodes closed
  - JPS: Jump points identified
  - Bellman-Ford: Relaxations performed

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
- **Bidirectional Dijkstra**: Reliable baseline with consistent O((V+E) log V) performance
- **A* Search**: 14-45% faster than BiDijkstra when good heuristic available
- **Jump Point Search**: 10-40× speedup on true grid structures
- **Bellman-Ford**: Necessary for graphs with negative weights; 2-5× slower on non-negative

## Implementation Notes

### Graph Representation
- Adjacency list: `Dict[int, List[Tuple[int, int]]]`
- Graph[u] = [(v, weight), ...] for each edge u→v

### Edge Weights
- Bidirectional Dijkstra, A*, JPS: Non-negative weights required
- Bellman-Ford: Handles negative weights (no negative cycles)

### Algorithm Properties

**Bidirectional Dijkstra**
- Terminates when searches meet
- Requires reverse graph lookups for true bidirectionality
- Better with undirected graphs

**A* Search**
- Uses heuristic functions (Manhattan, Euclidean distance)
- Zero heuristic equivalent to Dijkstra
- Performance depends on heuristic quality

**Jump Point Search**
- Heuristic-based optimization
- Particularly efficient on grids and lattice graphs
- Can be further optimized with preprocessing

**Bellman-Ford**
- Detects negative cycles
- Slower but guaranteed correct on any graph structure
- Each iteration relaxes all edges

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
