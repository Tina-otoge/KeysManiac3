import importlib
import time
from pathlib import Path

from pyglet.graphics import Batch

import strings
from game.grid import Grid


class Scene:
    scenes = {}

    def __init__(self, game):
        self.game = game
        self.objects = []
        self.batch = Batch()
        self.grid = Grid(self.game.window, 100, 100, batch=self.batch)
        self.start()
        for obj in self.objects:
            obj.batch = self.batch
        self.start_time = time.time()

    def __init_subclass__(cls):
        key = cls.__name__
        key = key.rstrip("Scene")
        key = strings.camel_to_snake(key)
        cls.scenes[key] = cls

    @classmethod
    def create(cls, game, scene_name):
        if scene_name not in cls.scenes:
            raise ValueError(f"No scene with name {scene_name}")
        return cls.scenes[scene_name](game)

    @staticmethod
    def prepare():
        for file in Path(__file__).parent.glob("*.py"):
            if file.stem == "__init__":
                continue
            importlib.import_module(f".{file.stem}", __package__)

    def start(self):
        pass

    def _update(self, dt):
        self.dt = dt
        self.age = time.time() - self.start_time
        self.update()

    def update(self):
        pass

    def draw(self):
        self.batch.draw()
        for obj in self.objects:
            obj.draw()

    def on_resize(self):
        self.grid.update()
