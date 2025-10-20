# A* Search (Three Modes)

This folder contains a reference implementation of **A\*** search that can be run in three modes on the same graph:

- **UCS mode**: h(n) = 0
- **A\* (Euclidean)**
- **A\* (Manhattan)**

It follows the assignment's required input format, statistics, and deterministic behavior.

## Files
- `astar.py` — main script
- `astar_small.txt` — small 5-node example
- `astar_medium.txt` — 6x6 grid (36 nodes), unit weights

## How to Run

```bash
# Run all three modes on a file
python astar.py astar_small.txt

# Run a single mode
python astar.py astar_small.txt --mode ucs
python astar.py astar_small.txt --mode euclidean
python astar.py astar_small.txt --mode manhattan
```

## Output Format (per mode)
```
MODE: <UCS | A* Euclidean | A* Manhattan>
Optimal cost: <number | NO PATH>
Path: <S -> ... -> D>
Expanded: <int>
Pushes: <int>
Max frontier: <int>
Runtime (s): <float>
```

At the end, the script also prints heuristic validity checks:
- Whether all edge weights >= Euclidean distances
- Whether all edge weights >= Manhattan distances

## Notes
- Duplicate heap entries are allowed; nodes are expanded only when the popped `g` equals the best-known `g`.
- Tie-breaking is deterministic using `(f, node_id)` in the priority queue.
- Coordinates come from `cell_id` via `x = cell_id // 10`, `y = cell_id % 10`.
