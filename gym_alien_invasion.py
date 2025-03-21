import gym
import numpy as np
from gym import spaces
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
import game_functions as gf
from scoreboard import Scoreboard

class AlienInvasionEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(AlienInvasionEnv, self).__init__()

        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats)
        self.ship = Ship(self.settings, self.screen)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        gf.create_fleet(self.settings, self.screen, self.ship, self.aliens)

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)

    def reset(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.ship.center_ship()
        self.bullets.empty()
        self.aliens.empty()
        gf.create_fleet(self.settings, self.screen, self.ship, self.aliens)
        return self._get_state()

    def step(self, action):
        reward = -0.01  
        done = False

        if action == 0:  
            self.ship.moving_left = True
            self.ship.moving_right = False
            reward += 0.2 
        elif action == 1: 
            self.ship.moving_right = True
            self.ship.moving_left = False
            reward += 0.3  
        elif action == 2:  
            self.ship.shoot(self.bullets)
            reward += 0.5  
        elif action == 3: 
            reward -= 0.01 
        
        if self.ship.rect.centerx < self.settings.screen_width // 3:
            reward -= 0.5
        elif self.ship.rect.centerx > 2 * self.settings.screen_width // 3:
            reward -= 0.4 
        else:
            reward += 0.1  

        
        reward += 0.05  

        
        self.ship.update()
        gf.update_bullets(self.settings, self.screen, self.stats, None, self.ship, self.aliens, self.bullets)
        gf.update_aliens(self.settings, self.stats, self.screen, self.ship, self.aliens, self.bullets)

        
        if not self.stats.game_active:
            done = True
            reward -= 50  

        
        reward += self.stats.score / 100.0  

        return self._get_state(), reward, done, {}

    def render(self, mode="human"):
        
        self.screen.fill(self.settings.bg_color) 
        gf.update_screen(self.settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets, None)
        pygame.display.flip()  

    def _get_state(self):
       
        if len(self.aliens) > 0:
            closest_alien = min(self.aliens, key=lambda alien: alien.rect.y)
            alien_x = closest_alien.rect.x / self.settings.screen_width
            alien_y = closest_alien.rect.y / self.settings.screen_height
        else:
            alien_x, alien_y = 0, 0  

        return np.array([
            self.ship.rect.centerx / self.settings.screen_width,  
            len(self.bullets) / 3.0,  
            len(self.aliens) / 50.0,  
            self.stats.score / 10000.0,  
            alien_x,  
            alien_y,  
            self.stats.ships_left / 3.0, 
        ], dtype=np.float32)