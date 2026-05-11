# Implementation Guide - Shortest Path Algorithms

## Overview

This document explains the implementation design decisions, key techniques, and important considerations for each algorithm.

---

## 1. Bidirectional Dijkstra Implementation

### Design Approach

**Two Independent Dijkstra Searches:**
- Forward search from source vertex
- Backward search from destination vertex
- Both use standard Dijkstra with priority queue
- Searches run alternately in main loop

### Key Data Structures

```python
# Forward search
forward_dist = {v: float('inf') for v in vertices}    # Distance from source
forward_prev = {v: None for v in vertices}            # Previous node
forward_heap = [(0, source)]                          # Priority queue

# Backward search  
backward_dist = {v: float('inf') for v in vertices}   # Distance from destination
backward_prev = {v: None for v in vertices}           # Previous node
backward_heap = [(0, destination)]                    # Priority queue

# Meeting detection
best_distance = float('inf')                          # Best path found so far
meeting_point = None                                  # Where searches meet
```

### Critical Implementation Details

**1. Termination Condition**
```python
# Continue while both queues have elements
while forward_heap and backward_heap:
    # Check for meeting after each expansion
    if u_forward in backward_dist:
        candidate = forward_dist[u_forward] + backward_dist[u_forward]
        if candidate < best_distance:
            best_distance = candidate
            meeting_point = u_forward
```

**Why this works:**
- Once searches meet, shortest path = forward distance + backward distance at meeting point
- Must check ALL possible meeting points (not just first meeting)
- Path may go through non-obvious nodes

**2. Path Reconstruction**
```python
path = []

# Backward from source to meeting point
current = meeting_point
while current is not None:
    path.append(current)
    current = forward_prev[current]
path.reverse()  # Reverse to get source → meeting

# Forward from meeting point to destination
current = backward_prev[meeting_point]
while current is not None:
    path.append(current)
    current = backward_prev[current]
```

**Challenge:** Backward search builds predecessor chain backwards, requires careful reconstruction

**3. Metrics Tracking**
```python
self.operations_count    # Total graph operations
self.heap_operations     # Push/pop operations
self.comparisons         # Distance comparison count
```

### Performance Optimization Tips

1. **Stop Early:** Terminate when forward distance < best_distance + margin
2. **Priority Queue:** Use binary heap (O(log V)), not Fibonacci (overhead too high for typical sizes)
3. **Closed Set:** Track visited nodes to avoid reprocessing
4. **Distance Pruning:** Skip nodes where current_dist > stored_distance

### Strengths
✓ Simple to understand and implement
✓ Guaranteed optimal (same as Dijkstra)
✓ Natural 2-4x speedup from both directions
✓ Linear space complexity

### Weaknesses
✗ Not optimal for all-pairs
✗ Overhead of maintaining two searches
✗ Requires reverse graph for true bidirectionality

---

## 2. Johnson's Algorithm Implementation

### Design Approach

**Three-Phase Algorithm:**
1. **Reweighting Phase:** Use Bellman-Ford to compute h values
2. **Dijkstra Phase:** Run Dijkstra from each vertex with reweighted edges
3. **Restoration Phase:** Convert distances back to original weights

### Key Data Structures

```python
# Phase 1: Reweighting
h = {v: float('inf') for v in vertices}               # h values
graph_extended = {**graph}                            # Add auxiliary vertex
graph_extended[-1] = [(v, 0) for v in vertices]       # Auxiliary edges

# Phase 2: Per-vertex Dijkstra
distances = {}  # Store all-pairs result
all_distances = {u: {} for u in vertices}             # Intermediate Dijkstra results

# Phase 3: Restoration  
d_original = {u: {} for u in vertices}                # Original weight distances
```

### Critical Implementation Details

**1. Bellman-Ford Reweighting**
```python
def _bellman_ford_reweighting(self):
    # Initialize with auxiliary vertex
    h = {v: float('inf') for v in self.vertices}
    h[auxiliary] = 0
    
    # V-1 relaxation rounds
    for _ in range(len(self.vertices)):
        for u in graph_extended:
            if h[u] != float('inf'):
                for v, weight in graph_extended.get(u, []):
                    if h[u] + weight < h[v]:
                        h[v] = h[u] + weight
    
    # Check for negative cycles
    for u in graph_extended:
        for v, weight in graph_extended.get(u, []):
            if h[u] + weight < h[v]:
                return None  # Negative cycle detected
    
    return h
```

**Why auxiliary vertex:**
- Provides single source to all vertices
- Edges with weight 0 don't affect shortest paths
- h[v] = shortest distance from auxiliary to v

