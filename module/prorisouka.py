import pygame
from .config import BLACK, TILE_SIZE, LEVEL
from .tank import Wall, Bush, Cloud, Player, EnemyTank

def create_level_objects_and_spawns():
    """Создание всех объектов уровня и поиск точек спавна"""
    walls = pygame.sprite.Group()
    bushes = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    # Точки спавна
    player_spawn = None
    enemy_spawns = []
    
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
            elif col == "t":  # Точка спавна игрока
                player_spawn = (pos_x, pos_y)
            elif col == "e":  # Точка спавна врага
                enemy_spawns.append((pos_x, pos_y))
    
    # Создаём игрока в точке спавна (если найдена)
    if player_spawn:
        player = Player(player_spawn[0], player_spawn[1])
    else:
        # Если точка спавна не найдена, используем старую позицию
        player = Player(TILE_SIZE * 2, TILE_SIZE * 13)
    
    # Создаём врагов в точках спавна
    for spawn_x, spawn_y in enemy_spawns:
        enemy = EnemyTank(spawn_x, spawn_y)
        enemies.add(enemy)
    
    return walls, bushes, clouds, player, enemies

def create_level_objects():
    """Старая функция для совместимости"""
    walls, bushes, clouds, player, enemies = create_level_objects_and_spawns()
    return walls, bushes, clouds

def render_game(screen, walls, bushes, clouds, player_group, enemies=None):
    """Отрисовка всех игровых объектов"""
    # Фон игрового поля (небесно-голубой для платформера)
    sky_color = (135, 206, 235)
    screen.fill(sky_color)
    
    # Отрисовка объектов в правильном порядке (задний план -> передний план)
    clouds.draw(screen)  # Облака на заднем плане
    walls.draw(screen)   # Стены
    bushes.draw(screen)  # Кустики поверх всего
    
    # Отрисовка врагов (если есть)
    if enemies:
        enemies.draw(screen)
    
    player_group.draw(screen)  # Игрок на переднем плане
    
    pygame.display.flip()

def initialize_display(width, height, caption):
    """Инициализация дисплея pygame"""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen