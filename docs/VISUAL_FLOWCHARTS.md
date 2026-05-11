# Algorithm Flowcharts and Visual Guides

## For Presentation Slides and Handouts

---

## 1. BIDIRECTIONAL DIJKSTRA - FLOWCHART

```
┌─────────────────────────────────────────────────────────────────┐
│           START: Initialize both searches                        │
│  Forward from SOURCE, Backward from DESTINATION                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Add SOURCE to   │
                    │ forward_queue   │
                    │ Add DESTINATION │
                    │ to backward_queue
                    └────────┬────────┘
                             │
                             ▼
          ┌──────────────────────────────────────┐
          │ WHILE both queues are not empty:    │
          │ (Main loop - keep searching)        │
          └───────────┬──────────────────────────┘
                      │
        ┌─────────────▼──────────────┐
        │ FORWARD STEP:              │
        │ 1. Pop node from forward   │
        │ 2. Check all neighbors     │
        │ 3. Update distances        │
        │ 4. Check if meets backward │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │ BACKWARD STEP:             │
        │ 1. Pop node from backward  │
        │ 2. Check all neighbors     │
        │ 3. Update distances        │
        │ 4. Check if meets forward  │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────────────────┐
        │ DID SEARCHES MEET?                     │
        └──────────┬─────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │   Is new meeting    │  NO: Continue loop
        │   distance better?  ├─────────────┐
        └──────┬──────────────┘             │
               │                            │
             YES                            │
               │                            │
        ┌──────▼──────────┐               │
        │Update best_dist │               │
        │& meeting_point  │               │
        └──────┬──────────┘               │
               │                          │
               └──────────┬───────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │ Both queues  │  YES: DONE!
                    │   empty?     ├────────────┐
                    └──────┬───────┘            │
                           │                    │
                          NO                    │
                           │                    │
                    (Continue loop)             │
                           │                    │
                           └──────┬─────────────┘
                                  │
                                  ▼
                        ┌──────────────────────┐
                        │ RECONSTRUCT PATH:    │
                        │ From SOURCE to       │
                        │ meeting_point to     │
                        │ DESTINATION         │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ RETURN:              │
                        │ (best_distance,      │
                        │  path)               │
                        └──────────────────────┘
```

---

## 2. JOHNSON'S ALGORITHM - FLOWCHART

```
┌───────────────────────────────────────────────┐
│        PHASE 1: REWEIGHTING                   │
│     Add auxiliary vertex S                   │
│     Connect to all V with weight 0           │
└────────────────────┬────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ Initialize h[] = ∞   │
          │ h[S] = 0             │
          └────────────┬─────────┘
                       │
        ┌──────────────▼──────────────┐
        │ BELLMAN-FORD: Relax edges  │
        │ (V-1) times                │
        └────────────┬────────────────┘
                     │
        ┌────────────▼────────────┐
        │ For each edge (u,v,w):  │
        │ If h[u] + w < h[v]:    │
        │   h[v] = h[u] + w      │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────────┐
        │ Check for negative cycles:  │
        │ Any edge improves after     │
        │ V-1 rounds?                 │
        └────────┬───────────────────┘
                 │
        ┌────────▼─────────┐
        │ Negative cycle   │  YES: ERROR!
        │ detected?        ├─────────┐
        └────────┬─────────┘         │
                 │                   │
                NO                   │
                 │                   │
   ┌─────────────▼──────────────────┤
   │                                 │
   │ PHASE 2: REWEIGHT EDGES        │
   │ For each edge (u,v,w):        │
   │   w' = w + h[u] - h[v]        │
   │                                 │
   └────────────┬────────────────────┘
                │
   ┌────────────▼──────────────────────────┐
   │ PHASE 3: RUN DIJKSTRA V TIMES         │
   │ For each vertex S in graph:           │
   │   distances[S] = Dijkstra(G', S)    │
   │   Store all results                   │
   └────────────┬──────────────────────────┘
                │
   ┌────────────▼──────────────────────────┐
   │ PHASE 4: RESTORE ORIGINAL WEIGHTS    │
   │ For each u,v pair:                    │
   │   d(u,v) = d'(u,v) + h[v] - h[u]    │
   │   Store in result matrix              │
   └────────────┬──────────────────────────┘
                │
                ▼
   ┌─────────────────────────────────┐
   │ RETURN:                         │
   │ All-pairs distance matrix       │
   │ O(V²) result                    │
   └─────────────────────────────────┘
```