**2. Edge Reweighting Formula**
```python
# Original edge weight: w(u,v)
# Reweighted: w'(u,v) = w(u,v) + h[u] - h[v]

# Properties:
# 1. All reweighted edges non-negative
# 2. Shortest path distances preserved!
#    Distance from u to v = d'(u,v) + h[v] - h[u]
```

**Mathematical Proof:**
- For any path P = u₀ → u₁ → ... → uₖ → v
- Original weight: Σ w(uᵢ, uᵢ₊₁)
- Reweighted: Σ [w(uᵢ, uᵢ₊₁) + h[uᵢ] - h[uᵢ₊₁]]
- Telescoping sum: w(original) + h[u] - h[v]
- Ratios preserved, so shortest paths same!

**3. All-Pairs Computation**
```python
def find_all_pairs_shortest_paths(self):
    h = self._bellman_ford_reweighting()  # O(VE)
    
    all_distances = {}
    for source in self.vertices:          # Run V times
        distances = self._dijkstra_reweighted(source, h)  # O((V+E)logV)
        all_distances[source] = distances
    
    # Restore original weights: O(V²)
    result = {}
    for u in self.vertices:
        for v in self.vertices:
            if all_distances[u][v] != float('inf'):
                result[u][v] = all_distances[u][v] + h[v] - h[u]
    
    return result
```

### Performance Optimization Tips

1. **Skip Bellman-Ford:** If graph has no negative weights (modify algorithm)
2. **Parallelize Dijkstra:** Run all V Dijkstra calls in parallel
3. **Fibonacci Heap:** Implement Dijkstra with Fibonacci heap for O(VE + V²logV)
4. **Caching:** Store all-pairs result for multiple queries

### Strengths
✓ Optimal for sparse graphs (better than Floyd-Warshall)
✓ Handles negative weights
✓ Amortizes cost over many queries
✓ Parallelizable Dijkstra phase

### Weaknesses
✗ High memory overhead (O(V²))
✗ Not ideal for single-pair queries
✗ Setup cost high (Bellman-Ford phase)
✗ Detects but can't handle negative cycles

---

## 3. Jump Point Search Implementation

### Design Approach

**A* Variant with Symmetry Exploitation:**
- Use heuristic to guide search (like A*)
- Identify "jump points" where path must turn
- Skip intermediate nodes on straight paths
- Recursively explore jump directions

### Key Data Structures

```python
# A* standard structures
open_set = [(f_score, g_score, node)]                 # Priority queue
came_from = {}                                        # Path reconstruction
g_score = {v: float('inf') for v in vertices}         # Cost from start
closed_set = set()                                    # Visited nodes

# JPS-specific
forced_neighbors = {}                                 # Cached forced neighbors
jump_directions = []                                  # Direction vectors (for grids)
```

### Critical Implementation Details

**1. Jump Point Detection**
```python
def _is_jump_point(self, current, parent, goal):
    # Goal is always a jump point
    if current == goal:
        return True
    
    # Otherwise, it's a jump point if it has forced neighbors
    forced = self._get_forced_neighbors(current, parent)
    return len(forced) > 0
```

**Jump Point Definition:**
- Vertex with forced neighbors
- Forces neighbors exist when there's an "obstacle" nearby
- In grids: corner or dead-end
- In graphs: neighbor unreachable from parent direction

**2. Forced Neighbors Concept**
```python
def _get_forced_neighbors(self, current, parent):
    # In grid: if obstacle blocks path, neighbor becomes forced
    # Example: Moving right, obstacle above → node above is forced
    #
    #  ■ → ■ (forced)
    #    X ■
    #
    # In general graphs: different neighbor not reachable from parent
    
    forced = []
    for neighbor in graph[current]:
        # If neighbor can't be reached directly from parent
        # (i.e., requires going through current)
        if neighbor not in graph[parent]:
            forced.append(neighbor)
    
    return forced
```

**3. Directional Jumping**
```python
# Key insight: if moving in same direction, keep going!
# Only expand new directions at jump points

# Forward from current
for neighbor, weight in graph[current]:
    if neighbor not in closed_set:
        tentative_g = g_score[current] + weight
        
        if tentative_g < g_score[neighbor]:
            # Is this a jump point?
            if _is_jump_point(neighbor, current, goal):
                # Add to open set for expansion
                heappush(open_set, (...))
            elif not _has_forced_neighbors(neighbor, current):
                # Same direction, keep jumping
                heappush(open_set, (...))
```

**4. Heuristic Integration**
```python
# f_score = g_score + heuristic(current, goal)
# Guides search toward goal
# Quality of heuristic critical to performance

# Good heuristics:
# - Manhattan distance (for grids)
# - Euclidean distance (for continuous space)
# - Chebyshev distance (for grid diagonals)

f_score = tentative_g + self.heuristic(neighbor, destination)
```

