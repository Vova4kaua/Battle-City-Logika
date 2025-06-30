import pygame
import sys
from module.config import WIDTH, HEIGHT, FPS, TILE_SIZE
from module.tank import Player
from module.tank_move import handle_input, update_player, update_enemies, handle_events
from module.prorisouka import create_level_objects_and_spawns, render_game, initialize_display

def main():
    # --- Инициализация ---
    pygame.init()
    screen = initialize_display(WIDTH, HEIGHT, "Battle Tank Platformer")
    clock = pygame.time.Clock()

    # --- Создание игровых объектов ---
    walls, bushes, clouds, player, enemies = create_level_objects_and_spawns()
    
    # Создаём группу для игрока
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
        update_enemies(enemies, walls, bushes, clouds)
        
        # --- Отрисовка ---
        render_game(screen, walls, bushes, clouds, player_group, enemies)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()