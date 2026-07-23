
from maze.config import Config
from maze.maze import Maze
from maze.cell import Cell
from maze.exceptions import MazeGenerationError
import random


class MazeGenerator:
    """Builds a maze from a Config using a DFS-based wall-carving algorithm."""
    PATTERN_42 = (
        "1010111",
        "1010001",
        "1110111",
        "0010100",
        "0010111",
    )

    def __init__(self, config: Config) -> None:
        """Create an empty Maze from the config and set up a seeded
          random generator."""
        self.config = config
        self.maze = Maze(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
        )
        self.rnd = random.Random(config.seed)

    def pattern(self) -> None:
        """Stamp the '42' pattern as blocked cells in the centre of the grid;
          skip it if it doesn't fit or overlaps entry/exit."""
        pattern_height = len(self.PATTERN_42)
        pattern_width = len(self.PATTERN_42[0])

        if (
            self.config.width < pattern_width
            or self.config.height < pattern_height
        ):
            print("Maze is too small for 42 pattern")
            return

        start_x = (self.config.width - pattern_width) // 2
        start_y = (self.config.height - pattern_height) // 2

        center_x = self.config.width // 2
        center_y = self.config.height // 2

        pattern_center_x = center_x - start_x
        pattern_center_y = center_y - start_y

        if (
            0 <= pattern_center_x < pattern_width
            and 0 <= pattern_center_y < pattern_height
            and self.PATTERN_42[pattern_center_y][pattern_center_x] == "1"
        ):
            if start_x + pattern_width < self.config.width:
                start_x += 1
            elif start_x > 0:
                start_x -= 1

        entry_x, entry_y = self.config.entry
        exit_x, exit_y = self.config.exit

        for pattern_y, row in enumerate(self.PATTERN_42):
            for pattern_x, value in enumerate(row):
                if value != "1":
                    continue
                maze_x = start_x + pattern_x
                maze_y = start_y + pattern_y

                if (maze_x, maze_y) == (entry_x, entry_y):
                    print("42 pattern skipped because it overlaps the entry")
                    return
                if (maze_x, maze_y) == (exit_x, exit_y):
                    print("42 pattern skipped because it overlaps the exit")
                    return

        for pattern_y, row in enumerate(self.PATTERN_42):
            for pattern_x, value in enumerate(row):
                if value != "1":
                    continue
                maze_x = start_x + pattern_x
                maze_y = start_y + pattern_y

                cell = self.maze.get_cell(maze_x, maze_y)
                cell.blocked = True

    def validate_connectivity(self) -> None:
        """Check that every non-'42' cell was visited during carving;
          raise an error otherwise."""
        for row in self.maze.grid:
            for cell in row:
                if not cell.blocked and not cell.visited:
                    raise MazeGenerationError(
                        "The 42 pattern disconnects part of the maze."
                        )

    def dead_end(self, cell: Cell) -> bool:
        """Return whether a cell has exactly one open passage,
          i.e. is a dead end."""
        open_path = 0
        for neighbor in self.maze.get_neighbors(cell):
            if neighbor.blocked:
                continue
            if not self.maze.has_wall(cell, neighbor):
                open_path += 1
        return open_path == 1

    def loop(self) -> None:
        """In PERFECT=False mode, remove random walls to cut dead ends
          and add at least two loops."""
        loops = 0
        max_dead_end = 2
        while True:
            dead_end = []
            for row in self.maze.grid:
                for cell in row:
                    if cell.blocked:
                        continue
                    if self.dead_end(cell):
                        dead_end.append(cell)
            if len(dead_end) <= max_dead_end and loops >= 2:
                break
            self.rnd.shuffle(dead_end)
            wall_removed = False
            for cell in dead_end:
                candidates = []
                for neighbor in self.maze.get_neighbors(cell):
                    if neighbor.blocked:
                        continue
                    if not self.maze.has_wall(cell, neighbor):
                        continue
                    candidates.append(neighbor)
                self.rnd.shuffle(candidates)
                for neighbor in candidates:
                    self.maze.remove_wall(cell, neighbor)
                    loops += 1
                    wall_removed = True
                    break
                if wall_removed:
                    break
            if not wall_removed:
                break
        if loops < 2:
            raise MazeGenerationError(
                "Unable to create at least two loops in the maze."
                )

    def generator(self) -> Maze:
        """Place the '42' pattern, carve the maze with DFS, add loops
          if not PERFECT, and return the Maze."""
        self.pattern()

        x, y = self.config.entry
        current = self.maze.get_cell(x, y)
        if current.blocked:
            raise MazeGenerationError("Entry cannot be inside the 42 pattern.")
        current.visited = True
        stack = []
        stack.append(current)
        while stack:
            current = stack[-1]
            neighbors = self.maze.get_neighbors(current)
            unvisited = []
            for neighbor in neighbors:
                if not neighbor.visited and not neighbor.blocked:
                    unvisited.append(neighbor)
            if not unvisited:
                stack.pop()
            else:
                next_choice = self.rnd.choice(unvisited)
                self.maze.remove_wall(current, next_choice)
                next_choice.visited = True
                stack.append(next_choice)
        self.validate_connectivity()
        if not self.config.perfect:
            self.loop()
        return self.maze
