import pygame
from src.core.circleshape import CircleShape
from src.core.constants import SHOT_RADIUS, NEON_GREEN

class Shot(CircleShape):
    def __init__(self, x, y, size_multiplier=1.0):
        radius = int(SHOT_RADIUS * size_multiplier)
        super().__init__(x, y, radius)

    def draw(self, screen):
        # Draw 3D energy bullet with depth layers
        
        # Draw motion trail/shadow (offset backward from velocity direction)
        if hasattr(self, 'velocity') and self.velocity.length() > 0:
            trail_offset = self.velocity.normalize() * -8
            trail_pos = (self.position.x + trail_offset.x, self.position.y + trail_offset.y)
            trail_color = (NEON_GREEN[0]//4, NEON_GREEN[1]//4, NEON_GREEN[2]//4)
            pygame.draw.circle(screen, trail_color, trail_pos, self.radius + 1, 0)
        
        # Draw layered energy core (3D sphere effect)
        for i in range(4):
            layer_radius = self.radius * (0.3 + 0.175 * i)
            intensity = 0.4 + 0.15 * i  # Brighter toward outside
            layer_color = (int(NEON_GREEN[0] * intensity), int(NEON_GREEN[1] * intensity), int(NEON_GREEN[2] * intensity))
            pygame.draw.circle(screen, layer_color, self.position, int(layer_radius), 0)
        
        # Draw bright outer glow with multiple layers
        for i in range(3):
            glow_radius = self.radius + 2 + i * 2
            alpha = 80 - i * 25
            glow_color = (*NEON_GREEN, alpha)
            pygame.draw.circle(screen, glow_color, self.position, glow_radius, 0)
        
        # Draw bright center core
        pygame.draw.circle(screen, (255, 255, 255), self.position, max(1, self.radius // 2), 0)

    def update(self, dt):
        self.position += (self.velocity * dt)  # type: ignore
        self.wrap_screen()