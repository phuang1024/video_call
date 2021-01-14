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
import cv2
from _constants import *
from _elements import Button, Text, TextInput, Scrollable


class Meeting:
    video_res = (640, 360)

    def __init__(self, conn):
        self.conn = conn

        self.active = True
        self.attendees = []
        self.videos = []

        self.video_on = False
        self.video_curr = pygame.image.tostring(pygame.Surface(self.video_res), "RGB")
        self.button_video_on = Button(FONT_SMALL.render("Video ON", 1, BLACK))
        self.button_video_off = Button(FONT_SMALL.render("Video OFF", 1, BLACK))

        threading.Thread(target=self.get_info).start()
        threading.Thread(target=self.update_video).start()

    def get_info(self):
        while self.active:
            try:
                self.conn.send({"type": "meeting_get"})
                self.attendees = self.conn.recv()["data"]
                self.videos = self.conn.recv()["data"]

                send_data = {"type": "meeting_get", "video_on": self.video_on}

            except KeyError:
                continue

    def update_video(self):
        capturer = cv2.VideoCapture(0)

        while self.active:
            if self.video_on:
                rval, image = capturer.read()
                image = cv2.resize(image, self.video_res)
                surface = pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")
                self.video_curr = pygame.image.tostring(surface)

            time.sleep(0.01)

    def draw(self, window, events):
        width, height = window.get_size()

        window.fill(WHITE)

        if self.video_on:
            if self.button_video_off.draw(window, events, (70, height-50), (100, 30)):
                self.video_on = False
        else:
            if self.button_video_on.draw(window, events, (70, height-50), (100, 30)):
                self.video_on = True
