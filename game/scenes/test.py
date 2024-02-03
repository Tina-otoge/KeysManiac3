import time

import pyglet
from pyglet.image import SolidColorImagePattern
from pyglet.media import StaticSource
from pyglet.sprite import Sprite

from game import colors

from . import Scene


class Cookie(Sprite):
    def __init__(self, x=0, y=0, width=0, height=0, **kwargs):
        color = kwargs.get("color", colors.PINK)
        if len(color) == 3:
            color = (*color, 255)
        image = SolidColorImagePattern(color).create_image(width, height)
        image.anchor_x = width // 2
        image.anchor_y = height // 2
        super().__init__(img=image, x=x, y=y, **kwargs)
        self.rotation = 45
        self.velocity = 10

    def update(self, dt):
        self.rotation += self.velocity * dt
        if self.velocity > 10:
            self.velocity -= 200 * dt
        self.velocity = max(10, self.velocity)


class TestScene(Scene):
    def start(self):
        self.cookie = Cookie(
            self.game.window.width // 2,
            self.game.window.height // 2,
            200,
            200,
        )
        self.objects.append(self.cookie)
        self.last_gong = time.time()
        self.gong = StaticSource(
            pyglet.resource.media("taiko-drum-hitnormal.wav")
        )

    def update(self):
        now = time.time()
        gong_dt = now - self.last_gong
        if gong_dt > 1:
            self.last_gong = now
            self.gong.play()
            self.cookie.velocity = 100
        self.cookie.update(self.dt)