---

## 3. JUMP POINT SEARCH - FLOWCHART

```
┌──────────────────────────────────────────┐
│    INITIALIZE:                           │
│    - Add SOURCE to open_set              │
│    - g_score[SOURCE] = 0                 │
│    - closed_set = empty                  │
└─────────────┬────────────────────────────┘
              │
              ▼
    ┌─────────────────────────┐
    │ WHILE open_set not empty│
    └────────────┬────────────┘
                 │
    ┌────────────▼────────────────┐
    │ Pop node with lowest f-score│
    │ (f = g + heuristic)         │
    └────────────┬────────────────┘
                 │
    ┌────────────▼────────────────────┐
    │ Is node in closed_set?          │
    └──────────┬──────────────────────┘
               │
          YES  │  NO
               │   │
               │   ▼
               │  ┌──────────────────────┐
               │  │ Is node GOAL?        │
               │  └────────┬─────────────┘
               │           │
               │        YES│  NO
               │           │  │
               │        FOUND│  ▼
               │        PATH!│ ┌────────────────────┐
               │           │  │ For each neighbor: │
               │           │  │ (Check if can      │
               │           │  │  jump there)       │
               │           │  └────────┬───────────┘
               │           │           │
               │           │  ┌────────▼──────────────┐
               │           │  │ Is neighbor a jump   │
               │           │  │ point or goal?       │
               │           │  └────────┬─────────────┘
               │           │           │
               │           │      YES  │  NO
               │           │           │  │
               │           │           │  ▼
               │           │           │ ┌──────────────────┐
               │           │           │ │ Has forced       │
               │           │           │ │ neighbors?       │
               │           │           │ └────┬─────────────┘
               │           │           │      │
               │           │           │  YES │  NO
               │           │           │      │  │
               │           │           │ ADD  │  KEEP JUMPING
               │           │           │TO    │  (same direction)
               │           │           │OPEN  │  │
               │           │           │SET   │  │
               │           │           │      │  │
               ▼           ▼           ▼      ▼  ▼
               │───────────┼───────────┼──────┼──│
                           │
        ┌──────────────────▼───────────┐
        │ Add current to closed_set    │
        │ (Marks node as visited)      │
        └──────────────┬────────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │ Loop back to while    │
           │ (process next node)   │
           └───────────────────────┘
                       
                       
            IF PATH FOUND:
            └─────────────────────────┐
                                      ▼
                        ┌─────────────────────────┐
                        │ RECONSTRUCT PATH from   │
                        │ came_from pointers      │
                        │                         │
                        │ RETURN (distance, path) │
                        └─────────────────────────┘
```

---

## 4. VISUAL COMPARISON - NODE EXPANSION PATTERNS

### Unidirectional Dijkstra
```
Searching from A to B:
Expands in a circle growing outward from A

        ●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●
    ●●●●●●●●●●●●●●●●●●●●●●
   ●●●●●●●●● A ●●●●●●●●●●●
    ●●●●●●●●●●●●●●●●●●●●●●
      ●●●●●●●●●●●●●●●●●●●
        ●●●●●●●●●●●●●●●●
        
Evaluates: ~π * r² nodes
Result: All nodes in circle expanded
```

### Bidirectional Dijkstra
```
Searching from A to B:
Two circles meeting in middle

    ●●●●◆◆◆◆●●●●
   ●●●●◆◆◆◆◆◆●●●
  ●●●●◆◆◆◆◆◆◆◆●●
 ●●● A ◆◆◆◆◆◆ B ●
  ●●●●◆◆◆◆◆◆◆◆●●
   ●●●●◆◆◆◆◆◆●●●
    ●●●●◆◆◆◆●●●●

Evaluates: ~2 * π * (r/2)² = ~π * r² / 2 nodes
Result: ~50% fewer nodes expanded!
```

