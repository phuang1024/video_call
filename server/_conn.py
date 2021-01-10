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
import colorama
from hashlib import sha256
from colorama import Fore
colorama.init()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.clients = []

    def start(self, manager):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            client = Client(conn, addr, manager)
            self.clients.append(client)


class Client:
    header = 65536

    def __init__(self, conn, addr, manager):
        self.conn = conn
        self.addr = addr
        self.manager = manager
        self.active = True
        self.alert("INFO", "Connected")
        threading.Thread(target=self.start).start()

    def start(self):
        self.auth()
        self.status = "IDLE"

        while True:
            msg = self.recv()

            if msg["type"] == "quit":
                self.conn.close()
                self.manager.remove(self.addr)
                self.active = False
                self.alert("INFO", "Disconnected")
                return

            elif msg["type"] == "new_meeting":
                key = self.manager.new_meeting()
                self.send({"type": "new_meeting", "key": key})

    def auth(self):
        test_data = str(time.time()).encode()
        real_ans = sha256(test_data).hexdigest()
        self.send({"type": "auth", "test": test_data})
        ans = self.recv()["ans"]

        if real_ans == ans:
            self.alert("INFO", "Authenticated")
        else:
            self.alert("ERROR", "Authentication failed")
            self.conn.close()
            self.active = False

    def alert(self, type, msg):
        color = Fore.WHITE
        if type == "INFO":
            color = Fore.CYAN
        elif type == "WARNING":
            color = Fore.YELLOW
        elif type == "ERROR":
            color = Fore.RED
        print(color + f"[{self.addr}] " + msg + Fore.WHITE)

    def send(self, obj):
        data = pickle.dumps(obj)
        length = len(data)
        len_msg = (str(length) + " "*self.header)[:self.header].encode()
        self.conn.send(len_msg)
        self.conn.send(data)

    def recv(self):
        length = int(self.conn.recv(self.header))
        data = self.conn.recv(length)
        return pickle.loads(data)
