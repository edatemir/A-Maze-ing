from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import ConfigFileError
from maze.output import convert_maze_to_grid
from renderer.ui import render_box_maze

def main() -> None:
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
        g
        render_box_maze(grid)

    except ConfigFileError as error:
        print(error)


if __name__ == "__main__":
    main()