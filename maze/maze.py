
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
    

    def inside(self, x: int, y: int) -> bool:
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        return False
    

    def get_cell(self, x: int, y: int) -> Cell:
        cell = self.grid[y][x]
        return cell
    

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors = []
        x = cell.x
        y = cell.y

        nx = x             #dongu mantigi yapilabilir   
        ny = y - 1
        if self.inside(nx, ny):
            neighbors.append(self.get_cell(nx, ny))
        
        ex = x + 1
        ey = y
        if self.inside(ex, ey):
            neighbors.append(self.get_cell(ex, ey))

        sx = x
        sy = y + 1
        if self.inside(sx, sy):
            neighbors.append(self.get_cell(sx, sy))

        wx = x - 1
        wy = y
        if self.inside(wx, wy):
            neighbors.append(self.get_cell(wx, wy))
        return neighbors

    def remove_wall(self, cell1: Cell, cell2: Cell) -> None:
        if cell2.x == cell1.x + 1 and cell2.y == cell1.y:
            cell1.walls["E"] = False
            cell2.walls["W"] = False
        elif cell2.x == cell1.x - 1 and cell2.y == cell1.y:
            cell1.walls["W"] = False
            cell2.walls["E"] = False
        elif cell2.x == cell1.x and cell2.y == cell1.y + 1:
            cell1.walls["S"] = False
            cell2.walls["N"] = False
        elif cell2.x == cell1.x and cell2.y == cell1.y - 1:
            cell1.walls["N"] = False
            cell2.walls["S"] = False
        #else:
            #raise ValueError("Cells are not adjacent.")
