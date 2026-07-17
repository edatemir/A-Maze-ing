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
        current_r, current_c = queue.popleft()
        if(current_r, current_c) == end:
            path = []
            curr = end
            while curr in parent_map:
                path.append(curr)
                 curr = parent_map[curr]
            path.append(start)
            path.reverse()
            return path

        for dr, dc in directions:
        nr, nc = current_r + dr, current_c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] in (0, 'E') and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent_map[(nr, nc)] = (current_r, current_c) 
                    queue.append((nr, nc))
    return False

 