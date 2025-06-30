# prorisouka.py - Прорисовка игры с новыми блоками

import pygame
from .config import BLACK, TILE_SIZE, LEVEL
from .tank import Wall, Bush, Cloud

def create_level_objects():
    """Создание всех объектов уровня на основе карты"""
    walls = pygame.sprite.Group()
    bushes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    
    for y, row in enumerate(LEVEL):
        for x, col in enumerate(row):
            pos_x = x * TILE_SIZE
            pos_y = y * TILE_SIZE
            
            if col == "w":  # Кирпичная стена
                wall = Wall(pos_x, pos_y)
                walls.add(wall)
            elif col == "s":  # Кустики
                bush = Bush(pos_x, pos_y)
                bushes.add(bush)
            elif col == "b":  # Облачная платформа
                cloud = Cloud(pos_x, pos_y)
                clouds.add(cloud)
    
    return walls, bushes, clouds

def render_game(screen, walls, bushes, clouds, player_group):
    """Отрисовка всех игровых объектов"""
    # Фон игрового поля (небесно-голубой для платформера)
    sky_color = (135, 206, 235)
    screen.fill(sky_color)
    
    # Отрисовка объектов в правильном порядке (задний план -> передний план)
    clouds.draw(screen)  # Облака на заднем плане
    walls.draw(screen)   # Стены
    bushes.draw(screen)  # Кустики поверх всего
    player_group.draw(screen)  # Игрок на переднем плане
    
    pygame.display.flip()

def initialize_display(width, height, caption):
    """Инициализация дисплея pygame"""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen