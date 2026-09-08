import pygame
import math

WIDTH, HEIGHT = 1080, 720
COLOR = (255, 0, 0)
BG = (0, 0, 0)
ACC = 500          # pixels / s^2 (acceleration)
MAX_SPEED = 300    # pixels / s (top forward speed)
DRAG = 300         # pixels / s^2 (natural deceleration when no throttle)
TURN_SPEED = 180   # degrees / s (base turning rate)
FPS = 75

class Player:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.speed = 0.0
        self.w, self.h = 35, 15
        self.base_surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.base_surf, COLOR, self.base_surf.get_rect())
        

    def update(self, keys, dt):
        forward = pygame.math.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))
        
        # throttle/brake
        throttle = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            throttle += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            throttle -= 1

        # accelerate / brake (scalar)
        self.speed += throttle * ACC * dt

        # natural drag/braking toward zero (frame-rate independent)
        if self.speed > 0:
            self.speed = max(0.0, self.speed - DRAG * dt)
        elif self.speed < 0:
            self.speed = min(0.0, self.speed + DRAG * dt)

        # clamp speed
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        if self.speed < -MAX_SPEED:
            self.speed = -MAX_SPEED

        # steering (scale turn by speed fraction)
        steer = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            steer += 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            steer -= 1

        if abs(self.speed) > 0:
            self.angle += steer * TURN_SPEED * (abs(self.speed) / MAX_SPEED) * dt

        # compute velocity from heading and scalar speed, then integrate
        # forward = forward.normalize()
        self.vel = forward * self.speed
        self.pos += self.vel * dt

        # clamp to screen (same as before)
        self.pos.x = max(25, min(WIDTH - 25, self.pos.x))
        self.pos.y = max(12, min(HEIGHT - 12, self.pos.y))
        
    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.base_surf, self.angle)
        blit_rect = rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(rotated_image, blit_rect.topleft)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Demo Clean")
    clock = pygame.time.Clock()

    player = Player(WIDTH / 2, HEIGHT / 2)

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