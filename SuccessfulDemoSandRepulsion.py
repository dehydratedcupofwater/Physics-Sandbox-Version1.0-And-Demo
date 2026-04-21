import pygame
import random
import math

# (IMPORTS ABOVE THIS LINE REMEMBER)
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Qusay's Sand Code Test")
clock = pygame.time.Clock()

# Actual particle settings and class
class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
    
    def update(self, mouse_x, mouse_y):
        # Distance to mouse
        dx = self.x - mouse_x
        dy = self.y - mouse_y
        dist = math.hypot(dx, dy)
        
        # How far ts is repelled
        if dist < 100 and dist > 0:
            force = (100 - dist) / 100
            angle = math.atan2(dy, dx)
            self.vx += math.cos(angle) * force * 2
            self.vy += math.sin(angle) * force * 2
        
        # Drift settings
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)
        
        # Friction settings
        self.vx *= 0.95
        self.vy *= 0.95
        
        # Move
        self.x += self.vx
        self.y += self.vy
        
        # Bounce walls
        if self.x < 0: self.x = 0; self.vx *= -0.5
        if self.x > WIDTH: self.x = WIDTH; self.vx *= -0.5
        if self.y < 0: self.y = 0; self.vy *= -0.5
        if self.y > HEIGHT: self.y = HEIGHT; self.vy *= -0.5
    
    def draw(self, surface):
        # Sand color (warm tan/gold)
        shade = random.randint(180, 255)
        color = (shade, int(shade * 0.8), 100)
        pygame.draw.rect(surface, color, (self.x, self.y, 2, 2))

# Particle numbers
particles = [Particle() for _ in range(2500)]

# Main loop
running = True
mouse_x, mouse_y = -1000, -1000

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
    
    # Fade effect aka the trail effect
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(40)
    fade.fill((0, 0, 0))
    screen.blit(fade, (0, 0))
    
    # Update and draw
    for p in particles:
        p.update(mouse_x, mouse_y)
        p.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()