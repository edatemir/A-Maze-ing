import sys
from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import ConfigFileError
from maze.output import convert_maze_to_grid
from renderer.ui import render_box_maze
from maze.output import generate_hex_content
from solver.bfs import bfs_solve
from maze.output import convert_path_to_directions, overlay_path_on_grid

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
        print(f"Entry: {config.entry}")
        print(f"Exit: {config.exit}")
        path_coords = bfs_solve(maze, config)
        
        if path_coords:
            directions = convert_path_to_directions(path_coords)
            print(f"Yol uzunluğu: {len(path_coords)} adım.")
            print(f"Yönler: {directions}")
        else:
            print("[-] Çıkışa ulaşan bir yol bulunamadı.")
            directions = ""
        grid = convert_maze_to_grid(maze)
        if path_coords:
            # Bulunan yolu matrisin üzerine nokta nokta işle
            grid = overlay_path_on_grid(grid, path_coords)
            
        print("\n--- LABİRENT ---")
        render_box_maze(grid)
        
        print("\n--- HEX ÇIKTISI ---") 
        hex_lines = generate_hex_content(maze)
        for line in hex_lines:
            print(line)
    except ConfigFileError as error:
        print(error)


if __name__ == "__main__":
    main()