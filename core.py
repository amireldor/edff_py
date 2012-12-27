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

    def append(self, model):
        self.models.append(model)

    def remove_old(self):
        """ Remove models which should not be kept """
        self.models[:] = [ m for m in self.models if m.should_keep() ]

    def render(self, screen):
        self.remove_old()

class Scene(object): # TODO: Maybe Scene()s should be Removable too
    def __init__(self, scene_manager):
        self.models = []
        self.views = []
        self.scene_manager = scene_manager
        self.active = True
        self.__active_toggle = False # will toggle the active state upon next update

    def activate(self, state=True):
        """Will active or deactivate the scene upon next `update()` (don't
        forget to call my update method when you subclass me)"""
        if (state is True and not self.is_active()) or (state is False and self.is_active()):
            self.__active_toggle = True

    def is_active(self):
        return self.active

    def on_event(self, event):
        pass

    def update(self, dt):
        if self.__active_toggle:
            self.active = not self.active
            self.__active_toggle = False

        if not self.is_active():
            return

        for model in self.models:
            model.update(dt)

        self.models[:] = [ m for m in self.models if m.should_keep() ]

    def render(self, screen):
        for view in self.views:
            view.render(screen)

        self.views[:] = [ v for v in self.views if v.should_keep() ]

class SceneManager(object):
    def __init__(self):
        self.scenes = []

    def append(self, scene):
        self.scenes.append(scene)

#    def next(self):
#        self.scenes.pop(0) # pop first item

    def on_event(self, event):
        for s in self.scenes:
            s.on_event(event)

    def update(self, dt):
        for s in self.scenes:
            s.update(dt)

    def render(self, screen):
        for s in self.scenes:
            s.render(screen)
