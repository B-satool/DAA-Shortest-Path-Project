"""
Bellman-Ford Algorithm for Single-Source Shortest Paths

Time Complexity: O(VE)
Space Complexity: O(V)

The Bellman-Ford algorithm finds the shortest path from a single source to all other
vertices in a weighted graph. Unlike Dijkstra's algorithm, it can handle negative edge
weights (but not negative cycles).

Key Properties:
- Handles negative edge weights
- Detects negative cycles
- Slower than Dijkstra for non-negative weights
- Guaranteed correctness for non-negative weights

Algorithm Steps:
1. Initialize distances to infinity (except source = 0)
2. Relax all edges V-1 times
3. Each relaxation updates shortest distances
4. Optional: Check for negative cycles (relaxing again shouldn't improve distances)
"""

from typing import Dict, List, Tuple, Optional


class BellmanFord:
    """
    Bellman-Ford shortest path algorithm for weighted graphs with optional negative edges.
    """
    
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]]):
        """
        Initialize Bellman-Ford algorithm with a weighted graph.
        
        Args:
            graph: Adjacency list representation {vertex: [(neighbor, weight), ...]}
        """
        self.graph = graph
        self.vertices = set(graph.keys())
        
        # Metrics tracking
        self.operations_count = 0
        self.comparisons = 0
        self.relaxations_performed = 0
    
    def reset_metrics(self):
        """Reset metrics counters for new benchmark run."""
        self.operations_count = 0
        self.comparisons = 0
        self.relaxations_performed = 0
    
    def find_shortest_path(self, source: int, destination: int) -> Tuple[int, List[int]]:
        """
        Find shortest path from source to destination using Bellman-Ford algorithm.
        
        Args:
            source: Starting vertex
            destination: Target vertex
        
        Returns:
            Tuple of (distance, path)
            - distance: Length of shortest path (infinity if unreachable)
            - path: List of vertices from source to destination (empty if unreachable)
        """
        self.reset_metrics()
        
        # Step 1: Initialize distances and predecessors
        distances: Dict[int, int] = {v: float('inf') for v in self.vertices}
        distances[source] = 0
        predecessors: Dict[int, Optional[int]] = {v: None for v in self.vertices}
        
        self.operations_count += len(self.vertices) * 2  # Initialization
        
        # Step 2: Relax edges V-1 times
        num_vertices = len(self.vertices)
        
        for iteration in range(num_vertices - 1):
            # Track if any relaxation occurred in this iteration
            relaxed_any = False
            
            # Relax each edge
            for u in self.graph:
                if distances[u] == float('inf'):
                    continue
                
                for v, weight in self.graph[u]:
                    self.operations_count += 1
                    self.comparisons += 1
                    
                    # Relax edge (u, v)
                    new_distance = distances[u] + weight
                    
                    if new_distance < distances[v]:
                        distances[v] = new_distance
                        predecessors[v] = u
                        self.relaxations_performed += 1
                        relaxed_any = True
                        self.operations_count += 2  # Update distance and predecessor
            
            # Early termination if no relaxations occurred
            if not relaxed_any:
                break
        
        # Reconstruct path
        distance = distances[destination]
        path = self._reconstruct_path(predecessors, source, destination)
        
        return (distance, path)
    
    def _reconstruct_path(self, predecessors: Dict[int, Optional[int]], 
                         source: int, destination: int) -> List[int]:
        """
        Reconstruct shortest path using predecessor pointers.
        
        Args:
            predecessors: Dictionary of parent pointers
            source: Starting vertex
            destination: Target vertex
        
        Returns:
            List of vertices representing the path (empty if no path exists)
        """
        path = []
        current = destination
        
        # Follow predecessors back to source
        while current is not None:
            path.append(current)
            if current == source:
                break
            current = predecessors[current]
        
        # Check if we reached the source
        if current is not None and current == source:
            path.reverse()
            return path
        
        return []  # No path found
    
    def _bellman_ford_all_pairs(self) -> Optional[Dict[int, Dict[int, int]]]:
        """
        Compute shortest paths from all vertices to all other vertices.
        This uses Bellman-Ford algorithm for each source.
        
        Returns:
            Dictionary: {source: {destination: distance}} or None if negative cycle detected
        """
        all_pairs = {}
        
        for source in self.vertices:
            distances = {v: float('inf') for v in self.vertices}
            distances[source] = 0
            predecessors = {v: None for v in self.vertices}
            
            # Relax edges V-1 times
            for _ in range(len(self.vertices) - 1):
                for u in self.graph:
                    if distances[u] == float('inf'):
                        continue
                    
                    for v, weight in self.graph[u]:
                        if distances[u] + weight < distances[v]:
                            distances[v] = distances[u] + weight
                            predecessors[v] = u
            
            # Check for negative cycles
            for u in self.graph:
                if distances[u] == float('inf'):
                    continue
                
                for v, weight in self.graph[u]:
                    if distances[u] + weight < distances[v]:
                        # Negative cycle detected
                        return None
            
            all_pairs[source] = distances
        
        return all_pairs
    
    def detect_negative_cycle(self) -> bool:
        """
        Detect if graph contains a negative cycle.
        
        Returns:
            True if negative cycle exists, False otherwise
        """
        # Initialize distances from an arbitrary source (vertex 0)
        source = next(iter(self.vertices))
        distances = {v: float('inf') for v in self.vertices}
        distances[source] = 0
        
        # Relax edges V-1 times
        for _ in range(len(self.vertices) - 1):
            for u in self.graph:
                if distances[u] == float('inf'):
                    continue
                
                for v, weight in self.graph[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
        
        # Check if further relaxation is possible (indicates negative cycle)
        for u in self.graph:
            if distances[u] == float('inf'):
                continue
            
            for v, weight in self.graph[u]:
                if distances[u] + weight < distances[v]:
                    return True  # Negative cycle found
        
        return False  # No negative cycle
    
    def get_metrics(self) -> Dict[str, int]:
        """
        Get current metrics from last algorithm execution.
        
        Returns:
            Dictionary with operation counts and statistics
        """
        return {
            'operations_count': self.operations_count,
            'comparisons': self.comparisons,
            'relaxations_performed': self.relaxations_performed
        }
