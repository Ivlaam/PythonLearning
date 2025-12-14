import numpy as np
from PIL import Image
# import random # 
import sys
import os

# Настройки симуляции
WIDTH, HEIGHT = 10, 10  # Размер сетки, должен совпадать с матрицей в файле (при методе загрузки из файла)
GENERATIONS = 20         # Количество поколений для симуляции
MAX_AGE = 3             # Максимальный возраст/количество градаций цвета. Если менять, то надо изменить и COLORS[]

COLORS = [
    (0, 0, 0),         # Черный (мертвая)
    (0, 100, 0),       # Темно-зеленый (старая клетка)
    (0, 180, 0),       # Средне-зеленый
    (0, 255, 0)        # Ярко-зеленый (новая клетка)
]
INPUT_FILENAME = "initial_map.txt"
OUTPUT_FILENAME = "life_simulation.png"

""" # генерация рандомом # заменили на загрузку из файла
def initialize_grid(width, height):
    # Создает начальную сетку со случайным распределением живых/мертвых клеток.
    # Заполнение с вероятностью 60% живых клеток
    grid = np.random.choice([0, 1], WIDTH * HEIGHT, p=[0.4, 0.6]).reshape(HEIGHT, WIDTH)
    return grid
"""

def load_grid_from_txt(filename, width, height):
    #Загружает начальное состояние из TXT файла.
    try:
        # Загружаем данные из файла в массив numpy
        grid = np.loadtxt(filename, dtype=int)
        # Проверяем на соответствие размеров
        if grid.shape != (height, width):
            print(f"Ошибка: Размеры сетки в файле {filename} ({grid.shape}) не соответствуют заданным WIDTH/HEIGHT ({width}, {height}).")
            sys.exit(1)
        # При загрузке 1 меняем на MAX_AGE, чтобы стартовали с яркого цвета
        grid[grid == 1] = MAX_AGE
        return grid
    # Обработка ошибок
    except IOError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        print("Пожалуйста, создайте файл initial_map.txt с расстановкой 1 и 0.")
        sys.exit(1)
    except ValueError:
        print(f"Ошибка: Некорректный формат данных в файле '{filename}'. Ожидаются целые числа 0 или 1.")
        sys.exit(1)

def update_grid(current_grid):
    """Вычисляет следующее поколение с учетом возраста клеток."""
    # Создаем булеву маску живых клеток для корректного подсчета соседей (True=1, False=0)
    alive_mask = (current_grid > 0).astype(int)
    new_grid = current_grid.copy()

    for i in range(HEIGHT):
        for j in range(WIDTH):
            # Подсчет соседей вручную с использованием тороидальных границ (%)
            
            """ Оператор % WIDTH или % HEIGHT гарантирует, что любое вычисленное значение индекса,
            будь оно отрицательным (смотрим на соседа слева у клетки с индексом width 0)
            или превышающим размер массива (сосед снизу у клетки с height 9), всегда будет приведено к
            корректному индексу внутри диапазона [0, Размер - 1]. Это и создает эффект "заворачивания" поля. """
            
            total_neighbors = (
                alive_mask[i, (j-1)%WIDTH] + alive_mask[i, (j+1)%WIDTH] +
                alive_mask[(i-1)%HEIGHT, j] + alive_mask[(i+1)%HEIGHT, j] +
                alive_mask[(i-1)%HEIGHT, (j-1)%WIDTH] + alive_mask[(i-1)%HEIGHT, (j+1)%WIDTH] +
                alive_mask[(i+1)%HEIGHT, (j-1)%WIDTH] + alive_mask[(i+1)%HEIGHT, (j+1)%WIDTH]
            )
            if current_grid[i, j] > 0: # Если клетка жива
                if (total_neighbors < 2) or (total_neighbors > 3):
                    new_grid[i, j] = 0 # Умирает
                else:
                    # Выживает, возраст уменьшается, но не ниже 1
                    if new_grid[i, j] > 1:
                         new_grid[i, j] -= 1
            else: # Если клетка мертва
                if total_neighbors == 3:
                    new_grid[i, j] = MAX_AGE # Рождается
    return new_grid

def save_as_png(grid, filename):
    
    """Преобразует сетку с возрастами в изображение Pillow и сохраняет как PNG."""
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLORS[0])
    pixels = img.load()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            age = grid[i, j]
            # Используем значение возраста как индекс в списке COLORS
            pixels[j, i] = COLORS[age]
     # Увеличим размер изображения, чтобы его было видно (Опционально \для дебага. Как работает - не знаю, честно украдено)
    img = img.resize((WIDTH * 10, HEIGHT * 10), resample=Image.NEAREST)
    img.save(filename, 'PNG')
    print(f"Симуляция сохранена в файл: {os.path.abspath(filename)}")


# --- Запуск симуляции ---
print(f"Запуск симуляции '{OUTPUT_FILENAME}' на {GENERATIONS} поколений...")
    # 1. Инициализация
    # current_grid = initialize_grid(WIDTH, HEIGHT) # Запуск рандомайзера, теперь не нужен
    # 1.1 Инициализация из файла
current_grid = load_grid_from_txt(INPUT_FILENAME, WIDTH, HEIGHT)

# 2. Сохраняем НУЛЕВОЕ поколение (до первого обновления) \было нужно в процессе отладки
save_as_png(current_grid, f"{OUTPUT_FILENAME}start.png")

    # 2. Симуляция поколений \кастуем нашу магию
for gen in range(GENERATIONS):
    current_grid = update_grid(current_grid)
    OUTPUT_FILENAME = f"life_simulation{gen}.png"
    save_as_png(current_grid, OUTPUT_FILENAME)
    # Сохраняем каждое поколение в отдельный файл,
    # чтобы потом собрать GIF-анимацию \гифку собирать вручную на отдельном сайте.
    # Лучше использовать рандомайзер с размерами побольше, на больше поколений, так будет красивее. Возможно ещё убрать ресайз
    # Чисто побаловаться