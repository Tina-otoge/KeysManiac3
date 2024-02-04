from pyglet.shapes import Rectangle

from . import Scene


class Test2Scene(Scene):
    def start(self):
        self.grid.add(Rectangle, 10, 10, 10, 10)
