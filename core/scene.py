from core.model import Model
from core.view import View

class Scene():
    """A scene holds references to objects which are "in the game" playing with you now."""

    def __init__(self):
        self.models = []
        self.views = []

    def update(self, dt):
        for x in self.models:
            x.update(dt)

    def render(self, screen):
        for view in self.views:
            view.render_all(screen)
