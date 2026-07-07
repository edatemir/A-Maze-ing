RESET = "\033[0m"
WALL_COLOR = "\033[96m"
ENTRY_COLOR = "\033[1;92m"
EXIT_COLOR = "\033[1;91m"
PATH_COLOR = "\033[93m"
LOGO_COLOR = "\033[1;95m"  # Parlak Mor

BOX_CHARS = {
    0: "■",   # Tek başına duran duvar
    1: "┃",   # üst
    2: "╺",   # Sağ
    3: "┗",   # üst ve sağ
    4: "┃",   # alt
    5: "┃",   # üst ve alt
    6: "┏",   # sağ ve alt
    7: "┣",   # üst sağ ve alt 
    8: "╸",   # sadece sol
    9: "┛",   # üst sol
    10: "━",  # sağ sol birlikte
    11: "┻",  # üst sağ sol
    12: "┓",  # alt sol
    13: "┫",  # üst + alt + sol
    14: "┳",  # alt + sağ + sol
    15: "╋"   # hepsi
}

def get_wall_mask(maze, row, col):
    mask = 0
    if row > 0 and maze[row - 1][col] in (1, 2):
        mask += 1

    if col < len(maze[0]) - 1 and maze[row][col + 1] in (1, 2):
        mask += 2

    if row < len(maze) - 1 and maze[row + 1][col] in (1, 2):
        mask += 4

    if col > 0 and maze[row][col - 1] in (1, 2):
        mask += 8
    
    return mask

def render_box_maze(maze):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == 1:
                mask = get_wall_mask(maze, r, c)
                box_char = BOX_CHARS[mask]
                if c < len(maze[0]) - 1 and maze[r][c + 1] in (1, 2):
                    connect_east = "━"
                else:
                    connect_east = " "

                print(f"{WALL_COLOR}{box_char}{connect_east}{RESET}", end="")
            
            elif cell == 2:
                mask = get_wall_mask(maze, r, c)
                box_char = BOX_CHARS[mask]
                
                if c < len(maze[0]) - 1 and maze[r][c + 1] in (1, 2):
                    connect_east = "━"
                else:
                    connect_east = " "

                print(f"{LOGO_COLOR}{box_char}{connect_east}{RESET}", end="")

            elif cell == 'S':
                print(f"{ENTRY_COLOR}S {RESET}", end="")
            elif cell == 'E':
                print(f"{EXIT_COLOR}E {RESET}", end="")
            elif cell == '*':
                print(f"{PATH_COLOR}• {RESET}", end="")
            else:
                print("  ", end="")

        print()

if __name__ == "__main__":
    mock_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 'S', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 0, 0, 2, 0, 2, 2, 2, 2, 1, 0, 1],
        [1, 0, 1, 0, 1, 2, 0, 0, 2, 0, 0, 0, 0, 2, 1, 0, 1],
        [1, 0, 1, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 2, 2, 2, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    print("\n--- KUTU ÇİZİM TESTİ ---\n")
    render_box_maze(mock_maze)