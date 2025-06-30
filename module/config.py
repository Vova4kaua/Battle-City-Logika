# config.py - Конфигурация игры

import pygame

# --- Настройки экрана ---
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32
FPS = 60

# --- Физика ---
GRAVITY = 0.3  # Уменьшенная сила гравитации для более контролируемого движения
MAX_FALL_SPEED = 6  # Уменьшенная максимальная скорость падения

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
TANK_IMAGE_PATH = "images/tank.png"
WALL_IMAGE_PATH = "images/wall.png"
BUSH_IMAGE_PATH = "images/bush.png"
CLOUD_IMAGE_PATH = "images/cloud.png"

# --- Карта уровня (боковой вид с гравитацией) ---
# w = кирпич (твёрдый блок)
# s = кустики (декорация, можно проходить сквозь)
# b = облако (платформа, на которой можно стоять, но можно пройти снизу)
# пробел = воздух
LEVEL = [
    "wwwwwwwwwwwwwwwwwwww",
    "w                  w",
    "w  bb        bb    w", 
    "w  ss        ss    w",
    "w                  w",
    "w    wwwwwwww      w",
    "w           w      w",
    "w    s      w   bb w",
    "w    s      w   ss w",
    "w    wwwwwwww      w",
    "w                  w",
    "w  bb        bb    w",
    "w  ss        ss    w",
    "w                  w",
    "wwwwwwwwwwwwwwwwwwww"
]