import math

from . import Scene


class Test3Scene(Scene):
    def update(self):
        test_object = self.get("test")
        test_object.x = 100 + 50 * math.sin(self.age)
