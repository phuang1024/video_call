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

import time
import threading
import pygame
from _constants import *
from _elements import Button, Text, TextInput, Scrollable


class Meeting:
    def __init__(self, conn):
        self.conn = conn

        self.active = True
        self.attendees = []
        self.videos = []

        self.video = False
        self.button_video_on = Button(FONT_SMALL.render("Video ON", 1, BLACK))
        self.button_video_off = Button(FONT_SMALL.render("Video OFF", 1, BLACK))

        threading.Thread(target=self.get_info).start()

    def get_info(self):
        while self.active:
            try:
                self.conn.send({"type": "meeting_get"})
                self.attendees = self.conn.recv()["data"]
                self.videos = self.conn.recv()["data"]

                send_data = {"type": "meeting_get", "video_on": self.video}

            except KeyError:
                continue

    def draw(self, window, events):
        width, height = window.get_size()

        window.fill(WHITE)

        if self.video:
            if self.button_video_off.draw(window, events, (70, height-50), (100, 30)):
                self.video = False
        else:
            if self.button_video_on.draw(window, events, (70, height-50), (100, 30)):
                self.video = True
