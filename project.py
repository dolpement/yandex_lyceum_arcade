import arcade 
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Collector"

PLAYER_SCALING = 0.8
ITEM_SCALING = 0.6 
ENEMY_SCALING = 0.7

PLAYER_SPEED = 300
ITEM_SPEED = 150
ENEMY_SPEED = 100

ITEM_SPAWN_TIME = 1.0
ENEMY_SPAWN_TIME = 2.0

HIGHSCORE_FILE = "highscore.txt"


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png", PLAYER_SCALING)
        self.centeer_x = SCREEN_WIDTH // 2
        self.center_y = 50
        self.change_x = 0


class Item(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/items/star.png", ITEM_SCALING)
        self.center_x = random.randint(20, SCREEN_WIDTH - 20)
        self.center_y = SCREEN_HEIGHT + 20
        self.change_y = -ITEM_SCALING


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/meteorGrey_big1.png", ENEMY_SCALING)
        self.center_x = random.randint(20, SCREEN_WIDTH - 20)
        self.center_y = SCREEN_HEIGHT + 20
        self.change_y = -ENEMY_SCALING


class StartView(arcade.View):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/meteorGrey_big1.png", ENEMY_SCALING)
        self.backgroung = None

    def on_show(self):
        arcade.set_bacground_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("SPACE COLLECTOR", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                         arcade.color.WHITE, 48, anchor_x="center")
        arcade.draw_text("Collect stars, avoid meteors!", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250,
                         arcade.color.YELLOW, 24, anchor_x="center")
        arcade.draw_text("Press SPACE to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.GREEN, 28, anchor_x="center")
        arcade.draw_text("Use LEFT / RIGHT arrows to move", SCREEN_WIDTH // 2, 100,
                         arcade.color.WHITE, 18, anchor_x="center")
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == '__main__':
    main()