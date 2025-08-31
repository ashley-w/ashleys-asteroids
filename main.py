import pygame
from constants import *


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

    # game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # drawing
        screen.fill((0, 0, 0))
        pygame.display.flip()


# runs the main function
if __name__ == "__main__":
    main()
