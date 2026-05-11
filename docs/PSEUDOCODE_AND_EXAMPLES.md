# Shortest Path Algorithms - Pseudocode & Examples

## For Presentation

This document contains clear pseudocode and worked examples for each algorithm, ready for presentation slides and explanation.

---

## 1. BIDIRECTIONAL DIJKSTRA

### Algorithm Concept

**Key Idea:** Run Dijkstra from both source and destination simultaneously, meeting in the middle to find the shortest path faster.

### Pseudocode

```
ALGORITHM BidirectionalDijkstra(Graph G, Vertex source, Vertex destination)
    
    // Forward search initialization
    forward_dist[source] ← 0
    forward_dist[all other vertices] ← ∞
    forward_heap ← {(0, source)}
    forward_prev ← empty map
    forward_visited ← empty set
    
    // Backward search initialization
    backward_dist[destination] ← 0
    backward_dist[all other vertices] ← ∞
    backward_heap ← {(0, destination)}
    backward_prev ← empty map
    backward_visited ← empty set
    
    best_distance ← ∞
    meeting_point ← null
    
    WHILE forward_heap is not empty AND backward_heap is not empty DO
        
        // FORWARD STEP
        current_dist_f, u_forward ← Extract minimum from forward_heap
        
        IF u_forward in forward_visited THEN
            continue  // Skip already processed nodes
        END IF
        
        forward_visited.add(u_forward)
        
        // Check if forward search meets backward search
        IF u_forward in backward_dist THEN
            candidate_distance ← forward_dist[u_forward] + backward_dist[u_forward]
            IF candidate_distance < best_distance THEN
                best_distance ← candidate_distance
                meeting_point ← u_forward
            END IF
        END IF
        
        // Expand neighbors from forward direction
        FOR EACH (neighbor, weight) in Adjacent(u_forward) DO
            new_dist ← forward_dist[u_forward] + weight
            IF new_dist < forward_dist[neighbor] THEN
                forward_dist[neighbor] ← new_dist
                forward_prev[neighbor] ← u_forward
                Insert (new_dist, neighbor) into forward_heap
            END IF
        END FOR
        
        // BACKWARD STEP (similar)
        current_dist_b, u_backward ← Extract minimum from backward_heap
        
        IF u_backward in backward_visited THEN
            continue
        END IF
        
        backward_visited.add(u_backward)
        
        // Check if backward search meets forward search
        IF u_backward in forward_dist THEN
            candidate_distance ← forward_dist[u_backward] + backward_dist[u_backward]
            IF candidate_distance < best_distance THEN
                best_distance ← candidate_distance
                meeting_point ← u_backward
            END IF
        END IF
        
        // Expand neighbors from backward direction
        FOR EACH (neighbor, weight) in Adjacent(u_backward) DO
            new_dist ← backward_dist[u_backward] + weight
            IF new_dist < backward_dist[neighbor] THEN
                backward_dist[neighbor] ← new_dist
                backward_prev[neighbor] ← u_backward
                Insert (new_dist, neighbor) into backward_heap
            END IF
        END FOR
    END WHILE
    
    IF best_distance = ∞ THEN
        RETURN (null, empty)  // No path exists
    END IF
    
    // Reconstruct path through meeting point
    path ← ReconstructPath(source, destination, forward_prev, backward_prev, meeting_point)
    RETURN (best_distance, path)
END ALGORITHM
```

### Example: Step-by-Step Walkthrough

**Graph:**
```
    (1)
   /   \
  0 --- 1 --- 2
  |     |     |
  3 --- 4 --- 5
  (4)   (2)   (1)

Edges with weights shown on left:
0 → 1: 1      1 → 2: 2      2 → 5: 1
0 → 3: 4      1 → 4: 5      4 → 5: 1
3 → 4: 2      
```

**Finding path from vertex 0 to vertex 5:**

**Initial State:**
```
Forward:  dist = {0: 0, 1: ∞, 2: ∞, 3: ∞, 4: ∞, 5: ∞}
Backward: dist = {0: ∞, 1: ∞, 2: ∞, 3: ∞, 4: ∞, 5: 0}
```

**Step 1: Forward expands from vertex 0**
```
Forward processes: 0 (dist=0)
  → Updates 1: dist=1, prev=0
  → Updates 3: dist=4, prev=0

Forward dist: {0: 0, 1: 1, 2: ∞, 3: 4, 4: ∞, 5: ∞}
```

