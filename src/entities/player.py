import pygame
from src.core.circleshape import CircleShape
from src.core.constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, NEON_CYAN

# Player class that represents the player's ship
class Player(CircleShape):
    def __init__(self, x, y):
        # Call the parent class constructor with player position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize rotation angle to 0 degrees
        self.rotation = 0
        # Initialize shoot timer
        self.shoot_timer = 0
        # Weapon system
        self.weapon_type = "normal"
        self.weapon_timer = 0

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
        # Draw the player as a clean neon cyan triangle
        points = self.triangle()
        
        # Draw main triangle with thin outline only
        pygame.draw.polygon(screen, NEON_CYAN, points, 1)

    def thrust(self, dt):
        # Add acceleration in forward direction
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt

    def apply_powerup(self, powerup_type):
        self.weapon_type = powerup_type
        self.weapon_timer = 10.0  # 10 seconds of special weapon
        
    def shoot(self):
        if self.shoot_timer > 0:
            return
        from src.entities.shot import Shot
        
        # Calculate the tip of the triangle
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        tip_position = self.position + (forward * self.radius)  # type: ignore
        
        cooldown = PLAYER_SHOOT_COOLDOWN
        
        if self.weapon_type == "rapid_fire":
            cooldown = PLAYER_SHOOT_COOLDOWN * 0.3  # Much faster
            shot = Shot(tip_position.x, tip_position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED  # type: ignore
            
        elif self.weapon_type == "spread_shot":
            # Fire 3 shots in a spread
            for angle_offset in [-20, 0, 20]:
                shot = Shot(tip_position.x, tip_position.y)
                shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle_offset) * PLAYER_SHOOT_SPEED  # type: ignore
                
        elif self.weapon_type == "big_shot":
            shot = Shot(tip_position.x, tip_position.y, size_multiplier=2.5)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * (PLAYER_SHOOT_SPEED * 0.8)  # type: ignore
            cooldown = PLAYER_SHOOT_COOLDOWN * 1.5  # Slower fire rate
            
        else:  # normal weapon
            shot = Shot(tip_position.x, tip_position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED  # type: ignore
            
        self.shoot_timer = cooldown

    def update(self, dt):
        # Decrease shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        # Handle weapon timer
        if self.weapon_timer > 0:
            self.weapon_timer -= dt
            if self.weapon_timer <= 0:
                self.weapon_type = "normal"
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.thrust(-dt)  # Reverse thrust
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        # Apply velocity to position
        self.position += self.velocity * dt
        
        # Apply drag/friction to slow down over time
        self.velocity *= 0.99
        
        # Wrap around screen edges
        self.wrap_screen()
