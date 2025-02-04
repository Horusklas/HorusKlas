import pygame
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(True)
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map)


import pygame

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 1200
height = 800

# Создание экрана ДО загрузки изображения
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Лабиринт")


# Загрузка изображения фона
try:
    background_image = pygame.image.load("walls/image.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))
except pygame.error as e:
    print(f"Ошибка загрузки изображения: {e}")
    background_image = None


# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)

# Шрифт
font = pygame.font.Font(None, 72)

# Текст кнопки
text = font.render("Начать игру", True, white)
text_rect = text.get_rect(center=(width // 2, height // 2))

# Состояние кнопки
button_color = gray


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if text_rect.collidepoint(mouse_pos):
                # Вы можете добавить логику для запуска игры здесь
                print("Начало игры...")
                running = False

    # Меняем цвет кнопки при наведении
    mouse_pos = pygame.mouse.get_pos()
    if text_rect.collidepoint(mouse_pos):
        button_color = white
    else:
        button_color = gray

    # Отрисовка фона
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(black)

    # Отрисовка кнопки (квадрата)
    pygame.draw.rect(screen, button_color, text_rect.inflate(20,20))
    # Отрисовка текста
    screen.blit(text, text_rect)

    # Обновление экрана
    pygame.display.flip()



pygame.mouse.set_visible(False)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    sc.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick(FPS)