**Step 2: Backward expands from vertex 5**
```
Backward processes: 5 (dist=0)
  → Updates 2: dist=1, prev=5
  → Updates 4: dist=1, prev=5

Backward dist: {0: ∞, 1: ∞, 2: 1, 3: ∞, 4: 1, 5: 0}
```

**Step 3: Forward expands from vertex 1**
```
Forward processes: 1 (dist=1)
  → Updates 2: dist=3, prev=1
  → Updates 4: dist=6, prev=1

Forward dist: {0: 0, 1: 1, 2: 3, 3: 4, 4: 6, 5: ∞}
```

**Step 4: Backward expands from vertex 4 or 2**
```
Backward processes: 4 (dist=1)
  → Updates 1: dist=6, prev=4
  → Updates 3: dist=3, prev=4

Check: Forward has 4? No
```

**Step 5: Forward checks vertex 2**
```
Forward processes: 2 (dist=3)
  → Updates 5: dist=4, prev=2

Forward dist: {0: 0, 1: 1, 2: 3, 3: 4, 4: 6, 5: 4}
```

**Check meeting at vertex 2:**
```
Forward dist[2] + Backward dist[2] = 3 + 1 = 4 ✓ (This is shortest!)
```

**Step 6: Continue until convergence**
```
Eventually finds best_distance = 4
meeting_point = 2

Path reconstruction:
  From 0 to 2 via forward: 0 → 1 → 2
  From 2 to 5 via backward: 2 ← 5
  Final path: 0 → 1 → 2 → 5
```

**Result:**
```
Shortest distance: 4
Path: [0, 1, 2, 5]
Edges: (0→1, weight 1) + (1→2, weight 2) + (2→5, weight 1) = 4
```

### Key Insights for Presentation

✅ **Advantage:** Searches meet from both directions → ~2-4x faster than unidirectional  
✅ **Why:** Reduces search space by meeting in middle  
✅ **When to use:** Single shortest path queries, general graphs  
❌ **Limitation:** Not ideal for all-pairs problems

---

## 2. JOHNSON'S ALGORITHM

### Algorithm Concept

**Key Idea:** 
1. Use Bellman-Ford to "reweight" graph edges (make all non-negative)
2. Run Dijkstra from each vertex with reweighted edges
3. Convert distances back to original weights

**Benefit:** Faster than Floyd-Warshall on sparse graphs!

### Pseudocode

```
ALGORITHM JohnsonsAlgorithm(Graph G)
    
    // PHASE 1: Reweight using Bellman-Ford
    
    // Create auxiliary vertex s
    auxiliary ← new vertex not in G
    
    // Add edges from auxiliary to all vertices with weight 0
    FOR EACH vertex v in G DO
        Add edge (auxiliary → v, weight 0)
    END FOR
    
    // Initialize distances from auxiliary
    h[auxiliary] ← 0
    h[all other vertices] ← ∞
    
    // Bellman-Ford: Relax edges V-1 times
    FOR i ← 1 TO |V| - 1 DO
        FOR EACH edge (u, v, weight) in all_edges DO
            IF h[u] ≠ ∞ AND h[u] + weight < h[v] THEN
                h[v] ← h[u] + weight
            END IF
        END FOR
    END FOR
    
    // Check for negative cycles
    FOR EACH edge (u, v, weight) in all_edges DO
        IF h[u] ≠ ∞ AND h[u] + weight < h[v] THEN
            RETURN "Negative cycle detected"
        END IF
    END FOR
    
    // Remove auxiliary vertex
    Remove auxiliary vertex and its edges
    
    // PHASE 2: Reweight edges
    // For each edge (u, v) with weight w:
    // new_weight(u, v) = w + h[u] - h[v]
    
    reweighted_graph ← empty graph
    FOR EACH edge (u, v, weight) in G DO
        new_weight ← weight + h[u] - h[v]
        Add edge (u, v, new_weight) to reweighted_graph
    END FOR
    
    // PHASE 3: Run Dijkstra from each vertex
    
    all_distances ← empty dictionary
    
    FOR EACH source vertex in G DO
        // Run Dijkstra with reweighted edges
        distances ← Dijkstra(reweighted_graph, source)
        all_distances[source] ← distances
    END FOR
    
    // PHASE 4: Restore original weights
    // Original distance: d(u,v) = d'(u,v) + h[v] - h[u]
    
    result ← empty dictionary
    FOR EACH u in G DO
        FOR EACH v in G DO
            IF all_distances[u][v] ≠ ∞ THEN
                original_dist ← all_distances[u][v] + h[v] - h[u]
                result[u][v] ← original_dist
            ELSE
                result[u][v] ← ∞
            END IF
        END FOR
    END FOR
    
    RETURN result
END ALGORITHM
```

