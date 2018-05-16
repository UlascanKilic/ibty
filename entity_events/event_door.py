import threading
import time


def click_door(self, player):
    time.sleep(self.sleep_time/1000)
    player.last_door_event = self
    player.client.ask(player.room.ports[self.port_name].question)

    if player.room.ports[self.port_name] in player.unlocked_doors:
        player.room.left_player(player)
        self.across_room.join_player(player, self.port_name)


class EventDoor:
    def __init__(self, entity, **kwargs):
        self.entity = entity
        self.port_name = kwargs["port_name"]
        self.across_room = kwargs["across_room"]

    def spawn(self, x, y, room):
        pass

    def despawn(self):
        pass

    def speech(self, message):
        pass

    def move(self, x, y, t):
        pass

    def update(self, dt):
        if self.answer_cooldown > 0:
            self.answer_cooldown -= dt
        else:
            self.answer_cooldown = 0

    answer_cooldown = 0
    def answer(self, player, text):
        if self.answer_cooldown <= 0:
            answer_wait = 10
            if str(text) == str(player.room.ports[self.port_name].answer):
                answer_wait = -1
                player.unlocked_doors.append(player.room.ports[self.port_name])
                player.room.left_player(player)
                self.across_room.join_player(player, self.port_name)
            else:
                self.answer_cooldown = 10
            player.client.answer_result(answer_wait)


    sleep_time = 0
    def on_click(self, player):
        pos_x = 0
        pos_y = 0
        if self.port_name is "N":
            pos_x = int(player.room.room_content.width / 2 + .5) - 1
            pos_y = 1
        elif self.port_name is "S":
            pos_x = int(player.room.room_content.width / 2 + .5) - 1
            pos_y = player.room.room_content.height - 2
        elif self.port_name is "W":
            pos_x = 1
            pos_y = int(player.room.room_content.height / 2 + .5) - 1
        elif self.port_name is "E":
            pos_x = player.room.room_content.width - 2
            pos_y = int(player.room.room_content.height / 2 + .5) - 1
        self.sleep_time = player.move(pos_x, pos_y)
        threading.Thread(target=click_door, args=(self, player,), kwargs={}).start()

