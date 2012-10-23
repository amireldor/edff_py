from core.model import Model
from core.view import View

class Scene():
    """A scene holds references to objects which are "in the game" playing with you now."""

    REMOVE = 1

    def __init__(self):
        self.models = []
        self.views = []

    def update(self, dt):
        for model in self.models:
            model.update(dt)

        # remove obsolete models
        new_models = self.models
        for model in self.models:
            if model.should_remove():
                new_models.remove(model)
        self.models = new_models

    def render(self, screen):
        for view in self.views:
            view.render_all(screen)
