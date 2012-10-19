from core.model import Model

class Scene(Model):

    def __init__(self):
        Model.__init__(self)
        self.models = []

    def update(self, dt):
        for x in self.models:
            x.update()
