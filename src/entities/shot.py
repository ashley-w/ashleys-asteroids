import pygame
import math
from src.core.circleshape import CircleShape
from src.core.constants import SHOT_RADIUS, NEON_GREEN

class Shot(CircleShape):
    def __init__(self, x, y, size_multiplier=1.0, bullet_type="normal"):
        radius = int(SHOT_RADIUS * size_multiplier)
        super().__init__(x, y, radius)
        self.bullet_type = bullet_type
        self.creation_time = pygame.time.get_ticks() / 1000.0  # For rainbow animation

    def get_rainbow_color(self, time_offset=0):
        """Generate rainbow color based on creation time and offset"""
        current_time = pygame.time.get_ticks() / 1000.0
        hue = (self.creation_time + current_time + time_offset) * 2  # Speed of color change
        
        # Convert HSV to RGB for rainbow effect
        r = (math.sin(hue) + 1) * 127.5
        g = (math.sin(hue + 2.094) + 1) * 127.5  # 2π/3 offset
        b = (math.sin(hue + 4.188) + 1) * 127.5  # 4π/3 offset
        
        return (int(r), int(g), int(b))
    
    def draw_diamond(self, screen, center, size, color):
        """Draw a diamond shape"""
        x, y = center
        points = [
            (x, y - size),      # Top
            (x + size, y),      # Right  
            (x, y + size),      # Bottom
            (x - size, y)       # Left
        ]
        pygame.draw.polygon(screen, color, points)
    
    def draw(self, screen):
        if self.bullet_type == "rapid_fire":
            # Rainbow rapid fire bullets - diamond shaped
            current_color = self.get_rainbow_color()
            
            # Draw motion trail with rainbow fade
            if hasattr(self, 'velocity') and self.velocity.length() > 0:
                for i in range(5):
                    trail_offset = self.velocity.normalize() * -(i * 3)
                    trail_pos = (self.position.x + trail_offset.x, self.position.y + trail_offset.y)
                    trail_color = self.get_rainbow_color(i * 0.2)
                    trail_color = (trail_color[0]//4, trail_color[1]//4, trail_color[2]//4)
                    self.draw_diamond(screen, trail_pos, self.radius - i, trail_color)
            
            # Draw rainbow glow layers
            for i in range(3):
                glow_size = self.radius + 2 + i * 2
                glow_color = self.get_rainbow_color(i * 0.3)
                glow_color = (glow_color[0]//3, glow_color[1]//3, glow_color[2]//3)
                self.draw_diamond(screen, self.position, glow_size, glow_color)
            
            # Draw main diamond with bright rainbow color
            self.draw_diamond(screen, self.position, self.radius, current_color)
            
            # Draw bright white center
            self.draw_diamond(screen, self.position, max(1, self.radius // 2), (255, 255, 255))
        
        else:
            # Normal green circular bullets
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
        
        # Kill bullet if it goes off screen instead of wrapping
        from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        if (self.position.x < -50 or self.position.x > SCREEN_WIDTH + 50 or 
            self.position.y < -50 or self.position.y > SCREEN_HEIGHT + 50):
            self.kill()