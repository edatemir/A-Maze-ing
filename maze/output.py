from maze.maze import Maze
from maze.cell import Cell

def convert_maze_to_grid(maze: Maze) -> list[list]:
    """Build the character grid used for rendering: walls, blocked cells, entry ('S') and exit ('E')."""
    rows = 2 * maze.height + 1
    cols = 2 * maze.width + 1

    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            grid_y = 2 * y + 1
            grid_x = 2 * x + 1
            grid[grid_y][grid_x] = 0
            if cell.blocked:
                grid[grid_y][grid_x] = 2

            if not cell.walls["E"]:
                grid[grid_y][grid_x + 1] = 0

            if not cell.walls["S"]:
                grid[grid_y + 1][grid_x] = 0
        
    entry_x, entry_y = maze.entry
    grid[2 * entry_y + 1][2 * entry_x + 1]= 'S'

    exit_x, exit_y = maze.exit
    grid[2 * exit_y + 1][2 * exit_x + 1] = 'E'

    return grid

def get_hex_char(cell: Cell) -> str:
    """Encode a cell's four walls (N/E/S/W) into the single hex digit used in the output file."""
    value = 0
    if cell.walls["N"]:
        value += 1
    if cell.walls["E"]:
        value += 2
    if cell.walls["S"]:
        value += 4
    if cell.walls["W"]:
        value += 8

    return f"{value:X}"

def generate_hex_content(maze: Maze) -> list[str]:
    """Return the maze as one hex-encoded wall string per row, ready to write to the output file."""
    lines = []
    for y in range(maze.height):
        row_chars = []
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            hex_char = get_hex_char(cell)
            row_chars.append(hex_char)

        lines.append("".join(row_chars))
    return lines

def convert_path_to_directions(path: list[tuple[int, int]]) -> str:
    """Convert a list of (x, y) path coordinates into a string of N/E/S/W compass letters."""
    if not path or len(path) < 2:
        return ""

    directions = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        if y2 < y1: directions.append("N")
        elif y2 > y1: directions.append("S")
        elif x2 > x1: directions.append("E")
        elif x2 < x1: directions.append("W")
    return "".join(directions)

def overlay_path_on_grid(grid, path):
    """Mark the solver's path cells and the walls it crosses on the render grid with '.'."""
    if not path or len(path) < 2:
        return grid
        
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        
        gy1, gx1 = y1 * 2 + 1, x1 * 2 + 1
        if grid[gy1][gx1] not in ('S', 'E'):
            grid[gy1][gx1] = '.'
            
        g_wall_y = y1 + y2 + 1
        g_wall_x = x1 + x2 + 1
        if grid[g_wall_y][g_wall_x] not in ('S', 'E'):
            grid[g_wall_y][g_wall_x] = '.'
            
    last_x, last_y = path[-1]
    gly, glx = last_y * 2 + 1, last_x * 2 + 1
    if grid[gly][glx] not in ('S', 'E'):
        grid[gly][glx] = '.'
        
    return grid