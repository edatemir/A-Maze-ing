from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import ConfigFileError


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

        print("\nMaze cells:")
        for row in maze.grid:
            for cell in row:
                print(
                    f"Cell ({cell.x}, {cell.y}) "
                    f"visited={cell.visited} "
                    f"walls={cell.walls}"
                )

    except ConfigFileError as error:
        print(error)


if __name__ == "__main__":
    main()