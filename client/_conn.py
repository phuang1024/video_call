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

import socket
import pickle
from hashlib import sha256


class Conn:
    header = 65536

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.auth()

    def auth(self):
        test = self.recv()["test"]
        ans = sha256(test).hexdigest()
        self.send({"type": "auth", "ans": ans})

    def send(self, obj):
        data = pickle.dumps(obj)
        length = len(data)
        len_msg = (str(length) + " "*self.header)[:self.header].encode()
        self.conn.send(len_msg)
        self.conn.send(data)

    def recv(self):
        length = int(self.conn.recv(self.header))
        data = self.conn.recv(length)
        print(data)
        return pickle.loads(data)
