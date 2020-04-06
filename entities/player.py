import re

from entities.character import Character


class Player(Character):
    def __init__(self, client):
        super(Player, self).__init__(client.skin)
        self.type = "player"
        self.name = client.nick
        self.client = client
        client.player = self
        self.unlocked_doors = []
        self.last_door_event = None
        self.last_clicked_object = None

    def despawn(self):
        if self.room is not None:
            self.room.left_player(self)
        super(Player, self).despawn()

    def arrived(self):
        super(Player, self).arrived()
        if "Door" in list(self.last_clicked_object.events.keys()):
            self.last_clicked_object.events["Door"].open(self)

    def update(self, dt):
        super(Player, self).update(dt)
        pass

    def speech(self, message):
        super(Player, self).speech(message)
        if message == "hile":
            for y in range(self.room.dungeon.height):
                for x in range(self.room.dungeon.width):
                    room = self.room.dungeon.rooms[x][y]
                    for door in list(room.ports.values()):
                        self.unlocked_doors.append(door)

        teleport_match = re.match(r"teleport (\d+) (\d+)", message, re.M | re.I)
        if teleport_match:
            self.room.left_player(self)
            self.room.dungeon.rooms[int(teleport_match.group(1))][int(teleport_match.group(2))].join_player(self)
