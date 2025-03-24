import gym
import numpy as np
import pygame
from gym import spaces

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
import game_functions as gf
from scoreboard import Scoreboard

class AlienInvasionEnv(gym.Env):
    """ OpenAI Gym environment for an Alien Invasion game. """
    
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(AlienInvasionEnv, self).__init__()

        pygame.init()

        # Initialize game settings
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats)
        self.ship = Ship(self.settings, self.screen)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create alien fleet
        gf.create_fleet(self.settings, self.screen, self.ship, self.aliens)

        # Define action space (0: left, 1: right, 2: shoot, 3: do nothing)
        self.action_space = spaces.Discrete(4)

        # Define observation space (normalized game state)
        self.observation_space = spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)

    def reset(self):
        """ Resets the game to the initial state. """
        self.stats.reset_stats()
        self.stats.game_active = True
        self.ship.center_ship()
        self.bullets.empty()
        self.aliens.empty()
        gf.create_fleet(self.settings, self.screen, self.ship, self.aliens)
        return self._get_state()

    def step(self, action):
        """ Updates the game state based on the action taken. """
        reward = -0.01  
        done = False

        # Handle player actions
        if action == 0:  # Move left
            self.ship.moving_left = True
            self.ship.moving_right = False
            reward += 0.2
        elif action == 1:  # Move right
            self.ship.moving_right = True
            self.ship.moving_left = False
            reward += 0.3
        elif action == 2:  # Shoot
            self.ship.shoot(self.bullets)
            reward += 0.5
        elif action == 3:  # Do nothing
            reward -= 0.01  

        # Encourage staying near the center of the screen
        ship_x = self.ship.rect.centerx
        screen_width = self.settings.screen_width

        if ship_x < screen_width // 3:
            reward -= 0.5  # Penalize for being too far left
        elif ship_x > 2 * screen_width // 3:
            reward -= 0.4  # Penalize for being too far right
        else:
            reward += 0.1  # Small reward for staying near the center

        reward += 0.05  # Constant small reward for staying active

        # Update game elements
        self.ship.update()
        gf.update_bullets(self.settings, self.screen, self.stats, None, self.ship, self.aliens, self.bullets)
        gf.update_aliens(self.settings, self.stats, self.screen, self.ship, self.aliens, self.bullets)

        # Check if game over
        if not self.stats.game_active:
            done = True
            reward -= 50  # Big penalty for losing

        # Reward based on score
        reward += self.stats.score / 100.0

        return self._get_state(), reward, done, {}

    def render(self, mode="human"):
        """ Renders the game screen. """
        self.screen.fill(self.settings.bg_color) 
        gf.update_screen(self.settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets, None)
        pygame.display.flip()  

    def _get_state(self):
        """ Returns the current game state as a normalized observation. """
        if self.aliens:
            closest_alien = min(self.aliens, key=lambda alien: alien.rect.y)
            alien_x = closest_alien.rect.x / self.settings.screen_width
            alien_y = closest_alien.rect.y / self.settings.screen_height
        else:
            alien_x, alien_y = 0, 0  

        return np.array([
            self.ship.rect.centerx / self.settings.screen_width,  # Ship position
            len(self.bullets) / 3.0,  # Number of bullets on screen
            len(self.aliens) / 50.0,  # Number of aliens remaining
            self.stats.score / 10000.0,  # Scaled score
            alien_x,  # Closest alien's X position
            alien_y,  # Closest alien's Y position
            self.stats.ships_left / 3.0,  # Number of ships left
        ], dtype=np.float32)
