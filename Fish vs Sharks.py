import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish vs Sharks")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

# Colors
OCEAN_BLUE = (10, 40, 120)
WHITE = (255, 255, 255)
FISH_COLOR = (255, 200, 50)
SHARK_COLOR = (180, 180, 180)
BULLET_COLOR = (255, 80, 80)

# Player (Fish)
player_width, player_height = 60, 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 3          # was 6

# Bullet
bullet_width, bullet_height = 6, 16
bullet_speed = 5          # was 10
bullets = []  # list of rects

# Enemy (Shark)
enemy_width, enemy_height = 70, 40
enemies = []
enemy_base_speed = 1      # was 2
enemy_spawn_delay = 2000  # ms, was 1000
last_spawn_time = pygame.time.get_ticks()

# Game state
score = 0
running = True

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = -enemy_height  # start just above the screen
    # speed increases with score, but more gradually
    speed = enemy_base_speed + score * 0.03
    enemies.append({"rect": pygame.Rect(x, y, enemy_width, enemy_height),
                    "speed": speed})

def draw_background():
    screen.fill(OCEAN_BLUE)
    # simple wave lines for ocean feel
    for i in range(0, HEIGHT, 40):
        pygame.draw.arc(screen, (20, 80, 180), (0, i, WIDTH, 80), 0, 3.14, 2)

def draw_fish(x, y, w, h, color):
    cx, cy = x + w // 2, y + h // 2
    # Body
    pygame.draw.ellipse(screen, color, (x + w // 5, y + h // 6, w * 3 // 5, h * 2 // 3))
    # Tail (triangle pointing left)
    tail_pts = [
        (x + w // 5, cy),
        (x, y + h // 6),
        (x, y + h * 5 // 6),
    ]
    pygame.draw.polygon(screen, color, tail_pts)
    # Eye
    eye_x = x + w * 3 // 5
    eye_y = y + h // 3
    pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 5)
    pygame.draw.circle(screen, (0, 0, 0), (eye_x + 1, eye_y), 3)
    # Top fin
    fin_pts = [
        (cx - 5, y + h // 4),
        (cx + 5, y + h // 4),
        (cx, y),
    ]
    pygame.draw.polygon(screen, (200, 150, 30), fin_pts)

def draw_player():
    draw_fish(player_x, player_y, player_width, player_height, FISH_COLOR)

def draw_bullets():
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b)

def draw_shark(x, y, w, h):
    cx = x + w // 2
    # Body
    pygame.draw.ellipse(screen, SHARK_COLOR, (x + w // 6, y + h // 4, w * 2 // 3, h // 2))
    # Snout pointing downward
    snout_pts = [
        (x + w // 3, y + h * 3 // 4),
        (x + w * 2 // 3, y + h * 3 // 4),
        (cx, y + h),
    ]
    pygame.draw.polygon(screen, SHARK_COLOR, snout_pts)
    # Tail fin at top
    tail_pts = [
        (x + w // 6, y + h // 2),
        (x, y),
        (x + w // 4, y + h // 3),
    ]
    pygame.draw.polygon(screen, SHARK_COLOR, tail_pts)
    # Dorsal fin
    fin_pts = [
        (cx - 6, y + h // 4),
        (cx + 6, y + h // 4),
        (cx - 2, y - h // 4),
    ]
    pygame.draw.polygon(screen, SHARK_COLOR, fin_pts)
    # Eye
    eye_x = x + w * 5 // 8
    eye_y = y + h * 2 // 5
    pygame.draw.circle(screen, (20, 20, 20), (eye_x, eye_y), 4)
    pygame.draw.circle(screen, WHITE, (eye_x - 1, eye_y - 1), 2)
    # Belly
    pygame.draw.ellipse(screen, (210, 210, 210),
                        (x + w // 4, y + h * 2 // 5, w // 2, h // 5))

def draw_enemies():
    for e in enemies:
        r = e["rect"]
        draw_shark(r.x, r.y, r.width, r.height)

def draw_score():
    text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def handle_player_movement(keys):
    global player_x
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    # keep on screen
    player_x = max(0, min(WIDTH - player_width, player_x))

def shoot_bullet():
    # bullet from center top of fish
    bx = player_x + player_width // 2 - bullet_width // 2
    by = player_y
    bullets.append(pygame.Rect(bx, by, bullet_width, bullet_height))

def update_bullets():
    global bullets
    for b in bullets:
        b.y -= bullet_speed
    bullets = [b for b in bullets if b.bottom > 0]

def update_enemies():
    global running
    for e in enemies:
        e["rect"].y += e["speed"]

        # if shark reaches fish level → game over
        if e["rect"].bottom >= player_y + player_height // 2:
            running = False

def check_collisions():
    global score, enemies, bullets
    new_enemies = []
    for e in enemies:
        hit = False
        for b in bullets:
            if e["rect"].colliderect(b):
                hit = True
                score += 10  # scoring per shark
                bullets.remove(b)
                break
        if not hit:
            new_enemies.append(e)
    enemies = new_enemies

# Main loop
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shoot_bullet()

    keys = pygame.key.get_pressed()
    handle_player_movement(keys)

    # Spawn enemies over time (slightly faster as score increases, but gentler)
    now = pygame.time.get_ticks()
    dynamic_delay = max(800, enemy_spawn_delay - score * 10)  # was max(300, ... - score*20)
    if now - last_spawn_time > dynamic_delay and len(enemies) < 10:
        spawn_enemy()
        last_spawn_time = now

    update_bullets()
    update_enemies()
    check_collisions()

    # Draw
    draw_background()
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_score()

    pygame.display.flip()

# Simple game over screen
screen.fill(OCEAN_BLUE)
msg = FONT.render(f"Game Over! Final Score: {score}", True, WHITE)
screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2,
                  HEIGHT // 2 - msg.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
