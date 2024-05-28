import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Stałe
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
BULLET_SPEED = 7
CHICKEN_SPEED = 3

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ustawienie okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Strzelanie do Kur")

# Wczytywanie obrazków
player_image = pygame.image.load('assets/player.png')
chicken_image = pygame.image.load('assets/chicken.png')
woman_image = pygame.image.load('assets/woman.png')
man_image = pygame.image.load('assets/man.png')
machine_image = pygame.image.load('assets/machine.png')
bullet_image = pygame.image.load('assets/bullet.png')
background_image = pygame.image.load('assets/background.png')

# Klasa Gracza
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Klasa Kury
class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = chicken_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = CHICKEN_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Klasa Pocisku
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Inicjalizacja grup sprite'ów
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
chickens = pygame.sprite.Group()

# Utworzenie obiektów
player = Player()
all_sprites.add(player)

for _ in range(8):
    chicken = Chicken()
    all_sprites.add(chicken)
    chickens.add(chicken)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # Sprawdzanie kolizji
    hits = pygame.sprite.groupcollide(chickens, bullets, True, True)
    for hit in hits:
        chicken = Chicken()
        all_sprites.add(chicken)
        chickens.add(chicken)

    # Rysowanie
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
