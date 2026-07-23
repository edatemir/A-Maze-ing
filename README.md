*This project has been created as part of the 42 curriculum by etemir, zozcan.*

# A-Maze-ing

## 📖 Description

**A-Maze-ing** is a Python maze generator and solver built for the 42 curriculum.
Given a small configuration file, it:

- generates a fully-connected, randomized maze of any size,
- embeds the "42" logo as a block of impassable cells inside the maze,
- can produce either a "Perfect" maze (exactly one path between any two cells)
  or a "Pac-Man"-style board with a couple of loops and no forced dead-end,
- finds the shortest path from the entry to the exit with a BFS solver,
- displays the result in a colored, box-drawing terminal UI with a small
  interactive menu, and
- writes the maze to a strictly formatted hexadecimal output file.

The goal of the project is to practice grid/graph algorithms (randomized DFS
maze carving, BFS pathfinding), config-file parsing with proper error
handling, and clean, reusable Python module design.

## Instructions

### Prerequisites

- Python 3.10+
- `make` 

### Running the project

```bash
make run
```

or directly:

```bash
python3 a_maze_ing.py config.txt
```

`config.txt` can be replaced by the path to any config file following the
format described below. The program prints the maze in the terminal and
writes it to the file named by `OUTPUT_FILE` in the config.

### Interactive menu

Once a maze is displayed, you can:

| Choice | Action                                             |
|--------|-----------------------------------------------------|
| 1      | Generate a new maze (reseeded from the current time) |
| 2      | Show/hide the shortest solution path                |
| 3      | Cycle the wall color                                 |
| 4      | Exit                                                  |

### Other Makefile targets

```bash
make install      # pip install flake8 mypy build
make debug        # run under pdb
make lint         # flake8 + mypy (relaxed)
make lint-strict   # flake8 + mypy --strict
make clean         # remove __pycache__, .mypy_cache, build artifacts
make fclean        # clean + remove the generated maze output file
make re            # fclean + run
```

### Using it as a library

The project is also packaged as an installable module (see
[`pyproject.toml`](pyproject.toml)):

