import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, NEON_CYAN

# Player class that represents the player's ship
class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class constructor with player position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize rotation angle to 0 degrees
        self.rotation = 0
        # Initialize shoot timer
        self.shoot_timer = 0

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
        # Draw the player as a 3D neon cyan triangle
        points = self.triangle()
        
        # Create shadow/depth offset points
        shadow_points = [(p.x + 3, p.y + 3) for p in points]
        shadow_color = (NEON_CYAN[0]//4, NEON_CYAN[1]//4, NEON_CYAN[2]//4)
        pygame.draw.polygon(screen, shadow_color, shadow_points, 0)
        
        # Draw beveled edge effect with gradient layers
        # Create slightly smaller triangles with increasing brightness
        for i in range(3):
            offset = i * 0.5  # Shrink each layer slightly
            bevel_points = []
            center = pygame.Vector2(sum(p.x for p in points)/3, sum(p.y for p in points)/3)
            
            for point in points:
                # Move point slightly toward center for bevel effect
                direction = center - point
                new_point = point + direction * (offset / self.radius)
                bevel_points.append(new_point)
            
            intensity = 0.4 + i * 0.2  # Increasing brightness toward center
            bevel_color = (int(NEON_CYAN[0] * intensity), int(NEON_CYAN[1] * intensity), int(NEON_CYAN[2] * intensity))
            pygame.draw.polygon(screen, bevel_color, bevel_points, 0)
        
        # Draw bright outer glow
        for i in range(3):
            glow_color = (*NEON_CYAN, 60 - i * 20)
            pygame.draw.polygon(screen, glow_color, points, 4 + i)
            
        # Draw crisp outer edge
        pygame.draw.polygon(screen, NEON_CYAN, points, 2)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        from shot import Shot
        # Calculate the tip of the triangle (same as point 'a' in triangle method)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        tip_position = self.position + (forward * self.radius)  # type: ignore
        shot = Shot(tip_position.x, tip_position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED  # type: ignore
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def update(self, dt):
        # Decrease shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