### Example: Step-by-Step Walkthrough

**Original Graph (4 vertices):**
```
    1
  0 → 1  (weight 1)
  1 → 2  (weight 2)
  2 → 3  (weight 1)
  3 → 0  (weight 4)
  
     2
  1 → 3  (weight 3)
```

**Phase 1: Bellman-Ford Reweighting**

**Step 1a: Add auxiliary vertex and edges**
```
auxiliary → 0: weight 0
auxiliary → 1: weight 0
auxiliary → 2: weight 0
auxiliary → 3: weight 0
```

**Step 1b: Relax edges (V-1 = 3 rounds)**

Round 1:
```
h[auxiliary] = 0
h[0] = 0  (from auxiliary)
h[1] = 0  (from auxiliary)
h[2] = 0  (from auxiliary)
h[3] = 0  (from auxiliary)
```

Round 2:
```
From edge (0 → 1, weight 1): h[1] = min(0, 0+1) = 0
From edge (1 → 2, weight 2): h[2] = min(0, 0+2) = 0
From edge (2 → 3, weight 1): h[3] = min(0, 0+1) = 0
From edge (3 → 0, weight 4): h[0] = min(0, 0+4) = 0
From edge (1 → 3, weight 3): h[3] = min(0, 0+3) = 0
```

Round 3: (no improvements)
```
Final h values: h[0]=0, h[1]=0, h[2]=0, h[3]=0
```

**Phase 2: Reweight edges**

```
Original edge → Reweighted edge
(0 → 1, 1)  → (0 → 1, 1+0-0 = 1)
(1 → 2, 2)  → (1 → 2, 2+0-0 = 2)
(2 → 3, 1)  → (2 → 3, 1+0-0 = 1)
(3 → 0, 4)  → (3 → 0, 4+0-0 = 4)
(1 → 3, 3)  → (1 → 3, 3+0-0 = 3)
```

**Phase 3: Run Dijkstra from each vertex**

For source = 0:
```
Dijkstra(reweighted_graph, 0) →
  distances = {0: 0, 1: 1, 2: 3, 3: 3}
```

For source = 1:
```
Dijkstra(reweighted_graph, 1) →
  distances = {1: 0, 2: 2, 3: 3, 0: 7}
```

For source = 2:
```
Dijkstra(reweighted_graph, 2) →
  distances = {2: 0, 3: 1, 0: 5, 1: 6}
```

For source = 3:
```
Dijkstra(reweighted_graph, 3) →
  distances = {3: 0, 0: 4, 1: 5, 2: 7}
```

**Phase 4: Restore original weights**

```
From 0 to 1:
  d'(0,1) = 1
  d(0,1) = 1 + h[1] - h[0] = 1 + 0 - 0 = 1 ✓

From 0 to 2:
  d'(0,2) = 3
  d(0,2) = 3 + h[2] - h[0] = 3 + 0 - 0 = 3 ✓

From 0 to 3:
  d'(0,3) = 3
  d(0,3) = 3 + h[3] - h[0] = 3 + 0 - 0 = 3 ✓
```

**Final Result: All-Pairs Shortest Paths**
```
     0  1  2  3
  0  0  1  3  3
  1  7  0  2  3
  2  5  6  0  1
  3  4  5  7  0
```

### Key Insights for Presentation

✅ **Advantage:** Better than Floyd-Warshall on sparse graphs  
✅ **Handles:** Negative edge weights (but not negative cycles)  
✅ **When to use:** All-pairs shortest paths, sparse graphs, multiple queries  
❌ **Limitation:** High memory (O(V²)), not good for single-pair  
❌ **Cost:** Expensive setup (Bellman-Ford + V×Dijkstra)

---

## 3. JUMP POINT SEARCH (JPS)

### Algorithm Concept

**Key Idea:** A* variant that "jumps" over unnecessary nodes by exploiting symmetry. If you're moving straight without turning, jump to next interesting point.

**Application:** Exceptional for grid-based pathfinding (game AI, robotics)

