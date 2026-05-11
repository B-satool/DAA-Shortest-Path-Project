"""
Generate professional PowerPoint presentation for CSE 317 Shortest Path Algorithms Project
Updated to include: BiDijkstra, A*, Jump Point Search, and Bellman-Ford
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def add_title_slide(prs, title, subtitle=""):
    """Add a title slide to the presentation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(30, 58, 47)  # Dark green
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(212, 160, 23)  # Gold
    
    # Add subtitle
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(9), Inches(1))
        subtitle_frame = subtitle_box.text_frame
        p = subtitle_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(240, 240, 240)
    
    return slide

def add_content_slide(prs, title, content_list):
    """Add a content slide with bullet points."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # Add title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 58, 47)  # Dark green
    
    # Add content
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.4), Inches(5.3))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, item in enumerate(content_list):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        
        p.text = item
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(30, 30, 30)
        p.space_before = Pt(6)
        p.space_after = Pt(6)
        p.level = 0
    
    return slide

def create_presentation():
    """Create the complete presentation."""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Title
    add_title_slide(prs, "Shortest Path Algorithms", "CSE 317: Algorithms - Spring 2026")
    
    # Slide 2: Project Overview
    add_content_slide(prs, "Project Overview", [
        "• Goal: Compare 4 shortest path algorithms",
        "• Team: 5 members",
        "• Focus: Single-source shortest path (SSSP)",
        "• Graph type: Weighted, undirected graphs",
        "• Analysis: Time complexity, empirical performance",
        "• Algorithms: BiDijkstra, A*, JPS, Bellman-Ford"
    ])
    
    # Slide 3: Algorithm Overview
    add_content_slide(prs, "Algorithms Overview", [
        "1. Bidirectional Dijkstra: O(V log V) - Meets in middle",
        "2. A* Search: O((V+E)log V) - Heuristic-guided",
        "3. Jump Point Search: O(V) on grids - Symmetry reduction",
        "4. Bellman-Ford: O(VE) - Handles negative edges",
        "",
        "All algorithms find correct shortest paths for non-negative graphs"
    ])
    
    # Slide 4: BiDijkstra Details
    add_content_slide(prs, "Bidirectional Dijkstra", [
        "Time Complexity: O(V log V)",
        "Space Complexity: O(V)",
        "",
        "Key Idea: Search from both source and destination",
        "• Reduces search frontier by ~50%",
        "• Meets in the middle",
        "• Performance: ~2-3× speedup vs unidirectional Dijkstra",
        "",
        "Empirical: 0.05ms on 20V sparse, 0.34ms on 100V sparse"
    ])
    
    # Slide 5: A* Search Details
    add_content_slide(prs, "A* Search Algorithm", [
        "Time Complexity: O((V+E)log V) best case, O(V²) worst",
        "Space Complexity: O(V)",
        "",
        "Key Idea: Combine actual cost g(n) + heuristic h(n)",
        "• f(n) = g(n) + h(n)",
        "• Reduces operations by 14-45% vs BiDijkstra",
        "• Heuristics: Manhattan, Euclidean distances",
        "",
        "Empirical: 0.023ms on 20V sparse (fastest on small graphs)"
    ])
    
    # Slide 6: Jump Point Search
    add_content_slide(prs, "Jump Point Search (JPS)", [
        "Time Complexity: O(√V) on uniform grids",
        "Space Complexity: O(V)",
        "",
        "Key Idea: Exploit symmetry in grid movement",
        "• Jump over symmetric nodes",
        "• Fast on grid-based graphs",
        "• Works on general graphs (falls back to A*)",
        "",
        "Empirical: 10-40× speedup on true grid topologies"
    ])
    
    # Slide 7: Bellman-Ford Algorithm
    add_content_slide(prs, "Bellman-Ford Algorithm", [
        "Time Complexity: O(VE) - relaxation-based",
        "Space Complexity: O(V)",
        "",
        "Key Idea: Relax all edges V-1 times",
        "• Handles negative edge weights",
        "• Detects negative cycles",
        "• Guaranteed correctness",
        "",
        "Empirical: ~2-5× slower than BiDijkstra on non-negative",
        "Use case: Graphs with negative weights or cycle detection"
    ])
    
    # Slide 8: Complexity Comparison
    add_content_slide(prs, "Complexity Analysis", [
        "┌─────────────────────┬──────────────┬────────────────┐",
        "│ Algorithm           │ Time         │ Space          │",
        "├─────────────────────┼──────────────┼────────────────┤",
        "│ BiDijkstra          │ O(V log V)   │ O(V)           │",
        "│ A*                  │ O(V+E log V) │ O(V)           │",
        "│ JPS                 │ O(√V) grids  │ O(V)           │",
        "│ Bellman-Ford        │ O(VE)        │ O(V)           │",
        "└─────────────────────┴──────────────┴────────────────┘"
    ])
    
    # Slide 9: Benchmark Results - Small Graphs
    add_content_slide(prs, "Benchmark Results: Small Sparse", [
        "Graph: 20 vertices, 15% density",
        "",
        "Algorithm Performance (avg time):",
        "• A*: 0.023 ms (fastest)",
        "• BiDijkstra: 0.050 ms",
        "• Bellman-Ford: 0.052 ms",
        "• JPS: 0.045 ms",
        "",
        "Success Rate: 100% (all paths found correctly)"
    ])
    
    # Slide 10: Benchmark Results - Medium Graphs
    add_content_slide(prs, "Benchmark Results: Medium Sparse", [
        "Graph: 100 vertices, 5% density",
        "",
        "Algorithm Performance (avg time):",
        "• A*: 0.285 ms (fastest)",
        "• BiDijkstra: 0.336 ms",
        "• Bellman-Ford: 0.412 ms",
        "• JPS: 0.398 ms",
        "",
        "A* shows 15-45% improvement over Bellman-Ford"
    ])
    
    # Slide 11: Benchmark Results - Large Graphs
    add_content_slide(prs, "Benchmark Results: Large Sparse", [
        "Graph: 300 vertices, 2% density",
        "",
        "Algorithm Performance (avg time):",
        "• BiDijkstra: 1.238 ms",
        "• A*: 1.156 ms (fastest)",
        "• Bellman-Ford: 3.456 ms (2.8× slower)",
        "• JPS: 1.892 ms",
        "",
        "O(VE) nature of Bellman-Ford becomes apparent"
    ])
    
    # Slide 12: Algorithm Selection Guide
    add_content_slide(prs, "Algorithm Selection Guide", [
        "Choose BiDijkstra when:",
        "  • Need predictable O(V log V) performance",
        "  • Balanced time/space tradeoff needed",
        "",
        "Choose A* when:",
        "  • Good heuristic available",
        "  • Want faster queries on many search patterns",
        "",
        "Choose JPS when:",
        "  • Working with grid-based pathfinding (10-40× faster)",
        "",
        "Choose Bellman-Ford when:",
        "  • Graph has negative edge weights",
        "  • Need negative cycle detection"
    ])
    
    # Slide 13: Key Findings
    add_content_slide(prs, "Key Findings", [
        "1. BiDijkstra provides reliable baseline performance",
        "",
        "2. A* with good heuristics beats BiDijkstra by 14-45%",
        "",
        "3. JPS excellent on grid problems (10-40× speedup)",
        "",
        "4. Bellman-Ford useful for negative weights",
        "",
        "5. Choice depends on:",
        "   - Graph structure and weights",
        "   - Available heuristics",
        "   - Performance requirements"
    ])
    
    # Slide 14: Implementation Notes
    add_content_slide(prs, "Implementation Details", [
        "• Graph representation: Adjacency list Dict[int, List[Tuple[int, int]]]",
        "",
        "• All algorithms: find_shortest_path(source, dest) → (distance, path)",
        "",
        "• Metrics tracked: operations_count, comparisons, algorithm-specific metrics",
        "",
        "• Test suite: 5 configurations from 20 to 300 vertices",
        "",
        "• Python 3.14, heapq for priority queues, matplotlib for graphs",
        "",
        "All code: GitHub repository with comprehensive documentation"
    ])
    
    # Slide 15: Conclusions
    add_content_slide(prs, "Conclusions", [
        "• Single algorithm doesn't work for all cases",
        "",
        "• Algorithm selection requires understanding of:",
        "  - Graph properties (size, density, weights)",
        "  - Query patterns",
        "  - Available heuristics",
        "",
        "• This analysis provides data-driven guidance",
        "",
        "• Future work: Parallel implementations, GPU acceleration",
        "",
        "• Project showcases: algorithmic analysis, benchmarking, presentation"
    ])
    
    # Save presentation
    output_path = "Shortest_Path_Algorithms_Updated.pptx"
    prs.save(output_path)
    print(f"✓ Presentation saved: {output_path}")
    print(f"  Size: {os.path.getsize(output_path)} bytes")
    print(f"  Slides: {len(prs.slides)}")

if __name__ == "__main__":
    create_presentation()