### Jump Point Search on Grid
```
Jumping along symmetric paths:

   . . . . .
   . . . . .
   S → → → E
   . . . . .
   . . . . .

On straight path: Just jump directly!
No need to check intermediate nodes.

Visited nodes: (S, intermediate_jump_pt, E)
vs Dijkstra: (S, 4 moves to E)
Speedup: 2-5x on simple grids, 10-40x with obstacles!
```

---

## 5. COMPLEXITY COMPARISON VISUALIZATION

### Time Complexity Growth

```
BIDIRECTIONAL DIJKSTRA: O((V+E)log V)
    ▁▂▄▇▅▄
Grows: ~linearly in E, log V in data structure ops

JOHNSON'S: O(V²log V + VE)  
    ▅▄▆▇█▁▂
Grows: ~quadratically in V, linearly in E

JUMP POINT: O(√V) grids, O(V+E) general
    ▂▁▁▁▁▂▃
Grows: ~sublinear on grids, linear on graphs

Visual on 100-vertex graph:
  BiDijkstra:  ~500 ops
  Johnson:     ~500,000 ops (all-pairs premium)
  JPS:         ~50-200 ops
```

### Space Complexity Comparison

```
BIDIRECTIONAL DIJKSTRA: O(V)
    ▓▓▓▓▓░░░░░░░░░░░░░░  (uses 1 unit per vertex)

JOHNSON'S: O(V²)
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  (stores all distances)

JUMP POINT: O(V)
    ▓▓▓▓▓░░░░░░░░░░░░░░  (same as BiDijkstra)

On 1000-vertex graph:
  BiDijkstra: ~4 KB
  Johnson:    ~4 MB ⚠️  (1000 × 1000 matrix)
  JPS:        ~4 KB
```

---

## 6. ALGORITHM SELECTION FLOWCHART

```
                    START: What's your problem?
                            │
                ┌───────────────────────────┐
                │                           │
                ▼                           ▼
        Need ONE path?              Need ALL paths?
        (Source to Dest)            (All-pairs)
             │                            │
          YES│                            │NO
             │                            │
        ┌────▼─────────┐            ┌────▼─────────┐
        │ GENERAL      │            │ Sparse graph?│
        │ GRAPH?       │            └────┬──────────┘
        └────┬──────────┘                 │
             │                      ┌─────▼──────┐
        ┌────▼──────────┐          │   YES  NO   │
        │ YES      NO   │          │    │    │   │
        │  │       │    │          │    │    │   │
        │  │       │    │          ▼    ▼    ▼   ▼
        │  │       │    │     JOHNSON'S FLOYD-WARSHALL
        │  │    GRID    │     (Use this)  (Use this)
        │  │    GRAPH?  │
        │  │       │    │
        │  │  ┌────▼──┐ │
        │  │  │YES NO │ │
        │  │  │ │  │  │ │
        │  ▼  ▼ ▼  ▼  ▼ ▼
        │  BIDIJKSTRA  JUMP POINT
        │  (Use this)  SEARCH
        │              (Use this)
        │
        └─► ANSWER: Algorithm selected!
```

---

## 7. PERFORMANCE GROWTH - GRAPHICAL

```
Performance vs Graph Size (100 queries)

Time
(ms) │
     │                    ╱╱╱  Johnson's (all-pairs)
  10K├                 ╱╱╱
     │              ╱╱╱
  5K │           ╱╱╱
     │        ╱╱╱
  1K ├     ╱╱╱
     │  ╱╱╱
 500 ├╱╱           ┌────┐
     │             │    ├─ BiDijkstra
 100 │         ┌──────┐ │ (single-pair)
     │      ┌──┘       │
  50 ├─────┘           │
     │            ┌─────┘
  10 │        ┌──┘
     │     ┌─┘  ╱ ╱ ╱ ╱  JPS
   5 ├────┘╱╱╱╱╱╱╱╱
     │   ╱╱╱╱ (on grid)
   1 └───────────────────────────────
     10   50   100   500  1000  5000
                    Vertices (V)
```

