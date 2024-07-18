# filename: pong_game.py
import pygame
import random

# Initialize pygame
pygame.init()

# Set up game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define paddle and ball properties
paddle_width, paddle_height = 10, 100
ball_size = 15
ball_speed = [3, 3]
paddle_speed = 5

# Initial positions
left_paddle = pygame.Rect(30, 250, paddle_width, paddle_height)
right_paddle = pygame.Rect(760, 250, paddle_width, paddle_height)
ball = pygame.Rect(400, 300, ball_size, ball_size)

# Scoring
left_score, right_score = 0, 0
font = pygame.font.Font(None, 74)

# Start game flag
game_started = False

# Game loop control
running = True
clock = pygame.time.Clock()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True
    
    if game_started:
        # Handle key presses for paddle movement
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < 600:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < 600:
            right_paddle.y += paddle_speed
        
        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= 600:
            ball_speed[1] = -ball_speed[1]
        
        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]
        
        # Scoring
        if ball.left <= 0:
            right_score += 1
            ball.center = (400, 300)
            ball_speed = [random.choice([3, -3]), random.choice([3, -3])]
            game_started = False
        if ball.right >= 800:
            left_score += 1
            ball.center = (400, 300)
            ball_speed = [random.choice([3, -3]), random.choice([3, -3])]
            game_started = False
        
        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (400, 0), (400, 600))
        
        left_text = font.render(str(left_score), True, WHITE)
        screen.blit(left_text, (320, 10))
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(right_text, (420, 10))
    else:
        title_font = pygame.font.Font(None, 40)
        title = title_font.render("Press SPACE to Start", True, WHITE)
        screen.fill(BLACK)
        screen.blit(title, (260, 250))
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()