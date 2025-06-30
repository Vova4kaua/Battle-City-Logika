# tank.py - Класс танка игрока с гравитацией (исправлен автоподъём)

import pygame
import os
from .config import (TILE_SIZE, GREEN, TANK_IMAGE_PATH, WALL_IMAGE_PATH, 
                     BRICK_COLOR, BUSH_COLOR, CLOUD_COLOR, GRAVITY, MAX_FALL_SPEED, BUSH_IMAGE_PATH, CLOUD_IMAGE_PATH)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.direction = 'RIGHT'
        
        # Физика
        self.velocity_x = 0
        self.velocity_y = 1  # Начинаем с небольшой скорости падения
        self.on_ground = False
        self.can_jump = True
        
        # Попытка загрузить изображение танка
        try:
            self.original_image = pygame.image.load(TANK_IMAGE_PATH)
            self.original_image = pygame.transform.scale(self.original_image, (TILE_SIZE, TILE_SIZE))
        except:
            # Создаем танк в боковом виде
            self.original_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.original_image.fill((0, 0, 0, 0))
            
            # Корпус танка
            pygame.draw.rect(self.original_image, (0, 150, 0), (6, 12, 20, 12))
            # Башня танка
            pygame.draw.rect(self.original_image, (0, 180, 0), (10, 8, 12, 10))
            # Дуло танка
            pygame.draw.rect(self.original_image, (0, 120, 0), (22, 11, 8, 3))
            # Нижняя гусеница
            pygame.draw.rect(self.original_image, (60, 60, 60), (4, 22, 24, 4))
            # Верхняя гусеница
            pygame.draw.rect(self.original_image, (60, 60, 60), (4, 6, 24, 4))
            
            # Колёса гусениц
            for i in range(6, 26, 4):
                pygame.draw.circle(self.original_image, (40, 40, 40), (i, 24), 2)
                pygame.draw.circle(self.original_image, (40, 40, 40), (i, 8), 2)
            
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def update(self, keys, walls, bushes, clouds):
        # Обработка горизонтального движения
        self.velocity_x = 0
        new_direction = self.direction
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            new_direction = 'LEFT'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            new_direction = 'RIGHT'
        
        # Прыжок
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground and self.can_jump:
            self.velocity_y = -6  # Уменьшенная сила прыжка
            self.on_ground = False
            self.can_jump = False
        
        # Отпускание клавиши прыжка
        if not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]):
            self.can_jump = True

        # Поворот танка
        if new_direction != self.direction:
            self.direction = new_direction
            self.rotate_tank()

        # Применение гравитации (постоянно действует)
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # Горизонтальное движение БЕЗ автоподъёма
        if self.velocity_x != 0:
            new_x = self.rect.x + self.velocity_x
            temp_rect = pygame.Rect(new_x, self.rect.y, self.rect.width, self.rect.height)
            
            # Проверка коллизий с твёрдыми блоками
            collision = False
            
            for wall in walls:
                if temp_rect.colliderect(wall.rect):
                    collision = True
                    break
            
            # Обычное движение, если нет коллизии и в пределах экрана
            if not collision and 0 <= new_x <= 640 - TILE_SIZE:
                self.rect.x = new_x

        # Вертикальное движение
        new_y = self.rect.y + self.velocity_y
        temp_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
        
        # Проверка на границы экрана
        if new_y < 0:
            new_y = 0
            self.velocity_y = 0
        elif new_y > 480 - TILE_SIZE:
            new_y = 480 - TILE_SIZE
            self.velocity_y = 0
            self.on_ground = True

        # Проверка коллизий с твёрдыми блоками (стены)
        temp_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
        collision_wall = False
        
        for wall in walls:
            if temp_rect.colliderect(wall.rect):
                collision_wall = True
                if self.velocity_y > 0:  # Падение вниз
                    new_y = wall.rect.top - self.rect.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # Прыжок вверх
                    new_y = wall.rect.bottom
                    self.velocity_y = 0
                break
        
        # Проверка коллизий с облаками (платформы)
        if not collision_wall:
            temp_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
            
            for cloud in clouds:
                if temp_rect.colliderect(cloud.rect):
                    # Облака работают как платформы - можно стоять сверху, но проходить снизу
                    if self.velocity_y > 0 and self.rect.bottom <= cloud.rect.top + 5:
                        new_y = cloud.rect.top - self.rect.height
                        self.velocity_y = 0
                        self.on_ground = True
                        break

        # Применение движения
        self.rect.y = new_y
        
        # Проверка на земле ли танк (более точная проверка)
        self.on_ground = False
        
        # Проверяем, стоит ли танк на твёрдой поверхности
        ground_check_rect = pygame.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height)
        
        for wall in walls:
            if ground_check_rect.colliderect(wall.rect):
                self.on_ground = True
                break
        
        if not self.on_ground:
            for cloud in clouds:
                if ground_check_rect.colliderect(cloud.rect) and self.velocity_y >= 0:
                    self.on_ground = True
                    break
        
        # Проверка на дно экрана
        if self.rect.bottom >= 480:
            self.on_ground = True
    
    def rotate_tank(self):
        """Поворот танка только влево/вправо"""
        if self.direction == 'RIGHT':
            self.image = self.original_image
        elif self.direction == 'LEFT':
            self.image = pygame.transform.flip(self.original_image, True, False)