### Pseudocode

```
ALGORITHM JumpPointSearch(Graph G, Vertex source, Vertex destination, 
                         Heuristic h)
    
    open_set ← PriorityQueue()
    open_set.add((h(source, destination), 0, source))
    
    came_from ← empty dictionary
    came_from[source] ← null
    
    g_score[source] ← 0  // Cost from start
    g_score[all other vertices] ← ∞
    
    closed_set ← empty set
    
    WHILE open_set is not empty DO
        
        f_score, current_g, current ← open_set.extract_min()
        
        IF current in closed_set THEN
            continue  // Already processed
        END IF
        
        closed_set.add(current)
        
        // Goal reached
        IF current = destination THEN
            path ← ReconstructPath(came_from, current)
            RETURN (current_g, path)
        END IF
        
        // Explore neighbors
        FOR EACH (neighbor, weight) in Adjacent(current) DO
            
            IF neighbor in closed_set THEN
                continue  // Already explored
            END IF
            
            tentative_g ← g_score[current] + weight
            
            IF tentative_g < g_score[neighbor] THEN
                
                came_from[neighbor] ← current
                g_score[neighbor] ← tentative_g
                
                // Check if neighbor is a jump point
                IF IsJumpPoint(neighbor, current, destination) 
                   OR neighbor = destination THEN
                    
                    f_score ← tentative_g + h(neighbor, destination)
                    open_set.add((f_score, tentative_g, neighbor))
                    
                ELSE IF NOT HasForcedNeighbors(neighbor, current) THEN
                    
                    // Continue in same direction (keep jumping)
                    f_score ← tentative_g + h(neighbor, destination)
                    open_set.add((f_score, tentative_g, neighbor))
                END IF
            END IF
        END FOR
    END WHILE
    
    RETURN (∞, empty)  // No path found
END ALGORITHM

FUNCTION IsJumpPoint(current, parent, goal):
    IF current = goal THEN
        RETURN true
    END IF
    
    // Check for forced neighbors
    forced ← GetForcedNeighbors(current, parent)
    RETURN forced is not empty
END FUNCTION

FUNCTION GetForcedNeighbors(current, parent):
    // In a grid: if there's an obstacle, neighbor is forced
    // In a graph: if neighbor not reachable from parent, it's forced
    
    forced ← empty list
    neighbors ← Adjacent(current)
    parent_neighbors ← Adjacent(parent)
    
    FOR EACH neighbor in neighbors DO
        // If not directly accessible from parent
        IF neighbor NOT IN parent_neighbors THEN
            forced.add(neighbor)
        END IF
    END FOR
    
    RETURN forced
END FUNCTION

FUNCTION HasForcedNeighbors(current, parent):
    RETURN GetForcedNeighbors(current, parent) is not empty
END FUNCTION
```

### Example: Step-by-Step Walkthrough

**Grid Graph (5×5):**
```
    0   1   2   3   4
  0 S . . . .
  1 . . . . .
  2 . . . . .
  3 . . . . E
  4 . . . . .

S = Start (0,0) = vertex 0
E = End (3,4) = vertex 19

All edges have weight 1 (adjacent cells)
Using Manhattan heuristic: h(u,v) = |u_row - v_row| + |u_col - v_col|
```

**Example Finding Path:**

**Step 1: Start from vertex 0**
```
current = 0, g_score = 0
h(0, 19) = |0-3| + |0-4| = 7
f_score = 0 + 7 = 7

Neighbors of 0: [1 (right), 5 (down)]
```

**Step 2: Check neighbor 1 (right)**
```
Check IsJumpPoint(1, 0, 19)?
  - 1 ≠ 19
  - GetForcedNeighbors(1, 0)?
    - Neighbors of 1: [0, 2, 6]
    - Parent neighbors of 0: [1, 5]
    - Forced: [6] (not in parent neighbors)
  - Result: IsJumpPoint = TRUE
  
Add to open_set: (1 + h(1,19), 1, 1)
                = (1 + 6, 1, 1) = (7, 1, 1)
```

**Step 3: Check neighbor 5 (down)**
```
Check IsJumpPoint(5, 0, 19)?
  - 5 ≠ 19
  - GetForcedNeighbors(5, 0)?
    - Neighbors of 5: [1, 4, 6, 10]
    - Parent neighbors of 0: [1, 5]
    - Forced: [4, 6, 10]
  - Result: IsJumpPoint = TRUE
  
Add to open_set: (5 + h(5,19), 5, 5)
                = (5 + 5, 5, 5) = (10, 5, 5)
```

