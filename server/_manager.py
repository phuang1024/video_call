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
        if msg["name"].strip() == "":
            return {"status": False, "error": "Please fill out your name"}
        if " " in msg["pword"]:
            return {"status": False, "error": "No spaces allowed in password"}
        if len(msg["pword"]) <= 4:
            return {"status": False, "error": "Password too short"}

        get_key = lambda: "".join(random.choices(string.ascii_lowercase, k=4))
        key = get_key()
        while key in self.meetings:
            key = get_key()

        self.meetings[key] = Meeting(key, host, msg)
        return {"status": True, "key": key}

    def join_meeting(self, attend, msg):
        if msg["key"] not in self.meetings:
            return {"status": False, "error": "Meeting code does not exist"}

        for key in self.meetings:
            if key == msg["key"]:
                result = self.meetings[key].add_attendee(attend, msg)
                return result

    def remove(self, addr):
        for key in self.meetings:
            self.meetings[key].remove(addr)


class Meeting:
    def __init__(self, key, host, msg):
        self.key = key
        self.host = host
        self.attendees = [(host, msg["name"])]
        self.password = msg["pword"]
        self.chat = []

    def add_attendee(self, client, msg):
        if msg["name"].strip() == "":
            return {"status": False, "error": "Please fill out your name"}
        elif msg["pword"] != self.password:
            return {"status": False, "error": "Invalid password"}

        self.attendees.append((client, msg["name"]))
        return {"status": True, "key": self.key}

    def get_names(self):
        return [attend[1] for attend in self.attendees]

    def new_chat_msg(self, client, msg):
        name = "Unknown"
        for attend in self.attendees:
            if attend[0] == client:
                name = attend[1]
                break

        self.chat.append((name, msg))

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