### Performance Optimization Tips

1. **Precompute Jump Points:** For grids, precompute all jump distances
2. **Better Heuristics:** Admissible and consistent heuristics crucial
3. **Caching:** Remember explored directions to avoid recomputation
4. **Recursive Jumping:** Implement recursive jump for smoother exploration
5. **Bidirectional:** Run JPS from both ends for further speedup

### Strengths
✓ Exceptional speedup on grids (10-40x)
✓ Remains efficient on general graphs (2-4x)
✓ Linear space complexity like A*
✓ Parallelizable jump exploration

### Weaknesses
✗ Overhead on very sparse or random graphs
✗ Quality depends heavily on heuristic
✗ Complex forced neighbor detection in general graphs
✗ Not optimal for all-pairs (single-pair focused)

---

## 4. Metrics Collection Strategy

### Metrics Tracked in Each Algorithm

```python
class BaseAlgorithm:
    def __init__(self):
        self.operations_count = 0      # Total operations
        self.comparisons = 0           # Distance comparisons
        self.relaxations = 0           # Successful distance updates
        
    def reset_metrics(self):
        """Reset counters for next test."""
        self.operations_count = 0
        self.comparisons = 0
        self.relaxations = 0
```

### Where to Increment

**operations_count:** Incremented at every graph traversal
```python
for neighbor, weight in graph[u]:
    self.operations_count += 1  # Count this edge examination
```

**comparisons:** Incremented at distance comparison
```python
if new_dist < distances[v]:
    self.comparisons += 1  # Count the comparison
    distances[v] = new_dist
    self.relaxations += 1
```

### Benchmark Collection

```python
class AlgorithmBenchmark:
    def benchmark_algorithm(self, name, algorithm, test_pairs, graph_size):
        for source, destination in test_pairs:
            algorithm.reset_metrics()  # Fresh start
            
            start = time.perf_counter()
            distance, path = algorithm.find_shortest_path(source, destination)
            elapsed = time.perf_counter() - start
            
            # Record metrics
            results["execution_times"].append(elapsed)
            results["operation_counts"].append(algorithm.operations_count)
            results["comparison_counts"].append(algorithm.comparisons)
```

---

## 5. Testing and Validation

### Correctness Verification

```python
# Multiple algorithms should find SAME shortest distance
# (though paths may differ)

distance1, _ = bidijkstra.find_shortest_path(u, v)
distance2, _ = johnson.find_shortest_path(u, v)
distance3, _ = jps.find_shortest_path(u, v)

assert distance1 == distance2 == distance3, "Algorithms disagree!"
```

### Test Case Categories

1. **Simple Graphs:** Manual verification possible
2. **Random Graphs:** Check consistency
3. **Grids:** Verify Manhattan distance matches
4. **Edge Cases:** Single vertex, disconnected, etc.

---

## 6. Common Pitfalls and Solutions

### Pitfall 1: Infinite Distances
**Problem:** Floating-point representation of infinity
**Solution:** Use `float('inf')` consistently, check `== float('inf')` before operations

### Pitfall 2: Off-by-One Errors
**Problem:** Path reconstruction goes one step too far
**Solution:** Carefully manage predecessor pointers, test with simple cases

### Pitfall 3: Modified Global State
**Problem:** Reusing graph without resetting algorithm state
**Solution:** Call `reset_metrics()` before each test

### Pitfall 4: Priority Queue Issues
**Problem:** Stale entries in heap with updated distances
**Solution:** Check `if current_dist > distances[u]: continue`

### Pitfall 5: Negative Cycle Handling
**Problem:** Johnson's doesn't specify behavior on negative cycles
**Solution:** Return `None` explicitly, handle in caller

---

## References and Further Reading

1. **Dijkstra's Algorithm:**
   - "A note on two problems in connexion with graphs" (1959)
   - Time: O((V+E)logV)

2. **Bidirectional Search:**
   - Natural speedup from both directions
   - Requires careful meeting point detection

3. **Johnson's Algorithm:**
   - "Efficient algorithms for shortest paths in sparse networks" (1977)
   - Time: O(V²logV + VE)

4. **Jump Point Search:**
   - "Jump Point Search" (2012)
   - Exploits symmetry in uniform-cost grids
   - Often 10-40x faster than A*

5. **A* Search:**
   - Hart, Nilsson, Raphael (1968)
   - Foundation for heuristic-based pathfinding

---

**Version:** 1.0  
**Status:** Complete  
**Last Updated:** 2026-05-11
