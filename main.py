import pygame
from constants import *
from player import Player


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

    # Create player at center of screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)

    # game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # drawing
        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.display.flip()

        # update game state
        clock.tick(60)
        dt = clock.tick(60) / 1000




# runs the main function
if __name__ == "__main__":
    main()
