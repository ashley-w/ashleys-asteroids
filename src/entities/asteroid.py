import pygame
import random
import math
from src.core.circleshape import CircleShape
from src.core.constants import ASTEROID_MIN_RADIUS, NEON_PURPLE, NEON_PINK, NEON_CYAN

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate random lumpy shape
        self.vertices = []
        num_points = random.randint(8, 12)  # Random complexity
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            # Random radius variation for lumpy effect
            r = radius * random.uniform(0.7, 1.3)
            x_offset = r * math.cos(angle)
            y_offset = r * math.sin(angle)
            self.vertices.append((x_offset, y_offset))

    def draw(self, screen):
        # Choose color based on asteroid size
        if self.radius >= ASTEROID_MIN_RADIUS * 2:
            color = NEON_PURPLE  # Large asteroids
        elif self.radius >= ASTEROID_MIN_RADIUS:
            color = NEON_PINK    # Medium asteroids  
        else:
            color = NEON_PURPLE  # Small asteroids
        
        # Create world coordinates for lumpy shape
        points = []
        shadow_points = []
        for x_offset, y_offset in self.vertices:
            world_x = self.position.x + x_offset
            world_y = self.position.y + y_offset
            points.append((world_x, world_y))
            shadow_points.append((world_x + 2, world_y + 2))
        
        # Draw shadow
        shadow_color = (color[0]//3, color[1]//3, color[2]//3)
        pygame.draw.polygon(screen, shadow_color, shadow_points, 0)
        
        # Draw gradient layers for depth
        for i in range(3):
            scale = 0.4 + 0.2 * i  # Inner to outer layers
            intensity = 0.4 + 0.2 * i  # Increasing brightness
            layer_color = (int(color[0] * intensity), int(color[1] * intensity), int(color[2] * intensity))
            
            scaled_points = []
            for x_offset, y_offset in self.vertices:
                scaled_x = self.position.x + x_offset * scale
                scaled_y = self.position.y + y_offset * scale
                scaled_points.append((scaled_x, scaled_y))
            pygame.draw.polygon(screen, layer_color, scaled_points, 0)
        
        # Draw outer glow
        glow_color = (*color, 40)
        glow_points = []
        for x_offset, y_offset in self.vertices:
            glow_x = self.position.x + x_offset * 1.2
            glow_y = self.position.y + y_offset * 1.2
            glow_points.append((glow_x, glow_y))
        pygame.draw.polygon(screen, glow_color, glow_points, 0)
        
        # Draw main lumpy asteroid
        pygame.draw.polygon(screen, color, points, 0)
        pygame.draw.polygon(screen, color, points, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)  # type: ignore
        self.wrap_screen()

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


class WordAsteroid(Asteroid):
    """Special asteroid that displays existential words instead of shapes"""
    
    WORD_LIST = ["WORK", "TAXES", "ANXIETY", "DEBT", "BILLS", "STRESS"]
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.word = random.choice(self.WORD_LIST)
        # Make word asteroids slightly more valuable
        self.is_word_asteroid = True
    
    def draw(self, screen):
        # Draw a subtle background glow
        glow_radius = self.radius * 1.3
        for i in range(3):
            alpha = 30 - i * 8
            glow_color = (*NEON_CYAN, alpha)
            pygame.draw.circle(screen, glow_color, self.position, int(glow_radius - i * 3), 0)
        
        # Choose font size based on asteroid size
        if self.radius >= ASTEROID_MIN_RADIUS * 2:
            font_size = 48
        elif self.radius >= ASTEROID_MIN_RADIUS:
            font_size = 36
        else:
            font_size = 24
            
        font = pygame.font.Font(None, font_size)
        
        # Create text with shadow effect
        shadow_text = font.render(self.word, True, (20, 20, 20))
        main_text = font.render(self.word, True, NEON_CYAN)
        
        # Center the text on the asteroid position
        shadow_rect = shadow_text.get_rect(center=(self.position.x + 2, self.position.y + 2))
        main_rect = main_text.get_rect(center=self.position)
        
        # Draw shadow then main text
        screen.blit(shadow_text, shadow_rect)
        screen.blit(main_text, main_rect)
        
        # Draw subtle border around text area
        border_rect = main_rect.inflate(10, 10)
        pygame.draw.rect(screen, NEON_CYAN, border_rect, 2)
    
    def split(self):
        # Word asteroids split into regular asteroids
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
        
        # Create two new REGULAR asteroids at current position
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        # Set velocities with 1.2 speed multiplier
        asteroid1.velocity = velocity1 * 1.2  # type: ignore
        asteroid2.velocity = velocity2 * 1.2  # type: ignore