---

## 8. EDGE CASE HANDLING

```
EDGE CASE: What if source = destination?

BiDijkstra:
  ┌──────────────────┐
  │ If S = D:        │
  │ Return (0, [S])  │
  │ No search needed │
  └──────────────────┘

EDGE CASE: What if no path exists?

BiDijkstra/JPS:
  ┌──────────────────┐
  │ Open set becomes │
  │ empty without    │
  │ reaching goal    │
  │ Return (∞, [])   │
  └──────────────────┘

Johnson's:
  ┌──────────────────┐
  │ Negative cycle?  │
  │ Return ERROR     │
  │ Can't solve!     │
  └──────────────────┘
```

---

## 9. METRIC TRACKING VISUALIZATION

### Bidirectional Dijkstra Metrics

```
Algorithm Execution Timeline:
│
├─ Forward expands: [0, 1, 2, ...]    } Tracked: operations_count
├─ Backward expands: [5, 4, 3, ...]   }
├─ Distance comparisons: ~250         } Tracked: comparisons
├─ Heap push/pop: ~180                } Tracked: heap_operations
├─ Meeting detected at node 3         } Tracked: meeting_point
│
└─ Result: distance=4, path=[0,1,2,5]

Metrics output:
  Operations: 892
  Comparisons: 324
  Heap ops: 521
  Time: 0.0012s
```

### Johnson's Algorithm Metrics

```
Phase 1 (Bellman-Ford):
  ├─ Relaxation round 1: 150 updates   } Tracked: relaxations
  ├─ Relaxation round 2: 85 updates    }
  ├─ Relaxation round 3: 12 updates    }
  └─ Total: 247 relaxations

Phase 2 (Dijkstra runs):
  ├─ Dijkstra call 1: 324 ops
  ├─ Dijkstra call 2: 289 ops
  ├─ ...
  └─ Dijkstra call 100: 312 ops    } Tracked: dijkstra_calls

Metrics output:
  Relaxations: 247
  Dijkstra calls: 100
  Total ops: 32,140
  Time: 0.0234s
```

### Jump Point Search Metrics

```
Search Execution:
  ├─ Node 0: expand neighbors
  ├─ Node 1: *** JUMP POINT *** → add to open
  ├─ Node 6: expand neighbors
  ├─ Node 11: *** JUMP POINT ***
  ├─ Node 16: expand neighbors
  ├─ Node 19: GOAL REACHED!
  │
  └─ Jump points found: 5    } Tracked: jump_points_found

Metrics output:
  Jump points: 5
  Operations: 127
  Comparisons: 89
  Time: 0.0004s
```

---

## 10. EXAMPLE GRAPHS FOR SLIDES

### Small Graph (for manual trace)
```
      1 ─ 2
     ╱│   │╲
    0 │   │ 3
    │╲│   │╱
    4 ─ 5
    
Vertex count: 6
Edge count: 12
Diameter: 3

Good for: Explaining step-by-step execution
```

### Medium Graph (typical benchmark)
```
100 vertices arranged as 10×10 grid
Each vertex connects to 2-4 neighbors
Density: ~12%
Diameter: ~18

Good for: Showing performance metrics
```

### Large Graph (stress test)
```
300 vertices
Density: 2% (sparse)
Edge count: ~1800

Good for: Demonstrating scalability
```

---

## PRESENTATION TIPS

**For showing complexity:**
- Use the flowcharts to explain algorithm flow
- Show pseudocode line-by-line
- Use graphs to compare performance

**For explaining concepts:**
- Bidirectional: "Meet in the middle" visualization
- Johnson's: "Reweighting magic" with before/after graphs
- JPS: "Jump! Don't walk!" with grid jumping example

**For Q&A:**
- Have the metric tracking visuals ready
- Reference edge case handling flowchart
- Use comparison table to justify algorithm choice

---

**Ready for Presentation:** ✅