class Wall(pygame.sprite.Sprite):
    """Твёрдый кирпичный блок"""
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load(WALL_IMAGE_PATH)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(BRICK_COLOR)
            
            dark_brick = (120, 60, 30)
            light_brick = (180, 90, 45)
            mortar = (100, 50, 25)
            
            self.image.fill(mortar)
            
            brick_height = 6
            brick_width = 14
            
            for row in range(0, TILE_SIZE, brick_height + 2):
                for col in range(0, TILE_SIZE, brick_width + 2):
                    offset = (brick_width // 2 + 1) if (row // (brick_height + 2)) % 2 else 0
                    brick_x = (col + offset) % TILE_SIZE
                    
                    if brick_x + brick_width <= TILE_SIZE and row + brick_height <= TILE_SIZE:
                        pygame.draw.rect(self.image, light_brick, 
                                       (brick_x, row, brick_width, brick_height))
                        pygame.draw.rect(self.image, dark_brick, 
                                       (brick_x, row, brick_width, brick_height), 1)
                        pygame.draw.line(self.image, (220, 110, 55), 
                                       (brick_x, row), (brick_x + brick_width - 1, row))
                        pygame.draw.line(self.image, (220, 110, 55), 
                                       (brick_x, row), (brick_x, row + brick_height - 1))
            
        self.rect = self.image.get_rect(topleft=(x, y))

class Bush(pygame.sprite.Sprite):
    """Декоративные кустики - можно проходить сквозь"""
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load(BUSH_IMAGE_PATH)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((0, 0, 0, 0))  # Прозрачный фон
            
            # Рисуем кустик
            bush_dark = (20, 100, 20)
            bush_light = (50, 150, 50)
            
            # Основа кустика
            pygame.draw.ellipse(self.image, bush_dark, (4, 16, 24, 16))
            pygame.draw.ellipse(self.image, bush_light, (6, 18, 20, 12))
            
            # Листики
            for i in range(3):
                for j in range(2):
                    x_pos = 8 + i * 6
                    y_pos = 20 + j * 4
                    pygame.draw.circle(self.image, bush_light, (x_pos, y_pos), 3)
                    pygame.draw.circle(self.image, bush_dark, (x_pos, y_pos), 3, 1)
            
        self.rect = self.image.get_rect(topleft=(x, y))

class Cloud(pygame.sprite.Sprite):
    """Облачная платформа - можно стоять сверху, проходить снизу"""
    def __init__(self, x, y):
        super().__init__()
        
        try:
            self.image = pygame.image.load(CLOUD_IMAGE_PATH)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((0, 0, 0, 0))  # Прозрачный фон
            
            # Рисуем облако
            cloud_color = CLOUD_COLOR
            cloud_shadow = (180, 180, 220)
            
            # Основа облака
            pygame.draw.ellipse(self.image, cloud_shadow, (2, 12, 28, 12))
            pygame.draw.ellipse(self.image, cloud_color, (4, 10, 24, 12))
            
            # Пушистые части облака
            pygame.draw.circle(self.image, cloud_color, (8, 16), 6)
            pygame.draw.circle(self.image, cloud_color, (16, 14), 7)
            pygame.draw.circle(self.image, cloud_color, (24, 16), 6)
            
            # Тени для объёма
            pygame.draw.circle(self.image, cloud_shadow, (8, 18), 4)
            pygame.draw.circle(self.image, cloud_shadow, (16, 16), 5)
            pygame.draw.circle(self.image, cloud_shadow, (24, 18), 4)
            
        self.rect = self.image.get_rect(topleft=(x, y))