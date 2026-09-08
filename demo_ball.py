import pygame

# Initialize Pygame
pygame.init()

size = width, height = 800, 600
red = 255, 0, 0

# Set up the game window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hello Pygame")


playerRect = pygame.draw.circle(screen, red, (width // 2, height // 2), 25)

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        playerRect.move_ip(0, -1)
    if keys[pygame.K_s]:
        playerRect.move_ip(0, 1)
    if keys[pygame.K_a]:
        playerRect.move_ip(-1, 0)
    if keys[pygame.K_d]:
        playerRect.move_ip(1, 0)
        
    pygame.draw.circle(screen, red, playerRect.center, 25)
    pygame.display.flip()

# Quit Pygame
pygame.quit()