"""
A* Search Algorithm - Heuristic-guided pathfinding

A* is an informed search algorithm that combines Dijkstra's algorithm with heuristics
to find optimal paths faster. It explores nodes using: f(n) = g(n) + h(n)
where g(n) is the cost from start and h(n) is the estimated cost to goal.

Time Complexity: O((V + E) log V) with good heuristic, can be O(V + E) with perfect heuristic
Space Complexity: O(V)

Best for: Pathfinding with heuristics (game AI, navigation)
"""

import heapq
from typing import Dict, List, Tuple, Callable, Optional


class AStarSearch:
    """A* Search algorithm implementation with heuristic support."""
    
    def __init__(self, graph: Dict[int, List[Tuple[int, int]]], 
                 heuristic: Optional[Callable[[int, int], float]] = None):
        """
        Initialize A* Search algorithm.
        
        Args:
            graph: Adjacency list representation {vertex: [(neighbor, weight), ...]}
            heuristic: Optional heuristic function h(current, goal) -> estimated_cost
                      Defaults to zero heuristic (becomes Dijkstra)
        """
        self.graph = graph
        self.heuristic = heuristic or (lambda u, v: 0)  # Zero heuristic by default
        self.operations_count = 0
        self.comparisons = 0
        self.nodes_opened = 0
        self.nodes_closed = 0
    
    def find_shortest_path(self, source: int, destination: int) -> Tuple[float, List[int]]:
        """
        Find shortest path from source to destination using A* search.
        
        Args:
            source: Starting vertex
            destination: Goal vertex
        
        Returns:
            (distance, path): Shortest distance and the path taken
        """
        self.operations_count = 0
        self.comparisons = 0
        self.nodes_opened = 0
        self.nodes_closed = 0
        
        # Initialize data structures
        open_set = []  # Priority queue: (f_score, counter, vertex)
        closed_set = set()
        came_from = {}
        g_score = {source: 0}  # Cost from start
        f_score = {source: self.heuristic(source, destination)}
        
        counter = 0  # For stable ordering in priority queue
        heapq.heappush(open_set, (f_score[source], counter, source))
        counter += 1
        
        self.operations_count += 2
        
        while open_set:
            current_f, _, current = heapq.heappop(open_set)
            self.operations_count += 1
            self.comparisons += 1
            
            if current == destination:
                # Reconstruct path
                path = self._reconstruct_path(came_from, current)
                return g_score[current], path
            
            if current in closed_set:
                continue
            
            closed_set.add(current)
            self.nodes_closed += 1
            self.operations_count += 1
            
            # Explore neighbors
            if current in self.graph:
                for neighbor, weight in self.graph[current]:
                    self.operations_count += 1
                    self.comparisons += 1
                    
                    if neighbor in closed_set:
                        continue
                    
                    tentative_g = g_score[current] + weight
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        # Found better path
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        h_value = self.heuristic(neighbor, destination)
                        f_score[neighbor] = tentative_g + h_value
                        self.operations_count += 3
                        self.comparisons += 1
                        
                        if neighbor not in [v for _, _, v in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                            counter += 1
                            self.nodes_opened += 1
                            self.operations_count += 1
        
        # No path found
        return float('inf'), []
    
    def _reconstruct_path(self, came_from: Dict[int, int], current: int) -> List[int]:
        """Reconstruct path from source to current node."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
            self.operations_count += 1
        
        return path[::-1]
    
    def find_all_paths(self, source: int, destinations: List[int]) -> Dict[int, Tuple[float, List[int]]]:
        """
        Find shortest paths from source to multiple destinations.
        
        Args:
            source: Starting vertex
            destinations: List of goal vertices
        
        Returns:
            Dictionary {destination: (distance, path)}
        """
        results = {}
        for dest in destinations:
            distance, path = self.find_shortest_path(source, dest)
            results[dest] = (distance, path)
        
        return results
    
    def reset_metrics(self):
        """Reset metric counters for benchmarking."""
        self.operations_count = 0
        self.comparisons = 0
        self.nodes_opened = 0
        self.nodes_closed = 0


def manhattan_distance(u: Tuple[int, int], v: Tuple[int, int]) -> float:
    """Manhattan distance heuristic for grid-based pathfinding."""
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def euclidean_distance(u: Tuple[int, int], v: Tuple[int, int]) -> float:
    """Euclidean distance heuristic for grid-based pathfinding."""
    return ((u[0] - v[0])**2 + (u[1] - v[1])**2)**0.5
