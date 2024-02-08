import pyglet
from pyglet.window import Window

from game.inputs import InputManager
from game.scenes import Scene


class Game:
    def __init__(self):
        print("Game created")
        self.window = Window()
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)
        self.window.event(self.on_key_release)
        self.scene = None
        Scene.prepare()
        pyglet.resource.path = ["game/resources"]
        pyglet.resource.reindex()
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.inputs = InputManager()

    def start(self):
        print("Game started")
        pyglet.app.run()

    def load_scene(self, scene_name):
        print(f"Loading scene {scene_name}")
        self.inputs.reset()
        self.scene = Scene.create(self, scene_name)

    def on_draw(self):
        self.window.clear()
        if not self.scene:
            return
        self.scene.draw()

    def on_key_press(self, symbol, modifiers):
        self.inputs.handle_key_press(symbol)

    def on_key_release(self, symbol, modifiers):
        self.inputs.handle_key_release(symbol)

    def update(self, dt):
        if not self.scene:
            return
        while raw_input := self.inputs.poll_raw():
            if self.scene.handle_raw_input(raw_input):
                self.inputs.reset_raw()
                break
        while input := self.inputs.poll():
            print(input)
            if self.scene.handle_input(input):
                self.inputs.reset_inputs()
                break
        self.scene._update(dt)
