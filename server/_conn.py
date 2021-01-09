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
import socket
import threading
import pickle
from hashlib import sha256


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.clients = []

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            client = Client(conn, addr)
            self.clients.append(client)

            print(f"[{addr[0]}] Connected")


class Client:
    header = 65536

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.active = True
        self.auth()

    def auth(self):
        test_data = str(time.time()).encode()
        real_ans = sha256(test_data).hexdigest()
        self.send({"type": "auth", "test": test_data})
        ans = self.recv()["ans"]

        if real_ans == ans:
            print(f"[{self.addr[0]}] Authenticated")
        else:
            print(f"[{self.addr[0]}] Authentication failed")
            self.conn.close()
            self.active = False

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
