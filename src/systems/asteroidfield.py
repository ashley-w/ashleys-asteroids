import pygame
import random
from src.entities.asteroid import Asteroid, WordAsteroid
from src.core.constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.time_elapsed = 0.0
        self.spawn_rate = ASTEROID_SPAWN_RATE
        self.speed_multiplier = 1.0

    def spawn(self, radius, position, velocity, is_word_asteroid=False):
        if is_word_asteroid:
            asteroid = WordAsteroid(position.x, position.y, radius)
        else:
            asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        self.time_elapsed += dt
        
        # Use level-based spawn rate if set, otherwise fall back to time-based
        if hasattr(self, 'spawn_rate') and self.spawn_rate != ASTEROID_SPAWN_RATE:
            current_spawn_rate = self.spawn_rate
        else:
            # Calculate dynamic spawn rate based on time (gets faster over time)
            difficulty_multiplier = max(0.6, 1 - (self.time_elapsed / 600))  # 10 minutes to reach max difficulty
            current_spawn_rate = ASTEROID_SPAWN_RATE * difficulty_multiplier
        
        if self.spawn_timer > current_spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            
            # Speed increases with level-based multiplier or time
            base_speed_min = 40 + int(self.time_elapsed / 20)  # +1 every 20 seconds
            base_speed_max = 100 + int(self.time_elapsed / 15)  # +1 every 15 seconds
            speed = random.randint(min(base_speed_min, 80), min(base_speed_max, 150))
            
            # Apply level-based speed multiplier if available
            if hasattr(self, 'speed_multiplier'):
                speed = int(speed * self.speed_multiplier)
            
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            
            # Bias towards larger asteroids over time, but still spawn smaller ones
            if self.time_elapsed > 60:  # After 1 minute, start favoring larger asteroids
                kind_weights = [3, 2, 1]  # Favor smaller asteroids less
            else:
                kind_weights = [1, 1, 1]  # Equal probability
                
            kind = random.choices([1, 2, 3], weights=kind_weights)[0]
            
            # 8% chance to spawn a word asteroid (not too often!)
            # Only spawn word asteroids for medium/large sizes (more readable)
            is_word = (kind >= 2) and (random.random() < 0.08)
            
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, is_word_asteroid=is_word)
