"""
Jump Point Search (JPS) Algorithm
An optimization of A* pathfinding that preprocesses symmetric optimal movement
to identify "jump points" and skip over many nodes.

Time Complexity: O(V) in best case, O(V + E) in worst case (for uniform graphs)
Space Complexity: O(V)
Note: Typically much faster than A* on uniform grids; here adapted for general graphs.
"""

import heapq
from typing import Dict, List, Tuple, Optional


class JumpPointSearch:
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]], 
                 heuristic: Optional[callable] = None):
        """
        Initialize JPS with optional heuristic function.
        
        Args:
            graph: Adjacency list where graph[u] = [(v, weight), ...]
            heuristic: Function h(node, goal) -> estimated cost (default: zero heuristic)
        """
        self.graph = graph
        self.vertices = set(graph.keys())
        self.heuristic = heuristic or (lambda u, v: 0)
        self.operations_count = 0
        self.jump_points_found = 0
        self.comparisons = 0
    
    def find_shortest_path(self, source: int, destination: int) -> Tuple[Optional[int], List[int]]:
        """
        Find shortest path using Jump Point Search.
        
        Returns:
            (distance, path) - distance is None if no path exists
        """
        if source not in self.vertices or destination not in self.vertices:
            return None, []
        
        if source == destination:
            return 0, [source]
        
        # Priority queue: (f_score, g_score, node)
        open_set = [(self.heuristic(source, destination), 0, source)]
        came_from = {source: None}
        g_score = {v: float('inf') for v in self.vertices}
        g_score[source] = 0
        closed_set = set()
        
        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            self.operations_count += 1
            
            self.comparisons += 1
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            # Goal found
            self.comparisons += 1
            if current == destination:
                path = self._reconstruct_path(came_from, current)
                return current_g, path
            
            # Explore neighbors and identify jump points
            for neighbor, weight in self.graph.get(current, []):
                self.operations_count += 1
                
                self.comparisons += 1
                if neighbor in closed_set:
                    continue
                
                # Check if we should jump to this neighbor
                tentative_g = g_score[current] + weight
                
                self.comparisons += 1
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, destination)
                    
                    # Check if neighbor is a jump point or forced neighbor
                    if self._is_jump_point(neighbor, current, destination) or neighbor == destination:
                        self.jump_points_found += 1
                        heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    elif not self._has_forced_neighbors(neighbor, current):
                        # Continue jumping in the same direction
                        heapq.heappush(open_set, (f_score, tentative_g, neighbor))
        
        return None, []
    
    def _is_jump_point(self, current: int, parent: int, goal: int) -> bool:
        """
        Check if current node is a jump point.
        A node is a jump point if it has forced neighbors or is the goal.
        """
        self.operations_count += 1
        self.comparisons += 1
        if current == goal:
            return True
        
        # Check for forced neighbors
        forced_neighbors = self._get_forced_neighbors(current, parent)
        return len(forced_neighbors) > 0
    
    def _has_forced_neighbors(self, current: int, parent: int) -> bool:
        """Check if current node has any forced neighbors."""
        self.operations_count += 1
        forced = self._get_forced_neighbors(current, parent)
        return len(forced) > 0
    
    def _get_forced_neighbors(self, current: int, parent: int) -> List[int]:
        """
        Get forced neighbors of current node.
        In graph context, a neighbor is "forced" if there's an obstacle
        between parent and the neighbor.
        """
        forced = []
        
        if parent is None:
            return forced
        
        # Get all neighbors of current
        neighbors = self.graph.get(current, [])
        parent_neighbors = self.graph.get(parent, [])
        
        self.operations_count += 1
        
        # Simple heuristic: if a neighbor is not a direct neighbor of parent,
        # it's potentially forced
        for neighbor, _ in neighbors:
            self.comparisons += 2
            if neighbor != parent:
                parent_neighbor_list = [n[0] for n in parent_neighbors]
                if neighbor not in parent_neighbor_list:
                    forced.append(neighbor)
        
        return forced
    
    def _reconstruct_path(self, came_from: Dict[int, Optional[int]], current: int) -> List[int]:
        """Reconstruct path from source to current."""
        path = [current]
        while came_from.get(current) is not None:
            current = came_from[current]
            path.append(current)
        
        path.reverse()
        return path
    
    def reset_metrics(self):
        """Reset operation counters."""
        self.operations_count = 0
        self.jump_points_found = 0
        self.comparisons = 0
