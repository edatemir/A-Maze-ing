
from maze.cell import Cell

class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = self._create_grid()

    def _create_grid(self) -> list[list[Cell]]:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            grid.append(row)
        return grid
    
