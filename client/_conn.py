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
import pickle
import colorama
from hashlib import sha256
from colorama import Fore
colorama.init()


class Conn:
    header = 64
    packet_size = 1024
    padding = " " * header

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        print(Fore.CYAN + "Connected to server" + Fore.WHITE)
        self.auth()

    def auth(self):
        test = self.recv()["test"]
        ans = sha256(test).hexdigest()
        self.send({"type": "auth", "ans": ans})

    def send(self, obj):
        data = pickle.dumps(obj)
        len_msg = (str(len(data)) + self.padding)[:self.header].encode()

        packets = []
        while data:
            curr_len = min(len(data), self.packet_size)
            packets.append(data[:curr_len])
            data = data[curr_len:]

        self.conn.send(len_msg)
        for packet in packets:
            self.conn.send(data)

    def recv(self):
        try:
            length = int(self.conn.recv(self.header))

            packet_sizes = [self.packet_size] * (length//self.packet_size)
            if (remain := (length % self.packet_size)) != 0:
                packet_sizes.append(remain)

            data = b""
            for size in packet_sizes:
                data += self.conn.recv(size)

            return pickle.loads(data)

        except Exception as e:
            e = str(e)
            error_msg = e if len(e) < 25 else e[:25] + "..."
            print(Fore.RED + f"Error in recv (catched): {error_msg}" + Fore.WHITE)
            return {"type": None}
