import json
import sys
import threading
import time

from colorama import Fore, Back, init

from random import randint
from math import sqrt, floor

from calculate.a_star import a_star
from calculate.dfs import dfs_search
from calculate.id_generator import generate_id
from dungeon_generator.door import Door
from dungeon_generator.room import Room

tick = 20

last_frame_time = time.time()
def update_tick(dungeon):
    global last_frame_time
    while True:
        current_time = time.time()
        dt = current_time - last_frame_time

        sleep_time = 0
        if dt < 1./tick:
            sleep_time = 1./tick - dt
            time.sleep(sleep_time)
            dt += sleep_time
        last_frame_time = current_time+sleep_time

        for room_coord in dungeon.valid_rooms:
            dungeon.rooms[room_coord[0]][room_coord[1]].update(dt)


class Dungeon:
    def __init__(self, width, height, room_limit=None, tolerance=1, strain=50, label="Dungeon1", subject=0):
        self.id = generate_id()

        self.width = width
        self.height = height

        self.label = label
        self.subject = subject

        self.rooms = []
        self.valid_rooms = []
        self.boos_room = None
        self.start_room = None

        print("Dungeon making "+str(width)+"x"+str(height))

        self.make_dungeon(room_limit, tolerance, strain)
        self.set_rooms_thema()
        self.start_room.is_start_room = True
        self.fill_room_contents()
        self.players = {}

        threading.Thread(target=update_tick, args=(self,), kwargs={}).start()

    def print_dungeon(self):
        init(strip=False)
        print("Dungeon: %d x %d\n" % (self.width, self.height), end='')
        print("  - valid rooms: %d\n" % len(self.valid_rooms), end='')
        print("+\t" + (self.width * "-\t") +"+\n", end='')
        for y in range(self.height):
            print("|\t", end='')
            for x in range(self.width):
                if self.rooms[x][y].room_thema == 0:
                    print(Back.MAGENTA, end='')
                elif self.rooms[x][y].room_thema == 1:
                    print(Fore.RED, end='')
                elif self.rooms[x][y].room_thema == 2:
                    print(Fore.YELLOW, end='')
                elif self.rooms[x][y].room_thema == 3:
                    print(Fore.GREEN, end='')
                elif self.rooms[x][y].room_thema == 4:
                    print(Fore.BLUE, end='')
                elif self.rooms[x][y].room_thema == 5:
                    print(Fore.CYAN, end='')
                if self.rooms[x][y].is_start_room:
                    print(Back.WHITE, end='')
                print(self.rooms[x][y].room_symbol+"\t", end='')
                print(Fore.RESET, end='')
                print(Back.RESET, end='')
            print("|\n", end='')

        print("+\t" + (self.width * "-\t") + "+\n")

    def make_dungeon(self, room_limit, tolerance, strain):
        self.rooms = [[self.make_room(x, y) for y in range(self.width)] for x in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                # nodeları kopar
                if x+1 < self.width and randint(1, 100) <= strain:
                    latitude_door = self.make_door()
                    self.rooms[x][y].add_door("E", latitude_door)
                    self.rooms[x+1][y].add_door("W", latitude_door)

                if y+1 < self.height and randint(1, 100) <= strain:
                    longitude_door = self.make_door()
                    self.rooms[x][y].add_door("S", longitude_door)
                    self.rooms[x][y+1].add_door("N", longitude_door)

        self.remove_blocked_rooms()

        print("\rStrain: %s" % strain, end="")
        sys.stdout.flush()
        if room_limit is not None:
            percent = (room_limit / 100 * tolerance)
            if len(self.valid_rooms) < room_limit - percent or len(self.valid_rooms) > room_limit + percent:
                if len(self.valid_rooms) < room_limit - percent:
                    strain += sorted([1, room_limit / len(self.valid_rooms), 10])[1]
                else:
                    strain -= sorted([1, len(self.valid_rooms) / room_limit, 10])[1]
                self.make_dungeon(room_limit, tolerance, strain)
            else:
                print()
    def make_room(self, x, y):
        room = Room(self, x, y)
        return room

    def make_door(self):
        door = Door()
        return door

    def make_graph(self):
        graph = {}
        for y in range(self.height):
            for x in range(self.width):
                connected_list = []
                for room in self.rooms[x][y].get_connected_rooms():
                    connected_list.append((room.pos_x, room.pos_y))
                graph[(x, y)] = connected_list
        return graph

    # 3x3 odalar
    def make_matrix_found_rooms(self):
        matrix = []
        for yyy in range(self.height*3):
            temp_list = []
            for x in range(self.width):
                if yyy % 3 == 0:
                    temp_list.append(1)
                    temp_list.append(int("N" not in self.rooms[x][int(yyy/3)].ports))
                    temp_list.append(1)
                elif yyy % 3 == 1:
                    temp_list.append(int("W" not in self.rooms[x][int(yyy / 3)].ports))
                    temp_list.append(0)
                    temp_list.append(int("E" not in self.rooms[x][int(yyy / 3)].ports))
                elif yyy % 3 == 2:
                    temp_list.append(1)
                    temp_list.append(int("S" not in self.rooms[x][int(yyy/3)].ports))
                    temp_list.append(1)
            matrix.append(temp_list)
        return matrix

    def remove_blocked_rooms(self):
        room_groups = []
        checked_rooms = []
        graph = self.make_graph()

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in checked_rooms:
                    temp_room_group = []
                    for checked_room in dfs_search(graph, (x, y)):
                        checked_rooms.append(checked_room)
                        temp_room_group.append(checked_room)
                    room_groups.append(temp_room_group)

        self.valid_rooms = max(room_groups, key=len)
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.valid_rooms:
                    for port_key in list(self.rooms[x][y].ports):
                        self.rooms[x][y].remove_door(port_key)

    def set_rooms_thema(self):
        boos_room = self.valid_rooms[randint(0, len(self.valid_rooms) - 1)]
        self.boos_room = self.rooms[boos_room[0]][boos_room[1]]
        found_matrix = self.make_matrix_found_rooms()
        far_distance = -1
        for y in range(self.height):
            for x in range(self.width):
                if self.rooms[x][y].found:
                    distance_to_boos = len(a_star(found_matrix, (x*3+1, y*3+1), (boos_room[0]*3+1, boos_room[1]*3+1)))/3

                    if distance_to_boos > far_distance:
                        far_distance = distance_to_boos
                        self.start_room = self.rooms[x][y]

                    value = int(floor(distance_to_boos / (sqrt(self.width * self.height) / 5)))+1
                    if value == 0:
                        self.rooms[x][y].room_thema = 0
                    elif value <= 1:
                        self.rooms[x][y].room_thema = 1
                    elif value <= 2:
                        self.rooms[x][y].room_thema = 2
                    elif value <= 3:
                        self.rooms[x][y].room_thema = 3
                    elif value <= 4:
                        self.rooms[x][y].room_thema = 4
                    else:
                        self.rooms[x][y].room_thema = 5
                print("\rGenerate dungeon progress: %%%s" % int(
                    (((y * self.width) + (x + 1)) / (self.width * self.height)) * 100
                ), end="")
                sys.stdout.flush()
        self.boos_room.room_thema = 0
        print()

    def fill_room_contents(self):
        groupped_by_theme_content_data = []
        self.room_objects = json.load(open('./config/room_objects.json'))

        for thema in range(6):
            temp_objects = []
            for room_object in self.room_objects["room_objects"]:
                if thema in room_object["themas"] and "luck" in room_object:
                    temp_objects.append(room_object)
            groupped_by_theme_content_data.append(temp_objects)

        for thema, by_theme_content_data in enumerate(groupped_by_theme_content_data):
            temp_total_luck = 0
            for room_object_data in by_theme_content_data:
                temp_total_luck += room_object_data["luck"]
            if temp_total_luck > 100:
                raise Exception("%s. Thema: luck toplamı(%s), 100 uzerinde olamaz!" % (thema, temp_total_luck))

        for valid_pos in self.valid_rooms:
            room = self.rooms[valid_pos[0]][valid_pos[1]]
            room.generate_room_content(groupped_by_theme_content_data)

    def join_player(self, player):
        self.players[player.id] = player
        self.start_room.join_player(player)
        print("connected player: %s, ip: %s" % (Fore.GREEN + player.name + Fore.RESET,
                                                Fore.GREEN + player.client.request.remote_addr + Fore.RESET))

    def left_player(self, player):
        print("disconnected player: %s" % player.name)
        del self.players[player.id]
