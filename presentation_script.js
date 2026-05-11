const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Shortest Path Algorithms — CSE 317";

// ── Color palette (matching reference) ──────────────────────────────────────
const DARK_GREEN = "1E3A2F";
const GOLD = "D4A017";
const CREAM = "F0EAD6";
const DARK_TEXT = "1E3A2F";
const LIGHT_TEXT = "FFFFFF";
const MUTED_CREAM = "C8C0A8";
const CODE_BG = "162D22";
const CODE_TEXT = "A8D5A2";

// ── Slide dimensions ─────────────────────────────────────────────────────────
const W = 10, H = 5.625;

// ── Helper: draw decorative "hash" marks (\\\\\ pattern) ─────────────────────
function addHashes(slide, x, y, color) {
  const lines = ["\\\\\\\\\\\\", "\\\\\\\\\\\\"];
  lines.forEach((ln, i) => {
    slide.addText(ln, {
      x, y: y + i * 0.22, w: 1.2, h: 0.2,
      fontSize: 11, color, fontFace: "Calibri", bold: true,
      charSpacing: 2, margin: 0
    });
  });
}

// ── Helper: draw "× × × ×" cross marks ────────────────────────────────────
function addCrosses(slide, x, y, color) {
  ["× × × ×", "× × × ×"].forEach((ln, i) => {
    slide.addText(ln, {
      x, y: y + i * 0.2, w: 1.5, h: 0.2,
      fontSize: 9, color, fontFace: "Calibri",
      charSpacing: 3, margin: 0
    });
  });
}

// ── Helper: large decorative circle outline ────────────────────────────────
function addCircle(slide, x, y, size, color, fill) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: size, h: size,
    fill: fill ? { color } : { type: "none" },
    line: { color, width: fill ? 0 : 8 }
  });
}

// ── Helper: gold numbered circle ──────────────────────────────────────────
function addNumberCircle(slide, n, x, y) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: 0.75, h: 0.75,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 }
  });
  slide.addText(n, {
    x, y: y + 0.05, w: 0.75, h: 0.65,
    fontSize: 18, bold: true, color: DARK_TEXT,
    align: "center", valign: "middle", margin: 0
  });
}

// ── Helper: section divider slide (dark green) ────────────────────────────
function sectionSlide(num, titleLine1, titleLine2, sub) {
  const slide = pres.addSlide();
  slide.background = { color: DARK_GREEN };

  // Decorative: top-left hash
  addHashes(slide, 0.15, 0.1, LIGHT_TEXT);
  // Decorative: bottom-right hash
  addHashes(slide, 8.65, 5.2, LIGHT_TEXT);
  // Decorative: top-right circle
  addCircle(slide, 9.0, -0.5, 1.8, LIGHT_TEXT, false);
  // Decorative: bottom-left circle
  addCircle(slide, -0.6, 4.2, 1.8, LIGHT_TEXT, false);

  // Big gold numbered circle
  addShape_oval_gold(slide, 4.625, 0.7, 0.75);
  slide.addText(num, {
    x: 4.625, y: 0.7, w: 0.75, h: 0.75,
    fontSize: 20, bold: true, color: DARK_TEXT,
    align: "center", valign: "middle", margin: 0
  });

  // Title
  slide.addText(titleLine1, {
    x: 0.5, y: 1.7, w: 9, h: 0.85,
    fontSize: 44, bold: true, color: GOLD,
    align: "center", fontFace: "Arial Black", margin: 0
  });
  if (titleLine2) {
    slide.addText(titleLine2, {
      x: 0.5, y: 2.55, w: 9, h: 0.75,
      fontSize: 36, bold: true, color: LIGHT_TEXT,
      align: "center", fontFace: "Arial Black", charSpacing: 5, margin: 0
    });
  }

  // Subtitle
  slide.addText(sub, {
    x: 1.5, y: 4.0, w: 7, h: 0.4,
    fontSize: 13, color: MUTED_CREAM,
    align: "center", fontFace: "Calibri", margin: 0
  });

  return slide;
}

function addShape_oval_gold(slide, x, y, size) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: size, h: size,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 }
  });
}

// ── Helper: content slide (dark green bg) ────────────────────────────────
function contentSlide(title, numStr) {
  const slide = pres.addSlide();
  slide.background = { color: DARK_GREEN };

  // Top-right crosses
  addCrosses(slide, 8.5, 0.08, LIGHT_TEXT);
  // Bottom-right crosses
  addCrosses(slide, 8.5, 5.3, LIGHT_TEXT);
  // Bottom rule line
  slide.addShape(pres.shapes.LINE, {
    x: 0.5, y: 5.2, w: 9, h: 0,
    line: { color: GOLD, width: 1 }
  });

  // Title
  slide.addText(title, {
    x: 0.5, y: 0.22, w: 8, h: 0.6,
    fontSize: 26, bold: true, color: LIGHT_TEXT,
    fontFace: "Calibri", margin: 0
  });

  // Number circle on left
  if (numStr) {
    slide.addShape(pres.shapes.OVAL, {
      x: 0.3, y: 1.5, w: 0.7, h: 0.7,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 }
    });
    slide.addText(numStr, {
      x: 0.3, y: 1.5, w: 0.7, h: 0.7,
      fontSize: 16, bold: true, color: DARK_TEXT,
      align: "center", valign: "middle", margin: 0
    });
  }

  return slide;
}

