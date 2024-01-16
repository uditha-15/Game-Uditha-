import pygame
import sys
import random
import time


pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

background_img = pygame.image.load('background.jpeg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

spaceship_img = pygame.image.load('spaceship.png')
spaceship_img = pygame.transform.scale(spaceship_img, (80, 60))  

play_button_img = pygame.image.load('play_button.png')
play_button_img = pygame.transform.scale(play_button_img, (150, 50))

restart_button_img = pygame.image.load('restart_button.png')
restart_button_img = pygame.transform.scale(restart_button_img, (150, 50))

alien_img = pygame.image.load('alien.png')
alien_img = pygame.transform.scale(alien_img, (50, 40))

bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (5, 15))

spaceship_rect = spaceship_img.get_rect()
alien_width, alien_height = 40, 30
bullet_width, bullet_height = 5, 15
spaceship_speed = 8
bullet_speed = 10
alien_speed = 5

spaceship_rect.topleft = (WIDTH // 2 - spaceship_rect.width // 2, HEIGHT - 50)

aliens = []
bullets = []

score = 0
score_font = pygame.font.Font(None, 36)  # Choose a font and font size
start_time = time.time()

game_over = False
show_instructions = True

def draw_game_over():
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 20))

    screen.blit(restart_button_img, (WIDTH // 2 - 75, HEIGHT // 2 + 100))

def draw_instructions():
    instructions_font = pygame.font.Font(None, 36)
    welcome_text = instructions_font.render("Welcome to Space Invaders!", True, WHITE)
    instructions_text1 = instructions_font.render("Instructions:", True, WHITE)
    instructions_text2 = instructions_font.render("Use LEFT and RIGHT arrow keys to move the spaceship.", True, WHITE)
    instructions_text3 = instructions_font.render("Press SPACE to shoot bullets.", True, WHITE)
    instructions_text4 = instructions_font.render("Avoid aliens reaching the spaceship.", True, WHITE)
    instructions_text5 = instructions_font.render("Click PLAY to start.", True, WHITE)

    text_width = max(welcome_text.get_width(), instructions_text1.get_width(), instructions_text2.get_width(),
                     instructions_text3.get_width(), instructions_text4.get_width(), instructions_text5.get_width())
    text_x = (WIDTH - text_width) // 2

    screen.blit(welcome_text, (text_x, HEIGHT // 2 - 130))
    screen.blit(instructions_text1, (text_x, HEIGHT // 2 - 100))
    screen.blit(instructions_text2, (text_x, HEIGHT // 2 - 70))
    screen.blit(instructions_text3, (text_x, HEIGHT // 2 - 40))
    screen.blit(instructions_text4, (text_x, HEIGHT // 2 - 10))
    screen.blit(instructions_text5, (text_x, HEIGHT // 2 + 20))

    screen.blit(play_button_img, (WIDTH // 2 - 75, HEIGHT // 2 + 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if not game_over:
        screen.blit(background_img, (0, 0))

        if show_instructions:
            draw_instructions()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
            if button_rect.collidepoint(mouse_x, mouse_y):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        show_instructions = False

        else:
            if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
                spaceship_rect.x -= spaceship_speed
            if keys[pygame.K_RIGHT] and spaceship_rect.right < WIDTH:
                spaceship_rect.x += spaceship_speed

            if keys[pygame.K_SPACE]:
                bullet = pygame.Rect(spaceship_rect.centerx - bullet_width // 2, spaceship_rect.top - bullet_height,
                                    bullet_width, bullet_height)
                bullets.append(bullet)
            for bullet in bullets:
                bullet.y -= bullet_speed
                if bullet.colliderect(spaceship_rect):
                    bullets.remove(bullet)
                for alien in aliens:
                    if bullet.colliderect(alien):
                        bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 10  

            for alien in aliens:
                alien.y += alien_speed
                if alien.top > HEIGHT:
                    aliens.remove(alien)
                    
            if random.random() < 0.02:
                new_alien = pygame.Rect(random.randint(0, WIDTH - alien_width), 0, alien_width, alien_height)
                aliens.append(new_alien)

            for alien in aliens:
                if alien.colliderect(spaceship_rect):
                    game_over = True
                    
            screen.blit(spaceship_img, spaceship_rect.topleft)

            for alien in aliens:
                screen.blit(alien_img, alien.topleft)

            for bullet in bullets:
                screen.blit(bullet_img, bullet.topleft)

            elapsed_time = time.time() - start_time
            score_text = score_font.render(f"Score: {score} | Time: {int(elapsed_time)}s", True, WHITE)
            screen.blit(score_text, (10, 10))

    else:
        screen.blit(background_img, (0, 0))
        draw_game_over()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
        if button_rect.collidepoint(mouse_x, mouse_y):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = False
                    show_instructions = True
                    spaceships = []
                    bullets = []
                    aliens = []
                    score = 0
                    start_time = time.time()

    pygame.display.flip()
    clock.tick(FPS)
