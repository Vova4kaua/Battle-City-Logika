import pygame

# --- Настройки экрана ---
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32
FPS = 60

# --- Физика ---
GRAVITY = 0.3  # Сила гравитации
MAX_FALL_SPEED = 8  # Максимальная скорость падения

# --- Цвета ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BRICK_COLOR = (200, 100, 50)
BUSH_COLOR = (34, 139, 34)
CLOUD_COLOR = (220, 220, 255)

# --- Пути к изображениям ---
TANK_IMAGE_PATH = "assets/src/tank_1.png"
WALL_IMAGE_PATH = "assets/src/wall.png"
BUSH_IMAGE_PATH = "assets/src/bush.png"
CLOUD_IMAGE_PATH = "assets/src/cloud.png"

# --- Карта уровня (боковой вид с гравитацией) ---
# w = камень (твёрдый блок)
# s = кустики (декорация, можно проходить сквозь)
# b = облако (платформа, на которой можно стоять, но можно пройти снизу)
# t = точка спавна игрока
# e = точка спавна врага
# пробел = воздух
LEVEL = [
    "wwwwwwwwwwwwwwwwwwww",
    "w                  w",
    "w                  w", 
    "w                  w",
    "w                  w",
    "w                  w",
    "w                  w",
    "w                  w",
    "w                  w",
    "wbbbbbbbb  bbbbbbbbw",
    "wws              sww",
    "wwws            swww",
    "wwwws          swwww",
    "wwwwwst       swwwww",
    "wwwwwwwwwwwwwwwwwwww"
]