
from maze.config import Config
from maze.maze import Maze
import random

class MazeGenerator:
    def __init__(self, config: Config)-> None:
        self.config = config
        self.maze = Maze(
            width = config.width,
            height = config.height,
            entry = config.entry,
            exit = config.exit,
        )
        self.rnd = random.Random(config.seed)
        

    def generator(self) -> Maze:
        x, y = self.config.entry
        current = self.maze.get_cell(x, y)
        current.visited = True
        stack = []
        stack.append(current)
        while stack:
            current = stack[-1]
            neighbors = self.maze.get_neighbors(current)
            unvisited = []
            for neighbor in neighbors:
                if not neighbor.visited:
                    unvisited.append(neighbor)
            if not unvisited:
                stack.pop()
            else:
                next_choice = self.rnd.choice(unvisited)
                self.maze.remove_wall(current, next_choice)
                next_choice.visited = True
                stack.append(next_choice) 


        return self.maze