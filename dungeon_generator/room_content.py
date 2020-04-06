import json
from pprint import pprint
from random import randint

from calculate.a_star import a_star
from calculate.dfs import dfs_search
from entities.npc import NPC
from entities.room_object import RoomObject


class RoomContent:
    width = 13
    height = 9

    def __init__(self, room, content_data):
        self.room = room

        self.__empty_content = {'id': 'empty', 'themas': [5, 4, 3, 2, 1, 0], 'luck': 0, 'solid': False, "clickable": False}

        self.contents = self.make_matrix(self.__empty_content)
        self.random_safe_point = None
        self.matrix_protect_base = self.make_protect_base()
        self.matrix_solid_base = self.make_matrix(0)

        self.fill_all(content_data)
        self.accessible_positions = self.set_accessible_positions()

        self.center_position = (int(self.width / 2 + .5) - 1, int(self.height / 2 + .5) - 1)

    def make_matrix(self, default):
        return [[default] * self.width for i in range(self.height)]

    def make_matrix_border(self, matrix):
        matrix[0] = [1] * self.width
        matrix[self.height - 1] = [1] * self.width
        for y in range(1, self.height - 1):
            matrix[y][0] = 1
            matrix[y][self.width - 1] = 1
        return matrix

    def make_protect_base(self):
        matrix = self.make_matrix(0)

        matrix = self.make_matrix_border(matrix)

        self.random_safe_point = (randint(1, self.width-2), randint(1, self.height-2))
        safe_point_path = []

        if self.room.is_ready_port("N"):
            matrix[0][int(self.width/2 + .5)-1] = 0
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, 0), self.random_safe_point))
        if self.room.is_ready_port("S"):
            matrix[self.height-1][int(self.width/2 + .5)-1] = 0
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, self.height-1), self.random_safe_point))
        if self.room.is_ready_port("W"):
            matrix[int(self.height/2 + .5)-1][0] = 0
            safe_point_path.append(a_star(matrix, (0, int(self.height/2 + .5)-1), self.random_safe_point))
        if self.room.is_ready_port("E"):
            matrix[int(self.height/2 + .5)-1][self.width-1] = 0
            safe_point_path.append(a_star(matrix, (self.width-1, int(self.height/2 + .5)-1), self.random_safe_point))

        if self.room.is_start_room:
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, int(self.height/2 + .5)-1), self.random_safe_point))

        for safe_path in safe_point_path:
            for safe_block in safe_path:
                matrix[safe_block[1]][safe_block[0]] = 1

        return matrix

    def get_random_one(self, content_data):
        luck_ranges = []
        for i, val in enumerate(content_data):
            luck_ranges.append(val["luck"])
            if i > 0:
                luck_ranges[-1] += luck_ranges[-2]

        random_val = randint(0, 100000)/1000
        for i, luck in enumerate(luck_ranges):
            if random_val <= luck:
                return content_data[i]
        return self.__empty_content

    def fill_all(self, content_data):
        for y in range(self.height):
            for x in range(self.width):
                if x in (0, self.width-1) or y in (0, self.height-1):
                    border_content = self.__empty_content.copy()
                    border_content["solid"] = True
                    self.contents[y][x] = RoomObject(border_content, self.room, x, y)
                    continue
                while True: #solid olmaması gereken yerde solid gelmeyene kadar
                    self.contents[y][x] = RoomObject(self.get_random_one(content_data), self.room, x, y)
                    if self.matrix_protect_base[y][x] == 0 or not self.contents[y][x].solid:
                        self.matrix_solid_base[y][x] = int(self.contents[y][x].solid)
                        break
        self.matrix_solid_base = self.make_matrix_border(self.matrix_solid_base)

        if self.room.is_ready_port("N"):
            door_x = int(self.width/2 + .5)-1
            door_y = 0
            door_content = self.__empty_content.copy()
            door_content["id"] = "kapi"+str(self.room.room_thema)+"N"
            door_content["solid"] = True
            door_content["clickable"] = True
            self.contents[door_y][door_x] = RoomObject(door_content, self.room, door_x, door_y)
            self.contents[door_y][door_x].add_event("Door", port_name="N",
                                                    across_room=self.room.ports["N"].get_across_room("N"))
            door_border_right = door_content.copy()
            door_border_right["id"] = "kapi_border_sag"+str(self.room.room_thema)+"N"
            self.contents[door_y][door_x+1] = RoomObject(door_border_right, self.room, door_x+1, door_y)
            door_border_left = door_border_right.copy()
            door_border_left["id"] = "kapi_border_sol" + str(self.room.room_thema) + "N"
            self.contents[door_y][door_x - 1] = RoomObject(door_border_left, self.room, door_x - 1, door_y)
        if self.room.is_ready_port("S"):
            door_x = int(self.width / 2 + .5) - 1
            door_y = self.height - 1
            door_content = self.__empty_content.copy()
            door_content["id"] = "kapi" + str(self.room.room_thema) + "S"
            door_content["solid"] = True
            door_content["clickable"] = True
            self.contents[door_y][door_x] = RoomObject(door_content, self.room, door_x, door_y)
            self.contents[door_y][door_x].add_event("Door", port_name="S",
                                                    across_room=self.room.ports["S"].get_across_room("S"))
            door_border_right = door_content.copy()
            door_border_right["id"] = "kapi_border_sag" + str(self.room.room_thema) + "S"
            self.contents[door_y][door_x - 1] = RoomObject(door_border_right, self.room, door_x - 1, door_y)
            door_border_left = door_border_right.copy()
            door_border_left["id"] = "kapi_border_sol" + str(self.room.room_thema) + "S"
            self.contents[door_y][door_x + 1] = RoomObject(door_border_left, self.room, door_x + 1, door_y)
        if self.room.is_ready_port("W"):
            door_x = 0
            door_y = int(self.height / 2 + .5) - 1
            door_content = self.__empty_content.copy()
            door_content["id"] = "kapi" + str(self.room.room_thema) + "W"
            door_content["solid"] = True
            door_content["clickable"] = True
            self.contents[door_y][door_x] = RoomObject(door_content, self.room, door_x, door_y)
            self.contents[door_y][door_x].add_event("Door", port_name="W",
                                                    across_room=self.room.ports["W"].get_across_room("W"))
            door_border_right = door_content.copy()
            door_border_right["id"] = "kapi_border_sag" + str(self.room.room_thema) + "W"
            self.contents[door_y-1][door_x] = RoomObject(door_border_right, self.room, door_x, door_y-1)
            door_border_left = door_border_right.copy()
            door_border_left["id"] = "kapi_border_sol" + str(self.room.room_thema) + "W"
            self.contents[door_y+1][door_x] = RoomObject(door_border_left, self.room, door_x, door_y+1)
        if self.room.is_ready_port("E"):
            door_x = self.width - 1
            door_y = int(self.height / 2 + .5) - 1
            door_content = self.__empty_content.copy()
            door_content["id"] = "kapi" + str(self.room.room_thema) + "E"
            door_content["solid"] = True
            door_content["clickable"] = True
            self.contents[door_y][door_x] = RoomObject(door_content, self.room, door_x, door_y)
            self.contents[door_y][door_x].add_event("Door", port_name="E",
                                                    across_room=self.room.ports["E"].get_across_room("E"))
            door_border_right = door_content.copy()
            door_border_right["id"] = "kapi_border_sag" + str(self.room.room_thema) + "E"
            self.contents[door_y + 1][door_x] = RoomObject(door_border_right, self.room, door_x, door_y + 1)
            door_border_left = door_border_right.copy()
            door_border_left["id"] = "kapi_border_sol" + str(self.room.room_thema) + "E"
            self.contents[door_y - 1][door_x] = RoomObject(door_border_left, self.room, door_x, door_y - 1)

    def get_room_objects_data(self):
        list_json_room_contents = []
        for y in range(self.height):
            for x in range(self.width):
                list_json_room_contents.append(self.contents[y][x].get_dict())
        return json.dumps(list_json_room_contents)

    def get_room_object(self, id):
        for y in range(self.height):
            for x in range(self.width):
                if self.contents[y][x].id == id:
                    return self.contents[y][x]
        return False

    def set_accessible_positions(self):
        graph = {}
        for y in range(self.height):
            for x in range(self.width):
                neighbor = []
                if x < self.width-1:
                    if self.matrix_solid_base[y][x+1] == 0:
                        neighbor.append((x+1, y))
                if x > 0:
                    if self.matrix_solid_base[y][x-1] == 0:
                        neighbor.append((x-1, y))
                if y < self.height-1:
                    if self.matrix_solid_base[y+1][x] == 0:
                        neighbor.append((x, y+1))
                if y > 0:
                    if self.matrix_solid_base[y-1][x] == 0:
                        neighbor.append((x, y-1))
                graph[(x, y)] = neighbor
        return dfs_search(graph, self.random_safe_point)

    def fill_npcs(self):
        if self.room.room_thema > 2:
            random_val = randint(0, 100000) / 1000
            if random_val < 10:
                for i in range(randint(3, 5)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions)-1)]
                    civciv = NPC("civciv", "")
                    civciv.speed = 2
                    civciv.posX = random_accessable_point[0]
                    civciv.posY = random_accessable_point[1]
                    civciv.add_event("RandomWalk")
                    civciv.add_event("Funky", speed=3)
                    self.room.join_npc(civciv)
                for i in range(randint(1, 3)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    tavuk = NPC("tavuk", "")
                    tavuk.speed = 0.7
                    tavuk.posX = random_accessable_point[0]
                    tavuk.posY = random_accessable_point[1]
                    tavuk.add_event("RandomWalk")
                    tavuk.add_event("Funky", speed=1.5)
                    self.room.join_npc(tavuk)
                for i in range(randint(0, 1)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    horoz = NPC("horoz", "")
                    horoz.speed = 0.5
                    horoz.posX = random_accessable_point[0]
                    horoz.posY = random_accessable_point[1]
                    horoz.add_event("RandomWalk")
                    horoz.add_event("Funky", speed=1.5)
                    self.room.join_npc(horoz)

            elif random_val < 20:
                for i in range(randint(1, 4)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions)-1)]
                    koyun = NPC("koyun", "")
                    koyun.speed = 0.4
                    koyun.posX = random_accessable_point[0]
                    koyun.posY = random_accessable_point[1]
                    koyun.add_event("RandomWalk")
                    koyun.add_event("Funky", speed=1.5)
                    self.room.join_npc(koyun)

            elif random_val < 30:
                for i in range(randint(1, 4)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions)-1)]
                    inek = NPC("inek", "")
                    inek.speed = 0.2
                    inek.posX = random_accessable_point[0]
                    inek.posY = random_accessable_point[1]
                    inek.add_event("RandomWalk")
                    inek.add_event("Funky", speed=1)
                    self.room.join_npc(inek)

            elif random_val < 35:
                for i in range(randint(0, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions)-1)]
                    kedi = NPC("kedi", "")
                    kedi.speed = 0.7
                    kedi.posX = random_accessable_point[0]
                    kedi.posY = random_accessable_point[1]
                    kedi.add_event("RandomWalk")
                    kedi.add_event("Funky", speed=1.5)
                    self.room.join_npc(kedi)
                for i in range(randint(0, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions)-1)]
                    kedi2 = NPC("kedi2", "")
                    kedi2.speed = 0.7
                    kedi2.posX = random_accessable_point[0]
                    kedi2.posY = random_accessable_point[1]
                    kedi2.add_event("RandomWalk")
                    kedi2.add_event("Funky", speed=1.5)
                    self.room.join_npc(kedi2)

            elif random_val < 40:
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kopek = NPC("kopek", "")
                    kopek.speed = 0.5
                    kopek.posX = random_accessable_point[0]
                    kopek.posY = random_accessable_point[1]
                    kopek.add_event("RandomWalk")
                    self.room.join_npc(kopek)

            elif random_val < 42:
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kurt = NPC("kurt", "")
                    kurt.speed = 0.3
                    kurt.posX = random_accessable_point[0]
                    kurt.posY = random_accessable_point[1]
                    kurt.add_event("RandomWalk")
                    self.room.join_npc(kurt)

            elif random_val < 47:
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kus = NPC("kus", "")
                    kus.speed = 0.3
                    kus.posX = random_accessable_point[0]
                    kus.posY = random_accessable_point[1]
                    kus.add_event("RandomWalk")
                    kus.add_event("Funky", speed=2)
                    self.room.join_npc(kus)
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kus2 = NPC("kus2", "")
                    kus2.speed = 2
                    kus2.posX = random_accessable_point[0]
                    kus2.posY = random_accessable_point[1]
                    kus2.add_event("RandomWalk")
                    kus2.add_event("Funky", speed=3)
                    self.room.join_npc(kus2)

            elif random_val < 50:
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    tavsan1 = NPC("tavsan1", "")
                    tavsan1.speed = 1
                    tavsan1.posX = random_accessable_point[0]
                    tavsan1.posY = random_accessable_point[1]
                    tavsan1.add_event("RandomWalk")
                    tavsan1.add_event("Funky", speed=2)
                    self.room.join_npc(tavsan1)

            elif random_val < 51:
                for i in range(randint(1, 2)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kurbaga = NPC("kurbaga", "")
                    kurbaga.speed = 1
                    kurbaga.posX = random_accessable_point[0]
                    kurbaga.posY = random_accessable_point[1]
                    kurbaga.add_event("RandomWalk")
                    kurbaga.add_event("Funky", speed=3)
                    self.room.join_npc(kurbaga)

            elif random_val < 52:
                for i in range(randint(1, 3)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    at = NPC("at", "")
                    at.speed = 0.5
                    at.posX = random_accessable_point[0]
                    at.posY = random_accessable_point[1]
                    at.add_event("RandomWalk")
                    at.add_event("Funky", speed=3)
                    self.room.join_npc(at)

            if randint(0, 100000) / 1000 < 5:
                for i in range(randint(0, 3)):
                    random_accessable_point = self.accessible_positions[randint(0, len(self.accessible_positions) - 1)]
                    kelebek = NPC("kelebek", "")
                    kelebek.speed = 0.2
                    kelebek.posX = random_accessable_point[0]
                    kelebek.posY = random_accessable_point[1]
                    kelebek.add_event("RandomWalk")
                    kelebek.add_event("Funky", speed=1)
                    self.room.join_npc(kelebek)

