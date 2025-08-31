import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


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

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)  # type: ignore
    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    AsteroidField.containers = (updatable,)  # type: ignore
    Shot.containers = (shots, updatable, drawable)  # type: ignore

    # Create player at center of screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    # Create asteroid field
    asteroid_field = AsteroidField()

    def reset_game():
        nonlocal player, asteroid_field
        # Clear all sprite groups
        updatable.empty()
        drawable.empty() 
        asteroids.empty()
        shots.empty()
        
        # Recreate player and asteroid field
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
    
    def draw_game_over(screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw game over text
        font_large = pygame.font.Font(None, 74)
        font_medium = pygame.font.Font(None, 48)
        
        game_over_text = font_large.render("GAME OVER", True, NEON_PINK)
        restart_text = font_medium.render("Press R to Restart", True, NEON_CYAN)
        quit_text = font_medium.render("Press Q to Quit", True, NEON_CYAN)
        
        # Center the text
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 40))

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
                    shot.kill()
                    asteroid.split()





# runs the main function
if __name__ == "__main__":
    main()
