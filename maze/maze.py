
from maze.cell import Cell


class Maze:
    """The maze grid of cells, plus its entry and exit positions."""
    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int]
            ) -> None:
        """Build a grid of the given size, made of cells with all walls
          closed."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = self._create_grid()

    def _create_grid(self) -> list[list[Cell]]:
        """Create a width x height grid of default Cell instances."""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            grid.append(row)
        return grid

    def inside(self, x: int, y: int) -> bool:
        """Return whether (x, y) lies within the maze bounds."""
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return True
        return False

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at (x, y)."""
        cell = self.grid[y][x]
        return cell

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        """Return the in-bounds neighbours (N/E/S/W) of a cell."""
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
        """Open the shared wall between two adjacent cells, on both sides."""
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
        else:
            raise ValueError("Cells are not adjacent.")

    def has_wall(self, cell1: Cell, cell2: Cell) -> bool:
        """Return whether a wall still stands between two adjacent cells."""
        if cell2.x == cell1.x + 1 and cell2.y == cell1.y:
            return cell1.walls["E"]
        elif cell2.x == cell1.x - 1 and cell2.y == cell1.y:
            return cell1.walls["W"]
        elif cell2.x == cell1.x and cell2.y == cell1.y + 1:
            return cell1.walls["S"]
        elif cell2.x == cell1.x and cell2.y == cell1.y - 1:
            return cell1.walls["N"]
        else:
            raise ValueError("Cells are not adjacent.")