**Step 4: Process neighbor 1 (lowest f-score)**
```
current = 1, g_score = 1
h(1, 19) = |0-3| + |1-4| = 6
f_score = 1 + 6 = 7

Neighbors of 1: [0, 2, 6]
- 0: already visited
- 2: check as jump point
- 6: check as jump point
```

**Step 5: Jump along top row**
```
Moving right from 1 to 2:
  IsJumpPoint(2, 1, 19)? 
    Forced neighbors? [3] (yes)
  → JumpPoint found

Moving right from 2 to 3:
  IsJumpPoint(3, 2, 19)?
    Forced neighbors? [4] (yes)
  → JumpPoint found

Moving right from 3 to 4:
  IsJumpPoint(4, 3, 19)?
    Forced neighbors? [] (no, but near wall)
  → Could jump further depending on obstacles
```

**Step 6: Continue search**
```
Open set now has:
  (2, 2, 2) = f=2+6=8, g=2
  (3, 3, 3) = f=3+5=8, g=3
  (10, 5, 5) = f=5+5=10, g=5
  ...
```

**Step 7: Path found when destination reached**
```
When current = 19 (destination):
  Reconstruct path from came_from pointers
  
Example path might be:
  0 → 1 → 6 → 11 → 16 → 17 → 18 → 19
  
Total distance: 7 moves (with jumps, many fewer nodes evaluated)
```

### Efficiency Comparison

```
Standard A*:
  Nodes evaluated: ~35 out of 25 nodes
  Expansions: ~25

Jump Point Search:
  Nodes evaluated: ~12 out of 25 nodes
  Expansions: ~8
  
Speedup: ~3x fewer evaluations!

On larger grids (100×100):
  Speedup: 10-40x!
```

### Key Insights for Presentation

✅ **Advantage:** 10-40x faster than A* on grids  
✅ **Why:** Jumps over symmetric nodes without evaluating them  
✅ **When to use:** Grid-based pathfinding (games, robotics), with good heuristic  
❌ **Limitation:** Overhead on arbitrary graphs, requires heuristic  
⚠️ **Dependency:** Quality of heuristic critical to performance

---

## COMPARISON SUMMARY TABLE

```
╔════════════════════╦═══════════════╦═════════════════════╦══════════════════╗
║ Algorithm          ║ Time Complexity║ Space Complexity  ║ Best Use Case    ║
╠════════════════════╬═══════════════╬═════════════════════╬══════════════════╣
║ Bidirectional      ║ O((V+E)log V) ║ O(V)               ║ Single-pair on   ║
║ Dijkstra           ║               ║                    ║ general graphs   ║
╠════════════════════╬═══════════════╬═════════════════════╬══════════════════╣
║ Johnson's          ║ O(V²log V +   ║ O(V²)              ║ All-pairs on     ║
║ Algorithm          ║ VE)           ║                    ║ sparse graphs    ║
╠════════════════════╬═══════════════╬═════════════════════╬══════════════════╣
║ Jump Point         ║ O(√V) on      ║ O(V)               ║ Grid-based       ║
║ Search             ║ grids,        ║                    ║ pathfinding      ║
║                    ║ O(V+E) general║                    ║ (game AI)        ║
╚════════════════════╩═══════════════╩═════════════════════╩══════════════════╝
```

---

## QUICK REFERENCE FOR SLIDES

### Slide: Bidirectional Dijkstra
```
🎯 Problem: Find shortest path from A to B

📊 Idea:
   • Start searching from both A and B simultaneously
   • Meet in the middle
   • Shortest path = forward_dist[meeting] + backward_dist[meeting]

⏱️ Performance: 2-4x faster than standard Dijkstra
💾 Space: Only need to store distances for 2 searches

✅ When: Single shortest path, general graphs
```

### Slide: Johnson's Algorithm
```
🎯 Problem: Find ALL shortest paths (all-pairs)

📊 Idea:
   1. Bellman-Ford: Compute reweighting function h
   2. Dijkstra: Run from each vertex with new weights
   3. Restore: Convert back to original distances
   
   Magic formula: d'(u,v) = w(u,v) + h[u] - h[v]
   
   Why? Makes all edges non-negative!

⏱️ Performance: Better than Floyd-Warshall on sparse
💾 Space: Store V² distances

✅ When: All-pairs, sparse graphs, multiple queries
```

