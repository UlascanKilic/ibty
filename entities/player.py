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

    def despawn(self):
        if self.room is not None:
            self.room.left_player(self)
        super(Player, self).despawn()

    def update(self, dt):
        super(Player, self).update(dt)
        pass
