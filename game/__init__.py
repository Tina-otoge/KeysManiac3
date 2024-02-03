import pyglet
from pyglet.window import Window

from game.scenes import Scene


class Game:
    def __init__(self):
        print("Game created")
        self.window = Window()
        self.window.event(self.on_draw)
        self.scene = None
        Scene.prepare()
        pyglet.resource.path = ["game/resources"]
        pyglet.resource.reindex()
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def start(self):
        print("Game started")
        pyglet.app.run()

    def load_scene(self, scene_name):
        print(f"Loading scene {scene_name}")
        self.scene = Scene.create(self, scene_name)

    def on_draw(self):
        self.window.clear()
        if not self.scene:
            return
        self.scene.draw()

    def update(self, dt):
        if not self.scene:
            return
        self.scene._update(dt)
