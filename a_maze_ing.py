import sys
import time
from maze.config import parse_config
from maze.generator import MazeGenerator
from maze.exceptions import ConfigFileError
from maze.output import convert_maze_to_grid, generate_hex_content, convert_path_to_directions, overlay_path_on_grid
from renderer.ui import render_box_maze
from solver.bfs import bfs_solve

def save_maze_to_file(filename: str, hex_lines: list[str], entry: tuple[int, int], exit: tuple[int, int], directions: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in hex_lines:
                f.write(f"{line}\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{directions}\n")
    except IOError as e:
        print(f"Çıktı dosyası yazılamadı: {e}")

def main() -> None:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) != 2:
        print("Kullanım: python3 a_maze_ing.py <config_dosyasi>")
        sys.exit(1)
    config_file = sys.argv[1]
    try:
        config = parse_config(config_file)
        print("[+] Config loaded successfully.")
        show_path = True
        colors = [
            "\033[38;2;168;228;160m",
            "\033[1;34m",
            "\033[1;33m",
            "\033[1;31m",
            "\033[1;36m"
        ]
        color_idx = 0

        generator = MazeGenerator(config)
        maze = generator.generator()
        path_coords = bfs_solve(maze, config)
        directions = convert_path_to_directions(path_coords) if path_coords else ""
        
        hex_lines = generate_hex_content(maze)
        save_maze_to_file(config.output_file, hex_lines, config.entry, config.exit, directions)
        while True:
            grid = convert_maze_to_grid(maze)
            if show_path and path_coords:
                grid = overlay_path_on_grid(grid, path_coords)
            print("\n" * 2) 
            print("--- LABİRENT ---")
            render_box_maze(grid, current_wall_color=colors[color_idx])
            
            print("\n=== A-Maze-ing ===")
            print("1. Yeni bir labirent üret (Re-generate)")
            print(f"2. En kısa yolu göster/gizle (Şu an: {'Gösteriliyor' if show_path else 'Gizli'})")
            print("3. Duvar rengini değiştir")
            print("4. Çıkış")
            choice = input("Seçiminiz (1-4): ").strip()
            
            if choice == "1":
                config.seed = int(time.time() * 1000) % 10000 
                generator = MazeGenerator(config)
                maze = generator.generator()
                path_coords = bfs_solve(maze, config)
                directions = convert_path_to_directions(path_coords) if path_coords else ""
                
                hex_lines = generate_hex_content(maze)
                save_maze_to_file(config.output_file, hex_lines, config.entry, config.exit, directions)
                print(f"\n[+] Yeni labirent üretildi ve '{config.output_file}' dosyasına kaydedildi!")
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                color_idx = (color_idx + 1) % len(colors)
            elif choice == "4":
                print("Çıkış yapılıyor...")
                break
            else:
                print("Geçersiz seçim, lütfen 1 ile 4 arasında bir değer girin.")

    except ConfigFileError as error:
        print(error)

if __name__ == "__main__":
    main()