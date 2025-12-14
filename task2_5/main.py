import numpy as np
from PIL import Image
import sys
import os

WIDTH, HEIGHT = 10, 10  
GENERATIONS = 20         
MAX_AGE = 3             
COLORS = [
    (0, 0, 0),         
    (0, 100, 0),       
    (0, 180, 0),       
    (0, 255, 0)        
]
INPUT_FILENAME = "initial_map.txt"
OUTPUT_FILENAME = "life_simulation.png"

def load_grid_from_txt(filename, width, height):
    try:
        grid = np.loadtxt(filename, dtype=int)
        if grid.shape != (height, width):
            print(f"Ошибка: Размеры сетки в файле {filename} ({grid.shape}) не соответствуют заданным WIDTH/HEIGHT ({width}, {height}).")
            sys.exit(1)
        grid[grid == 1] = MAX_AGE
        return grid
    except IOError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        print("Пожалуйста, создайте файл initial_map.txt с расстановкой 1 и 0.")
        sys.exit(1)
    except ValueError:
        print(f"Ошибка: Некорректный формат данных в файле '{filename}'. Ожидаются целые числа 0 или 1.")
        sys.exit(1)
        
def update_grid(current_grid):
    alive_mask = (current_grid > 0).astype(int)
    new_grid = current_grid.copy()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            total_neighbors = (
                alive_mask[i, (j-1)%WIDTH] + alive_mask[i, (j+1)%WIDTH] +
                alive_mask[(i-1)%HEIGHT, j] + alive_mask[(i+1)%HEIGHT, j] +
                alive_mask[(i-1)%HEIGHT, (j-1)%WIDTH] + alive_mask[(i-1)%HEIGHT, (j+1)%WIDTH] +
                alive_mask[(i+1)%HEIGHT, (j-1)%WIDTH] + alive_mask[(i+1)%HEIGHT, (j+1)%WIDTH]
            )
            if current_grid[i, j] > 0: 
                if (total_neighbors < 2) or (total_neighbors > 3):
                    new_grid[i, j] = 0 
                else:
                    if new_grid[i, j] > 1:
                         new_grid[i, j] -= 1
            else:
                if total_neighbors == 3:
                    new_grid[i, j] = MAX_AGE
    return new_grid

def save_as_png(grid, filename):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLORS[0])
    pixels = img.load()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            age = grid[i, j]
            pixels[j, i] = COLORS[age]
    img = img.resize((WIDTH * 10, HEIGHT * 10), resample=Image.NEAREST)
    img.save(filename, 'PNG')
    print(f"Симуляция сохранена в файл: {os.path.abspath(filename)}")

print(f"Запуск симуляции '{OUTPUT_FILENAME}' на {GENERATIONS} поколений...")
current_grid = load_grid_from_txt(INPUT_FILENAME, WIDTH, HEIGHT)
save_as_png(current_grid, f"{OUTPUT_FILENAME}start.png")
for gen in range(GENERATIONS):
    current_grid = update_grid(current_grid)
    OUTPUT_FILENAME = f"life_simulation{gen}.png"
    save_as_png(current_grid, OUTPUT_FILENAME)