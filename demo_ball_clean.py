import pygame

WIDTH, HEIGHT = 800, 600
RADIUS = 25
COLOR = (255, 0, 0)
BG = (0, 0, 0)
SPEED = 300  # pixels per second
FPS = 60

class Player:
    def __init__(self, x, y, radius):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = radius

    def update(self, keys, dt):
        vel = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vel.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vel.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vel.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vel.x = 1
        if vel.length_squared() > 0:
            vel = vel.normalize()
        self.pos += vel * SPEED * dt
        # clamp to screen
        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR, (int(self.pos.x), int(self.pos.y)), self.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Demo Clean")
    clock = pygame.time.Clock()

    player = Player(WIDTH / 2, HEIGHT / 2, RADIUS)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys, dt)

        screen.fill(BG)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()