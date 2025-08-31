import pygame
import random
import math
from src.core.circleshape import CircleShape
from src.core.constants import NEON_GREEN, NEON_PURPLE, ELECTRIC_BLUE, NEON_PINK

class Powerup(CircleShape):
    TYPES = {
        "rapid_fire": {"color": NEON_GREEN, "symbol": "R"},
        "spread_shot": {"color": NEON_PURPLE, "symbol": "S"}, 
        "piercing": {"color": ELECTRIC_BLUE, "symbol": "P"},
        "big_shot": {"color": NEON_PINK, "symbol": "B"}
    }
    
    def __init__(self, x, y):
        super().__init__(x, y, 15)  # 15 pixel radius
        self.powerup_type = random.choice(list(self.TYPES.keys()))
        self.color = self.TYPES[self.powerup_type]["color"]
        self.symbol = self.TYPES[self.powerup_type]["symbol"]
        self.pulse_timer = 0
        self.lifetime = 15.0  # Disappear after 15 seconds
        
        # Slow drift
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(10, 30)
        self.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()
        
        self.pulse_timer += dt * 3  # Pulsing effect
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.kill()
            
    def draw(self, screen):
        # Pulsing effect
        pulse = 1 + 0.3 * math.sin(self.pulse_timer)
        radius = int(self.radius * pulse)
        
        # Draw outer glow
        glow_color = (*self.color, 80)
        pygame.draw.circle(screen, glow_color, self.position, radius + 5, 0)
        
        # Draw main circle
        pygame.draw.circle(screen, self.color, self.position, radius, 3)
        
        # Draw symbol in center
        font = pygame.font.SysFont('courier', 24, bold=True)
        text = font.render(self.symbol, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)