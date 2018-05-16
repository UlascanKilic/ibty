import json

from websocket.ws import *
from http_server import *
import sys

from dungeon_generator.dungeon import Dungeon

dungeons = []

sys.setrecursionlimit(9999999)
if __name__ == '__main__':
    print("init")
    d1 = Dungeon(10, 10, room_limit=100, tolerance=10, label="Dungeon 1", subject=0)
    d1.print_dungeon()

    """oda = d1.start_room
    content = oda.room_content
    for l in content.matrix_solid_base:
        print(l)"""

    dungeons.append(d1)

    http_start()
    websocket_start(dungeons)

#https://gsahinpi.gitbooks.io/bil214/coxntent/chapter1.html
