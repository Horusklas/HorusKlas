from settings import *
import pygame
import random
from numba.core import types
from numba.typed import Dict
from numba import int32


def generate_matrix_map(rows, cols):
    """Генерирует лабиринт с использованием алгоритма Randomized DFS."""

    # 1. Инициализация карты
    matrix_map = [['1' for _ in range(cols)] for _ in range(rows)]
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if row % 2 != 0 and col % 2 != 0:
                matrix_map[row][col] = '_'

    # 2. Запуск DFS из случайной точки
    start_row = random.randrange(1, rows, 2)
    start_col = random.randrange(1, cols, 2)

    stack = [(start_row, start_col)]
    visited = set()

    while stack:
        row, col = stack[-1]  # Берем последний элемент стека
        visited.add((row, col))

        # Получение непосещенных соседей
        neighbors = get_unvisited_neighbors(row, col, matrix_map, visited)

        if neighbors:
            next_row, next_col = random.choice(neighbors)

            # Проходим между текущей точкой и следующей
            matrix_map[(row + next_row) // 2][(col + next_col) // 2] = '_'
            stack.append((next_row, next_col))
        else:
            stack.pop()

    return matrix_map


def get_unvisited_neighbors(row, col, matrix_map, visited):
    """Получает список непосещенных соседей текущей клетки."""
    neighbors = []
    rows, cols = len(matrix_map), len(matrix_map[0])

    # Определение возможных направлений движения (шаги через 2 клетки)
    moves = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 1 <= new_row < rows - 1 and 1 <= new_col < cols - 1 and (new_row, new_col) not in visited:
            neighbors.append((new_row, new_col))
    return neighbors


def add_start_and_finish(matrix_map):
    """Добавляет стартовую и финишную точки."""
    rows, cols = len(matrix_map), len(matrix_map[0])
    matrix_map[1][0] = 'S'
    matrix_map[rows - 2][cols - 1] = 'F'


def add_demons(matrix_map, demon_count):
    """Добавляет демонов в случайные проходы и возвращает словарь индексов."""
    rows, cols = len(matrix_map), len(matrix_map[0])
    passage_cells = []
    for row in range(rows):
        for col in range(cols):
            if matrix_map[row][col] == '_':
                passage_cells.append((row, col))

    if demon_count > len(passage_cells):
      demon_count = len(passage_cells)

    demons = random.sample(passage_cells, demon_count)
    demon_indices = {}
    for i, (row, col) in enumerate(demons):
      matrix_map[row][col] = 'D'
      demon_indices[i + 1] = (row, col)
    return demon_indices

def print_matrix_map(matrix_map):
    """Печатает лабиринт в консоль."""
    for row in matrix_map:
        print(' '.join(str(cell) for cell in row))

# Пример использования:
rows = 21  # Нечетное число для DFS
cols = 31  # Нечетное число для DFS
demon_count = 10
matrix_map = generate_matrix_map(rows, cols)
add_start_and_finish(matrix_map)
demon_indices = add_demons(matrix_map, demon_count)
print_matrix_map(matrix_map)
WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char != '_' and char != 'D':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = 1
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 'S':
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 'F':
                world_map[(i * TILE, j * TILE)] = 2
print(demon_indices)