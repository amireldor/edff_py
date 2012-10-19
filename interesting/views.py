import pygame

from core.view import View

class ViewMatos(View):

    def __init__(self, matos):
        View.__init__(self)
        self.matos = matos

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.matos.x - 15, self.matos.y - 15, 30, 30), 1)
