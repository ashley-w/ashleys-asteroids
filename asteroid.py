import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, NEON_PURPLE, NEON_PINK

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        # Choose color based on asteroid size
        if self.radius >= ASTEROID_MIN_RADIUS * 2:
            color = NEON_PURPLE  # Large asteroids
        elif self.radius >= ASTEROID_MIN_RADIUS:
            color = NEON_PINK    # Medium asteroids  
        else:
            color = NEON_PURPLE  # Small asteroids
        
        # Create 3D depth effect with layered circles
        # Draw shadow/depth layer (darker, offset)
        shadow_pos = (self.position.x + 2, self.position.y + 2)
        shadow_color = (color[0]//3, color[1]//3, color[2]//3)  # Much darker
        pygame.draw.circle(screen, shadow_color, shadow_pos, self.radius, 0)
        
        # Draw gradient layers for roundness (from dark center to bright edge)
        for i in range(5):
            layer_radius = self.radius * (0.2 + 0.16 * i)  # Increasing size
            intensity = 0.3 + 0.14 * i  # Increasing brightness
            layer_color = (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))
            pygame.draw.circle(screen, layer_color, self.position, int(layer_radius), 0)
        
        # Draw bright outer glow
        glow_color = (*color, 60)
        pygame.draw.circle(screen, glow_color, self.position, self.radius + 3, 0)
        
        # Draw crisp outer edge
        pygame.draw.circle(screen, color, self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)  # type: ignore

    def split(self):
        # Kill this asteroid
        self.kill()
        
        # If this is a small asteroid, just disappear
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Generate random angle between 20-50 degrees
        random_angle = random.uniform(20, 50)
        
        # Create two new velocity vectors by rotating current velocity
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)
        
        # Calculate new radius for smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Create two new asteroids at current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        # Set velocities with 1.2 speed multiplier
        asteroid1.velocity = velocity1 * 1.2  # type: ignore
        asteroid2.velocity = velocity2 * 1.2  # type: ignore
