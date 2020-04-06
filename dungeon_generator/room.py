from sorular.randomsoru import *
from dungeon_generator.room_content import RoomContent


class Room:
    def __init__(self, dungeon, x ,y):
        self.dungeon = dungeon
        self.pos_x = x
        self.pos_y = y
        self.ports = {}
        self.found = False
        self.room_symbol = " "
        self.room_thema = 100
        self.room_content = None
        self.is_start_room = False

        self.players = {}
        self.npcs = {}

    def add_door(self, port_name, door):
        if port_name in ["N", "S", "W", "E"]:
            self.ports[port_name] = door.set(self, port_name)
            self.found = True
            self.room_symbol_update()
        else:
            raise Exception('gecersiz kapi adi')

    def remove_door(self, port_name):
        if port_name in ["N", "S", "W", "E"]:
            self.ports[port_name].remove(port_name)
            del self.ports[port_name]
            self.room_symbol_update()
        else:
            raise Exception('gecersiz kapi adi')

    def room_symbol_update(self):
        if not self.found:
            self.room_symbol = " "
        elif all(k in self.ports for k in ("N", "S", "W", "E")):
            self.room_symbol = "╋"
        elif all(k in self.ports for k in ("N", "W", "E")):
            self.room_symbol = "┻"
        elif all(k in self.ports for k in ("S", "W", "E")):
            self.room_symbol = "┳"
        elif all(k in self.ports for k in ("N", "S", "W")):
            self.room_symbol = "┫"
        elif all(k in self.ports for k in ("N", "S", "E")):
            self.room_symbol = "┣"
        elif all(k in self.ports for k in ("N", "W")):
            self.room_symbol = "┛"
        elif all(k in self.ports for k in ("N", "E")):
            self.room_symbol = "┗"
        elif all(k in self.ports for k in ("S", "W")):
            self.room_symbol = "┓"
        elif all(k in self.ports for k in ("S", "E")):
            self.room_symbol = "┏"
        elif all(k in self.ports for k in ("N", "S")):
            self.room_symbol = "┃"
        elif all(k in self.ports for k in ("W", "E")):
            self.room_symbol = "━"
        elif all(k in self.ports for k in ("N",)):
            self.room_symbol = "╹"
        elif all(k in self.ports for k in ("S",)):
            self.room_symbol = "╻"
        elif all(k in self.ports for k in ("W",)):
            self.room_symbol = "╸"
        elif all(k in self.ports for k in ("E",)):
            self.room_symbol = "╺"
        else:
            self.room_symbol = " "
            self.found = False
        # https://en.wikipedia.org/wiki/Box-drawing_character

    def __str__(self):
        return "(%d, %d) %s" % (self.pos_x, self.pos_y, str(hex(id(self)).upper()))

    def is_ready_port(self, port_name):
        return port_name in self.ports and self.ports[port_name].exist

    def get_connected_rooms(self):
        connected_rooms = []
        for port_key, port_value in self.ports.items():
            if port_value.exist:
                connected_rooms.append(port_value.get_across_room(port_key))
        return connected_rooms

    def generate_room_content(self, groupped_by_theme_content_data):
        self.room_content = RoomContent(self, groupped_by_theme_content_data[self.room_thema])
        for door in list(self.ports.values()):
            soru_data = dortislem(10)
            if self.room_thema == 5:
                soru_data = dortislem(10)
            elif self.room_thema == 4:
                soru_data = dortislem(50)
            elif self.room_thema == 3:
                soru_data = dortislem(200)
            elif self.room_thema == 2:
                soru_data = dortislem(1000)
            else:
                soru_data = terstenislem()

            door.answer = soru_data[0]
            door.question = soru_data[1]

    def join_player(self, player, port=None):
        print(player.name + " joined to", self.pos_x, self.pos_y)
        player.despawn()
        spawn_x = int(self.room_content.width/2 + .5)-1
        spawn_y = int(self.room_content.height/2 + .5)-1

        if port is "N":
            spawn_x = int(self.room_content.width / 2 + .5) - 1
            spawn_y = self.room_content.height - 2
        elif port is "S":
            spawn_x = int(self.room_content.width / 2 + .5) - 1
            spawn_y = 1
        elif port is "W":
            spawn_x = self.room_content.width - 2
            spawn_y = int(self.room_content.height / 2 + .5) - 1
        elif port is "E":
            spawn_x = 1
            spawn_y = int(self.room_content.height / 2 + .5) - 1
        self.players[player.id] = player
        player.spawn(spawn_x, spawn_y, self)
        player.client.load_room_data()
        player.client.get_characters() #sends characthers to player

    def left_player(self, player):
        if player.id in self.players:
            del self.players[player.id]

    def join_npc(self, npc):
        npc.despawn()
        self.npcs[npc.id] = npc
        npc.spawn(npc.posX, npc.posY, self)

    def left_npc(self, npc):
        if npc.id in self.npcs:
            del self.players[npc.id]

    def get_characters(self):
        characters = dict(self.players)
        characters.update(self.npcs)
        return characters

    def get_character(self, id):
        for character in list(self.get_characters().values()):
            if character.id == id:
                return character
        return False

    def room_ready(self):
        self.room_content.fill_npcs()

    def update(self, dt):
        for y in range(self.room_content.height):
            for x in range(self.room_content.width):
                self.room_content.contents[y][x].update(dt)

        for character in list(self.get_characters().values()):
            character.update(dt)
