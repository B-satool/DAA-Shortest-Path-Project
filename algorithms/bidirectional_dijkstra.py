"""
Bidirectional Dijkstra's Algorithm
Runs Dijkstra from both source and destination simultaneously,
meeting in the middle for faster pathfinding.

Time Complexity: O((V + E) log V) - same as Dijkstra but often faster in practice
Space Complexity: O(V)
"""

import heapq
from typing import Dict, List, Tuple, Optional


class BidirectionalDijkstra:
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]]):
        """
        Initialize the graph representation.
        
        Args:
            graph: Adjacency list where graph[u] = [(v, weight), ...]
        """
        self.graph = graph
        self.vertices = set(graph.keys())
        self.operations_count = 0
        self.heap_operations = 0
        self.comparisons = 0
    
    def find_shortest_path(self, source: int, destination: int) -> Tuple[Optional[int], List[int]]:
        """
        Find shortest path from source to destination using bidirectional search.
        
        Returns:
            (distance, path) - distance is None if no path exists
        """
        if source not in self.vertices or destination not in self.vertices:
            return None, []
        
        if source == destination:
            return 0, [source]
        
        # Forward search from source
        forward_dist = {v: float('inf') for v in self.vertices}
        forward_prev = {v: None for v in self.vertices}
        forward_dist[source] = 0
        forward_heap = [(0, source)]
        
        # Backward search from destination
        backward_dist = {v: float('inf') for v in self.vertices}
        backward_prev = {v: None for v in self.vertices}
        backward_dist[destination] = 0
        backward_heap = [(0, destination)]
        
        best_distance = float('inf')
        meeting_point = None
        
        while forward_heap and backward_heap:
            # Forward step
            forward_dist_val, u_forward = heapq.heappop(forward_heap)
            self.heap_operations += 1
            self.operations_count += 1
            
            if forward_dist_val > forward_dist[u_forward]:
                self.comparisons += 1
                continue
            
            # Check if we've met the backward search
            if u_forward in backward_dist:
                self.comparisons += 1
                candidate_distance = forward_dist[u_forward] + backward_dist[u_forward]
                if candidate_distance < best_distance:
                    best_distance = candidate_distance
                    meeting_point = u_forward
            
            # Explore neighbors from forward direction
            for neighbor, weight in self.graph.get(u_forward, []):
                self.operations_count += 1
                new_dist = forward_dist[u_forward] + weight
                if new_dist < forward_dist[neighbor]:
                    self.comparisons += 1
                    forward_dist[neighbor] = new_dist
                    forward_prev[neighbor] = u_forward
                    heapq.heappush(forward_heap, (new_dist, neighbor))
                    self.heap_operations += 1
            
            # Backward step
            if backward_heap:
                backward_dist_val, u_backward = heapq.heappop(backward_heap)
                self.heap_operations += 1
                self.operations_count += 1
                
                if backward_dist_val > backward_dist[u_backward]:
                    self.comparisons += 1
                    continue
                
                # Check if we've met the forward search
                if u_backward in forward_dist:
                    self.comparisons += 1
                    candidate_distance = forward_dist[u_backward] + backward_dist[u_backward]
                    if candidate_distance < best_distance:
                        best_distance = candidate_distance
                        meeting_point = u_backward
                
                # Explore neighbors from backward direction
                for neighbor, weight in self.graph.get(u_backward, []):
                    self.operations_count += 1
                    new_dist = backward_dist[u_backward] + weight
                    if new_dist < backward_dist[neighbor]:
                        self.comparisons += 1
                        backward_dist[neighbor] = new_dist
                        backward_prev[neighbor] = u_backward
                        heapq.heappush(backward_heap, (new_dist, neighbor))
                        self.heap_operations += 1
        
        if best_distance == float('inf'):
            return None, []
        
        # Reconstruct path
        path = self._reconstruct_path(source, destination, forward_prev, backward_prev, meeting_point)
        return best_distance, path
    
    def _reconstruct_path(self, source: int, destination: int, 
                         forward_prev: Dict, backward_prev: Dict, 
                         meeting_point: int) -> List[int]:
        """Reconstruct path from source to destination through meeting point."""
        path = []
        
        # Path from source to meeting point
        current = meeting_point
        while current is not None:
            path.append(current)
            current = forward_prev[current]
        path.reverse()
        
        # Path from meeting point to destination
        current = backward_prev[meeting_point]
        while current is not None:
            path.append(current)
            current = backward_prev[current]
        
        return path
    
    def reset_metrics(self):
        """Reset operation counters."""
        self.operations_count = 0
        self.heap_operations = 0
        self.comparisons = 0
