import pygame
import sys

# --- Налаштування ---
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 40
FPS = 60

# --- Ініціалізація ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

# --- Кольори ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)

# --- Клас гравця ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

    def update(self, keys, walls):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Перевірка на стіни
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x -= dx
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.y -= dy

# --- Клас стіни ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Побудова мапи ---
level = [
    "WWWWWWWWWWWW",
    "W          W",
    "W   WW     W",
    "W          W",
    "W     W    W",
    "W          W",
    "WWWWWWWWWWWW"
]

walls = pygame.sprite.Group()
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == "W":
            wall = Wall(x * TILE_SIZE, y * TILE_SIZE)
            walls.add(wall)

# --- Створення гравця ---
player = Player(60, 60)
player_group = pygame.sprite.GroupSingle(player)

# --- Ігровий цикл ---
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення
    player.update(keys, walls)

    # Відображення
    screen.fill(BLACK)
    walls.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
