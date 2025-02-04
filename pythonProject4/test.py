import random

def generate_maze(rows, cols):
    """Генерирует лабиринт с использованием алгоритма Randomized DFS."""

    # 1. Инициализация карты
    maze = [['1' for _ in range(cols)] for _ in range(rows)]
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if row % 2 != 0 and col % 2 != 0:
                maze[row][col] = '_'

    # 2. Запуск DFS из случайной точки
    start_row = random.randrange(1, rows, 2)
    start_col = random.randrange(1, cols, 2)

    stack = [(start_row, start_col)]
    visited = set()

    while stack:
        row, col = stack[-1]  # Берем последний элемент стека
        visited.add((row, col))

        # Получение непосещенных соседей
        neighbors = get_unvisited_neighbors(row, col, maze, visited)

        if neighbors:
            next_row, next_col = random.choice(neighbors)

            # Проходим между текущей точкой и следующей
            maze[(row + next_row) // 2][(col + next_col) // 2] = '_'
            stack.append((next_row, next_col))
        else:
            stack.pop()

    return maze


def get_unvisited_neighbors(row, col, maze, visited):
    """Получает список непосещенных соседей текущей клетки."""
    neighbors = []
    rows, cols = len(maze), len(maze[0])

    # Определение возможных направлений движения (шаги через 2 клетки)
    moves = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 1 <= new_row < rows - 1 and 1 <= new_col < cols - 1 and (new_row, new_col) not in visited:
            neighbors.append((new_row, new_col))
    return neighbors


def add_start_and_finish(maze):
    """Добавляет стартовую и финишную точки."""
    rows, cols = len(maze), len(maze[0])
    maze[1][0] = 'S'
    maze[rows - 2][cols - 1] = 'F'


def add_demons(maze, demon_count):
    """Добавляет демонов в случайные проходы и возвращает словарь индексов."""
    rows, cols = len(maze), len(maze[0])
    passage_cells = []
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == '_':
                passage_cells.append((row, col))

    if demon_count > len(passage_cells):
      demon_count = len(passage_cells)

    demons = random.sample(passage_cells, demon_count)
    demon_indices = {}
    for i, (row, col) in enumerate(demons):
      maze[row][col] = 'D'
      demon_indices[i + 1] = (row, col)
    return demon_indices

def print_maze(maze):
    """Печатает лабиринт в консоль."""
    for row in maze:
        print(' '.join(str(cell) for cell in row))

# Пример использования:
rows = 17  # Нечетное число для DFS
cols = 25  # Нечетное число для DFS
demon_count = 5
maze = generate_maze(rows, cols)
add_start_and_finish(maze)
demon_indices = add_demons(maze, demon_count)
print_maze(maze)
print("\nИндексы демонов:", demon_indices)