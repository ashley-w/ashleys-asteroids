import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius


    def collision(self, other):
        # Special case for Player triangle collision
        from src.entities.player import Player
        
        if isinstance(self, Player):
            return self._triangle_collision(other)
        elif isinstance(other, Player):
            return other._triangle_collision(self)
        else:
            # Standard circle-circle collision
            distance = self.position.distance_to(other.position)
            return distance < self.radius + other.radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass
    
    def wrap_screen(self):
        # Wrap around screen edges
        from src.core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
