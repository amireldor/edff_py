import collections

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

    def get_manager(self):
        return self.scene_manager

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
        """Append a scene to my stack of scenes! You can use `.next()` to move
        to the next scene. Append a list/iterable of scenes and you can have
        several scenes play around together at the same time! You don't have to
        use a single scene at a time anymore!"""
        self.scenes.append(scene)

    def next(self):
        self.scenes.pop(0) # pop first item

    def on_event(self, event):
        scene = self.scenes[0]
        if isinstance(scene, collections.Iterable):
            for s in scene:
                s.on_event(event)
        else:
            scene.on_event(event)

    def update(self, dt):
        scene = self.scenes[0]
        if isinstance(scene, collections.Iterable):
            for s in scene:
                s.update(dt)
        else:
            scene.update(dt)

    def render(self, screen):
        scene = self.scenes[0]
        if isinstance(scene, collections.Iterable):
            for s in scene:
                s.render(screen)
        else:
            scene.render(screen)
