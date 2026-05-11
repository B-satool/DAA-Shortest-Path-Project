"""
Johnson's Algorithm for All-Pairs Shortest Paths
Combines Bellman-Ford and Dijkstra to efficiently solve all-pairs shortest paths.
Particularly efficient for sparse graphs.

Time Complexity: O(V²log V + VE) where log V comes from Dijkstra
Space Complexity: O(V²) for storing all-pairs distances
"""

import heapq
from typing import Dict, List, Tuple, Optional


class JohnsonsAlgorithm:
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]]):
        """
        Initialize the graph representation.
        
        Args:
            graph: Adjacency list where graph[u] = [(v, weight), ...]
        """
        self.graph = graph
        self.vertices = set(graph.keys())
        self.operations_count = 0
        self.relaxations = 0
        self.dijkstra_calls = 0
        self.comparisons = 0
    
    def find_all_pairs_shortest_paths(self) -> Optional[Dict[int, Dict[int, int]]]:
        """
        Find shortest paths between all pairs of vertices.
        
        Returns:
            Dictionary where result[u][v] = shortest distance from u to v
        """
        # Step 1: Create auxiliary vertex and reweight using Bellman-Ford
        h = self._bellman_ford_reweighting()
        if h is None:
            return None  # Negative cycle detected
        
        # Step 2: Run Dijkstra from each vertex with reweighted edges
        all_distances = {}
        for source in self.vertices:
            distances = self._dijkstra_reweighted(source, h)
            all_distances[source] = distances
            self.dijkstra_calls += 1
        
        # Step 3: Restore original weights
        result = {}
        for u in self.vertices:
            result[u] = {}
            for v in self.vertices:
                if all_distances[u][v] == float('inf'):
                    result[u][v] = float('inf')
                else:
                    # Restore: d(u,v) = d'(u,v) + h[v] - h[u]
                    result[u][v] = all_distances[u][v] + h[v] - h[u]
                    self.operations_count += 2
        
        return result
    
    def _bellman_ford_reweighting(self) -> Optional[Dict[int, int]]:
        """
        Use Bellman-Ford to find reweighting function h.
        This makes all edge weights non-negative.
        
        Returns:
            h values for reweighting, or None if negative cycle exists
        """
        # Create auxiliary vertex (not in original graph)
        auxiliary = -1
        
        # Initialize distances
        h = {v: float('inf') for v in self.vertices}
        h[auxiliary] = 0
        
        # Add edges from auxiliary vertex to all others with weight 0
        graph_extended = self.graph.copy()
        graph_extended[auxiliary] = [(v, 0) for v in self.vertices]
        
        # Relax edges |V| times
        for _ in range(len(self.vertices)):
            for u in graph_extended:
                if h[u] != float('inf'):
                    for v, weight in graph_extended.get(u, []):
                        self.operations_count += 1
                        self.comparisons += 1
                        if h[u] + weight < h[v]:
                            h[v] = h[u] + weight
                            self.relaxations += 1
        
        # Check for negative cycles
        for u in graph_extended:
            if h[u] != float('inf'):
                for v, weight in graph_extended.get(u, []):
                    self.comparisons += 1
                    if h[u] + weight < h[v]:
                        return None  # Negative cycle detected
        
        # Remove auxiliary vertex from h
        del h[auxiliary]
        return h
    
    def _dijkstra_reweighted(self, source: int, h: Dict[int, int]) -> Dict[int, int]:
        """
        Run Dijkstra with reweighted edges.
        Reweighting: w'(u,v) = w(u,v) + h[u] - h[v]
        """
        distances = {v: float('inf') for v in self.vertices}
        distances[source] = 0
        heap = [(0, source)]
        
        while heap:
            current_dist, u = heapq.heappop(heap)
            self.operations_count += 1
            
            self.comparisons += 1
            if current_dist > distances[u]:
                continue
            
            for v, weight in self.graph.get(u, []):
                self.operations_count += 1
                # Reweighted edge
                reweighted = weight + h[u] - h[v]
                new_dist = distances[u] + reweighted
                
                self.comparisons += 1
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    self.relaxations += 1
                    heapq.heappush(heap, (new_dist, v))
        
        return distances
    
    def find_shortest_path(self, source: int, destination: int) -> Tuple[Optional[int], List[int]]:
        """
        Find shortest path between two vertices.
        This is less efficient than running full all-pairs,
        but provided for compatibility.
        """
        all_pairs = self.find_all_pairs_shortest_paths()
        if all_pairs is None or source not in all_pairs:
            return None, []
        
        distance = all_pairs[source].get(destination, float('inf'))
        if distance == float('inf'):
            return None, []
        
        return distance, [source, destination]  # Simplified path
    
    def reset_metrics(self):
        """Reset operation counters."""
        self.operations_count = 0
        self.relaxations = 0
        self.dijkstra_calls = 0
        self.comparisons = 0
