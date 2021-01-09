#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
from _constants import *


class Text:
    def __init__(self, text):
        self.text = text

    def draw(self, window, loc):
        text_loc = [loc[i] - self.text.get_size()[i]//2 for i in range(2)]
        window.blit(self.text, text_loc)


class Button:
    def __init__(self, text):
        self.text = text

    def draw(self, window, events, loc, size):
        loc = [loc[0]-size[0]//2, loc[1]]
        clicked = self.clicked(events, loc, size)
        color = (GRAY_DARK if clicked else GRAY_LIGHT) if self.hovered(loc, size) else WHITE
        text_loc = [loc[i] + (size[i]-self.text.get_size()[i])//2 for i in range(2)]

        pygame.draw.rect(window, color, (*loc, *size))
        pygame.draw.rect(window, BLACK, (*loc, *size), 2)
        window.blit(self.text, text_loc)

        return clicked

    def hovered(self, loc, size):
        mouse = pygame.mouse.get_pos()
        if loc[0] <= mouse[0] <= loc[0]+size[0] and loc[1] <= mouse[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events, loc, size):
        if self.hovered(loc, size):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True
        return False
