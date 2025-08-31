import pygame
import math
from src.core.circleshape import CircleShape
from src.core.constants import NEON_PINK, SCREEN_WIDTH, SCREEN_HEIGHT

class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 15)  # Small bomb radius
        self.timer = 3.0  # 3 seconds until explosion
        self.pulse_timer = 0
        self.has_exploded = False
        self.explosion_radius = 0
        self.max_explosion_radius = 150
        self.explosion_duration = 1.0
        
    def update(self, dt):
        if not self.has_exploded:
            self.timer -= dt
            self.pulse_timer += dt * 8  # Fast pulsing
            
            if self.timer <= 0:
                self.explode()
        else:
            # Expand explosion
            self.explosion_radius += (self.max_explosion_radius / self.explosion_duration) * dt
            if self.explosion_radius >= self.max_explosion_radius:
                self.kill()
                
    def explode(self):
        self.has_exploded = True
        self.explosion_radius = 0
        
        # Damage all asteroids within explosion radius
        # Need to access asteroid group from main game loop
        # For now, we'll handle this collision detection in main.py
                    
    def draw(self, screen):
        if not self.has_exploded:
            # Draw pulsing bomb
            pulse = 1 + 0.5 * math.sin(self.pulse_timer)
            size = int(self.radius * pulse)
            
            # Warning color gets more intense as timer counts down
            intensity = max(0.3, 1 - (self.timer / 3.0))
            color = (int(NEON_PINK[0] * intensity), int(NEON_PINK[1] * intensity), int(NEON_PINK[2] * intensity))
            
            # Draw bomb core
            pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), size, 0)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), size, 2)
            
            # Draw timer indicator
            font = pygame.font.SysFont('courier', 16, bold=True)
            timer_text = f"{self.timer:.1f}"
            text = font.render(timer_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=self.position)
            screen.blit(text, text_rect)
        else:
            # Draw expanding explosion
            explosion_alpha = int(255 * (1 - self.explosion_radius / self.max_explosion_radius))
            
            # Multiple explosion rings
            for i in range(3):
                ring_radius = self.explosion_radius - (i * 20)
                if ring_radius > 0:
                    alpha = max(0, explosion_alpha - (i * 60))
                    color = (*NEON_PINK, alpha)
                    pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), 
                                     int(ring_radius), 3)