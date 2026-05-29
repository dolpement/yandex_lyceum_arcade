import arcade
from arcade.gui import UIManager, UIFlatButton, UIAnchorLayout, UIBoxLayout, UILabel
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_view import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()

        anchor = UIAnchorLayout()
        box = UIBoxLayout(vertical=True, space_between=20)

        title = UILabel(text="PLATFORMER ADVENTURE", font_size=48, text_color=arcade.color.YELLOW)
        box.add(title)

        start_btn = UIFlatButton(text="Start Game", width=250, height=60)
        start_btn.on_click = self.start_game
        box.add(start_btn)

        anchor.add(box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def start_game(self, event):
        game_view = GameView(level_num=1)
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = UIManager()
        self.manager.enable()

        anchor = UIAnchorLayout()
        box = UIBoxLayout(vertical=True, space_between=20)

        resume_btn = UIFlatButton(text="Resume", width=200, height=50)
        resume_btn.on_click = self.resume_game
        box.add(resume_btn)

        quit_btn = UIFlatButton(text="Quit to Menu", width=200, height=50)
        quit_btn.on_click = self.quit_to_menu
        box.add(quit_btn)

        anchor.add(box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def resume_game(self, event):
        self.window.show_view(self.game_view)

    def quit_to_menu(self, event):
        start_view = StartView()
        self.window.show_view(start_view)

    def on_draw(self):
        self.clear()
        self.game_view.on_draw()
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 400, 200, (0, 0, 0, 180))
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.highscore = self._load_highscore()
        if score > self.highscore:
            self._save_highscore(score)
            self.highscore = score
        self.manager = UIManager()
        self.manager.enable()

        anchor = UIAnchorLayout()
        box = UIBoxLayout(vertical=True, space_between=15)

        title = UILabel(text="GAME OVER", font_size=48, text_color=arcade.color.RED)
        box.add(title)

        score_label = UILabel(text=f"Your score: {score}", font_size=24)
        box.add(score_label)

        highscore_label = UILabel(text=f"Highscore: {self.highscore}", font_size=24)
        box.add(highscore_label)

        retry_btn = UIFlatButton(text="Play Again", width=200, height=50)
        retry_btn.on_click = self.retry_game
        box.add(retry_btn)

        quit_btn = UIFlatButton(text="Quit", width=200, height=50)
        quit_btn.on_click = self.quit_game
        box.add(quit_btn)

        anchor.add(box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def retry_game(self, event):
        game_view = GameView(level_num=1)
        self.window.show_view(game_view)

    def quit_game(self, event):
        start_view = StartView()
        self.window.show_view(start_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def _load_highscore(self):
        import os
        import json
        if os.path.exists("highscore.json"):
            with open("highscore.json", 'r') as f:
                return json.load(f).get("highscore", 0)
        return 0

    def _save_highscore(self, score):
        import json
        with open("highscore.json", 'w') as f:
            json.dump({"highscore": score}, f)