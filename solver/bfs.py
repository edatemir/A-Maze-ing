from collections import deque


def bfs_solve(maze, config):
    """Find the shortest entry-to-exit path via BFS over open passages.
    Returns the path as a list of (x, y) coordinates, or False if the
      exit is unreachable."""
    start = config.entry
    end = config.exit

    queue = deque([start])
    visited = set([start])
    parent_map = {}

    directions = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0)
    }

    while queue:
        curr_x, curr_y = queue.popleft()

        if (curr_x, curr_y) == end:
            path = []
            curr = end
            while curr in parent_map:
                path.append(curr)
                curr = parent_map[curr]
            path.append(start)
            path.reverse()
            return path

        current_cell = maze.get_cell(curr_x, curr_y)

        for direction_name, (dx, dy) in directions.items():
            if not current_cell.walls[direction_name]:
                nx, ny = curr_x + dx, curr_y + dy

                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent_map[(nx, ny)] = (curr_x, curr_y)
                        queue.append((nx, ny))

    return False
