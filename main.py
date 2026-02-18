import pygame
import random
import sys

pygame.init()

# Configuración
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 150, 255)
BLACK = (15, 15, 35)

# Jugador
player_width = 60
player_height = 20
player = pygame.Rect(WIDTH//2 - 30, HEIGHT - 60, player_width, player_height)
player_speed = 6

# Variables globales
bullets = []
enemies = []
score = 0
lives = 3


# ================= FUNCIONES =================

def draw_text(text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    surface = font.render(text, True, WHITE)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def reset_game():
    global bullets, enemies, score, lives, player
    bullets = []
    enemies = []
    score = 0
    lives = 3
    player.x = WIDTH // 2 - 30


def show_menu():
    while True:
        screen.fill(BLACK)

        draw_text("SPACE SHOOTER", 60, WIDTH//2, HEIGHT//3)
        draw_text("Press ENTER to Start", 30, WIDTH//2, HEIGHT//2)
        draw_text("Press ESC to Exit", 25, WIDTH//2, HEIGHT//1.8)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def show_game_over():
    while True:
        screen.fill(BLACK)

        draw_text("GAME OVER", 60, WIDTH//2, HEIGHT//3)
        draw_text(f"Score: {score}", 40, WIDTH//2, HEIGHT//2)
        draw_text("Press ENTER to Restart", 30, WIDTH//2, HEIGHT//1.6)
        draw_text("Press M for Menu", 30, WIDTH//2, HEIGHT//1.45)
        draw_text("Press ESC to Exit", 25, WIDTH//2, HEIGHT//1.3)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    return "restart"

                if event.key == pygame.K_m:
                    reset_game()
                    return "menu"

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    enemy = pygame.Rect(x, -40, 40, 40)
    enemies.append(enemy)


def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= 8
        if bullet.y < 0:
            bullets.remove(bullet)


def move_enemies():
    global lives
    for enemy in enemies[:]:
        enemy.y += 4
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            lives -= 1


def check_collisions():
    global score
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break


# ================= INICIO =================

show_menu()

enemy_timer = 0
running = True

while running:
    clock.tick(60)
    screen.fill(BLACK)

    enemy_timer += 1
    if enemy_timer > 60:
        spawn_enemy()
        enemy_timer = 0

    # Movimiento jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player_width:
        player.x += player_speed

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 5, player.y, 10, 20)
                bullets.append(bullet)

    move_bullets()
    move_enemies()
    check_collisions()

    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, player)

    # Dibujar balas
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Dibujar enemigos
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # UI
    draw_text(f"Score: {score}", 25, 80, 30)
    draw_text(f"Lives: {lives}", 25, WIDTH - 80, 30)

    if lives <= 0:
        choice = show_game_over()

        if choice == "menu":
            show_menu()

        if choice == "restart":
            continue

    pygame.display.update()

pygame.quit()
