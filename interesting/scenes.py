from core.scene import Scene
from core.model import Model

class MainMenu(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)


class Game(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)
