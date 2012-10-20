import pygame

from core.view import View
import conf

class ViewMatos(View):

    def __init__(self):
        View.__init__(self)

    def render(self, screen, matos):
        rad = conf.matos.radius
        pygame.draw.rect(screen, (255, 0, 0), (matos.x - rad, matos.y - rad, rad * 2, rad * 2), 1)
