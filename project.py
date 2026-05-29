import arcade 
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Collector"

PLAYER_SCALING = 0.8
ITEM_SCALING = 0.6 
ENEMY_SCALING = 0.7


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