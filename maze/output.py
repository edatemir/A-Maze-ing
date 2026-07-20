from maze.maze import Maze
from maze.cell import Cell

def convert_maze_to_grid(maze: Maze) -> list[list]:
    rows = 2 * maze.height + 1
    cols = 2 * maze.width + 1

    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            grid_y = 2 * y + 1
            grid_x = 2 * x + 1
            grid[grid_y][grid_x] = 0

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