import arcade
import random
from settings import *

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/enemy.png", ENEMY_SCALE)
        
        # Set random direction/speed
        self.change_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.change_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        
    def update(self, *args, **kwargs):
        """ Move the enemy and bounce off walls """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Bounce off edges of screen
        if self.left < 0:
            self.change_x *= -1
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.change_x *= -1
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.change_y *= -1
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1
            self.top = SCREEN_HEIGHT
