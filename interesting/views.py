import pygame

from core.view import View

class ViewMatos(View):

    def __init__(self):
        View.__init__(self)

    def render(self, screen, matos):
        pygame.draw.rect(screen, (255, 0, 0), (matos.x - 15, matos.y - 15, 30, 30), 1)
