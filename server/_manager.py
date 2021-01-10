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

    def new_meeting(self, host, msg):
        get_key = lambda: "".join(random.choices(string.ascii_lowercase, k=8))
        key = get_key()
        while key in self.meetings:
            key = get_key()

        self.meetings[key] = Meeting(key, host, msg)
        return key

    def remove(self, addr):
        for key in self.meetings:
            self.meetings[key].remove(addr)


class Meeting:
    def __init__(self, key, host, msg):
        self.key = key
        self.host = host
        self.attendees = [(host, msg["name"])]
        self.password = msg["pword"]

    def add_attendee(self, client):
        self.attendees.append(client)

    def get_names(self):
        return [attend[1] for attend in self.attendees]

    def get_info(self):
        data = {
            "host": self.attendees[0][1],
            "key": self.key,
            "pword": self.password,
            "num_people": len(self.attendees),
        }
        return data

    def remove(self, addr):
        for i, attendee in enumerate(self.attendees):
            if attendee[0].addr == addr:
                del self.attendees[i]
