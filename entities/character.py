import threading
import time

from calculate.id_generator import generate_id
from calculate.distance import *
from entity_events import *


def delayed_pos_update(self, sleep_time, x, y):
    time.sleep(sleep_time/1000)
    self.posX = x
    self.posY = y

class Character:
    def __init__(self, skin):
        self.id = generate_id()
        self.spawned = False
        self.skin = skin
        self.room = None
        self.posX = 0
        self.posY = 0
        self.name = self.skin
        self.speed = 2
        self.direction = "S"
        self.type = "character"
        self.events = {}

    def get_dict(self):
        return {"id": self.id,
                "skin": self.skin,
                "x": self.posX,
                "y": self.posY,
                "type": self.type,
                "name": self.name,
                "direction": self.direction}

    def add_event(self, event_name, **kwargs):
        constructor = globals()["Event"+event_name]
        self.events[event_name] = constructor(self, **kwargs)

    def spawn(self, x, y, room):
        [event.spawn(x, y, room) for event in list(self.events.values())]
        self.posX = x
        self.posY = y
        self.room = room
        self.spawned = True
        for player in list(self.room.players.values()):
            player.client.spawn(self)

    def despawn(self):
        [event.despawn() for event in list(self.events.values())]
        self.spawned = False
        if self.room is not None:
            for player in list(self.room.players.values()):
                player.client.despawn(self)

    def speech(self, message):
        [event.speech(message) for event in list(self.events.values())]
        if self.room is not None:
            for player in list(self.room.players.values()):
                player.client.speech({"id": self.id, "message": message})

    move_cooldown = 0
    def move(self, x, y):
        [event.move(x, y) for event in list(self.events.values())]
        time = 0
        if self.room is not None:
            for player in list(self.room.players.values()):
                distance = distance_2d(self.posX, self.posY, x, y)
                time = (distance*1000)/self.speed
                self.move_cooldown = time/1000
                player.client.move(self.id, x, y, time)
                threading.Thread(target=delayed_pos_update, args=(self, time, x, y), kwargs={}).start()
        return time

    def update(self, dt):
        [event.update(dt) for event in list(self.events.values())]
        if self.move_cooldown > 0:
            self.move_cooldown -= dt
        else:
            self.move_cooldown = 0
        pass

    def on_click(self, player):
        [event.on_click(player) for event in list(self.events.values())]
        pass

