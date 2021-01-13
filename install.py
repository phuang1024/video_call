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

import sys
import os
import json
import shutil


def main():
    parent = os.path.realpath(os.path.dirname(__file__))
    os.chdir(parent)
    server = os.path.join(parent, "server")
    client = os.path.join(parent, "client")
    clone = os.path.join(parent, "clone")

    if os.path.isdir(server) or os.path.isdir(client) or os.path.isdir(clone):
        print("Directories \"server\", \"client\", or \"clone\" already exist.")
        return

    ip = input("Server local IP address: ")
    encrypt_offset = input("Encryption offset (best if hard to guess): ")
    settings = {"ip": ip, "encrypt_offset": encrypt_offset}

    print("Cloning repository...")
    os.system(f"git clone https://github.com/HuangPatrick16777216/video_call.git {clone}")

    print("Copying files...")
    shutil.copytree(os.path.join(clone, "server"), server)
    shutil.copytree(os.path.join(clone, "client"), client)

    print("Removing cloned files...")
    #shutil.rmtree(clone)
    print(clone)

    print("Setting up settings...")
    with open(os.path.join(server, "settings.json"), "w") as file:
        json.dump(settings, file)
    with open(os.path.join(client, "settings.json"), "w") as file:
        json.dump(settings, file)

    print("Installing packages...")
    os.system("pip install pygame")
    os.system("pip install colorama")


main()
