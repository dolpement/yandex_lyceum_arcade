import arcade
import random
from arcade.particles import FadeParticle, Emitter, EmitBurst


def make_dust_emitter(x, y):
    texture = arcade.make_soft_circle_texture(8, (200, 200, 200, 180))
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(8),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=texture,
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 1.5),
            lifetime=random.uniform(0.3, 0.7),
            start_alpha=180, end_alpha=0,
            scale=random.uniform(0.3, 0.6),
        ),
    )


def make_explosion_emitter(x, y):
    textures = [
        arcade.make_soft_circle_texture(12, arcade.color.ORANGE_RED),
        arcade.make_soft_circle_texture(10, arcade.color.YELLOW),
    ]
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(25),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(textures),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 5.0),
            lifetime=random.uniform(0.5, 1.0),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.4, 0.8),
        ),
    )