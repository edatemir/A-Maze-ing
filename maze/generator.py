
from maze.config import Config
from maze.maze import Maze
from maze.cell import Cell
import random

class MazeGenerator:
    PATTERN_42 = (
        "1010111",
        "1010001",
        "1110111",
        "0010100",
        "0010111",
    )
    

    def __init__(self, config: Config)-> None:
        self.config = config
        self.maze = Maze(
            width = config.width,
            height = config.height,
            entry = config.entry,
            exit = config.exit,
        )
        self.rnd = random.Random(config.seed)


    def pattern(self) -> None:
        pattern_height = len(self.PATTERN_42)
        pattern_width = len(self.PATTERN_42[0])

        if (
            self.config.width < pattern_width or self.config.height < pattern_height
        ):
            raise ValueError("Maze is too small for 42 pattern")
        
        start_x = (self.config.width - pattern_width) // 2
        start_y = (self.config.height - pattern_height) // 2

        entry_x, entry_y = self.config.entry
        exit_x, exit_y = self.config.exit

        for pattern_y, row in enumerate(self.PATTERN_42):
            for pattern_x, value in enumerate(row):
                if value != "1":
                    continue
                maze_x = start_x + pattern_x
                maze_y = start_y + pattern_y

                if (maze_x, maze_y) == (entry_x, entry_y):
                    raise ValueError("Entry can't overlap the 42 pattern")
                if (maze_x, maze_y) == (exit_x, exit_y):
                    raise ValueError("Exit can't overlap the 42 pattern")
                cell = self.maze.get_cell(maze_x, maze_y)
                cell.blocked = True


    def validate_connectivity(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                if not cell.blocked and not cell.visited:
                    raise ValueError("The 42 pattern disconnects part of the maze.")


    def loop(self) -> None:
        loops = 0
        candidates= []

        for row in self.maze.grid:
            for cell in row:
                if cell.blocked:
                    continue
                for neighbor in self.maze.get_neighbors(cell):
                    if neighbor.blocked:
                        continue
                    if not self.maze.has_wall(cell, neighbor):
                        continue
                    group = tuple(sorted((cell, neighbor), key=lambda current: (current.y, current.x)))
                    if group not in candidates:
                        candidates.append(group)
        self.rnd.shuffle(candidates)
        for cell, neighbor in candidates:
            if loops >= 2:
                break
            if not self.maze.has_wall(cell, neighbor):
                continue
            self.maze.remove_wall(cell, neighbor)
            loops += 1
        
        if loops < 2:
            raise ValueError("Unable to create at least two loops in the maze.")


    def generator(self) -> Maze:
        self.pattern()

        x, y = self.config.entry
        current = self.maze.get_cell(x, y)
        if current.blocked:
            raise ValueError("Entry cannot be inside the 42 pattern.")
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