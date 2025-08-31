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
        # Shield system
        self.has_shield = False
        self.shield_timer = 0
        # Speed boost system
        self.speed_boost = False
        self.speed_timer = 0
        # Bomb system
        self.bomb_count = 0
        self.bomb_cooldown = 0
        # Invulnerability system
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.flash_timer = 0

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

        # Draw shield if active
        if self.has_shield:
            from src.core.constants import ELECTRIC_BLUE
            import math
            # Pulsing shield effect
            pulse = 1 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01)
            shield_radius = self.radius * 1.5 * pulse

            # Draw shield as a glowing circle
            for i in range(3):
                alpha = 60 - i * 15
                color = (*ELECTRIC_BLUE, alpha)
                pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)),
                                 int(shield_radius + i * 2), 2)

        # Draw speed boost effects
        if self.speed_boost:
            import math
            # Draw trailing particles effect
            trail_length = 5
            for i in range(trail_length):
                alpha = 100 - (i * 15)
                trail_pos = self.position - (self.velocity.normalize() * (i + 1) * 8) if self.velocity.length() > 0 else self.position
                color = (*NEON_CYAN, alpha)
                pygame.draw.circle(screen, color, (int(trail_pos.x), int(trail_pos.y)), 2)

        # Draw main triangle with thin outline only
        triangle_color = NEON_CYAN
        if self.speed_boost:
            # Brighter when speed boost is active
            triangle_color = (min(255, NEON_CYAN[0] + 50), min(255, NEON_CYAN[1] + 50), min(255, NEON_CYAN[2] + 50))
        
        # Flash effect when invulnerable
        if self.invulnerable and int(self.flash_timer * 10) % 2 == 0:
            # Make semi-transparent when flashing
            triangle_color = (triangle_color[0] // 2, triangle_color[1] // 2, triangle_color[2] // 2)
            
        pygame.draw.polygon(screen, triangle_color, points, 1)

    def thrust(self, dt):
        # Add acceleration in forward direction
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        speed_multiplier = 2.0 if self.speed_boost else 1.0
        self.velocity += forward * PLAYER_SPEED * dt * speed_multiplier

    def apply_powerup(self, powerup_type):
        if powerup_type == "shield":
            self.has_shield = True
            self.shield_timer = 15.0  # 15 seconds of shield
        elif powerup_type == "speed":
            self.speed_boost = True
            self.speed_timer = 12.0  # 12 seconds of speed boost
        elif powerup_type == "bomb":
            self.bomb_count += 3  # Give 3 bombs
        else:
            # Weapon powerups
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

    def drop_bomb(self):
        if self.bomb_count <= 0 or self.bomb_cooldown > 0:
            return

        from src.entities.bomb import Bomb
        bomb = Bomb(self.position.x, self.position.y)
        self.bomb_count -= 1
        self.bomb_cooldown = 2.0  # 2 second cooldown between bombs
        
    def make_invulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_timer = duration
        self.flash_timer = 0

    def _update_timers(self, dt):
        # Decrease shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Handle weapon timer
        if self.weapon_timer > 0:
            self.weapon_timer -= dt
            if self.weapon_timer <= 0:
                self.weapon_type = "normal"

        # Handle shield timer
        if self.shield_timer > 0:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.has_shield = False

        # Handle speed timer
        if self.speed_timer > 0:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_boost = False

        # Handle bomb cooldown
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= dt
            
        # Handle invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            self.flash_timer += dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.flash_timer = 0

    def _handle_input(self, dt):
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
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.drop_bomb()

    def update(self, dt):
        self._update_timers(dt)
        self._handle_input(dt)

        # Apply velocity to position
        self.position += self.velocity * dt

        # Apply drag/friction to slow down over time
        self.velocity *= 0.985  # Less drag for more responsive feel

        # Wrap around screen edges
        self.wrap_screen()

    def _triangle_collision(self, other):
        # If shield is active or invulnerable, player is invincible
        if self.has_shield or self.invulnerable:
            return False

        # Triangle-to-circle collision detection
        triangle_points = self.triangle()

        # Check if circle center is inside triangle
        if self._point_in_triangle(other.position, triangle_points):
            return True

        # Check if circle intersects any triangle edge
        for i in range(3):
            edge_start = triangle_points[i]
            edge_end = triangle_points[(i + 1) % 3]

            if self._circle_line_collision(other.position, other.radius, edge_start, edge_end):
                return True

        return False

    def _point_in_triangle(self, point, triangle):
        # Use barycentric coordinates to check if point is inside triangle
        a, b, c = triangle

        v0 = c - a
        v1 = b - a
        v2 = point - a

        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)

        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def _circle_line_collision(self, circle_pos, circle_radius, line_start, line_end):
        # Find closest point on line segment to circle center
        line_vec = line_end - line_start
        line_length_sq = line_vec.length_squared()

        if line_length_sq == 0:
            # Line segment is actually a point
            return circle_pos.distance_to(line_start) <= circle_radius

        t = max(0, min(1, (circle_pos - line_start).dot(line_vec) / line_length_sq))
        closest_point = line_start + t * line_vec

        return circle_pos.distance_to(closest_point) <= circle_radius
