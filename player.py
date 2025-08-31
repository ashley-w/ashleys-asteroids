import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED

# Player class that represents the player's ship
class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class constructor with player position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize rotation angle to 0 degrees
        self.rotation = 0

    def triangle(self):
        # Calculate triangle points for the player ship
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * float(self.radius / 1.5)  # type: ignore
        a = self.position + (forward * self.radius)  # type: ignore
        b = self.position - (forward * self.radius) - right  # type: ignore
        c = self.position - (forward * self.radius) + right  # type: ignore
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def draw(self, screen):
        # Draw the player as a white triangle
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, 2)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
