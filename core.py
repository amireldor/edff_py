class Removable(object):
    def __init__(self):
        self.keep = True

    def dont_keep(self):
        self.keep = False

    def should_keep(self):
        return self.keep


class Model(Removable):
    def __init__(self):
        Removable.__init__(self)

    def update(self, dt):
        pass

class View(Removable):
    def __init__(self):
        Removable.__init__(self)
        self.models = []

    def render(self, screen):
        pass

class Scene(object): # TODO: Maybe Scene()s should be Removable too
    def __init__(self):
        self.models = []
        self.views = []

    def update(self, dt):
        for model in self.models:
            model.update(dt)

        self.models[:] = [ m for m in self.models if m.should_keep() ]

    def render(self, screen):
        for view in self.views:
            view.render(screen)

        self.views[:] = [ v for v in self.views if v.should_keep() ]

class Controller(object):
    def __init__(self):
        self.controllers = []

    def control(self):
        for controller in self.controllers:
            controller.control()

        self.controller[:] = [ c for c in self.controllers if c.should_keep() ]

class ConcreteController(object):
    def __init__(self, scene):
        self.scene = scene

    def control(self):
        pass

class KeyboardController(ConcreteController):
    def __init__(self, scene):
        ConcreteController.__init__(self, scene)

    def control(self, key):
        pass

#class MouseController(object):
#    pass
