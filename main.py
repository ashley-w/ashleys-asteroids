import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


# main game loop
def main():
    # initializing pygame
    pygame.init()

    # printing required statements
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
    game_state = "playing"  # "playing" or "game_over"
    score = 0

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = (updatable, drawable)  # type: ignore
    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = (updatable,)  # type: ignore
    Shot.containers = (shots, updatable, drawable)  # type: ignore
    Explosion.containers = (explosions, updatable, drawable)  # type: ignore

    # Create player at center of screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    # Create asteroid field
    asteroid_field = AsteroidField()

    def reset_game():
        nonlocal player, asteroid_field, score
        # Clear all sprite groups
        updatable.empty()
        drawable.empty() 
        asteroids.empty()
        shots.empty()
        explosions.empty()
        
        # Recreate player and asteroid field
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
        score = 0
    
    def draw_star(screen, x, y, size, color):
        # Draw a 5-pointed star using lines
        import math
        points = []
        for i in range(10):  # 10 points for 5-pointed star (outer and inner points)
            angle = i * math.pi / 5
            if i % 2 == 0:  # Outer points
                radius = size
            else:  # Inner points
                radius = size * 0.4
            point_x = x + radius * math.cos(angle - math.pi/2)
            point_y = y + radius * math.sin(angle - math.pi/2)
            points.append((point_x, point_y))
        
        # Draw star with glow effect
        glow_color = (*color, 60)
        pygame.draw.polygon(screen, glow_color, points, 0)
        pygame.draw.polygon(screen, color, points, 2)
    
    def draw_game_over(screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        # Use retro monospace font
        font_large = pygame.font.SysFont('courier', 74, bold=True)
        font_medium = pygame.font.SysFont('courier', 48, bold=True)
        font_small = pygame.font.SysFont('courier', 36)
        
        game_over_text = font_large.render("GAME OVER", True, NEON_PINK)
        
        # Create subtitle with custom stars around "dead"
        subtitle_part1 = font_small.render("It's giving ", True, NEON_PURPLE)
        dead_text = font_small.render("dead", True, NEON_PURPLE)
        subtitle_part2 = font_small.render(", babes.", True, NEON_PURPLE)
        
        final_score_text = font_medium.render(f"Final Score: {score}", True, NEON_GREEN)
        restart_text = font_medium.render("Press R to Restart", True, NEON_CYAN)
        quit_text = font_medium.render("Press Q to Quit", True, NEON_CYAN)
        
        # Center the text
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 120))
        
        # Draw subtitle with stars around "dead"
        subtitle_y = SCREEN_HEIGHT//2 - 70
        total_width = subtitle_part1.get_width() + dead_text.get_width() + subtitle_part2.get_width() + 60  # +60 for star space
        start_x = SCREEN_WIDTH//2 - total_width//2
        
        # Draw "It's giving "
        screen.blit(subtitle_part1, (start_x, subtitle_y))
        current_x = start_x + subtitle_part1.get_width()
        
        # Draw left star
        draw_star(screen, current_x + 10, subtitle_y + dead_text.get_height()//2, 8, NEON_PINK)
        current_x += 25
        
        # Draw "dead"
        screen.blit(dead_text, (current_x, subtitle_y))
        current_x += dead_text.get_width()
        
        # Draw right star
        draw_star(screen, current_x + 10, subtitle_y + dead_text.get_height()//2, 8, NEON_PINK)
        current_x += 25
        
        # Draw ", babes."
        screen.blit(subtitle_part2, (current_x, subtitle_y))
        
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 70))

    # game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if game_state == "game_over":
                    if event.key == pygame.K_r:
                        game_state = "playing"
                        reset_game()
                    elif event.key == pygame.K_q:
                        return
        # drawing - dark space background
        screen.fill(DARK_SPACE)
        
        if game_state == "playing":
            for sprite in drawable:
                sprite.draw(screen)
            updatable.update(dt)
            
            # Draw score
            font = pygame.font.SysFont('courier', 48, bold=True)
            score_text = font.render(f"Score: {score}", True, NEON_CYAN)
            screen.blit(score_text, (20, 20))
        elif game_state == "game_over":
            # Still draw the game objects but frozen
            for sprite in drawable:
                sprite.draw(screen)
            draw_game_over(screen)
        
        pygame.display.flip()

        # update game state
        clock.tick(60)
        dt = clock.tick(60) / 1000

        if game_state == "playing":
            for asteroid in asteroids:
                if player.collision(asteroid):
                    game_state = "game_over"

        # Check for shot-asteroid collisions
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    # Award points based on asteroid size
                    if asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                        score += 20  # Large asteroid
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS:
                        score += 50  # Medium asteroid
                    else:
                        score += 100  # Small asteroid
                    
                    # Create explosion at asteroid position
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    
                    shot.kill()
                    asteroid.split()





# runs the main function
if __name__ == "__main__":
    main()
