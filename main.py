import pygame
import json
from settings import *
from player import Player
from sprite_objects import *
from ray_casting import ray_casting_walls
from drawing import Drawing
import time
import os
import random

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(True)
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map)

width = 1200
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Лабиринт")

try:
    background_image = pygame.image.load("walls/image.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))
except pygame.error as e:
    print(f"Ошибка загрузки изображения: {e}")
    background_image = None

white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
green = (0, 255, 0)
red = (255, 0, 0)

font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)

start_text = font.render("Начать игру", True, white)
start_rect = start_text.get_rect(center=(width // 2, height // 2 + 200))

easy_text = small_font.render("Простой (мини-карта включена)", True, black)
easy_rect = easy_text.get_rect(center=(width // 2, height // 2 - 50))

hard_text = small_font.render("Сложный (мини-карта выключена)", True, black)
hard_rect = hard_text.get_rect(center=(width // 2, height // 2 + 50))

# Гравитация для частиц
gravity = 0.1  # Уменьшена гравитация для более плавного падения

# Загрузка изображения для частиц
def load_image(name, colorkey=None):
    fullname = os.path.join('sprite', name)
    if not os.path.isfile(fullname):
        print(f"Файл не найден: {fullname}")
        raise FileNotFoundError(f"Файл не найден: {fullname}")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

class Particle(pygame.sprite.Sprite):
    fire = [load_image("monstr.png")]
    for scale in (2, 3, 4):  # Уменьшены размеры частиц
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx * 0.5, dy * 0.5]  # Уменьшена скорость
        self.rect.x, self.rect.y = pos
        self.gravity = 0.1  # Уменьшена гравитация

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()

# Функция для создания частиц
def create_particles(position):
    particle_count = 5  # Уменьшено количество частиц
    numbers = range(-2, 3)  # Уменьшена скорость частиц
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

# Группа для спрайтов частиц
all_sprites = pygame.sprite.Group()

# Прямоугольник экрана для проверки выхода частиц за границы
screen_rect = (0, 0, width, height)

def save_time_to_file(elapsed_time, difficulty):
    data = {}
    if os.path.exists("game_time.txt"):
        try:
            with open("game_time.txt", "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}

    current_best = data.get(difficulty)
    if current_best is None or elapsed_time < current_best:
        data[difficulty] = int(elapsed_time)

    with open("game_time.txt", "w") as file:
        json.dump(data, file)

def get_best_time(difficulty):
    if os.path.exists("game_time.txt"):
        try:
            with open("game_time.txt", "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data.get(difficulty)
                else:
                    with open("game_time.txt", "w") as file:
                        json.dump({}, file)
                    return None
        except (json.JSONDecodeError, FileNotFoundError):
            with open("game_time.txt", "w") as file:
                json.dump({}, file)
            return None
    else:
        with open("game_time.txt", "w") as file:
            json.dump({}, file)
        return None

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


def main_menu():
    running = True
    difficulty = 'easy'
    show_minimap = True
    if os.path.isfile(music_path):
        play_music(music_path)
    else:
        print(f"Музыкальный файл не найден: {music_path}")
    # Создаем частицы постепенно
    particle_timer = 0
    particle_delay = 10  # Задержка между созданием частиц (в кадрах)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    print("Начало игры...")
                    return True, difficulty
                elif easy_rect.collidepoint(mouse_pos):
                    difficulty = 'easy'
                    show_minimap = True
                elif hard_rect.collidepoint(mouse_pos):
                    difficulty = 'hard'
                    show_minimap = False

        mouse_pos = pygame.mouse.get_pos()
        start_color = white if start_rect.collidepoint(mouse_pos) else gray
        easy_color = green if easy_rect.collidepoint(mouse_pos) else gray
        hard_color = red if hard_rect.collidepoint(mouse_pos) else gray

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(black)

        # Создаем частицы с задержкой
        particle_timer += 1
        if particle_timer >= particle_delay:
            create_particles((random.randint(0, width), 0))  # Частицы появляются сверху
            particle_timer = 0

        # Отрисовка частиц
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.draw.rect(screen, start_color, start_rect.inflate(20, 20))
        pygame.draw.rect(screen, easy_color, easy_rect.inflate(20, 10))
        pygame.draw.rect(screen, hard_color, hard_rect.inflate(20, 10))

        screen.blit(start_text, start_rect)
        screen.blit(easy_text, easy_rect)
        screen.blit(hard_text, hard_rect)

        best_time = get_best_time(difficulty)
        if best_time is not None:
            record_text = small_font.render(f"Рекорд ({difficulty}): {best_time} сек", True, white)
        else:
            record_text = small_font.render(f"Рекорд ({difficulty}): ---", True, white)
        screen.blit(record_text, (width - 300, 20))

        pygame.display.flip()
        clock.tick(50)  # Ограничение FPS для меню

def pause_menu():
    pygame.mouse.set_visible(True)
    pause_text = font.render("Пауза", True, white)
    resume_text = small_font.render("Нажмите ESC для продолжения", True, white)
    sc.blit(pause_text, (WIDTH // 2 - 100 + 50, HEIGHT // 2 - 50))
    sc.blit(resume_text, (WIDTH // 2 - 200 + 50, HEIGHT // 2 + 50))
    pygame.display.flip()

def game_loop(show_minimap, difficulty):
    pygame.mouse.set_visible(False)
    pygame.mixer.music.set_volume(0.2)
    start_time = time.time()
    paused = False
    pause_start_time = 0
    total_paused_time = 0

    player.reset()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pause_start_time = time.time()
                    else:
                        total_paused_time += time.time() - pause_start_time

        if not paused:
            pygame.mouse.set_visible(False)
            player.movement()
            sc.fill(BLACK)

            drawing.background(player.angle)
            walls = ray_casting_walls(player, drawing.textures)
            drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
            drawing.fps(clock)

            if show_minimap:
                drawing.mini_map(player)

            elapsed_time = time.time() - start_time - total_paused_time
            timer_text = f"Time: {int(elapsed_time)}s"
            timer_surface = font.render(timer_text, True, white)
            sc.blit(timer_surface, (10, 10))

            if player.x > 2915 and player.x < 2935 and player.y > 1939 and player.y < 1959:
                save_time_to_file(elapsed_time, difficulty)
                pygame.mouse.set_visible(True)
                return

            pygame.display.flip()
        else:
            pause_menu()

        clock.tick(FPS)

while True:
    start_game, difficulty = main_menu()
    if not start_game:
        break
    show_minimap = (difficulty == 'easy')
    game_loop(show_minimap, difficulty)