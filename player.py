import arcade
from constants import PLAYER_SCALING


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=PLAYER_SCALING)
        self.idle_texture = arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")
        self.walk_textures = []
        for i in range(8):
            tex = arcade.load_texture(f":resources:images/animated_characters/female_person/femalePerson_walk{i}.png")
            self.walk_textures.append(tex)

        self.texture = self.idle_texture
        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.08
        self.is_walking = False
        self.face_direction = 1

    def update_animation(self, delta_time):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture = (self.current_texture + 1) % len(self.walk_textures)
                tex = self.walk_textures[self.current_texture]
                if self.face_direction == -1:
                    tex = tex.flip_horizontally()
                self.texture = tex
        else:
            tex = self.idle_texture
            if self.face_direction == -1:
                tex = tex.flip_horizontally()
            self.texture = tex