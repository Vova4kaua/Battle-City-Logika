# tank_move.py - Логика движения танка с гравитацией

import pygame

def handle_input():
    """Обработка ввода с клавиатуры"""
    keys = pygame.key.get_pressed()
    return keys

def update_player(player, keys, walls, bushes, clouds):
    """Обновление позиции игрока с учётом новых блоков"""
    player.update(keys, walls, bushes, clouds)

def handle_events():
    """Обработка событий pygame"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True