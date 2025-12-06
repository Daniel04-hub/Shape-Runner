import arcade
from settings import *

class Player(arcade.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__("assets/player.png", PLAYER_SCALE)
        
        # Position the player in the center of the screen initially
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

    def update(self):
        """ Move the player """
        # Move player.
        # This is strictly for simple movement WITHOUT a physics engine.
        # However, we will use a physics engine in main.py, which overrides this.
        # If we weren't using a physics engine, we'd do:
        # self.center_x += self.change_x
        # self.center_y += self.change_y
        
        # Keep player on screen (optional, if no walls)
        if self.left < 0:
            self.left = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
