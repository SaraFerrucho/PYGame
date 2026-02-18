import pygame
import random
import sys

pygame.init()

# ================= Config =================

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter: Aesthetic Edition")
clock = pygame.time.Clock()

# ================= Paleta de Colores =================

COLOR_FONDO = (73, 53, 78)
COLOR_PLAYER = (0, 204, 238)
COLOR_ENEMY = (255, 158, 222)
COLOR_BULLET = (223, 205, 199)
COLOR_UI = (209, 219, 199)
COLOR_SHADOW = (40, 30, 45)

# ================= Fuentes =================

FONTS = {
    18: pygame.font.SysFont("verdana", 18, bold=True),
    20: pygame.font.SysFont("verdana", 20, bold=True),
    22: pygame.font.SysFont("verdana", 22, bold=True),
    25: pygame.font.SysFont("verdana", 25, bold=True),
    40: pygame.font.SysFont("verdana", 40, bold=True),
    45: pygame.font.SysFont("verdana", 45, bold=True),
    50: pygame.font.SysFont("verdana", 50, bold=True),
}

# ================= Estado de Juego =================

game_state = "menu"

# ================= Jugador =================

player_width = 60
player_height = 15
player = pygame.Rect(WIDTH//2 - 30, HEIGHT - 80, player_width, player_height)
player_speed = 7

# ================= Variables =================

bullets = []
enemies = []
score = 0
lives = 3
enemy_timer = 0

# ================= Estrellas =================

stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random() * 3] for _ in range(60)]

# ================= Funciones =================

def draw_text(text, size, x, y, color=COLOR_UI, shadow=True):
    font = FONTS[size]

    if shadow:
        shadow_surface = font.render(text, True, COLOR_SHADOW)
        shadow_rect = shadow_surface.get_rect(center=(x+3, y+3))
        screen.blit(shadow_surface, shadow_rect)

    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def draw_background():
    screen.fill(COLOR_FONDO)
    for star in stars:
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, (150, 140, 160), (int(star[0]), int(star[1])), 2)


def draw_ui_panel(rect):
    pygame.draw.rect(screen, COLOR_SHADOW,
                     (rect[0]+5, rect[1]+5, rect[2], rect[3]), border_radius=15)
    pygame.draw.rect(screen, COLOR_FONDO, rect, border_radius=15)
    pygame.draw.rect(screen, COLOR_UI, rect, 3, border_radius=15)


def reset_game():
    global bullets, enemies, score, lives
    bullets = []
    enemies = []
    score = 0
    lives = 3
    player.x = WIDTH // 2 - 30


def spawn_enemy():
    x = random.randint(30, WIDTH - 70)
    enemies.append(pygame.Rect(x, -50, 40, 40))


def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= 10
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
                score += 10
                break


# ================= Loop Principal =================

running = True

while running:
    clock.tick(60)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "playing"
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "playing":
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player.centerx - 4, player.y, 8, 20))

            elif game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "playing"
                if event.key == pygame.K_m:
                    game_state = "menu"

    # ================= Estados =================

    if game_state == "menu":

        panel = (WIDTH//2 - 200, HEIGHT//2 - 150, 400, 300)
        draw_ui_panel(panel)

        draw_text("SPACE SHOOTER", 40, WIDTH//2, HEIGHT//2 - 80, COLOR_PLAYER)
        draw_text("PRESS ENTER TO START", 22, WIDTH//2, HEIGHT//2 + 10)
        draw_text("ESC TO EXIT", 18, WIDTH//2, HEIGHT//2 + 60)

    elif game_state == "playing":

        enemy_timer += 1
        if enemy_timer > 50:
            spawn_enemy()
            enemy_timer = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_width:
            player.x += player_speed

        move_bullets()
        move_enemies()
        check_collisions()

        # balas
        for bullet in bullets:
            pygame.draw.rect(screen, COLOR_BULLET, bullet, border_radius=4)

        # enemigos
        for enemy in enemies:
            pygame.draw.rect(screen, COLOR_ENEMY, enemy, border_radius=10)
            pygame.draw.rect(screen, COLOR_SHADOW, enemy, 2, border_radius=10)

        # Jugador
        pygame.draw.rect(screen, COLOR_PLAYER, player, border_radius=3)
        pygame.draw.rect(screen, COLOR_PLAYER,
                         (player.centerx-10, player.y-10, 20, 15),
                         border_top_left_radius=10,
                         border_top_right_radius=10)

        # UI superior
        pygame.draw.rect(screen, COLOR_SHADOW, (0, 0, WIDTH, 60))
        pygame.draw.line(screen, COLOR_UI, (0, 60), (WIDTH, 60), 2)

        draw_text(f"SCORE: {score}", 25, 100, 30)
        draw_text(f"LIVES: {lives}", 25, WIDTH - 100, 30,
                  COLOR_ENEMY if lives == 1 else COLOR_UI)

        if lives <= 0:
            game_state = "game_over"

    elif game_state == "game_over":

        panel = (WIDTH//2 - 180, HEIGHT//2 - 180, 360, 360)
        draw_ui_panel(panel)

        draw_text("MISSION OVER", 40, WIDTH//2, HEIGHT//2 - 100, COLOR_ENEMY)
        draw_text(f"SCORE: {score}", 50, WIDTH//2, HEIGHT//2 - 20, COLOR_PLAYER)
        draw_text("PRESS ENTER TO RESTART", 20, WIDTH//2, HEIGHT//2 + 60)
        draw_text("PRESS M FOR MENU", 20, WIDTH//2, HEIGHT//2 + 100)

    pygame.display.update()

pygame.quit()
sys.exit()
