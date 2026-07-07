from collections import deque

def bfs_solve(maze):


    start = None
    end = None

    rows = len(maze)
    cols = len(maze[0])

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    
    if not start or not end:
        return False

    queue = deque([start])
    visited = set([start])
    parent_map = {}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        
 