"""
Graph utilities and test data generation for shortest path algorithms.
Includes graph builders, test case generators, and validation utilities.
"""

import random
from typing import Dict, List, Tuple, Set


class GraphGenerator:
    """Generate various types of graphs for testing."""
    
    @staticmethod
    def create_weighted_graph(num_vertices: int, edge_density: float, 
                             max_weight: int = 100, seed: Optional[int] = None) -> Dict[int, List[Tuple[int, int]]]:
        """
        Create a random weighted graph.
        
        Args:
            num_vertices: Number of vertices (0 to num_vertices-1)
            edge_density: Probability of edge existence (0.0 to 1.0)
            max_weight: Maximum edge weight
            seed: Random seed for reproducibility
        
        Returns:
            Adjacency list representation
        """
        if seed is not None:
            random.seed(seed)
        
        graph = {i: [] for i in range(num_vertices)}
        
        for u in range(num_vertices):
            for v in range(num_vertices):
                if u != v and random.random() < edge_density:
                    weight = random.randint(1, max_weight)
                    graph[u].append((v, weight))
        
        return graph
    
    @staticmethod
    def create_sparse_graph(num_vertices: int, num_edges: int, 
                           max_weight: int = 100, seed: Optional[int] = None) -> Dict[int, List[Tuple[int, int]]]:
        """
        Create a sparse graph with exact number of edges.
        
        Args:
            num_vertices: Number of vertices
            num_edges: Number of edges to create
            max_weight: Maximum edge weight
            seed: Random seed
        
        Returns:
            Adjacency list representation
        """
        if seed is not None:
            random.seed(seed)
        
        graph = {i: [] for i in range(num_vertices)}
        edges_added = 0
        max_attempts = num_edges * 10
        attempts = 0
        
        while edges_added < num_edges and attempts < max_attempts:
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            
            if u != v:
                # Check if edge already exists
                if not any(neighbor == v for neighbor, _ in graph[u]):
                    weight = random.randint(1, max_weight)
                    graph[u].append((v, weight))
                    edges_added += 1
            
            attempts += 1
        
        return graph
    
    @staticmethod
    def create_dense_graph(num_vertices: int, max_weight: int = 100) -> Dict[int, List[Tuple[int, int]]]:
        """Create a complete graph where every vertex connects to every other."""
        graph = {i: [] for i in range(num_vertices)}
        
        for u in range(num_vertices):
            for v in range(num_vertices):
                if u != v:
                    weight = random.randint(1, max_weight)
                    graph[u].append((v, weight))
        
        return graph
    
    @staticmethod
    def create_grid_graph(rows: int, cols: int, 
                         max_weight: int = 100) -> Dict[int, List[Tuple[int, int]]]:
        """
        Create a 2D grid graph.
        Nodes are numbered: 0 to rows*cols-1
        """
        graph = {}
        
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j
                graph[node] = []
                
                # Connect to adjacent cells
                for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbor = ni * cols + nj
                        weight = random.randint(1, max_weight)
                        graph[node].append((neighbor, weight))
        
        return graph


class GraphValidator:
    """Validate graph properties and test results."""
    
    @staticmethod
    def is_valid_graph(graph: Dict[int, List[Tuple[int, int]]]) -> bool:
        """Check if graph has valid structure."""
        vertices = set(graph.keys())
        
        for u in graph:
            for v, weight in graph[u]:
                if v not in vertices:
                    return False
                if weight <= 0:
                    return False
        
        return True
    
    @staticmethod
    def get_graph_stats(graph: Dict[int, List[Tuple[int, int]]]) -> Dict:
        """Get statistics about the graph."""
        num_vertices = len(graph)
        num_edges = sum(len(neighbors) for neighbors in graph.values())
        
        if num_vertices == 0:
            return {"vertices": 0, "edges": 0}
        
        densities = [len(neighbors) for neighbors in graph.values()]
        avg_degree = sum(densities) / len(densities)
        max_degree = max(densities) if densities else 0
        min_degree = min(densities) if densities else 0
        
        return {
            "vertices": num_vertices,
            "edges": num_edges,
            "density": num_edges / (num_vertices * (num_vertices - 1)) if num_vertices > 1 else 0,
            "avg_degree": avg_degree,
            "max_degree": max_degree,
            "min_degree": min_degree
        }


class TestCaseGenerator:
    """Generate test cases for algorithm testing."""
    
    @staticmethod
    def generate_test_pairs(num_vertices: int, num_pairs: int, 
                           seed: Optional[int] = None) -> List[Tuple[int, int]]:
        """Generate random source-destination pairs."""
        if seed is not None:
            random.seed(seed)
        
        pairs = []
        for _ in range(num_pairs):
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            if u != v:
                pairs.append((u, v))
        
        return pairs


# Type hint import
from typing import Optional
