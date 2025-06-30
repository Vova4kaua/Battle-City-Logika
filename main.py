# main.py - Главный файл игры-платформера

import pygame
import sys
from module.config import WIDTH, HEIGHT, FPS, TILE_SIZE
from module.tank import Player
from module.tank_move import handle_input, update_player, handle_events
from module.prorisouka import create_level_objects, render_game, initialize_display

def main():
    # --- Инициализация ---
    pygame.init()
    screen = initialize_display(WIDTH, HEIGHT, "Battle Tank Platformer")
    clock = pygame.time.Clock()

    # --- Создание игровых объектов ---
    walls, bushes, clouds = create_level_objects()
    
    # Найдём хорошую стартовую позицию (где есть твёрдая земля)
    start_x = TILE_SIZE * 2
    start_y = TILE_SIZE * 13  # Ближе к низу, чтобы танк упал на платформу
    
    player = Player(start_x, start_y)
    player_group = pygame.sprite.GroupSingle(player)

    # --- Игровой цикл ---
    running = True
    while running:
        clock.tick(FPS)
        
        # --- Обработка событий ---
        running = handle_events()
        
        # --- Обработка ввода ---
        keys = handle_input()
        
        # --- Обновление ---
        update_player(player, keys, walls, bushes, clouds)
        
        # --- Отрисовка ---
        render_game(screen, walls, bushes, clouds, player_group)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()