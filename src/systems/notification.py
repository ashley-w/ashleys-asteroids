import pygame
import math
from src.core.constants import NEON_GREEN, NEON_PURPLE, ELECTRIC_BLUE, NEON_CYAN, NEON_PINK

class PowerupNotification:
    def __init__(self, powerup_name, powerup_type):
        self.name = powerup_name
        self.type = powerup_type
        self.timer = 3.0  # Show for 3 seconds
        self.fade_timer = 0.5  # Fade in/out duration
        self.y_offset = 0  # For floating animation
        
        # Color based on powerup type
        type_colors = {
            "rapid_fire": NEON_GREEN,
            "spread_shot": NEON_PURPLE,
            "shield": ELECTRIC_BLUE,
            "speed": NEON_CYAN,
            "bomb": NEON_PINK
        }
        self.color = type_colors.get(powerup_type, NEON_GREEN)
        
    def update(self, dt):
        self.timer -= dt
        self.y_offset += dt * 20  # Slow float upward
        return self.timer > 0  # Return False when expired
        
    def draw(self, screen):
        if self.timer <= 0:
            return
            
        # Calculate alpha based on fade in/out
        if self.timer > 2.5:  # Fade in
            alpha = min(255, int(255 * (3.0 - self.timer) / 0.5))
        elif self.timer < 0.5:  # Fade out
            alpha = int(255 * (self.timer / 0.5))
        else:
            alpha = 255
            
        # Position in center-top of screen
        from src.core.constants import SCREEN_WIDTH
        center_x = SCREEN_WIDTH // 2
        base_y = 250 - int(self.y_offset)
        
        # Draw background box
        font = pygame.font.SysFont('courier', 36, bold=True)
        text = font.render(f"PICKED UP: {self.name}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, base_y))
        
        # Background with padding
        bg_rect = pygame.Rect(text_rect.left - 20, text_rect.top - 10, 
                             text_rect.width + 40, text_rect.height + 20)
        
        # Semi-transparent background
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(min(alpha, 180))
        bg_surface.fill((20, 10, 40))  # Dark purple
        screen.blit(bg_surface, bg_rect.topleft)
        
        # Colored border
        border_color = (*self.color, min(alpha, 200))
        pygame.draw.rect(screen, border_color, bg_rect, 3)
        
        # Text with alpha
        text_surface = font.render(f"PICKED UP: {self.name}", True, (*self.color, alpha))
        screen.blit(text_surface, text_rect)

class NotificationManager:
    def __init__(self):
        self.notifications = []
        
    def add_powerup_notification(self, powerup_name, powerup_type):
        # Remove any existing notifications to avoid stacking
        self.notifications.clear()
        # Add new notification
        notification = PowerupNotification(powerup_name, powerup_type)
        self.notifications.append(notification)
        
    def update(self, dt):
        # Update all notifications and remove expired ones
        self.notifications = [n for n in self.notifications if n.update(dt)]
        
    def draw(self, screen):
        for notification in self.notifications:
            notification.draw(screen)