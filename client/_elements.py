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


class Button:
    def __init__(self, loc, size, text):
        self.loc = loc
        self.size = size
        self.text = text
        self.text_loc = (loc[0] + (size[0]-text.get_width())//2, loc[1] + (size[1]-text.get_height())//2)

    def draw(self, window, events):
        color = (GRAY_DARK if self.clicked(events) else GRAY_LIGHT) if self.hovered() else WHITE
        pygame.draw.rect(window, color, self.loc+self.size)
        pygame.draw.rect(window, WHITE, self.loc+self.size, 2)
        window.blit(self.text, self.text_loc)

    def hovered(self):
        loc = self.loc
        size = self.size
        mouse_pos = pygame.mouse.get_pos()
        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            return True
        return False

    def clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered():
                return True
        return False


class Slider:
    def __init__(self, loc, size, circle_size, font, label, default_val, val_range):
        self.loc = loc
        self.size = size
        self.circle_size = circle_size
        self.font = font
        self.label = label
        self.value = default_val
        self.range = val_range
        self.val_dist = val_range[1] - val_range[0]
        self.dragging = False

    def draw(self, window, events):
        loc = self.loc
        size = self.size

        text = self.font.render(f"{self.label}: {self.value}", 1, WHITE)
        text_loc = (loc[0] + (self.size[0]-text.get_width())//2, self.loc[1]+self.size[1]+7)
        pygame.draw.rect(window, GRAY, loc+size)
        pygame.draw.rect(window, WHITE, loc+size, 1)
        pygame.draw.circle(window, WHITE, (self.value_to_loc(), self.loc[1]+self.size[1]//2), self.circle_size)
        window.blit(text, text_loc)

        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
                    self.dragging = True

        clicked = pygame.mouse.get_pressed()[0]
        if not clicked:
            self.dragging = False
        
        if clicked and self.dragging:
            self.value = self.loc_to_value(mouse_pos[0])

    def loc_to_value(self, loc):
        fac = max(min((loc-self.loc[0]) / self.size[0], 1), 0)
        return int(fac*self.val_dist + self.range[0])

    def value_to_loc(self):
        fac = (self.value-self.range[0]) / self.val_dist
        return fac * self.size[0] + self.loc[0]


class TextInput:
    options = {
        "border.color": (0, 0, 0),
        "border.width": 5,
        "background.color": (255, 255, 255),
        "text.color": (0, 0, 0),
        "cursor.color": (0, 0, 1)
    }

    def __init__(self,
                 loc,
                 size,
                 initial_text="",
                 label="",
                 font=pygame.font.SysFont("comicsans", 35),
                 repeat_initial=400,
                 repeat_interval=35,
                 max_len=-1,
                 password=False,
                 editing=False):

        self.password_field = password

        self.loc, self.size = loc, size

        self.editing = editing

        self.text_col = self.options["text.color"]
        self.password = password
        self.text = initial_text
        self.label = label
        self.max_len = max_len

        self.rect = pygame.Rect(*loc, *size)
        self.bg_col = self.options["background.color"]
        self.border_col, self.border_width = self.options["border.color"], self.options["border.width"]

        self.font = font

        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        self.key_repeat_counters = {}
        self.key_repeat_initial = repeat_initial
        self.key_repeat_interval = repeat_interval

        self.cursor_surf = pygame.Surface(
            (int(font.get_height() / 20 + 1), font.get_height()))
        self.cursor_surf.fill(self.options["cursor.color"])
        self.cursor_pos = len(initial_text)
        self.cursor_visible = True
        self.cursor_switch = 500
        self.cursor_counter = 0

        self.clock = pygame.time.Clock()

    def draw(self, window, events):
        pygame.draw.rect(window, self.bg_col, self.rect)
        if self.border_width:
            pygame.draw.rect(window, self.border_col,
                             self.rect, self.border_width)

        text_pos = (int(self.loc[0] + self.size[0]//2 - self.surface.get_width()/2),
                   int(self.loc[1] + self.size[1]//2 - self.surface.get_height()/2))
        window.blit(self.surface, text_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.editing = True
                else:
                    self.editing = False

            if not self.text:
                self.password = False
                self.text = self.label

            if self.editing and self.text == self.label:
                self.clear_text()
                self.password = True if self.password_field else False

            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True

                if event.key not in self.key_repeat_counters:
                    if not event.key == pygame.K_RETURN:
                        self.key_repeat_counters[event.key] = [0, event.unicode]

                if self.editing:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = (
                                self.text[:max(self.cursor_pos - 1, 0)]
                            + self.text[self.cursor_pos:]
                        )

                        self.cursor_pos = max(self.cursor_pos - 1, 0)
                    elif event.key == pygame.K_DELETE:
                        self.text = (
                                self.text[:self.cursor_pos]
                            + self.text[self.cursor_pos + 1:]
                        )

                    elif event.key == pygame.K_RETURN:
                        return True

                    elif event.key == pygame.K_RIGHT:
                        self.cursor_pos = min(
                            self.cursor_pos + 1, len(self.text))

                    elif event.key == pygame.K_LEFT:
                        self.cursor_pos = max(self.cursor_pos - 1, 0)

                    elif event.key == pygame.K_END:
                        self.cursor_pos = len(self.text)

                    elif event.key == pygame.K_HOME:
                        self.cursor_pos = 0

                    elif len(self.text) < self.max_len or self.max_len == -1:
                        self.text = (
                                self.text[:self.cursor_pos]
                            + event.unicode
                            + self.text[self.cursor_pos:]
                        )
                        self.cursor_pos += len(event.unicode)

            elif event.type == pygame.KEYUP:
                if event.key in self.key_repeat_counters:
                    del self.key_repeat_counters[event.key]

        for key in self.key_repeat_counters:
            self.key_repeat_counters[key][0] += self.clock.get_time()

            if self.key_repeat_counters[key][0] >= self.key_repeat_initial:
                self.key_repeat_counters[key][0] = (
                    self.key_repeat_initial
                    - self.key_repeat_interval
                )

                event_key, event_unicode = key, self.key_repeat_counters[key][1]
                pygame.event.post(pygame.event.Event(
                    pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        string = self.text
        if self.password:
            string = "*" * len(self.text)
        if self.text:
            self.surface = self.font.render(str(string), 1, self.text_col)
        else:
            self.surface = pygame.Surface(self.cursor_surf.get_size(), pygame.SRCALPHA)
            self.surface.fill((0, 0, 0, 0))

        self.cursor_counter += self.clock.get_time()
        if self.cursor_counter >= self.cursor_switch:
            self.cursor_counter %= self.cursor_switch
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y = self.font.size(self.text[:self.cursor_pos])[0]
            if self.cursor_pos > 0:
                cursor_y -= self.cursor_surf.get_width()
            if self.editing:
                self.surface.blit(self.cursor_surf, (cursor_y, 0))

        self.clock.tick()
        return False

    def get_cursor_pos(self):
        return self.cursor_pos

    def set_text_color(self, color):
        self.text_col = color

    def set_cursor_color(self, color):
        self.cursor_surf.fill(color)

    def clear_text(self):
        self.text = ""
        self.cursor_pos = 0

    def __repr__(self):
        return self.text
