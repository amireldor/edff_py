from core.scene import Scene
from core.model import Model

from interesting.matos import Matos
from interesting.views import ViewMatos

class MainMenu(Scene):

    def __init__(self):
        Scene.__init__(self)

    def update(self, dt):
        Scene.update(self, dt)


class Game(Scene):

    def __init__(self):
        Scene.__init__(self)

        matos = Matos()
        view_matos = ViewMatos()
        view_matos.actors.append(matos)

        self.models.append(matos)
        self.views.append(view_matos)

    def update(self, dt):
        Scene.update(self, dt)
