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

import threading
import pygame
from _constants import *
from _elements import Button, Text, TextInput


class Waiting:
    def __init__(self):
        self.text_header = Text(FONT_LARGE.render("Meeting", 1, BLACK))
        self.text_attendees = Text(FONT_MED.render("Attendees", 1, BLACK))
        self.text_info = Text(FONT_MED.render("Info", 1, BLACK))

        self.frame = 0
        self.attendees = []
        self.info = {}

    def draw(self, window, events, conn):
        self.frame += 1
        width, height = window.get_size()

        if self.frame % 30 == 1:
            conn.send({"type": "get", "data": "attendees"})
            self.attendees = conn.recv()["data"]
            conn.send({"type": "get", "data": "info"})
            self.info = conn.recv()["data"]

        window.fill(WHITE)
        self.text_header.draw(window, (width//2, 50))
        self.text_attendees.draw(window, (width//3, 100))
        self.text_info.draw(window, (width//1.5, 100))

        for i, attend in enumerate(self.attendees):
            Text(FONT_SMALL.render(attend, 1, BLACK)).draw(window, (width//3, 150+i*30))
        for i, key in enumerate(self.info):
            name = {"host": "Host", "key": "Key", "pword": "Password", "num_people": "Number of people"}[key]
            Text(FONT_SMALL.render(f"{name}: {self.info[key]}", 1, BLACK)).draw(window, (width//1.5, 150+i*30))
