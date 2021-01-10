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

import string
import random


class Manager:
    def __init__(self):
        self.meetings = {}

    def new_meeting(self):
        get_key = lambda: "".join(random.choices(string.ascii_lowercase, k=8))
        key = get_key()
        while key in self.meetings:
            key = get_key()

        self.meetings[key] = Meeting(key)
        return key

    def remove(self, addr):
        for meeting in self.meetings:
            meeting.remove(addr)


class Meeting:
    def __init__(self, key):
        self.key = key
        self.attendees = []

    def add_attendee(self, client):
        self.attendees.append(client)

    def remove(self, addr):
        for i, attendee in enumerate(self.attendees):
            if attendee.addr == addr:
                del self.attendees[i]
