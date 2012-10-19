from core.scene import Scene
from core.model import Model

class MainMenu(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)
        print "Choose", range(1, 4)

        return [Model.REMOVE, Game()]


class Game(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)
        print "Lousy Man"