### Slide: Jump Point Search
```
🎯 Problem: Find path in grid (like game AI)

📊 Idea:
   • A* variant that exploits grid symmetry
   • Jump over redundant nodes
   • Only stop at "forced neighbors" or goal
   
   Why jump? If moving straight without obstacles,
   why check every intermediate node?

⏱️ Performance: 10-40x faster than A* on grids!
💾 Space: Same as A* (just visited nodes)

✅ When: Grid-based pathfinding (games, robots)
```

---

## ANIMATED EXPLANATION (For Presentation)

### Bidirectional Dijkstra Animation Description
```
Frame 1: Two searches starting
  Source (0) → expanding orange
  Destination (5) → expanding blue
  
Frame 2: Searches expanding
  Orange spreads distance 1
  Blue spreads distance 1
  
Frame 3: Almost meeting
  Orange reaches vertices 1,2
  Blue reaches vertices 4,5
  
Frame 4: Meeting point found!
  Both searches meet at vertex 3
  Shortest path = orange_path + blue_path
  
Final: Show unified path in GREEN
```

### Johnson's Algorithm Animation Description
```
Frame 1: Add auxiliary vertex
  New vertex "S" connects to all with weight 0
  
Frame 2: Bellman-Ford reweighting
  Compute h values (heights)
  Show which edges get new weights
  
Frame 3: Run Dijkstra multiple times
  From each vertex, show Dijkstra search
  Color vertices by distance
  
Frame 4: All-pairs matrix
  Show completed distance matrix
  Highlight a few paths in different colors
```

### Jump Point Search Animation Description
```
Frame 1: Start at S, expand neighbors
  Look at each adjacent cell
  Check if it's a jump point
  
Frame 2: Jump along straight lines
  Moving right → jump multiple cells
  Jump stops at corner (forced neighbor)
  
Frame 3: Multiple jump directions
  Jumping right, down, diagonal
  Each direction has jump points
  
Frame 4: Path reconstructed
  Show completed path (much shorter than A*)
  Compare: "Evaluated 15 nodes vs 40 with A*"
  
Final: Show efficiency gain!
```

---

## WORKED EXAMPLE FOR Q&A

### Q: "Why is Bidirectional faster if time complexity is the same?"

**A:** 
```
Unidirectional Dijkstra from 0 to 19 in grid:
  Expands ~200 nodes before reaching goal
  
Bidirectional from 0 and from 19:
  Forward expands ~100 nodes
  Backward expands ~100 nodes
  Meet at node ~50
  
Theory: O((V+E)logV) for both
Reality: ~half the nodes visited!
```

### Q: "When should we NOT use Johnson's?"

**A:**
```
❌ Bad for: Single shortest path query
   - Need O(VE) Bellman-Ford setup
   - Then O((V+E)logV) Dijkstra
   - Total: O(VE + (V+E)logV) >> Bidirectional O((V+E)logV)

❌ Bad for: Dense graphs
   - Bellman-Ford painful with many edges
   - Floyd-Warshall becomes better

✅ Good for: 100 queries on same graph
   - Setup once: O(VE + (V+E)logV)
   - Then 100 O(1) lookups
   - Amortizes to O((VE + (V+E)logV) / 100)
```

### Q: "How does JPS work on non-grid graphs?"

**A:**
```
On grids: Forced neighbors = cells blocked by obstacles
          Clear definition, very efficient

On general graphs: Forced neighbor = neighbor unreachable
                  from parent direction
                  Less clear → more overhead
                  
Benefit reduces: 2-4x instead of 10-40x

Still useful: If good heuristic available + graph structure
```

---

## KEY TAKEAWAYS FOR PRESENTATION

1. **Bidirectional Dijkstra**: Meet in the middle saves time
2. **Johnson's**: Reweight trick makes Dijkstra work for sparse all-pairs
3. **Jump Point Search**: Exploit symmetry for grid pathfinding

**Remember to highlight:**
- ✅ When each algorithm shines
- ✅ Trade-offs (time vs space)
- ✅ Real-world applications
- ✅ Empirical speedups from our tests

---

**Ready for Presentation:** ✅  
**Includes:** Pseudocode, Examples, Animations, Q&A  
**Presentation Duration:** 20-30 minutes for all three algorithms
