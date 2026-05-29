import arcade
import random
import json
import os
from arcade.camera import Camera2D
from constants import *
from player import Player
from enemies import Enemy
from particles import make_dust_emitter, make_explosion_emitter


class GameView(arcade.View):
    def __init__(self, level_num=1):
        super().__init__()
        self.level_num = level_num
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()
        self.emitters = []

        self.player_list = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.platforms = arcade.SpriteList()
        self.ladders = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

        self.player = Player()
        self.player_list.append(self.player)

        self.engine = None

        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0

        self.score = 0
        self.coins_collected = 0
        self.total_coins = 0

        self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.enemy_hit_sound = arcade.load_sound(":resources:sounds/hit2.wav")
        self.level_complete_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.fall_sound = arcade.load_sound(":resources:sounds/hurt3.wav")

        self.setup_level()

    def setup_level(self):
        self.walls.clear()
        self.platforms.clear()
        self.ladders.clear()
        self.coins.clear()
        self.enemies.clear()
        self.emitters.clear()

        if self.level_num == 1:
            self._build_level1()
        else:
            self._build_level2()

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.walls,
            platforms=self.platforms,
            ladders=self.ladders
        )

    def _build_level1(self):
        for x in range(0, SCREEN_WIDTH + 400, 64):
            tile = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            tile.center_x = x
            tile.center_y = 64
            self.walls.append(tile)

        plat = arcade.Sprite(":resources:images/tiles/grassHalf.png", TILE_SCALING)
        plat.center_x = 500
        plat.center_y = 200
        self.walls.append(plat)

        plat2 = arcade.Sprite(":resources:images/tiles/grassHalf.png", TILE_SCALING)
        plat2.center_x = 800
        plat2.center_y = 300
        self.walls.append(plat2)

        for y in range(64, 400, 64):
            ladder = arcade.Sprite(":resources:images/tiles/ladderMid.png", TILE_SCALING)
            ladder.center_x = 1100
            ladder.center_y = y
            self.ladders.append(ladder)

        for x in range(1000, 1201, 64):
            top = arcade.Sprite(":resources:images/tiles/grassHalf.png", TILE_SCALING)
            top.center_x = x
            top.center_y = 420
            self.walls.append(top)

        for x in [400, 450, 500, 550]:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.4)
            coin.center_x = x
            coin.center_y = 150
            self.coins.append(coin)

        for x in [750, 800, 850]:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.4)
            coin.center_x = x
            coin.center_y = 250
            self.coins.append(coin)

        for x in [1050, 1100, 1150]:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.4)
            coin.center_x = x
            coin.center_y = 370
            self.coins.append(coin)

        enemy = Enemy(600, 150)
        self.enemies.append(enemy)

        self.player.center_x = 200
        self.player.center_y = 120

        self.total_coins = len(self.coins)
        self.coins_collected = 0

    def _build_level2(self):
        for x in range(0, SCREEN_WIDTH + 600, 64):
            tile = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            tile.center_x = x
            tile.center_y = 64
            self.walls.append(tile)

        for i, y in enumerate([150, 220, 290, 360, 430]):
            plat = arcade.Sprite(":resources:images/tiles/grassHalf.png", TILE_SCALING)
            plat.center_x = 400 + i * 80
            plat.center_y = y
            self.walls.append(plat)

        for x in range(900, 1400, 64):
            plat = arcade.Sprite(":resources:images/tiles/grassHalf.png", TILE_SCALING)
            plat.center_x = x
            plat.center_y = 350
            self.walls.append(plat)

        for i in range(5):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.4)
            coin.center_x = 430 + i * 80
            coin.center_y = 200 + i * 70
            self.coins.append(coin)

        for x in range(950, 1350, 70):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.4)
            coin.center_x = x
            coin.center_y = 400
            self.coins.append(coin)

        for x in [1050, 1150, 1250]:
            enemy = Enemy(x, 290)
            self.enemies.append(enemy)

        self.player.center_x = 200
        self.player.center_y = 120

        self.total_coins = len(self.coins)
        self.coins_collected = 0

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.walls.draw()
        self.platforms.draw()
        self.ladders.draw()
        self.coins.draw()
        self.enemies.draw()
        self.player_list.draw()
        for e in self.emitters:
            e.draw()

        self.gui_camera.use()
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)
        arcade.draw_text(f"Level: {self.level_num}", 10, SCREEN_HEIGHT - 55, arcade.color.WHITE, 16)
        arcade.draw_text(f"Coins: {self.coins_collected}/{self.total_coins}", 10, SCREEN_HEIGHT - 80, arcade.color.YELLOW, 16)
        arcade.draw_text("ESC - pause", SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30, arcade.color.GRAY, 12)

    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
            self.player.face_direction = -1
        elif self.right and not self.left:
            move = MOVE_SPEED
            self.player.face_direction = 1
        self.player.change_x = move

        on_ladder = self.engine.is_on_ladder()
        if on_ladder:
            if self.up and not self.down:
                self.player.change_y = LADDER_SPEED
            elif self.down and not self.up:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0

        self.player.is_walking = move != 0
        self.player.update_animation(delta_time)

        grounded = self.engine.can_jump(y_distance=10)
        if grounded:
            self.time_since_ground = 0
        else:
            self.time_since_ground += delta_time

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)
        if want_jump and (grounded or self.time_since_ground <= COYOTE_TIME):
            self.engine.jump(JUMP_SPEED)
            self.jump_buffer_timer = 0
            self.jump_sound.play(volume=0.6)
            dust = make_dust_emitter(self.player.center_x, self.player.center_y - 20)
            self.emitters.append(dust)

        self.engine.update()

        if self.player.center_y < -100:
            self.fall_sound.play()
            self.score = max(0, self.score - 30)
            self.player.center_x = 200
            self.player.center_y = 120
            self.player.change_x = 0
            self.player.change_y = 0
            self.time_since_ground = 999
            return

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coins)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 10
            self.coins_collected += 1
            self.coin_sound.play(volume=0.5)

        if self.coins_collected >= self.total_coins and self.total_coins > 0:
            if self.level_num == 1:
                self.level_complete_sound.play()
                next_level = GameView(level_num=2)
                self.window.show_view(next_level)
            else:
                highscore = self._load_highscore()
                if self.score > highscore:
                    self._save_highscore(self.score)
                from views import GameOverView
                game_over = GameOverView(self.score)
                self.window.show_view(game_over)
            return

        enemies_hit = arcade.check_for_collision_with_list(self.player, self.enemies)
        for enemy in enemies_hit:
            enemy.remove_from_sprite_lists()
            self.score = max(0, self.score - 20)
            self.enemy_hit_sound.play()
            explosion = make_explosion_emitter(enemy.center_x, enemy.center_y)
            self.emitters.append(explosion)

        for enemy in self.enemies:
            enemy.update(delta_time)

        for e in self.emitters:
            e.update(delta_time)
        self.emitters = [e for e in self.emitters if not e.can_reap()]

        target_x = self.player.center_x
        target_y = self.player.center_y
        cx, cy = self.world_camera.position
        smooth_x = cx + (target_x - cx) * CAMERA_LERP
        smooth_y = cy + (target_y - cy) * CAMERA_LERP

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2
        world_w = SCREEN_WIDTH + 600
        world_h = SCREEN_HEIGHT + 500
        cam_x = max(half_w, min(world_w - half_w, smooth_x))
        cam_y = max(half_h, min(world_h - half_h, smooth_y))
        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER
        elif key == arcade.key.ESCAPE:
            from views import PauseView
            pause_view = PauseView(self)
            self.window.show_view(pause_view)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.5

    def _load_highscore(self):
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, 'r') as f:
                return json.load(f).get("highscore", 0)
        return 0

    def _save_highscore(self, score):
        with open(RECORD_FILE, 'w') as f:
            json.dump({"highscore": score}, f)