import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

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
