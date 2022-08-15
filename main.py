import arcade
import random
import os

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "RunGames"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1        # здесь менятся размер персонажа
TILE_SCALING = 0.5          # здесь менятся размер растения
MONEY_SCALING = 0.5         # здесь менятся размер монетки

# скорость игрока
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1                 # гравитация
PLAYER_JUMP_SPEED = 16      # высота прыжка


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.laser_sound = arcade.load_sound("No More Magic.mp3")         # загружает песню
        arcade.play_sound(self.laser_sound)                               # проигрывает песню

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None                                                                 # камера показывает сколько счета

        # Keep track of the score
        self.check = 0                                                                         # счет = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin5.wav")             # загрузка музыки для сбора монет
        self.jump_sound = arcade.load_sound(":resources:sounds/jump4.wav")                     # загрузка музыки для прыжка

        # фон
        self.background = None

        #self.setup()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.background = arcade.load_texture("Background1.png")           # загрузка фона

        # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)
        # Set up the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Keep track of the score
        self.check = 0

        # Initialize Scene
        self.scene = arcade.Scene()

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/Stop.png"      #загрузка текстуры персонажа
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64        # координаты персонажа
        self.player_sprite.center_y = 100
        self.scene.add_sprite("Player", self.player_sprite)


        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images Tiles/Tile_02.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 100              # тут меняется координаты растения
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[509, 160], [256, 160], [768, 160]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images Tiles/36.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            money = arcade.Sprite("Images Money/Gold_21.png")
            money.center_x = x
            money.center_y = 150                    #тут изменить координаты монетки
            self.scene.add_sprite("Money", money)

            # Create the 'physics engine'
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
            )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # зарисовка фона
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Activate our Camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        check_text = f"CHECK: {self.check}"                                      # расположение текста и его размер и свет
        arcade.draw_text(
            check_text,
            20,
            20,
            arcade.csscolor.YELLOW,
            10,
        )


    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed."""

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)                         # проигрывает песню при прыжке

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


    def on_update(self, delta_time):

        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # See if we hit any coins
        money_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Money"]
        )

        # Loop through each coin we hit (if any) and remove it
        for money in money_hit_list:
            # Remove the coin
            money.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.check += 5                                                             # размер монет, когда собирает персонаж

        # Position the camera
        self.center_camera_to_player()

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()