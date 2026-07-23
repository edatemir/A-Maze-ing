RESET = "\033[0m"
WALL_COLOR = "\033[38;2;168;228;160m"
ENTRY_COLOR = "\033[1;92m"
EXIT_COLOR = "\033[1;91m"
PATH_COLOR =  "\033[38;2;219;112;147m"

BOX_CHARS = {
    0: "■",
    1: "┃",   # top
    2: "╺",   # right
    3: "┗",   # top and right
    4: "┃",   # bottom
    5: "┃",   # top and bottom
    6: "┏",   # right and bottom
    7: "┣",   # top, right and bottom
    8: "╸",   # left
    9: "┛",   # top and left
    10: "━",  # right and left together
    11: "┻",  # top, right, and left
    12: "┓",  # bottom and left
    13: "┫",  # top + bottom + left
    14: "┳",  # bottom + right + left
    15: "╋"   # all
}

def get_wall_mask(maze: list[list[int | str]], row: int, col: int) -> int:
    """Compute the bitmask (from neighbouring wall cells) that selects the right box-drawing character."""
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

def render_box_maze(
    maze: list[list[int | str]], current_wall_color: str = WALL_COLOR
) -> None:
"""Print the character grid to the terminal using box-drawing characters and colors for walls/entry/exit/path."""
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell in (1, 2):
                mask = get_wall_mask(maze, r, c)
                box_char = BOX_CHARS[mask]

                if c < len(maze[0]) - 1 and maze[r][c + 1] in (1, 2):
                    connect_east = "━"
                else:
                    connect_east = " "

                print(f"{current_wall_color}{box_char}{connect_east}{RESET}", end="")
            
            elif cell == 'S':
                print(f"{ENTRY_COLOR}S {RESET}", end="")
            elif cell == 'E':
                print(f"{EXIT_COLOR}E {RESET}", end="")
            elif cell == '.':
                print(f"{PATH_COLOR}• {RESET}", end="")
            else:
                print("  ", end="")

        print()