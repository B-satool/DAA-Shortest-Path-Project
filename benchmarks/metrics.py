"""
Benchmarking and metrics collection for shortest path algorithms.
Measures time complexity, operation counts, and comparative analysis.
"""

import time
from typing import Dict, List, Tuple, Callable, Any
import statistics


class MetricsCollector:
    """Collect and analyze performance metrics."""
    
    def __init__(self):
        self.metrics = {}
    
    def start_timer(self, key: str):
        """Start timing a section."""
        if key not in self.metrics:
            self.metrics[key] = {"times": [], "start": None}
        self.metrics[key]["start"] = time.perf_counter()
    
    def end_timer(self, key: str):
        """End timing and record elapsed time."""
        if key in self.metrics and self.metrics[key]["start"] is not None:
            elapsed = time.perf_counter() - self.metrics[key]["start"]
            self.metrics[key]["times"].append(elapsed)
            self.metrics[key]["start"] = None
    
    def record_metric(self, key: str, value: Any):
        """Record a single metric value."""
        if key not in self.metrics:
            self.metrics[key] = {"values": []}
        
        if "values" not in self.metrics[key]:
            self.metrics[key]["values"] = []
        
        self.metrics[key]["values"].append(value)
    
    def get_stats(self, key: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        if key not in self.metrics:
            return {}
        
        data = self.metrics[key]
        values = data.get("times", []) or data.get("values", [])
        
        if not values:
            return {}
        
        return {
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0,
            "count": len(values),
            "total": sum(values)
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {}


class AlgorithmBenchmark:
    """Benchmark and compare shortest path algorithms."""
    
    def __init__(self):
        self.results = {}
        self.metrics = MetricsCollector()
    
    def benchmark_algorithm(self, algorithm_name: str, 
                           algorithm_instance: Any,
                           test_pairs: List[Tuple[int, int]],
                           graph_size: int) -> Dict[str, Any]:
        """
        Benchmark a single algorithm on multiple test cases.
        
        Args:
            algorithm_name: Name of the algorithm
            algorithm_instance: Instance with find_shortest_path method
            test_pairs: List of (source, destination) pairs
            graph_size: Number of vertices in graph
        
        Returns:
            Dictionary with benchmark results
        """
        self.metrics.start_timer(f"{algorithm_name}_total")
        
        results = {
            "algorithm": algorithm_name,
            "test_cases": len(test_pairs),
            "graph_size": graph_size,
            "paths_found": 0,
            "paths_not_found": 0,
            "total_distance": 0,
            "execution_times": [],
            "operation_counts": [],
            "comparison_counts": [],
            "errors": 0
        }
        
        for source, destination in test_pairs:
            algorithm_instance.reset_metrics()
            
            # Time the algorithm
            start_time = time.perf_counter()
            try:
                distance, path = algorithm_instance.find_shortest_path(source, destination)
                elapsed = time.perf_counter() - start_time
                
                results["execution_times"].append(elapsed)
                
                if distance is not None:
                    results["paths_found"] += 1
                    results["total_distance"] += distance
                else:
                    results["paths_not_found"] += 1
                
                # Collect algorithm-specific metrics
                if hasattr(algorithm_instance, 'operations_count'):
                    results["operation_counts"].append(algorithm_instance.operations_count)
                
                if hasattr(algorithm_instance, 'comparisons'):
                    results["comparison_counts"].append(algorithm_instance.comparisons)
                    
            except Exception as e:
                results["errors"] += 1
                print(f"Error in {algorithm_name} for pair ({source}, {destination}): {e}")
        
        self.metrics.end_timer(f"{algorithm_name}_total")
        
        # Calculate statistics
        if results["execution_times"]:
            results["avg_time"] = statistics.mean(results["execution_times"])
            results["min_time"] = min(results["execution_times"])
            results["max_time"] = max(results["execution_times"])
            results["total_time"] = sum(results["execution_times"])
            results["time_stdev"] = statistics.stdev(results["execution_times"]) if len(results["execution_times"]) > 1 else 0
        
        if results["operation_counts"]:
            results["avg_operations"] = statistics.mean(results["operation_counts"])
            results["max_operations"] = max(results["operation_counts"])
            results["min_operations"] = min(results["operation_counts"])
        
        if results["comparison_counts"]:
            results["avg_comparisons"] = statistics.mean(results["comparison_counts"])
            results["max_comparisons"] = max(results["comparison_counts"])
        
        self.results[algorithm_name] = results
        return results
    
    def generate_report(self) -> str:
        """Generate a formatted comparison report."""
        if not self.results:
            return "No results to report"
        
        report = "\n" + "="*80 + "\n"
        report += "ALGORITHM PERFORMANCE REPORT\n"
        report += "="*80 + "\n\n"
        
        for algo_name, result in self.results.items():
            report += f"\n{'─'*60}\n"
            report += f"Algorithm: {result['algorithm']}\n"
            report += f"{'─'*60}\n"
            
            report += f"Graph Size: {result['graph_size']} vertices\n"
            report += f"Test Cases: {result['test_cases']}\n"
            report += f"Paths Found: {result['paths_found']}\n"
            report += f"Paths Not Found: {result['paths_not_found']}\n"
            report += f"Errors: {result['errors']}\n"
            
            if result.get('avg_time'):
                report += f"\nTiming Metrics:\n"
                report += f"  Total Time: {result['total_time']:.6f}s\n"
                report += f"  Average Time: {result['avg_time']:.6f}s\n"
                report += f"  Min Time: {result['min_time']:.6f}s\n"
                report += f"  Max Time: {result['max_time']:.6f}s\n"
                report += f"  Std Dev: {result['time_stdev']:.6f}s\n"
            
            if result.get('avg_operations'):
                report += f"\nOperation Metrics:\n"
                report += f"  Average Operations: {result['avg_operations']:.2f}\n"
                report += f"  Max Operations: {result['max_operations']}\n"
                report += f"  Min Operations: {result['min_operations']}\n"
            
            if result.get('avg_comparisons'):
                report += f"\nComparison Metrics:\n"
                report += f"  Average Comparisons: {result['avg_comparisons']:.2f}\n"
                report += f"  Max Comparisons: {result['max_comparisons']}\n"
            
            report += "\n"
        
        # Comparative analysis
        report += f"\n{'='*80}\n"
        report += "COMPARATIVE ANALYSIS\n"
        report += f"{'='*80}\n"
        
        if len(self.results) > 1:
            # Find fastest algorithm
            fastest_algo = min(self.results.items(), 
                             key=lambda x: x[1].get('avg_time', float('inf')))
            report += f"\nFastest Algorithm: {fastest_algo[0]}\n"
            report += f"Average Time: {fastest_algo[1]['avg_time']:.6f}s\n"
            
            # Find most efficient in operations
            if all('avg_operations' in r for r in self.results.values()):
                most_efficient = min(self.results.items(),
                                    key=lambda x: x[1].get('avg_operations', float('inf')))
                report += f"\nMost Operation-Efficient: {most_efficient[0]}\n"
                report += f"Average Operations: {most_efficient[1]['avg_operations']:.2f}\n"
        
        report += "\n" + "="*80 + "\n"
        return report
    
    def export_to_csv(self, filename: str):
        """Export results to CSV format."""
        import csv
        
        if not self.results:
            print("No results to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Algorithm', 'Graph Size', 'Test Cases', 'Paths Found',
                'Avg Time (s)', 'Min Time (s)', 'Max Time (s)',
                'Avg Operations', 'Max Operations', 'Avg Comparisons'
            ])
            
            # Data rows
            for algo_name, result in self.results.items():
                writer.writerow([
                    result['algorithm'],
                    result['graph_size'],
                    result['test_cases'],
                    result['paths_found'],
                    result.get('avg_time', 'N/A'),
                    result.get('min_time', 'N/A'),
                    result.get('max_time', 'N/A'),
                    result.get('avg_operations', 'N/A'),
                    result.get('max_operations', 'N/A'),
                    result.get('avg_comparisons', 'N/A')
                ])
        
        print(f"Results exported to {filename}")
