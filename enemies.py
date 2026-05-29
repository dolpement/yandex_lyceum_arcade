import arcade
import random
from constants import ENEMY_SCALING


class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/space_shooter/meteorGrey_big1.png", ENEMY_SCALING)
        self.center_x = x
        self.center_y = y
        self.change_x = random.choice([-1, 1]) * 80
        self.boundary_left = x - 200
        self.boundary_right = x + 200

    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        if self.center_x <= self.boundary_left:
            self.center_x = self.boundary_left
            self.change_x = abs(self.change_x)
        elif self.center_x >= self.boundary_right:
            self.center_x = self.boundary_right
            self.change_x = -abs(self.change_x)