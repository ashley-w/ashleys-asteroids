import pygame
import random
from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.5, 2.0)
        self.twinkle_timer = 0
        
    def update(self, dt):
        # Slow twinkling effect
        self.twinkle_timer += dt * self.twinkle_speed
        
    def draw(self, screen):
        # Calculate twinkling brightness
        twinkle = (1 + 0.3 * (1 + pygame.math.Vector2(1, 0).rotate(self.twinkle_timer * 180).x)) / 2
        alpha = int(255 * self.brightness * twinkle)
        
        # Draw star as a small dot
        color = (alpha, alpha, alpha)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 1, 0)

class Starfield:
    def __init__(self):
        self.stars = []
        # Create lots of stars for a dense field
        for _ in range(150):
            self.stars.append(Star())
            
    def update(self, dt):
        for star in self.stars:
            star.update(dt)
            
    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)