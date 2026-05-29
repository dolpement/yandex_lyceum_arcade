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


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_list = None
        self.item_list= None
        self.enemy_list = None
        self.score = 0
        self.score_text = None
        self.item_timer = 0
        self.enemy_timer = 0
        self.collect_sound = None
        self.hit_sound = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.player_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.player_list.append(self.player)
        self.score = 0
        self.item_timer = 0
        self.enemy_timer = 0
        self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit2.wav")

    def on_draw(self):
        self.cler()
        self.player_list.draw()
        self.item_list.draw()
        self.enemy_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)

    def on_update(self, delta_time):
        self.player.center_x += self.player.change_x * delta_time
        if self.player.center_x < 20:
            self.player.center_x = 20
        elif self.player.center_x > SCREEN_WIDTH - 20:
            self.player.center_x = SCREEN_WIDTH - 20

        self.player.center_x += self.player.change_x * delta_time
        if self.player.center_x < 20:
            self.player.center_x = 20
        elif self.player.center_x > SCREEN_WIDTH - 20:
            self.player.center_x = SCREEN_WIDTH - 20

        for item in self.item_list:
            item.center_y += item.change_y * delta_time
            if item.center_y < -20:
                item.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            enemy.center_y += enemy.change_y * delta_time
            if enemy.center_y < -20:
                enemy.remove_from_sprite_lists()

        items_hit = arcade.check_for_collision_with_list(self.player, self.item_list)
        for item in items_hit:
            item.remove_from_sprite_lists()
            self.score += 10
            arcade.play_sound(self.collect_sound)

        enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        if enemies_hit:
            arcade.play_sound(self.hit_sound)
            game_over = GameOverView(self.score)
            self.window.show_view(game_over)
            return

        self.item_timer += delta_time
        if self.item_timer >= ITEM_SPAWN_TIME:
            self.item_timer = 0
            item = Item()
            self.item_list.append(item)

        self.enemy_timer += delta_time
        if self.enemy_timer >= ENEMY_SPAWN_TIME:
            self.enemy_timer = 0
            enemy = Enemy()
            self.enemy_list.append(enemy)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == '__main__':
    main()