import pygame
import sys
import asyncio
from src.core.constants import *
from src.entities.player import Player
from src.entities.asteroid import Asteroid
from src.systems.asteroidfield import AsteroidField
from src.entities.shot import Shot
from src.systems.explosion import Explosion
from src.systems.starfield import Starfield
from src.entities.powerup import Powerup
from src.entities.bomb import Bomb
from src.systems.notification import NotificationManager
from src.systems.level_system import LevelSystem


# main game loop
async def main():
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
    game_state = "start"  # "start", "playing", "paused", "game_over", or "level_transition"
    score = 0
    lives = 3
    respawn_timer = 0
    level_system = LevelSystem()
    level_transition_timer = 0
    level_transition_duration = 3.0  # 3 seconds to show level message

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    Player.containers = (updatable, drawable)  # type: ignore
    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = (updatable,)  # type: ignore
    Shot.containers = (shots, updatable, drawable)  # type: ignore
    Explosion.containers = (explosions, updatable, drawable)  # type: ignore
    Powerup.containers = (powerups, updatable, drawable)  # type: ignore
    Bomb.containers = (bombs, updatable, drawable)  # type: ignore

    # Create player at center of screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    # Create asteroid field, starfield, and notification manager
    asteroid_field = AsteroidField()
    starfield = Starfield()
    notification_manager = NotificationManager()

    def get_retro_font(size, bold=False):
        """Get consistent retro font that works across platforms"""
        try:
            return pygame.font.SysFont('consolas,courier new,monospace', size, bold=bold)
        except:
            return pygame.font.Font(None, size)
    
    def reset_game():
        nonlocal player, asteroid_field, score, lives, respawn_timer, notification_manager, level_system
        # Clear all sprite groups
        updatable.empty()
        drawable.empty() 
        asteroids.empty()
        shots.empty()
        explosions.empty()
        powerups.empty()
        bombs.empty()
        
        # Recreate player, asteroid field, and notification manager
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
        notification_manager = NotificationManager()
        level_system = LevelSystem()
        score = 0
        lives = 3
        respawn_timer = 0
    
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
        
        # Draw game over text using consistent retro fonts
        font_large = get_retro_font(74, bold=True)
        font_medium = get_retro_font(48, bold=True) 
        font_small = get_retro_font(36, bold=True)
        
        game_over_text = font_large.render("GAME OVER", True, NEON_PINK)
        
        # Create subtitle with custom stars around "dead"
        subtitle_part1 = font_small.render("It's giving ", True, NEON_PURPLE)
        dead_text = font_small.render("dead", True, NEON_PURPLE)
        subtitle_part2 = font_small.render(", babes.", True, NEON_PURPLE)
        
        final_score_text = font_medium.render(f"Final Score: {score}", True, NEON_GREEN)
        restart_text = font_medium.render("Press R to Restart", True, NEON_CYAN)
        quit_text = font_medium.render("Press Q to Quit", True, NEON_CYAN)
        
        # Center the text properly
        game_over_x = SCREEN_WIDTH // 2 - game_over_text.get_width() // 2
        game_over_y = SCREEN_HEIGHT // 2 - 120
        screen.blit(game_over_text, (game_over_x, game_over_y))
        
        # Draw subtitle with stars around "dead" - properly centered
        subtitle_y = SCREEN_HEIGHT//2 - 50  # Closer to Game Over text
        total_width = subtitle_part1.get_width() + dead_text.get_width() + subtitle_part2.get_width() + 50  # +50 for star space
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
        
        # Center remaining text elements
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 70))

    def draw_pause_menu(screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw pause menu
        font_large = get_retro_font(64, bold=True)
        font_medium = get_retro_font(48, bold=True)
        
        pause_text = font_large.render("PAUSED", True, NEON_CYAN)
        resume_text = font_medium.render("Press ESC to Resume", True, NEON_GREEN)
        restart_text = font_medium.render("Press R to Restart", True, NEON_PURPLE)
        quit_text = font_medium.render("Press Q to Quit", True, NEON_PINK)
        
        # Center the text
        screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 120))
        screen.blit(resume_text, (SCREEN_WIDTH//2 - resume_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 70))

    def draw_start_screen(screen):
        # Draw title
        font_title = get_retro_font(72, bold=True)
        font_subtitle = get_retro_font(32, bold=True)
        font_controls = get_retro_font(24, bold=True)
        font_start = get_retro_font(48, bold=True)
        
        title_text = font_title.render("ASHLEY'S ASTEROIDS", True, NEON_CYAN)
        subtitle_text = font_subtitle.render("A Triangle Simulator", True, NEON_PURPLE)
        
        # Controls section
        controls_title = font_subtitle.render("CONTROLS:", True, NEON_PINK)
        controls = [
            "A/D - Turn Left/Right",
            "W/S - Thrust Forward/Backward", 
            "SPACE - Shoot",
            "SHIFT - Drop Bomb",
            "ESC - Pause Game"
        ]
        
        start_text = font_start.render("Press SPACEBAR to Start", True, NEON_GREEN)
        
        # Position everything
        y_pos = 150
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, y_pos))
        y_pos += 80
        screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, y_pos))
        
        y_pos += 120
        screen.blit(controls_title, (SCREEN_WIDTH//2 - controls_title.get_width()//2, y_pos))
        y_pos += 50
        
        for control in controls:
            control_text = font_controls.render(control, True, ELECTRIC_BLUE)
            screen.blit(control_text, (SCREEN_WIDTH//2 - control_text.get_width()//2, y_pos))
            y_pos += 35
            
        # Pulsing start text
        pulse = 1 + 0.3 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() * 0.2).x
        alpha = int(255 * pulse)
        start_surface = pygame.Surface(start_text.get_size())
        start_surface.set_alpha(alpha)
        start_surface.blit(start_text, (0, 0))
        screen.blit(start_surface, (SCREEN_WIDTH//2 - start_text.get_width()//2, y_pos + 40))

    def draw_level_transition(screen, level, message):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Rainbow effect for level text
        import math
        current_time = pygame.time.get_ticks() / 1000.0
        hue = current_time * 3  # Faster rainbow cycling
        r = (math.sin(hue) + 1) * 127.5
        g = (math.sin(hue + 2.094) + 1) * 127.5
        b = (math.sin(hue + 4.188) + 1) * 127.5
        rainbow_color = (int(r), int(g), int(b))
        
        font_huge = get_retro_font(120, bold=True)
        font_medium = get_retro_font(48, bold=True)
        
        level_text = font_huge.render(f"LEVEL {level}", True, rainbow_color)
        message_text = font_medium.render(message, True, NEON_PURPLE)
        
        # Center the text with some animation
        pulse = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
        level_y = SCREEN_HEIGHT//2 - 100
        message_y = SCREEN_HEIGHT//2 + 20
        
        # Pulsing effect for level text
        level_width = level_text.get_width() * pulse
        level_height = level_text.get_height() * pulse
        scaled_level = pygame.transform.scale(level_text, (int(level_width), int(level_height)))
        
        screen.blit(scaled_level, 
                   (SCREEN_WIDTH//2 - scaled_level.get_width()//2, level_y))
        screen.blit(message_text, 
                   (SCREEN_WIDTH//2 - message_text.get_width()//2, message_y))

    # game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if game_state == "start":
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        reset_game()
                elif game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "paused"
                elif game_state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "playing"
                    elif event.key == pygame.K_r:
                        game_state = "playing"
                        reset_game()
                    elif event.key == pygame.K_q:
                        return
                elif game_state == "game_over":
                    if event.key == pygame.K_r:
                        game_state = "playing"
                        reset_game()
                    elif event.key == pygame.K_q:
                        return
                elif game_state == "level_transition":
                    # Skip level transition with any key
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        game_state = "playing"
                        level_transition_timer = 0
        # drawing - dark space background with starfield
        screen.fill(DARK_SPACE)
        starfield.draw(screen)
        
        if game_state == "start":
            draw_start_screen(screen)
        elif game_state == "playing":
            starfield.update(dt)
            notification_manager.update(dt)
            for sprite in drawable:
                sprite.draw(screen)
            updatable.update(dt)
            
            # Draw arcade-style HUD across the top
            hud_font = get_retro_font(36)
            hud_y = 15
            
            # Create semi-transparent background strip for entire HUD
            hud_bg = pygame.Surface((SCREEN_WIDTH, 50))
            hud_bg.set_alpha(120)
            hud_bg.fill((0, 0, 0))
            screen.blit(hud_bg, (0, 0))
            
            # Draw top border line
            pygame.draw.line(screen, NEON_CYAN, (0, 50), (SCREEN_WIDTH, 50), 2)
            
            # Left side: Score
            score_text = hud_font.render(f"SCORE: {score:08d}", True, NEON_CYAN)
            screen.blit(score_text, (20, hud_y))
            
            # Center-left: Level (positioned after score with proper spacing)
            level_text = hud_font.render(f"LEVEL: {level_system.current_level:02d}", True, NEON_GREEN)
            level_x = 20 + score_text.get_width() + 40  # Score + 40px gap
            screen.blit(level_text, (level_x, hud_y))
            
            # Center-right: Lives (positioned dynamically)
            lives_text = hud_font.render("LIVES:", True, NEON_PINK)
            lives_x = level_x + level_text.get_width() + 40  # Level + 40px gap
            screen.blit(lives_text, (lives_x, hud_y))
            
            # Draw life triangles
            life_start_x = lives_x + lives_text.get_width() + 10
            for i in range(lives):
                # Small triangle for each life
                triangle_size = 8
                triangle_x = life_start_x + i * 25
                triangle_y = hud_y + lives_text.get_height() - triangle_size
                
                points = [
                    (triangle_x, triangle_y - triangle_size),
                    (triangle_x - triangle_size, triangle_y + triangle_size), 
                    (triangle_x + triangle_size, triangle_y + triangle_size)
                ]
                pygame.draw.polygon(screen, NEON_PINK, points)
            
            # Right side: Bombs
            bombs_text = hud_font.render(f"BOMBS: {player.bomb_count if respawn_timer <= 0 else 0}", True, NEON_PURPLE)
            bombs_x = SCREEN_WIDTH - bombs_text.get_width() - 20
            screen.blit(bombs_text, (bombs_x, hud_y))
            
            # Draw notifications on top
            notification_manager.draw(screen)
        elif game_state == "paused":
            # Draw game objects frozen
            for sprite in drawable:
                sprite.draw(screen)
            
            # Draw same arcade-style HUD as playing state
            hud_font = get_retro_font(36)
            hud_y = 15
            
            # Create semi-transparent background strip for entire HUD
            hud_bg = pygame.Surface((SCREEN_WIDTH, 50))
            hud_bg.set_alpha(120)
            hud_bg.fill((0, 0, 0))
            screen.blit(hud_bg, (0, 0))
            
            # Draw top border line
            pygame.draw.line(screen, NEON_CYAN, (0, 50), (SCREEN_WIDTH, 50), 2)
            
            # Left side: Score
            score_text = hud_font.render(f"SCORE: {score:08d}", True, NEON_CYAN)
            screen.blit(score_text, (20, hud_y))
            
            # Center-left: Level (positioned after score with proper spacing) 
            level_text = hud_font.render(f"LEVEL: {level_system.current_level:02d}", True, NEON_GREEN)
            level_x = 20 + score_text.get_width() + 40  # Score + 40px gap
            screen.blit(level_text, (level_x, hud_y))
            
            # Center-right: Lives (positioned dynamically)
            lives_text = hud_font.render("LIVES:", True, NEON_PINK)
            lives_x = level_x + level_text.get_width() + 40  # Level + 40px gap
            screen.blit(lives_text, (lives_x, hud_y))
            
            # Draw life triangles
            life_start_x = lives_x + lives_text.get_width() + 10
            for i in range(lives):
                # Small triangle for each life
                triangle_size = 8
                triangle_x = life_start_x + i * 25
                triangle_y = hud_y + lives_text.get_height() - triangle_size
                
                points = [
                    (triangle_x, triangle_y - triangle_size),
                    (triangle_x - triangle_size, triangle_y + triangle_size), 
                    (triangle_x + triangle_size, triangle_y + triangle_size)
                ]
                pygame.draw.polygon(screen, NEON_PINK, points)
            
            # Right side: Bombs
            bombs_text = hud_font.render(f"BOMBS: {player.bomb_count if respawn_timer <= 0 else 0}", True, NEON_PURPLE)
            bombs_x = SCREEN_WIDTH - bombs_text.get_width() - 20
            screen.blit(bombs_text, (bombs_x, hud_y))
            
            # Draw pause menu
            draw_pause_menu(screen)
        elif game_state == "game_over":
            # Still draw the game objects but frozen
            for sprite in drawable:
                sprite.draw(screen)
            draw_game_over(screen)
        elif game_state == "level_transition":
            # Draw frozen game state in background
            for sprite in drawable:
                sprite.draw(screen)
            # Draw level transition screen
            draw_level_transition(screen, level_system.current_level, level_system.get_level_message())
        
        pygame.display.flip()

        # update game state
        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

        if game_state == "level_transition":
            # Handle level transition timer
            level_transition_timer += dt
            if level_transition_timer >= level_transition_duration:
                game_state = "playing"
                level_transition_timer = 0

        elif game_state == "playing":
            # Check for level up
            if level_system.check_level_up(score):
                game_state = "level_transition"
                level_transition_timer = 0
                # Apply new difficulty to asteroid field
                asteroid_field.spawn_rate = level_system.get_asteroid_spawn_rate()
                asteroid_field.speed_multiplier = level_system.get_asteroid_speed_multiplier()
            
            # Handle respawn timer
            if respawn_timer > 0:
                respawn_timer -= dt
                if respawn_timer <= 0:
                    # Respawn player at center with temporary invulnerability
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.make_invulnerable(3.0)  # 3 seconds of invulnerability
            
            # Only check collisions if player exists and isn't respawning
            elif respawn_timer <= 0:
                for asteroid in asteroids:
                    if player.collision(asteroid):
                        lives -= 1
                        if lives <= 0:
                            game_state = "game_over"
                        else:
                            # Set respawn timer and remove player temporarily
                            respawn_timer = 2.0  # 2 seconds invincibility
                            player.kill()
                            # Create explosion at player position
                            explosion = Explosion(player.position.x, player.position.y, player.radius)
            
            # Check for powerup collection
            for powerup in powerups:
                if player.collision(powerup):
                    player.apply_powerup(powerup.powerup_type)
                    notification_manager.add_powerup_notification(powerup.name, powerup.powerup_type)
                    powerup.kill()

        # Check for shot-asteroid collisions
        for asteroid in asteroids:
            for shot in shots:
                if shot.collision(asteroid):
                    # Award points based on asteroid size and type
                    base_points = 0
                    if asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                        base_points = 20  # Large asteroid
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS:
                        base_points = 50  # Medium asteroid
                    else:
                        base_points = 100  # Small asteroid
                    
                    # Word asteroids give bonus points!
                    if hasattr(asteroid, 'is_word_asteroid') and asteroid.is_word_asteroid:
                        score += base_points * 3  # 3x points for defeating existential dread
                    else:
                        score += base_points
                    
                    # Create explosion at asteroid position
                    explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    
                    # 10% chance to spawn powerup when destroying asteroid
                    import random
                    if random.random() < 0.1:
                        powerup = Powerup(asteroid.position.x, asteroid.position.y)
                    
                    shot.kill()
                    asteroid.split()
                    
        # Check for bomb explosions hitting asteroids
        for bomb in bombs:
            if bomb.has_exploded and bomb.explosion_radius > 0:
                for asteroid in asteroids.copy():  # Use copy to avoid modification during iteration
                    distance = bomb.position.distance_to(asteroid.position)
                    if distance <= bomb.explosion_radius:
                        # Award points based on asteroid size and type
                        base_points = 0
                        if asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                            base_points = 20  # Large asteroid
                        elif asteroid.radius >= ASTEROID_MIN_RADIUS:
                            base_points = 50  # Medium asteroid
                        else:
                            base_points = 100  # Small asteroid
                        
                        # Word asteroids give bonus points!
                        if hasattr(asteroid, 'is_word_asteroid') and asteroid.is_word_asteroid:
                            score += base_points * 3  # 3x points for defeating existential dread
                        else:
                            score += base_points
                        
                        # Create explosion at asteroid position
                        explosion = Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        asteroid.split()





# runs the main function
if __name__ == "__main__":
    asyncio.run(main())
