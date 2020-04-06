from entities.character import Character


class NPC(Character):
    def __init__(self, skin, name):
        super(NPC, self).__init__(skin)
        self.type = "npc"
        self.name = name

    def despawn(self):
        if self.room is not None:
            self.room.left_npc(self)
        super(NPC, self).despawn()

    def update(self, dt):
        super(NPC, self).update(dt)
        pass
