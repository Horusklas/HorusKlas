import pygame
import os

def play_music(music_file):
    """Запускает воспроизведение музыки."""
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение
    except pygame.error as e:
        print(f"Ошибка при загрузке музыки: {e}")

# Инициализация Pygame
pygame.init()

# Загрузка музыки (вызываем play_music сразу после pygame.init())
music_path = os.path.join('music', 'Start.mp3')
if os.path.isfile(music_path):
    play_music(music_path)
else:
    print(f"Музыкальный файл не найден: {music_path}")

# Создание окна
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Моя игра")

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ваша игровая логика здесь

    pygame.display.flip()

pygame.quit()