import pygame

def handle_input():
    """Обработка ввода с клавиатуры"""
    keys = pygame.key.get_pressed()
    return keys

def update_player(player, keys, walls, bushes, clouds):
    """Обновление позиции игрока"""
    player.update(keys, walls, bushes, clouds)

def update_enemies(enemies, walls, bushes, clouds):
    """Обновление всех вражеских танков"""
    for enemy in enemies:
        enemy.update(walls, bushes, clouds)

def handle_events():
    """Обработка событий pygame"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True