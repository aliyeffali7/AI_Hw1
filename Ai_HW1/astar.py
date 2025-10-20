#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import math
import time
import heapq
from collections import defaultdict

def read_graph(path):
    vertices = {}
    coords = {}
    adj = defaultdict(list)
    src = None
    dst = None

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s or s.startswith("#"):
                continue

            if s.startswith(("S,", "s,")):
                parts = s.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Bad source line: {s}")
                src = int(parts[1])
                continue

            if s.startswith(("D,", "d,")):
                parts = s.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Bad destination line: {s}")
                dst = int(parts[1])
                continue

            parts = [p.strip() for p in s.split(",")]
            if len(parts) == 2:
                try:
                    vid = int(parts[0]); cell = int(parts[1])
                except ValueError as e:
                    raise ValueError(f"Bad vertex line: {s}") from e
                vertices[vid] = cell
                coords[vid] = (cell // 10, cell % 10)
            elif len(parts) == 3:
                try:
                    u = int(parts[0]); v = int(parts[1]); w = float(parts[2])
                except ValueError as e:
                    raise ValueError(f"Bad edge line: {s}") from e
                if w < 0:
                    raise ValueError(f"Edge weight must be non-negative: {s}")
                adj[u].append((v, w))
                adj[v].append((u, w))
            else:
                raise ValueError(f"Unrecognized line: {s}")

    if src is None or dst is None:
        raise ValueError("Missing source (S,...) or destination (D,...).")

    for u, nbrs in list(adj.items()):
        if u not in coords:
            raise ValueError(f"Node {u} has edges but no vertex line.")
        for v, _ in nbrs:
            if v not in coords:
                raise ValueError(f"Node {v} has edges but no vertex line.")

    return vertices, coords, adj, src, dst

# -----------------------------
# Heuristics
# -----------------------------

def h0(n, goal, coords):
    return 0.0

def h_euc(n, goal, coords):
    x1, y1 = coords[n]; x2, y2 = coords[goal]
    return math.hypot(x1 - x2, y1 - y2)

def h_man(n, goal, coords):
    x1, y1 = coords[n]; x2, y2 = coords[goal]
    return abs(x1 - x2) + abs(y1 - y2)

HEURISTICS = {
    "ucs": h0,
    "euclidean": h_euc,
    "manhattan": h_man,
}

def search(source, dest, adj, coords, heuristic):
    t0 = time.perf_counter()
    g_best = {source: 0.0}
    parent = {source: None}
    heap = []
    heapq.heappush(heap, (heuristic(source, dest, coords), source, 0.0, source))

    pushes = 1
    max_frontier = 1
    expanded = 0

    while heap:
        if len(heap) > max_frontier:
            max_frontier = len(heap)

        f, tie, g, node = heapq.heappop(heap)
        if g_best.get(node, float("inf")) != g:
            continue

        expanded += 1

        if node == dest:
            path = []
            cur = dest
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return g, path, {
                "expanded": expanded,
                "pushes": pushes,
                "max_frontier": max_frontier,
                "runtime_s": time.perf_counter() - t0,
            }

        for nbr, w in adj.get(node, []):
            ng = g + w
            if ng < g_best.get(nbr, float("inf")):
                g_best[nbr] = ng
                parent[nbr] = node
                fn = ng + heuristic(nbr, dest, coords)
                heapq.heappush(heap, (fn, nbr, ng, nbr))
                pushes += 1

    return None, None, {
        "expanded": expanded,
        "pushes": pushes,
        "max_frontier": max_frontier,
        "runtime_s": time.perf_counter() - t0,
    }

# -----------------------------
# Reporting & checks
# -----------------------------
def check_h_ok(adj, coords):
    ok_e = True
    ok_m = True
    seen = set()
    for u, nbrs in adj.items():
        for v, w in nbrs:
            if (v, u) in seen:
                continue
            seen.add((u, v))
            x1, y1 = coords[u]; x2, y2 = coords[v]
            eu = math.hypot(x1 - x2, y1 - y2)
            ma = abs(x1 - x2) + abs(y1 - y2)
            if w < eu - 1e-12:
                ok_e = False
            if w < ma - 1e-12:
                ok_m = False
    return {"euclidean_ok": ok_e, "manhattan_ok": ok_m}

def render_stats(mode_name, cost, path, stats):
    out = []
    out.append(f"MODE: {mode_name}")
    if cost is None:
        out.append("Optimal cost: NO PATH")
    else:
        c_str = str(int(cost)) if abs(cost - int(cost)) < 1e-12 else f"{cost:.6f}"
        out.append(f"Optimal cost: {c_str}")
    if path is not None:
        out.append("Path: " + " -> ".join(map(str, path)))
    out.append(f"Expanded: {stats['expanded']}")
    out.append(f"Pushes: {stats['pushes']}")
    out.append(f"Max frontier: {stats['max_frontier']}")
    out.append(f"Runtime (s): {stats['runtime_s']:.6f}")
    return "\n".join(out)

def run_modes(path):
    _, coords, adj, src, dst = read_graph(path)
    results = []
    for key, name in [("ucs", "UCS"), ("euclidean", "A* Euclidean"), ("manhattan", "A* Manhattan")]:
        cost, p, st = search(src, dst, adj, coords, HEURISTICS[key])
        results.append((name, cost, p, st))

    for name, cost, p, st in results:
        print(render_stats(name, cost, p, st))
        print()

    valid = check_h_ok(adj, coords)
    print("Heuristic validity checks:")
    print(f"  Edge weights >= Euclidean distances: {'YES' if valid['euclidean_ok'] else 'NO'}")
    print(f"  Edge weights >= Manhattan distances: {'YES' if valid['manhattan_ok'] else 'NO'}")
# -----------------------------
# CLI
# -----------------------------
def main():
    ap = argparse.ArgumentParser(description="A* on undirected non-negative graph.")
    ap.add_argument("input", help="Path to input file")
    ap.add_argument("--mode", choices=["ucs","euclidean","manhattan","all"], default="all")
    args = ap.parse_args()

    _, coords, adj, src, dst = read_graph(args.input)

    if args.mode == "all":
        run_modes(args.input)
        return

    h = HEURISTICS[args.mode]
    cost, p, st = search(src, dst, adj, coords, h)
    print(render_stats(
        {"ucs":"UCS","euclidean":"A* Euclidean","manhattan":"A* Manhattan"}[args.mode],
        cost, p, st
    ))

    valid = check_h_ok(adj, coords)
    print()
    print("Heuristic validity checks:")
    print(f"  Edge weights >= Euclidean distances: {'YES' if valid['euclidean_ok'] else 'NO'}")
    print(f"  Edge weights >= Manhattan distances: {'YES' if valid['manhattan_ok'] else 'NO'}")

if __name__ == "__main__":
    main()
