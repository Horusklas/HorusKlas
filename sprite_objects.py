import pygame
from settings import *
from player import *
from collections import deque
from map import demon_indices
import math


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_devil': {
                'sprite': [pygame.image.load(f'sprite/devil/stat/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.5,
                'animation': deque(
                    [pygame.image.load(f'sprite/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 200,
                'animation_speed': 10,
                'blocked': True,
            },
        }

        self.list_of_objects = [

        ]

        for i in demon_indices.values():
            self.list_of_objects.append(SpriteObject(self.sprite_parameters['sprite_devil'], (i[1] + 0.5, i[0] + 0.5)))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']  # Коллизия спрайта
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        self.animation_played = 0  # Счетчик проигранных анимаций
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            # Выбор спрайта для угла
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                # Выбор правильного спрайта из списка
                sprite_index = int(theta / 45) % len(self.object)
                sprite_object = self.object[sprite_index]
            else:
                sprite_object = self.object

            # Анимация спрайта
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
                    self.animation_played += 1  # Увеличиваем счетчик проигранных анимаций

            # Если анимация проиграна два раза, отключаем коллизию
            if self.animation_played >= 18:
                self.blocked = False  # Отключаем коллизию
                return (False,)  # Спрайт больше не отображается

            # Масштабирование и позиционирование спрайта
            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)