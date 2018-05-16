import json
from random import randint

from calculate.a_star import a_star
from entities.room_object import RoomObject


class RoomContent:
    width = 13
    height = 9

    def __init__(self, room, content_data):
        self.room = room

        self.__empty_content = {'id': 'empty', 'themas': [5, 4, 3, 2, 1, 0], 'luck': 0, 'solid': False, "clickable": False}

        self.contents = self.make_matrix(self.__empty_content)
        self.matrix_protect_base = self.make_protect_base()
        self.matrix_solid_base = self.make_matrix(0)

        self.fill_all(content_data)

        self.starter_position = (int(self.width / 2 + .5) - 1, int(self.height / 2 + .5) - 1)

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

        random_safe_point = (randint(1, self.width-2), randint(1, self.height-2))
        safe_point_path = []

        if self.room.is_ready_port("N"):
            matrix[0][int(self.width/2 + .5)-1] = 0
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, 0), random_safe_point))
        if self.room.is_ready_port("S"):
            matrix[self.height-1][int(self.width/2 + .5)-1] = 0
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, self.height-1), random_safe_point))
        if self.room.is_ready_port("W"):
            matrix[int(self.height/2 + .5)-1][0] = 0
            safe_point_path.append(a_star(matrix, (0, int(self.height/2 + .5)-1), random_safe_point))
        if self.room.is_ready_port("E"):
            matrix[int(self.height/2 + .5)-1][self.width-1] = 0
            safe_point_path.append(a_star(matrix, (self.width-1, int(self.height/2 + .5)-1), random_safe_point))

        if self.room.is_start_room:
            safe_point_path.append(a_star(matrix, (int(self.width/2 + .5)-1, int(self.height/2 + .5)-1), random_safe_point))

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