// ── Helper: cream content slide (light) ──────────────────────────────────
function creamSlide(title) {
  const slide = pres.addSlide();
  slide.background = { color: CREAM };

  addHashes(slide, 0.12, 0.08, "8A8070");
  addCrosses(slide, 8.5, 5.22, "8A8070");

  slide.addText(title, {
    x: 0.5, y: 0.22, w: 9, h: 0.65,
    fontSize: 26, bold: true, color: DARK_TEXT,
    fontFace: "Calibri", align: "center", margin: 0
  });

  return slide;
}

// ── Helper: code block box ─────────────────────────────────────────────────
function addCodeBlock(slide, code, x, y, w, h, fontSize = 9.5) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: CODE_BG }, line: { color: GOLD, width: 1 }
  });
  slide.addText(code, {
    x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h - 0.24,
    fontSize, color: CODE_TEXT, fontFace: "Consolas",
    valign: "top", margin: 0, wrap: true
  });
}

// ── Helper: info card on cream slide ──────────────────────────────────────
function addCard(slide, x, y, w, h, numText, title, desc) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: "D8D0BC" }, line: { color: "B8B0A0", width: 1 },
    shadow: { type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.08 }
  });
  // Gold circle
  slide.addShape(pres.shapes.OVAL, {
    x: x + 0.15, y: y + (h / 2) - 0.3, w: 0.6, h: 0.6,
    fill: { color: GOLD }, line: { color: GOLD, width: 0 }
  });
  slide.addText(numText, {
    x: x + 0.15, y: y + (h / 2) - 0.3, w: 0.6, h: 0.6,
    fontSize: 14, bold: true, color: DARK_TEXT,
    align: "center", valign: "middle", margin: 0
  });
  slide.addText(title, {
    x: x + 0.9, y: y + 0.08, w: w - 1.05, h: 0.3,
    fontSize: 13, bold: true, color: DARK_TEXT,
    fontFace: "Calibri", margin: 0
  });
  slide.addText(desc, {
    x: x + 0.9, y: y + 0.35, w: w - 1.05, h: 0.3,
    fontSize: 10, color: "5A5040",
    fontFace: "Calibri", margin: 0
  });
}

