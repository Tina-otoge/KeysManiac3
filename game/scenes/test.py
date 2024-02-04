import random
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
        self.particles = []

    def update(self, dt):
        self.rotation += self.velocity * dt
        if self.velocity > 10:
            self.velocity -= 200 * dt
        self.velocity = max(10, self.velocity)

        for particle in self.particles:
            particle.update(dt)

    def draw(self):
        super().draw()
        for particle in self.particles:
            if not particle.alive:
                self.particles.remove(particle)
                del particle
                continue

            particle.draw()

    def spawn_particles(self):
        for _ in range(10):
            particle = Particle(self.x, self.y)
            self.particles.append(particle)


class Particle(Sprite):
    def __init__(self, x, y):
        width, height = 5, 5
        color = (*colors.WHITE, 255)
        image = SolidColorImagePattern(color).create_image(width, height)
        image.anchor_x = width // 2
        image.anchor_y = height // 2
        super().__init__(img=image, x=x, y=y)
        self.dx = random.uniform(-50, 50)
        self.dy = random.uniform(50, 150)
        self.birth = time.time()

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy -= 100 * dt
        self.opacity = 255 * (1 - self.age / 3)

    @property
    def age(self):
        return time.time() - self.birth

    @property
    def alive(self):
        return self.age < 3


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
            self.cookie.spawn_particles()
        self.cookie.update(self.dt)
