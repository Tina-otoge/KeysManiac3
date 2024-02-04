import importlib
import time
from pathlib import Path

import tomli
from pyglet.graphics import Batch

import strings
from game.grid import Grid


class Scene:
    scenes = {}

    def __init__(self, game):
        self.game = game
        self.refs = {}
        self.objects = []
        self.batch = Batch()
        self.grid = Grid(self.game.window, 100, 100, batch=self.batch)
        scene_file = (Path(__file__).parent / self.key).with_suffix(".toml")
        if scene_file.exists():
            self.load_from_file(scene_file)
        self.start()
        for obj in self.objects:
            obj.batch = self.batch
        self.start_time = time.time()

    def __init_subclass__(cls):
        key = cls.__name__
        key = key.rstrip("Scene")
        key = strings.camel_to_snake(key)
        cls.key = key
        cls.scenes[cls.key] = cls

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

    def get(self, key):
        return self.refs[key]

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

    def load_from_file(self, path):
        with path.open("rb") as f:
            data = tomli.load(f)
        for object in data.get("objects", []):
            object_type = object["type"]
            types = {
                "rectangle": "pyglet.shapes/Rectangle",
            }
            module = types.get(object_type)
            module, cls = module.split("/")
            module = importlib.import_module(module)
            color = object.get("color")
            if color:
                if isinstance(color, str) and color[0].isalpha:
                    color_module = importlib.import_module("game.colors")
                    color = getattr(color_module, color.upper())
            if len(color) == 3:
                color = (*color, 255)
            cls = getattr(module, cls)
            drawable = cls(
                x=object["x"],
                y=object["y"],
                width=object["w"],
                height=object["h"],
                color=color,
            )
            self.objects.append(drawable)
            name = object.get("name")
            if name:
                self.refs[name] = drawable