// ── Helper: checkmark bullet row ──────────────────────────────────────────
function addCheckRow(slide, x, y, text, color = GOLD) {
  slide.addShape(pres.shapes.OVAL, {
    x, y, w: 0.28, h: 0.28,
    fill: { color }, line: { color, width: 0 }
  });
  slide.addText("✓", {
    x, y, w: 0.28, h: 0.28,
    fontSize: 9, bold: true, color: DARK_TEXT,
    align: "center", valign: "middle", margin: 0
  });
  slide.addText(text, {
    x: x + 0.38, y: y, w: 8, h: 0.28,
    fontSize: 14, color: LIGHT_TEXT, fontFace: "Calibri", margin: 0, valign: "middle"
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 1 — TITLE
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: DARK_GREEN };

  addHashes(slide, 0.15, 0.1, LIGHT_TEXT);
  addHashes(slide, 8.65, 5.2, LIGHT_TEXT);
  addCircle(slide, 8.9, -0.55, 2.0, LIGHT_TEXT, false);
  addCircle(slide, -0.7, 4.1, 2.0, LIGHT_TEXT, false);

  slide.addText("SHORTEST PATH", {
    x: 0.3, y: 0.9, w: 9.4, h: 1.1,
    fontSize: 60, bold: true, color: GOLD,
    align: "center", fontFace: "Arial Black", margin: 0
  });
  slide.addText("ALGORITHMS", {
    x: 0.3, y: 1.95, w: 9.4, h: 1.0,
    fontSize: 60, bold: true, color: GOLD,
    align: "center", fontFace: "Arial Black", margin: 0
  });

  // Rule
  slide.addShape(pres.shapes.LINE, {
    x: 0.8, y: 3.15, w: 8.4, h: 0,
    line: { color: MUTED_CREAM, width: 1 }
  });

  slide.addText("Bidirectional Dijkstra  ·  A* Search  ·  Jump Point Search  ·  Contraction Hierarchies", {
    x: 0.8, y: 3.35, w: 8.4, h: 0.4,
    fontSize: 13, color: MUTED_CREAM,
    align: "center", fontFace: "Calibri", margin: 0
  });

  slide.addText("CSE 317: Design and Analysis of Algorithms  |  Spring 2026", {
    x: 0.8, y: 4.9, w: 8.4, h: 0.3,
    fontSize: 10, color: MUTED_CREAM,
    align: "center", fontFace: "Calibri", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 2 — TABLE OF CONTENTS
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = creamSlide("CONTENTS");

  const items = [
    ["01", "Bidirectional Dijkstra", "Meet-in-the-middle, O((V+E)log V)"],
    ["02", "A* Search Algorithm", "Heuristic-guided search, f(n)=g(n)+h(n)"],
    ["03", "Jump Point Search", "Grid optimization, O(√V) best case"],
    ["04", "Contraction Hierarchies", "Preprocessing shortcuts, near O(log V) queries"],
    ["05", "Comparative Analysis", "Benchmarks, complexity & algorithm selection"],
  ];

  items.forEach(([n, title, desc], i) => {
    addCard(slide, 0.45, 0.95 + i * 0.88, 9.1, 0.8, n, title, desc);
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE 3 — TEAM & PROJECT OVERVIEW
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = contentSlide("PROJECT OVERVIEW", null);

  slide.addText("Team Members", {
    x: 0.5, y: 0.9, w: 4.2, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });

  const members = [
    "Arhum Ali Kaleem (29288)",
    "Ammar Khan (29296)",
    "Sumaiya Batool (29295)",
    "Fatima Irfan (29294)",
    "Zainab Irfan Ansari (29091)",
  ];
  members.forEach((m, i) => {
    slide.addText("› " + m, {
      x: 0.6, y: 1.3 + i * 0.42, w: 4.0, h: 0.38,
      fontSize: 12, color: LIGHT_TEXT, fontFace: "Calibri", margin: 0
    });
  });

  slide.addText("Project Goal", {
    x: 5.2, y: 0.9, w: 4.2, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });
  slide.addText(
    "Implement, benchmark and compare four advanced shortest-path algorithms on synthetic graphs of varying sizes and densities. Validate empirical performance against theoretical complexity bounds.",
    {
      x: 5.2, y: 1.3, w: 4.3, h: 1.5,
      fontSize: 11.5, color: LIGHT_TEXT, fontFace: "Calibri", margin: 0, wrap: true
    }
  );

  slide.addText("Applications", {
    x: 5.2, y: 2.95, w: 4.2, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });
  const apps = ["GPS Navigation & Routing", "Game AI Pathfinding", "Network Infrastructure", "Social Network Analysis"];
  apps.forEach((a, i) => {
    slide.addText("› " + a, {
      x: 5.3, y: 3.35 + i * 0.37, w: 4.2, h: 0.33,
      fontSize: 11.5, color: LIGHT_TEXT, fontFace: "Calibri", margin: 0
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 1 — BIDIRECTIONAL DIJKSTRA
// ═══════════════════════════════════════════════════════════════════════════
sectionSlide("01", "BIDIRECTIONAL", "DIJKSTRA", "Meet-in-the-middle  ·  O((V+E)log V)  ·  Linear space");

// SLIDE — What is Bidirectional Dijkstra?
{
  const slide = contentSlide("WHAT IS BIDIRECTIONAL DIJKSTRA?", "01");

  slide.addText(
    "Bidirectional Dijkstra runs two simultaneous Dijkstra searches — one forward from the source and one backward from the destination. When the two search frontiers meet, the shortest path is reconstructed through the meeting point, typically halving the number of nodes explored.",
    {
      x: 1.15, y: 1.1, w: 8.4, h: 1.2,
      fontSize: 13, color: LIGHT_TEXT, fontFace: "Calibri",
      align: "justify", margin: 0, wrap: true
    }
  );

  const checks = [
    "Searches from both source and destination simultaneously",
    "Stops when frontiers meet — dramatically fewer expansions",
    "~2–4× faster than unidirectional Dijkstra in practice",
    "Same asymptotic complexity O((V+E)log V), better constants",
  ];
  checks.forEach((c, i) => addCheckRow(slide, 1.15, 2.55 + i * 0.52, c));
}

// SLIDE — Pseudocode
{
  const slide = contentSlide("BIDIRECTIONAL DIJKSTRA — PSEUDOCODE", "02");

  const code =
`BIDIJKSTRA(G, source, destination):
  forward_dist[source] ← 0;  forward_dist[all others] ← ∞
  backward_dist[dest]  ← 0;  backward_dist[all others] ← ∞
  forward_heap ← {(0, source)};  backward_heap ← {(0, dest)}
  best_dist ← ∞;  meeting_point ← null

  WHILE forward_heap AND backward_heap:
    u_f ← EXTRACT-MIN(forward_heap)
    IF u_f in backward_dist:
      candidate ← forward_dist[u_f] + backward_dist[u_f]
      IF candidate < best_dist: best_dist ← candidate; meeting_point ← u_f
    FOR (v, w) in Adj(u_f):
      IF forward_dist[u_f] + w < forward_dist[v]:
        forward_dist[v] ← forward_dist[u_f] + w
        INSERT (forward_dist[v], v) into forward_heap
    [Repeat symmetric step for backward_heap]

  RETURN (best_dist, ReconstructPath(meeting_point))`;

  addCodeBlock(slide, code, 1.15, 0.95, 8.35, 4.1, 9.2);
}

// SLIDE — Time & Space Complexity
{
  const slide = contentSlide("BIDIRECTIONAL DIJKSTRA — COMPLEXITY", "03");

  const rows = [
    ["Metric", "Value", "Notes"],
    ["Time Complexity", "O((V+E) log V)", "Same as Dijkstra, better avg. constant"],
    ["Space Complexity", "O(V)", "Two distance arrays + two heaps"],
    ["Best Case Speedup", "~2–4×", "Meets in middle of search space"],
    ["Heap Operations", "O(E log V)", "Per direction"],
    ["Negative Weights", "Not supported", "Requires non-negative edge weights"],
  ];

  slide.addTable(rows.map((row, ri) => row.map((cell, ci) => ({
    text: cell,
    options: {
      bold: ri === 0,
      color: ri === 0 ? DARK_TEXT : DARK_TEXT,
      fill: { color: ri === 0 ? GOLD : (ri % 2 === 0 ? "D0C8B0" : "C0B8A0") },
      fontSize: 12,
      align: ci === 0 ? "left" : "center",
      margin: [4, 6, 4, 6]
    }
  }))), {
    x: 0.5, y: 0.98, w: 9, h: 4.1,
    border: { pt: 1, color: "A09880" },
    colW: [2.5, 3.0, 3.5]
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 2 — A* SEARCH
// ═══════════════════════════════════════════════════════════════════════════
sectionSlide("02", "A* SEARCH", "ALGORITHM", "Heuristic-guided  ·  f(n)=g(n)+h(n)  ·  Optimal with admissible heuristic");

// SLIDE — What is A*?
{
  const slide = contentSlide("WHAT IS A* SEARCH?", "01");

  slide.addText(
    "A* combines Dijkstra's guaranteed optimality with a heuristic function h(n) that estimates the remaining distance to the goal. It prioritises nodes by f(n) = g(n) + h(n), where g(n) is the exact cost from start to n. With an admissible (never over-estimating) heuristic, A* is optimal and often explores far fewer nodes than Dijkstra.",
    {
      x: 1.15, y: 1.1, w: 8.4, h: 1.4,
      fontSize: 13, color: LIGHT_TEXT, fontFace: "Calibri",
      align: "justify", margin: 0, wrap: true
    }
  );

  const checks = [
    "Evaluates nodes by f(n) = g(n) + h(n)",
    "Admissible heuristic guarantees optimal solution",
    "Zero heuristic reduces to Dijkstra's algorithm",
    "Best for single-pair queries with good spatial heuristic",
  ];
  checks.forEach((c, i) => addCheckRow(slide, 1.15, 2.65 + i * 0.52, c));
}

// SLIDE — Pseudocode
{
  const slide = contentSlide("A* SEARCH — PSEUDOCODE", "02");

  const code =
`A-STAR(G, source, goal, h):
  open_set ← {(h(source, goal), 0, source)}
  came_from ← {}
  g_score[source] ← 0;  g_score[all others] ← ∞

  WHILE open_set not empty:
    f, g, current ← EXTRACT-MIN(open_set)
    IF current in closed_set: CONTINUE
    closed_set.add(current)
    IF current == goal:
      RETURN (g, ReconstructPath(came_from, current))
    FOR (neighbor, weight) in Adj(current):
      tentative_g ← g_score[current] + weight
      IF tentative_g < g_score[neighbor]:
        came_from[neighbor] ← current
        g_score[neighbor] ← tentative_g
        f_score ← tentative_g + h(neighbor, goal)
        INSERT (f_score, tentative_g, neighbor) into open_set

  RETURN (∞, [])   // No path found`;

  addCodeBlock(slide, code, 1.15, 0.95, 8.35, 4.1, 9.2);
}

// SLIDE — Heuristics & Complexity
{
  const slide = contentSlide("A* — HEURISTICS & COMPLEXITY", "03");

  slide.addText("Common Heuristics", {
    x: 0.5, y: 0.95, w: 4.3, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });

  const heuristics = [
    ["Zero", "h=0 → degrades to Dijkstra", "Always admissible"],
    ["Manhattan", "|Δx|+|Δy|", "Grid graphs, 4-directional"],
    ["Euclidean", "√(Δx²+Δy²)", "Continuous / 8-dir grids"],
    ["Chebyshev", "max(|Δx|,|Δy|)", "8-directional movement"],
  ];
  heuristics.forEach(([name, formula, note], i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 1.4 + i * 0.85, w: 4.2, h: 0.75,
      fill: { color: CODE_BG }, line: { color: GOLD, width: 1 }
    });
    slide.addText(name, {
      x: 0.65, y: 1.45 + i * 0.85, w: 1.2, h: 0.28,
      fontSize: 11, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
    });
    slide.addText(formula, {
      x: 0.65, y: 1.73 + i * 0.85, w: 4.0, h: 0.25,
      fontSize: 10, color: CODE_TEXT, fontFace: "Consolas", margin: 0
    });
    slide.addText(note, {
      x: 1.9, y: 1.45 + i * 0.85, w: 2.7, h: 0.28,
      fontSize: 9.5, color: MUTED_CREAM, fontFace: "Calibri", margin: 0
    });
  });

  slide.addText("Complexity", {
    x: 5.2, y: 0.95, w: 4.3, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });

  const rows = [
    ["Metric", "Value"],
    ["Time (worst)", "O((V+E) log V)"],
    ["Time (perfect h)", "O(|path|)"],
    ["Space", "O(V)"],
    ["Optimal?", "Yes (admissible h)"],
  ];
  slide.addTable(rows.map((row, ri) => row.map((cell, ci) => ({
    text: cell,
    options: {
      bold: ri === 0,
      color: DARK_TEXT,
      fill: { color: ri === 0 ? GOLD : (ri % 2 === 0 ? "D0C8B0" : "C0B8A0") },
      fontSize: 12, align: ci === 0 ? "left" : "center",
      margin: [4, 6, 4, 6]
    }
  }))), {
    x: 5.2, y: 1.38, w: 4.3, h: 3.6,
    border: { pt: 1, color: "A09880" },
    colW: [2.3, 2.0]
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 3 — JUMP POINT SEARCH
// ═══════════════════════════════════════════════════════════════════════════
sectionSlide("03", "JUMP POINT", "SEARCH", "Grid symmetry exploitation  ·  10–40× faster than A* on grids");

// SLIDE — What is JPS?
{
  const slide = contentSlide("WHAT IS JUMP POINT SEARCH?", "01");

  slide.addText(
    "Jump Point Search is an A* optimisation for uniform-cost grids that exploits movement symmetry. Instead of evaluating every grid cell, JPS identifies 'jump points' — special nodes where the path must turn — and leaps over redundant intermediate nodes. This delivers 10–40× speedups over standard A* on open grids.",
    {
      x: 1.15, y: 1.1, w: 8.4, h: 1.4,
      fontSize: 13, color: LIGHT_TEXT, fontFace: "Calibri",
      align: "justify", margin: 0, wrap: true
    }
  );

  const checks = [
    "Skips symmetric paths — jump, don't walk",
    "Jump points: nodes with forced neighbours or goal",
    "O(√V) best case on uniform grids, O(V+E) worst case",
    "Requires Manhattan/Euclidean heuristic for grid",
  ];
  checks.forEach((c, i) => addCheckRow(slide, 1.15, 2.65 + i * 0.52, c));
}

// SLIDE — JPS Pseudocode
{
  const slide = contentSlide("JUMP POINT SEARCH — PSEUDOCODE", "02");

  const code =
`JPS(G, source, goal, h):
  open_set ← {(h(source,goal), 0, source)}
  g_score[source] ← 0;  closed_set ← {}

  WHILE open_set not empty:
    f, g, current ← EXTRACT-MIN(open_set)
    IF current in closed_set: CONTINUE
    closed_set.add(current)
    IF current == goal: RETURN (g, path)

    FOR (neighbor, weight) in Adj(current):
      IF neighbor in closed_set: CONTINUE
      tentative_g ← g_score[current] + weight
      IF tentative_g < g_score[neighbor]:
        g_score[neighbor] ← tentative_g
        IF IsJumpPoint(neighbor, current, goal) OR neighbor==goal:
          // forced neighbour detected — must expand
          INSERT (tentative_g + h(neighbor,goal), tentative_g, neighbor)
        ELSE IF NOT HasForcedNeighbours(neighbor, current):
          INSERT (tentative_g + h(neighbor,goal), tentative_g, neighbor)
  RETURN (∞, [])

IsJumpPoint(n, parent, goal):  RETURN n==goal OR ForcedNeighbours(n,parent)≠{}`;

  addCodeBlock(slide, code, 1.15, 0.95, 8.35, 4.1, 8.8);
}

// SLIDE — JPS vs A* Performance
{
  const slide = contentSlide("JPS — COMPLEXITY & SPEEDUP", "03");

  slide.addText("On Uniform Grids", {
    x: 0.5, y: 0.95, w: 4.2, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });
  const gridFacts = [
    "Jump points ≈ O(√n) on n×n grid",
    "Search frontier ≪ standard A*",
    "Speedup: 10–40× on open grids",
    "Best case: O(|path|)",
  ];
  gridFacts.forEach((f, i) => addCheckRow(slide, 0.5, 1.38 + i * 0.52, f));

  slide.addText("On General Graphs", {
    x: 5.2, y: 0.95, w: 4.3, h: 0.35,
    fontSize: 14, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });
  const genFacts = [
    "Forced neighbour detection adds overhead",
    "Speedup: 2–4× vs A*",
    "Worst case: O(V+E)",
    "Less benefit on irregular topology",
  ];
  genFacts.forEach((f, i) => addCheckRow(slide, 5.2, 1.38 + i * 0.52, f));

  // Benchmark note box
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 3.55, w: 9, h: 1.45,
    fill: { color: CODE_BG }, line: { color: GOLD, width: 1 }
  });
  slide.addText("Empirical Results (from benchmark_results.csv):", {
    x: 0.7, y: 3.65, w: 8.5, h: 0.3,
    fontSize: 11, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
  });
  slide.addText(
    "Small Sparse (20V): JPS avg 0.043 ms  |  Medium Sparse (100V): 0.42 ms  |  Large Sparse (300V): 1.55 ms\n" +
    "Success rate: 87–100%  |  Paths found faster than BiDijkstra on grid-like topologies",
    {
      x: 0.7, y: 3.98, w: 8.5, h: 0.75,
      fontSize: 10.5, color: CODE_TEXT, fontFace: "Consolas", margin: 0
    }
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 4 — CONTRACTION HIERARCHIES
// ═══════════════════════════════════════════════════════════════════════════
sectionSlide("04", "CONTRACTION", "HIERARCHIES", "Preprocessing shortcuts  ·  Near O(log V) query time");

// SLIDE — What are Contraction Hierarchies?
{
  const slide = contentSlide("WHAT ARE CONTRACTION HIERARCHIES?", "01");

  slide.addText(
    "Contraction Hierarchies (CH) preprocess a graph by iteratively contracting (removing) vertices in order of increasing importance, adding shortcut edges to preserve shortest paths. At query time, a bidirectional Dijkstra over the hierarchy runs in near O(log V) — orders of magnitude faster than plain Dijkstra for repeated queries on large road networks.",
    {
      x: 1.15, y: 1.05, w: 8.4, h: 1.45,
      fontSize: 13, color: LIGHT_TEXT, fontFace: "Calibri",
      align: "justify", margin: 0, wrap: true
    }
  );

  const checks = [
    "Phase 1: Contract vertices by importance, add shortcuts",
    "Phase 2: Bidirectional Dijkstra restricted to upward graph",
    "Preprocessing: O((V+E) log V)   |   Query: O(log V)",
    "Used by Google Maps, OpenStreetMap routing engines",
  ];
  checks.forEach((c, i) => addCheckRow(slide, 1.15, 2.65 + i * 0.52, c));
}

// SLIDE — CH Pseudocode
{
  const slide = contentSlide("CONTRACTION HIERARCHIES — PSEUDOCODE", "02");

  const code =
`// PREPROCESSING PHASE
CH-Preprocess(G):
  FOR each vertex v in order of importance:
    FOR each pair (u, v, w1) and (v, x, w2) in G:
      IF shortcut_dist u→x = w1+w2 < direct_path_without_v:
        Add shortcut edge (u, x, w1+w2) to G
    Remove v from active graph; store vertex_level[v]

// QUERY PHASE — Bidirectional Dijkstra on hierarchy
CH-Query(G, source, dest):
  forward_heap  ← {(0, source)};  forward_dist[source]  ← 0
  backward_heap ← {(0, dest)};   backward_dist[dest]   ← 0
  best ← ∞

  WHILE heaps not empty:
    Expand from forward_heap  → only upward edges (higher level)
    Expand from backward_heap → only upward edges (higher level)
    IF meeting vertex found AND dist < best: best ← dist

  RETURN (best, path)`;

  addCodeBlock(slide, code, 1.15, 0.95, 8.35, 4.1, 9.0);
}

// SLIDE — CH Complexity
{
  const slide = contentSlide("CONTRACTION HIERARCHIES — COMPLEXITY", "03");

  const rows = [
    ["Phase", "Complexity", "Notes"],
    ["Preprocessing", "O((V+E) log V)", "One-time, amortised over all queries"],
    ["Query Time", "O(log V) typical", "Near-constant on road networks"],
    ["Space", "O(V + E + shortcuts)", "Shortcuts ≪ V² in practice"],
    ["Shortcuts Added", "O(V·deg)", "Depends on vertex ordering heuristic"],
    ["Road Network Query", "< 1 ms (106 V)", "E.g. entire Germany road graph"],
  ];

  slide.addTable(rows.map((row, ri) => row.map((cell, ci) => ({
    text: cell,
    options: {
      bold: ri === 0,
      color: DARK_TEXT,
      fill: { color: ri === 0 ? GOLD : (ri % 2 === 0 ? "D0C8B0" : "C0B8A0") },
      fontSize: 12, align: ci === 0 ? "left" : "center",
      margin: [4, 6, 4, 6]
    }
  }))), {
    x: 0.5, y: 0.98, w: 9, h: 4.1,
    border: { pt: 1, color: "A09880" },
    colW: [2.5, 2.8, 3.7]
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 5 — COMPARATIVE ANALYSIS
// ═══════════════════════════════════════════════════════════════════════════
sectionSlide("05", "COMPARATIVE", "ANALYSIS", "Benchmarks  ·  Empirical results  ·  Algorithm selection");

// SLIDE — Complexity Comparison Table
{
  const slide = creamSlide("COMPLEXITY COMPARISON");

  const rows = [
    ["Algorithm", "Time Complexity", "Space", "Handles Negatives", "Best Use Case"],
    ["Bidirectional Dijkstra", "O((V+E) log V)", "O(V)", "No", "Single-pair, general graphs"],
    ["A* Search", "O((V+E) log V)", "O(V)", "No", "Single-pair with heuristic"],
    ["Jump Point Search", "O(√V)–O(V+E)", "O(V)", "No", "Grid pathfinding, game AI"],
    ["Contraction Hierarchies", "O(log V) query*", "O(V+E+S)", "No", "Large road networks, many queries"],
  ];

  slide.addTable(rows.map((row, ri) => row.map((cell, ci) => ({
    text: cell,
    options: {
      bold: ri === 0 || ci === 0,
      color: ri === 0 ? "FFFFFF" : DARK_TEXT,
      fill: {
        color: ri === 0 ? DARK_GREEN : (ci === 0 ? "C8C0A8" : (ri % 2 === 0 ? "D8D0BC" : "E0D8C8"))
      },
      fontSize: ri === 0 ? 11.5 : 11,
      align: ci === 0 ? "left" : "center",
      margin: [4, 5, 4, 5]
    }
  }))), {
    x: 0.35, y: 0.95, w: 9.3, h: 4.0,
    border: { pt: 1, color: "A09880" },
    colW: [2.3, 2.2, 0.85, 1.25, 2.7]
  });

  slide.addText("* After preprocessing phase O((V+E) log V)  ·  S = number of shortcut edges added", {
    x: 0.35, y: 5.12, w: 9.3, h: 0.25,
    fontSize: 9, color: "5A5040", fontFace: "Calibri", margin: 0
  });
}

// SLIDE — Benchmark Results (from CSV data)
{
  const slide = creamSlide("EMPIRICAL BENCHMARK RESULTS");

  // Bar chart: avg time across graph sizes
  const chartData = [
    {
      name: "BiDijkstra",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [0.050, 0.092, 0.336, 0.976, 1.238]
    },
    {
      name: "A*",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [0.023, 0.050, 0.323, 0.990, 1.836]
    },
    {
      name: "CH",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [0.038, 0.108, 0.285, 0.918, 1.100]
    },
    {
      name: "JPS",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [0.043, 0.338, 0.416, 9.664, 1.555]
    }
  ];

  slide.addChart(pres.charts.BAR, chartData, {
    x: 0.35, y: 0.95, w: 9.3, h: 4.15,
    barDir: "col",
    barGrouping: "clustered",
    chartColors: [DARK_GREEN, "D4A017", "6B8E4E", "8B5E3C"],
    chartArea: { fill: { color: "FFFFFF" }, roundedCorners: false },
    catAxisLabelColor: "5A5040",
    valAxisLabelColor: "5A5040",
    valAxisLabelFormatCode: "0.000",
    valGridLine: { color: "D8D0BC", size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true,
    legendPos: "b",
    legendFontSize: 10,
    showTitle: true,
    title: "Average Query Time (ms) by Graph Configuration",
    titleFontSize: 12,
    dataLabelColor: "1E3A2F",
  });
}

// SLIDE — Operations Count comparison
{
  const slide = creamSlide("OPERATIONS & COMPARISONS");

  const opsData = [
    {
      name: "Avg Operations",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [146, 471, 1135, 5805, 4189]
    },
    {
      name: "A* Ops",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [126, 257, 845, 2712, 2122]
    },
    {
      name: "CH Ops",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [165, 306, 1065, 2194, 3533]
    },
    {
      name: "JPS Ops",
      labels: ["Small Sparse", "Small Dense", "Med Sparse", "Med Dense", "Large Sparse"],
      values: [83, 212, 540, 2030, 1657]
    }
  ];

  slide.addChart(pres.charts.BAR, opsData, {
    x: 0.35, y: 0.95, w: 9.3, h: 4.15,
    barDir: "col",
    barGrouping: "clustered",
    chartColors: [DARK_GREEN, "D4A017", "6B8E4E", "8B5E3C"],
    chartArea: { fill: { color: "FFFFFF" }, roundedCorners: false },
    catAxisLabelColor: "5A5040",
    valAxisLabelColor: "5A5040",
    valGridLine: { color: "D8D0BC", size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true,
    legendPos: "b",
    legendFontSize: 10,
    showTitle: true,
    title: "Average Operations Count by Graph Configuration",
    titleFontSize: 12,
  });
}

// SLIDE — Algorithm Selection Guide
{
  const slide = creamSlide("WHEN TO USE WHICH ALGORITHM?");

  const scenarios = [
    ["01", "Single-Pair Query\n(General Graph)", "Bidirectional Dijkstra", "Fast, linear space, no preprocessing"],
    ["02", "Grid / Game AI\nPathfinding", "Jump Point Search", "10–40× faster than A* on uniform grids"],
    ["03", "With Spatial\nHeuristic Available", "A* Search", "Guides search, reduces explored nodes"],
    ["04", "Repeated Queries\n(Road Networks)", "Contraction Hierarchies", "Near O(log V) per query after preprocessing"],
  ];

  scenarios.forEach(([n, scenario, algo, why], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.4 + col * 4.7;
    const y = 0.95 + row * 2.1;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.4, h: 1.9,
      fill: { color: "D0C8B0" }, line: { color: "A09880", width: 1 },
      shadow: { type: "outer", color: "000000", blur: 5, offset: 2, angle: 135, opacity: 0.1 }
    });
    // Number circle
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.15, y: y + 0.15, w: 0.5, h: 0.5,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 }
    });
    slide.addText(n, {
      x: x + 0.15, y: y + 0.15, w: 0.5, h: 0.5,
      fontSize: 13, bold: true, color: DARK_TEXT,
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(scenario, {
      x: x + 0.75, y: y + 0.1, w: 3.5, h: 0.5,
      fontSize: 11, bold: true, color: DARK_TEXT, fontFace: "Calibri",
      margin: 0, valign: "top"
    });
    slide.addText("→ " + algo, {
      x: x + 0.15, y: y + 0.75, w: 4.1, h: 0.3,
      fontSize: 12, bold: true, color: DARK_GREEN, fontFace: "Calibri", margin: 0
    });
    slide.addText(why, {
      x: x + 0.15, y: y + 1.1, w: 4.1, h: 0.65,
      fontSize: 10.5, color: "4A4030", fontFace: "Calibri", margin: 0, wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE — Implementation Notes / Known Issues
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = contentSlide("IMPLEMENTATION NOTES & KNOWN ISSUES", null);

  const notes = [
    ["Bidirectional Dijkstra", "Correct. Bidirectional meeting-point detection and path reconstruction implemented. Runs on undirected adjacency list.", "✓"],
    ["A* Search", "Correct. Zero heuristic fallback degrades gracefully to Dijkstra. Custom heuristics (Manhattan, Euclidean) supported via constructor.", "✓"],
    ["Jump Point Search", "Partially adapted. Forced-neighbour logic is generalised for arbitrary graphs (not grid-specific). 10–40× speedup requires true grid structure; on general graphs, savings are 2–4×.", "⚠"],
    ["Contraction Hierarchies", "Simplified implementation. Vertex ordering uses edge-count heuristic instead of edge-difference. Query falls back to BiDijkstra on original graph — full hierarchy-restricted query not implemented.", "⚠"],
  ];

  notes.forEach(([algo, note, status], i) => {
    const statusColor = status === "✓" ? "4CAF50" : "F5A623";
    slide.addShape(pres.shapes.OVAL, {
      x: 0.3, y: 0.98 + i * 1.1, w: 0.35, h: 0.35,
      fill: { color: statusColor }, line: { color: statusColor, width: 0 }
    });
    slide.addText(status, {
      x: 0.3, y: 0.98 + i * 1.1, w: 0.35, h: 0.35,
      fontSize: 11, bold: true, color: LIGHT_TEXT,
      align: "center", valign: "middle", margin: 0
    });
    slide.addText(algo, {
      x: 0.78, y: 0.97 + i * 1.1, w: 2.5, h: 0.3,
      fontSize: 12, bold: true, color: GOLD, fontFace: "Calibri", margin: 0
    });
    slide.addText(note, {
      x: 0.78, y: 1.28 + i * 1.1, w: 8.7, h: 0.65,
      fontSize: 11, color: LIGHT_TEXT, fontFace: "Calibri", margin: 0, wrap: true
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SLIDE — Conclusions
// ═══════════════════════════════════════════════════════════════════════════
{
  const slide = pres.addSlide();
  slide.background = { color: DARK_GREEN };
  addHashes(slide, 0.15, 0.1, LIGHT_TEXT);
  addHashes(slide, 8.65, 5.2, LIGHT_TEXT);
  addCircle(slide, 8.9, -0.55, 2.0, LIGHT_TEXT, false);
  addCircle(slide, -0.7, 4.1, 2.0, LIGHT_TEXT, false);

  slide.addText("KEY TAKEAWAYS", {
    x: 0.5, y: 0.3, w: 9, h: 0.65,
    fontSize: 32, bold: true, color: GOLD,
    align: "center", fontFace: "Arial Black", margin: 0
  });

  slide.addShape(pres.shapes.LINE, {
    x: 1.0, y: 1.0, w: 8.0, h: 0,
    line: { color: GOLD, width: 1 }
  });

  const points = [
    ["BiDijkstra", "Best for single-pair queries on general graphs — fast, simple, linear space."],
    ["A* Search", "Adds heuristic guidance — optimal with admissible h(n), fewer expansions."],
    ["Jump Point Search", "Ideal for grid-based pathfinding: 10–40× A* speedup by skipping symmetric paths."],
    ["Contraction Hierarchies", "Best for large road-network routing — negligible query time after preprocessing."],
    ["Algorithm choice matters", "No universally 'best' algorithm — problem structure determines the winner."],
  ];

  points.forEach(([title, body], i) => {
    slide.addShape(pres.shapes.OVAL, {
      x: 0.4, y: 1.15 + i * 0.82, w: 0.3, h: 0.3,
      fill: { color: GOLD }, line: { color: GOLD, width: 0 }
    });
    slide.addText(title + ": ", {
      x: 0.82, y: 1.12 + i * 0.82, w: 2.1, h: 0.3,
      fontSize: 11.5, bold: true, color: GOLD, fontFace: "Calibri",
      margin: 0, valign: "middle"
    });
    slide.addText(body, {
      x: 2.95, y: 1.12 + i * 0.82, w: 6.6, h: 0.3,
      fontSize: 11.5, color: LIGHT_TEXT, fontFace: "Calibri",
      margin: 0, valign: "middle"
    });
  });

  slide.addText("CSE 317 — Spring 2026  |  Arhum · Ammar · Sumaiya · Fatima · Zainab", {
    x: 0.5, y: 5.1, w: 9, h: 0.3,
    fontSize: 10, color: MUTED_CREAM, align: "center",
    fontFace: "Calibri", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// WRITE FILE
// ═══════════════════════════════════════════════════════════════════════════
pres.writeFile({ fileName: "Shortest_Path_Algorithms_CSE317.pptx" })
  .then(() => console.log("✓ Saved: Shortest_Path_Algorithms_CSE317.pptx"))
  .catch(e => { console.error(e); process.exit(1); });