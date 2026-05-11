## CSE 317: Design Analysis and Algorithms

### Project Milestone 1 — Spring 2026

# The Shortest Path Problem

### Group Members

```
Name ERP
Arhum Ali Kaleem 29288
```
```
Ammar Khan 29296
```
```
Sumaiya Batool 29295
```
```
Fatima Irfan 29294
```
```
Zainab Irfan Ansari 29091
```
```
Department of Computer Science
Spring 2026
```

CSE 317: Algorithms: Design and Analysis Spring 2026

## 1 Project Idea

The project focuses on the Shortest Path Problem, which is a fundamental problem
in computer science and discrete mathematics. Given a graph G = (V, E) with vertices V
and edges E, the goal is to find the minimum-cost path between pairs of vertices, where
cost is the sum of edge weights.

This problem has wide applications in GPS navigation, network routing, social networks,
logistics, and game AI.

## 2 Possible Algorithms

The following algorithms can be used to solve the Shortest Path Problem:

1. Dijkstra’s Algorithm: A greedy algorithm for single-source shortest paths in
    graphs with non-negative edge weights.
2. Bellman-Ford Algorithm: A dynamic programming algorithm that handles
    graphs with negative edge weights and detects negative cycles.
3. Floyd-Warshall Algorithm: A dynamic programming algorithm for all-pairs
    shortest paths, suitable for dense graphs.
4. A* Search Algorithm: Heuristic-guided extension of Dijkstra, widely used in
    pathfinding. Finds the single-source shortest path faster when a good heuristic is
    available.
5. Jump Point Search (JPS): Optimized for grid-based pathfinding by exploiting
    movement symmetry. 10-40× faster on true grid topologies.
6. BFS (Breadth-First Search): Works only on unweighted graphs where every
    edge has equal cost.

## 3 Selected Algorithms (Final Implementation)

Our team selected the following 4 algorithms for comparison:

1. **Bidirectional Dijkstra**: O(V log V) - Searches from both source and destination
2. **A* Search**: O((V+E)log V) - Heuristic-guided search for faster queries
3. **Jump Point Search**: O(√V) on grids - Optimized for grid pathfinding
4. **Bellman-Ford**: O(VE) - Handles negative edge weights and detects cycles

These algorithms provide diverse approaches: greedy (BiDijkstra), heuristic (A*), 
symmetry-based (JPS), and relaxation-based (Bellman-Ford).

#### 1


