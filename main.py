import arcade
import random
from settings import *
from player import Player
from enemy import Enemy

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """ Class Constructor """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.coin_list = None
        self.player_list = None
        self.enemy_list = None 

        self.player_sprite = None
        self.physics_engine = None

        self.score = 0
        self.level = 1
        self.game_over = False

        # Load Sounds
        self.coin_sound = arcade.load_sound("assets/coin.wav")
        self.hit_sound = arcade.load_sound("assets/hit.wav")
        self.gameover_sound = arcade.load_sound("assets/gameover.wav")

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        
        self.game_over = False
        
        # Don't reset score if leveling up, but if we wanted a full restart we could.
        # For now, let's keep score across levels.
        if self.level == 1:
            self.score = 0
            
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # -- Set up the walls --
        # Increase walls per level?
        num_walls = 15 + (self.level * 2) 
        
        for i in range(num_walls):
            wall = arcade.Sprite("assets/wall.png", WALL_SCALE)
            wall.center_x = random.randrange(SCREEN_WIDTH)
            wall.center_y = random.randrange(SCREEN_HEIGHT)
            
            # Simple check to ensure wall isn't on top of player
            if arcade.check_for_collision(wall, self.player_sprite):
                 continue
            self.wall_list.append(wall)

        # Create border walls
        for x in range(0, SCREEN_WIDTH + 1, 32):
            wall_bottom = arcade.Sprite("assets/wall.png", WALL_SCALE)
            wall_bottom.center_x = x
            wall_bottom.center_y = 0
            self.wall_list.append(wall_bottom)
            
            wall_top = arcade.Sprite("assets/wall.png", WALL_SCALE)
            wall_top.center_x = x
            wall_top.center_y = SCREEN_HEIGHT
            self.wall_list.append(wall_top)

        for y in range(0, SCREEN_HEIGHT + 1, 32):
            wall_left = arcade.Sprite("assets/wall.png", WALL_SCALE)
            wall_left.center_x = 0
            wall_left.center_y = y
            self.wall_list.append(wall_left)

            wall_right = arcade.Sprite("assets/wall.png", WALL_SCALE)
            wall_right.center_x = SCREEN_WIDTH
            wall_right.center_y = y
            self.wall_list.append(wall_right)

        # -- Set up the coins --
        for i in range(COIN_COUNT):
            coin = arcade.Sprite("assets/coin.png", COIN_SCALE)

            coin_placed_successfully = False
            while not coin_placed_successfully:
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)

                wall_hit_list = arcade.check_for_collision_with_list(coin, self.wall_list)
                player_hit_list = arcade.check_for_collision_with_list(coin, self.player_list)

                if len(wall_hit_list) == 0 and len(player_hit_list) == 0:
                    coin_placed_successfully = True

            self.coin_list.append(coin)

        # -- Set up Enemies --
        # More enemies per level
        num_enemies = ENEMY_COUNT + (self.level - 1)
        
        for i in range(num_enemies):
            enemy = Enemy()
            
            placed = False
            while not placed:
                enemy.center_x = random.randrange(SCREEN_WIDTH)
                enemy.center_y = random.randrange(SCREEN_HEIGHT)
                
                # Check collision with walls (optional, maybe enemies can fly over walls? lets keep them separate)
                wall_its = arcade.check_for_collision_with_list(enemy, self.wall_list)
                if len(wall_its) == 0 and arcade.get_distance_between_sprites(enemy, self.player_sprite) > 100:
                    placed = True
            
            self.enemy_list.append(enemy)


        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """ Render the screen. """
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.score}   Level: {self.level}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)
        
        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, arcade.color.RED, 40, width=200, align="center")
            arcade.draw_text("Click to Restart", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, arcade.color.WHITE, 20, width=200, align="center")

    def on_mouse_press(self, x, y, button, modifiers):
        """ Restart game on click if game over """
        if self.game_over:
            self.level = 1
            self.setup()

    def on_key_press(self, key, modifiers):
        if self.game_over:
            return
            
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S]:
            self.player_sprite.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        
        if self.game_over:
            return

        self.physics_engine.update()
        self.enemy_list.update()

        # Check for coin collection
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.coin_sound)
            
        # Check Level Completion
        if len(self.coin_list) == 0:
            self.level += 1
            self.setup()
            
        # Check Enemy Collision
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if len(enemy_hit_list) > 0:
            print("Collision detected! Game Over.")
            self.game_over = True
            arcade.play_sound(self.gameover_sound)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
