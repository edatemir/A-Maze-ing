from maze.maze import Maze

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