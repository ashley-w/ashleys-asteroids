import pygame
import random
import math
from src.core.circleshape import CircleShape
from src.core.constants import NEON_GREEN, NEON_PURPLE, ELECTRIC_BLUE, NEON_PINK, NEON_CYAN

class Powerup(CircleShape):
    TYPES = {
        "rapid_fire": {"color": NEON_GREEN, "symbol": "⚡", "name": "RAPID FIRE"},
        "spread_shot": {"color": NEON_PURPLE, "symbol": "◄►", "name": "SPREAD SHOT"}, 
        "shield": {"color": ELECTRIC_BLUE, "symbol": "◊", "name": "SHIELD"},
        "speed": {"color": NEON_CYAN, "symbol": "►", "name": "SPEED BOOST"},
        "bomb": {"color": NEON_PINK, "symbol": "●", "name": "BOMB"}
    }
    
    def __init__(self, x, y):
        super().__init__(x, y, 20)  # Larger than before for distinction
        self.powerup_type = random.choice(list(self.TYPES.keys()))
        self.color = self.TYPES[self.powerup_type]["color"]
        self.symbol = self.TYPES[self.powerup_type]["symbol"]
        self.name = self.TYPES[self.powerup_type]["name"]
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
        size = int(self.radius * pulse)
        
        # Draw rotating square instead of circle to distinguish from asteroids
        points = []
        rotation = self.pulse_timer * 45  # Slow rotation
        for i in range(4):
            angle = (i * 90 + rotation) * math.pi / 180
            x = self.position.x + size * math.cos(angle) * 0.7
            y = self.position.y + size * math.sin(angle) * 0.7
            points.append((x, y))
        
        # Draw outer glow
        glow_color = (*self.color, 60)
        for i in range(3):
            glow_points = []
            for px, py in points:
                glow_x = px + (px - self.position.x) * 0.3 * i
                glow_y = py + (py - self.position.y) * 0.3 * i
                glow_points.append((glow_x, glow_y))
            pygame.draw.polygon(screen, glow_color, glow_points, 0)
        
        # Draw main square
        pygame.draw.polygon(screen, self.color, points, 0)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        
        # Draw symbol in center
        font = pygame.font.SysFont('courier', 20, bold=True)
        text = font.render(self.symbol, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)