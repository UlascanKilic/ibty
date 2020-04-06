import entity_events
from calculate.id_generator import generate_id
from entity_events import *


class RoomObject:
    def __init__(self, data, room, x, y):
        self.id = generate_id()
        self.room = room
        self.posX = x
        self.posY = y
        self.name = data["id"]
        self.solid = data["solid"]
        self.rotate = 0
        self.clickable = data["clickable"]
        self.events = {}

    def get_dict(self):
        return {"id": self.id,
                "name": self.name,
                "x": self.posX,
                "y": self.posY,
                "solid": self.solid,
                "rotate": self.rotate,
                "clickable": self.clickable}

    def add_event(self, event_name, **kwargs):
        constructor = globals()["Event"+event_name]
        self.events[event_name] = constructor(self, **kwargs)

    def update(self, dt):
        [event.update(dt) for event in list(self.events.values())]

    def on_click(self, player):
        [event.on_click(player) for event in list(self.events.values())]
        player.last_clicked_object = self
        if self.room.room_content.height-1 > self.posY > 0:
            if self.room.room_content.width-1 > self.posX > 0:
                player.move(self.posX, self.posY)

