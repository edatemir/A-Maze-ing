import sys
import time
from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import (
    ConfigFileError,
    ConfigSyntaxError,
    ConfigMissingKeyError,
    ConfigValueError,
    ConfigValidationError,
    MazeGenerationError,
)
from maze.output import (
    convert_maze_to_grid,
    generate_hex_content,
    convert_path_to_directions,
    overlay_path_on_grid,
)
from renderer.ui import render_box_maze
from solver.bfs import bfs_solve


def save_maze_to_file(
    filename: str,
    hex_lines: list[str],
    entry: tuple[int, int],
    exit: tuple[int, int],
    directions: str,
) -> None:
    """Write the hex-encoded maze, entry/exit coordinates and solution path to
    filename.Prints an error instead of raising if the file can't be written.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in hex_lines:
                f.write(f"{line}\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{directions}\n")
    except IOError as e:
        print(f"Failed to write output file: {e}")


def main() -> None:
    """Parse the config, generate and solve a maze, save it, then run the
    interactive menu."""
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parse_config(config_file)
    except (
        ConfigFileError,
        ConfigSyntaxError,
        ConfigMissingKeyError,
        ConfigValueError,
        ConfigValidationError,
    ) as error:
        print(error)
        return

    show_path = True
    colors = [
        "\033[38;2;168;228;160m",
        "\033[1;34m",
        "\033[1;33m",
        "\033[1;31m",
        "\033[1;36m",
    ]
    color_idx = 0

    try:
        generator = MazeGenerator(config)
        maze = generator.generator()
    except MazeGenerationError as error:
        print(error)
        return

    path_coords = bfs_solve(maze, config)
    directions = (
        convert_path_to_directions(path_coords) if path_coords else ""
    )

    hex_lines = generate_hex_content(maze)
    save_maze_to_file(
        config.output_file,
        hex_lines,
        config.entry,
        config.exit,
        directions,
    )

    while True:
        grid = convert_maze_to_grid(maze)

        if show_path and path_coords:
            grid = overlay_path_on_grid(grid, path_coords)

        render_box_maze(grid, current_wall_color=colors[color_idx])

        print("\n=== A-Maze-ing ===")
        print("1. Generate a new maze")
        print(
            f"2. Show/Hide the shortest path "
            f"(Currently: {'Visible' if show_path else 'Hidden'})"
        )
        print("3. Change wall color")
        print("4. Exit")

        choice = input("Your choice (1-4): ").strip()

        if choice == "1":
            config.seed = int(time.time() * 1000) % 10000

            try:
                generator = MazeGenerator(config)
                maze = generator.generator()
            except MazeGenerationError as error:
                print(error)
                return

            path_coords = bfs_solve(maze, config)
            directions = (
                convert_path_to_directions(path_coords)
                if path_coords
                else ""
            )

            hex_lines = generate_hex_content(maze)
            save_maze_to_file(
                config.output_file,
                hex_lines,
                config.entry,
                config.exit,
                directions,
            )

            print(
                f"\n[+] New maze generated and saved to "
                f"'{config.output_file}'!"
            )
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(colors)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print(
                "Invalid choice. Please enter a number between 1 and 4."
            )


if __name__ == "__main__":
    main()