```bash
pip install build
python -m build                 # produces dist/mazegen-1.0.0(.tar.gz|-py3-none-any.whl)
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

Once installed, the `maze` package can be imported from any other Python
project (see [Reusable code](#-reusable-code) below).

## 🗂️ Config file format

The config file is a plain text file of `KEY=VALUE` lines (one assignment per
line). Blank lines and lines starting with `#` are ignored; keys are
case-insensitive, must be unique, and every value must be non-empty.

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=43
```

| Key           | Required | Format                | Meaning                                                                 |
|---------------|:--------:|------------------------|--------------------------------------------------------------------------|
| `WIDTH`       | yes      | positive integer       | maze width, in cells                                                    |
| `HEIGHT`      | yes      | positive integer       | maze height, in cells                                                   |
| `ENTRY`       | yes      | `x,y`                  | entry cell, `0 <= x < WIDTH`, `0 <= y < HEIGHT`                          |
| `EXIT`        | yes      | `x,y`                  | exit cell, same bounds as `ENTRY`; must differ from `ENTRY`              |
| `OUTPUT_FILE` | yes      | file path              | where the generated maze is written                                     |
| `PERFECT`     | yes      | `True` / `False`       | `True`: single-path maze, no loops. `False`: adds exactly two loops     |
| `SEED`        | no       | integer                | RNG seed, for a reproducible maze; omitted → a random maze every run    |

Any missing required key, malformed value, or out-of-bounds/overlapping
coordinate raises a descriptive `ConfigError` (see
[`maze/exceptions.py`](maze/exceptions.py)) instead of crashing.

## 📄 Output file format

The output file (`maze.txt` by default) has four parts:

1. **`HEIGHT` lines of `WIDTH` hex digits.** Each digit is a 4-bit wall mask
   for that cell: `1`=North, `2`=East, `4`=South, `8`=West wall present
   (bits are summed, e.g. `D` = `1101` = N+S+W walls, only the East side is
   open).
2. A **blank line**.
3. The **entry** coordinate, as `x,y`.
4. The **exit** coordinate, as `x,y`.
5. The **shortest path**, as a string of compass letters (`N`/`E`/`S`/`W`)
   from entry to exit, as found by the BFS solver.

Example (from `config.txt` above):

```
D5397955515539179553
93A856D39693AEA9693A
...
0,0
19,14
EESSSWWSESWSSSEEENEN...
```

## 🧩 Maze generation algorithm

The maze is carved using an iterative randomized depth-first search (DFS - recursive backtracker), utilizing an explicit stack to avoid Python's recursion limits (see [`maze/generator.py`](maze/generator.py)):

1. **"42" Pattern (Optional):** A 7x5 pattern is stamped in the center of the grid.  These cells are marked as `blocked` and act as permanent walls that the carving process must work around.
2. **Carving Process (DFS):** Starting from the `ENTRY`, the algorithm selects a random unvisited neighbor (using SEED for reproducibility), tears down the wall between them, and moves forward. When there are no unvisited neighbors left, it backtracks to the previous cell on the stack.
3. **Connectivity Check:** Once the stack is empty, if any reachable cells remain unvisited (e.g., if the 42 pattern split the map), the program raises an error to prevent generating a broken maze.
4. Pac-Man Mode: If `PERFECT=False`, two random walls are knocked down to add loops without altering the core carving logic.

### Why this algorithm?

- **Guaranteed Perfection:** It inherently builds a spanning tree. This guarantees the PERFECT=True condition (exactly one path between any two cells, zero unreachable areas) without requiring any post-processing.

- **Better Gameplay:** Compared to Prim's or Kruskal's, it tends to produce longer, winding corridors and fewer dead ends, making it much better suited for game-style mazes.

- **Memory Friendly:** Using an explicit stack instead of recursion prevents crashes on massive mazes (large WIDTH/HEIGHT values).

- **Deterministic:** The SEED parameter ensures the exact same maze can be reproduced for debugging and evaluation.

- **Modularity:** Perfect and Pac-Man modes share the exact same core algorithm; there is no need to switch to a different algorithm just to add loops.

## ♻️ Reusable code

- The **`maze` package** (`Cell`, `Maze`, `MazeGenerator`, `config.parse_config`)
  has no dependency on the terminal UI or on the solver. Any part of it can be
  imported on its own, e.g.:
  ```python
  from maze.config import parse_config
  from maze.generator import MazeGenerator

  config = parse_config("config.txt")
  maze = MazeGenerator(config).generator()
  ```
- **`maze/output.py`**'s conversion functions (`generate_hex_content`,
  `convert_maze_to_grid`, `convert_path_to_directions`) are pure functions —
  they take a `Maze`/path and return data, with no I/O or global state — so
  they can back a different exporter (e.g. JSON, SVG, PNG) without touching
  the generator.
- **`solver/bfs.py`** only depends on `Maze.get_cell(...)` and
  `Cell.walls`, so it works against a maze produced by any generator, not
  just `MazeGenerator` — a different carving algorithm could be dropped in
  without changing the solver.
- The whole `maze` package is **pip-packaged** as `mazegen`
  (see `pyproject.toml`), so it can be installed and imported from other
  Python projects instead of being copy-pasted.

## 👥 Team & project management

| Login    | Name              | Focus                                                                 |
|----------|-------------------|------------------------------------------------------------------------|
| `zozcan` | Zehra Sıla Özcan  | Core maze engine: project scaffolding, config parsing/validation, `Cell`/`Maze` grid & adjacency logic, `MazeGenerator` (DFS carving, "42" pattern, loop carving) |
| `etemir` | Eda Temir         | Solver & presentation: BFS solver, hex/grid output encoding, terminal renderer (box-drawing UI, RGB colors), interactive menu, Makefile, pip packaging |

Work was split into feature branches (`feature/...`, `feat/...`, `fix/...`,
`menu-and-output`) merged into `master` through pull requests, roughly in
this order: project scaffolding → config parser and core `Cell`/`Maze`
classes → UI draft and BFS solver in parallel → `MazeGenerator` (DFS + "42"
pattern) and grid/hex rendering → BFS integration and colored output → bug
fixes (BFS edge cases, grid carving, path-direction conversion) →
interactive menu and loop mode for non-perfect mazes → packaging, Makefile
and documentation.

### Planning

The initial plan was to fix the module boundaries (`Config`, `Maze`/`Cell`,
`MazeGenerator`) first, so both of us could build on the same data model
and work in parallel from day one: one person on the generation engine, the
other on the solver and terminal UI. That part held up well. What shifted
along the way: the interactive menu and the loop-carving step for
`PERFECT=False` boards were originally meant to land early but were pushed
back until the DFS carving and the "42" pattern placement were fully
stable, since the loop logic depends on a correct dead-end count. Packaging
the `maze` package for pip and writing this documentation were always
planned as the last step, once the public API (`MazeGenerator`,
`parse_config`) had stopped changing.

### What worked well / what could be improved

- **Worked well:** splitting the code into independent modules
  (`maze.config`, `maze.maze`, `maze.generator`, `maze.output`,
  `solver.bfs`, `renderer.ui`) let both of us work in parallel with very
  few merge conflicts. Choosing an explicit stack over recursion for the
  DFS carving avoided any recursion-limit issues on large mazes. Using the
  subject's `maze_analyzer.py` early caught wall-coherence and dead-end
  bugs before they became hard to track down.
- **Could be improved:** `flake8`/`mypy` compliance was treated as a
  final cleanup step instead of being enforced from the first commit,
  which meant fixing a batch of style and typing issues late; docstrings
  and type hints on some helper functions (`bfs_solve`,
  `overlay_path_on_grid`, `get_wall_mask`) were added after the fact rather
  than as each function was written. The packaged `mazegen-*.whl`/`.tar.gz`
  at the repository root also drifted out of sync with `maze/`'s source
  during development; rebuilding it is now a dedicated `make package` step
  that should be run on every change to `maze/`, ideally before every
  commit rather than only before submission.

### Tools

- **Python 3.10+**, `git` branches and pull requests for parallel work.
- **flake8** and **mypy** (wired into `make lint` / `make lint-strict`)
  for style and static type checking.
- **`python -m build`** / `pip` to build and install the `mazegen` package.
- The subject-provided **`maze_analyzer.py`** to verify wall coherence and
  that each config produces the correct mode (`PERFECT` vs. Pac-Man
  board).

## 📚 Resources

- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — overview of maze-carving algorithms, including recursive backtracking.
- [Jamis Buck — "Maze Generation: Algorithm Recap"](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) — a classic comparison of recursive backtracker, Prim's, Kruskal's, Eller's, etc., with the trade-offs each one produces.
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search) — the algorithm used by the solver to find the shortest entry→exit path.
- [Python `random` module documentation](https://docs.python.org/3/library/random.html) — used for seeded, reproducible maze generation.

**AI usage:** AI tools were utilized throughout this project as a reference for information gathering, debugging, and code review. Additionally, an AI assistant was used to help structure and draft this `README.md` file by analyzing the existing codebase to accurately document the configuration format, output structure, and algorithm logic.
