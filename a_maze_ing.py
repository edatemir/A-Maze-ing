import sys
from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import ConfigFileError
from maze.output import convert_maze_to_grid
from renderer.ui import render_box_maze
from maze.output import generate_hex_content

def main() -> None:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        config = parse_config("config.txt")

        print("Config loaded successfully.")
        print(config)

        generator = MazeGenerator(config)
        maze = generator.generator()

        print("\nMaze generated successfully.")
        print(f"Size: {maze.width} x {maze.height}")
        print(f"Entry: {maze.entry}")
        print(f"Exit: {maze.exit}")

        grid = convert_maze_to_grid(maze)
        
        render_box_maze(grid)
        
        hex_lines = generate_hex_content(maze)
        for line in hex_lines:
            print(line)
    except ConfigFileError as error:
        print(error)


if __name__ == "__main__":
    main()