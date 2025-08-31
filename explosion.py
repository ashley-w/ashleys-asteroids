import pygame
import random
import math
from constants import NEON_PINK, NEON_PURPLE, NEON_GREEN, ELECTRIC_BLUE

class ExplosionParticle:
    def __init__(self, x, y, color):
        self.position = pygame.Vector2(x, y)
        # Random velocity in all directions
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        self.velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.color = color
        self.life = 1.0  # Full life
        self.max_life = random.uniform(0.5, 1.5)  # How long it lives
        self.size = random.uniform(2, 6)
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.life -= dt / self.max_life
        # Slow down particles over time
        self.velocity *= 0.98
        
    def draw(self, screen):
        if self.life <= 0:
            return
        # Fade out as life decreases
        alpha = int(255 * max(0, self.life))
        size = int(self.size * self.life)
        if size > 0:
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(screen, color_with_alpha, (int(self.position.x), int(self.position.y)), size, 0)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
            
        self.position = pygame.Vector2(x, y)
        self.particles = []
        
        # Create particles based on explosion size
        num_particles = int(size / 5) + 10  # More particles for bigger explosions
        colors = [NEON_PINK, NEON_PURPLE, NEON_GREEN, ELECTRIC_BLUE]
        
        for _ in range(num_particles):
            color = random.choice(colors)
            particle = ExplosionParticle(x, y, color)
            self.particles.append(particle)
            
        self.timer = 2.0  # Explosion lasts 2 seconds
        
    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
            return
            
        # Update all particles
        for particle in self.particles[:]:  # Copy list to avoid modification issues
            particle.update(dt)
            if particle.life <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)