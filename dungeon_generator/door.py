class Door:
    def __init__(self):
        self.exist = False
        self.isLocket = False
        self.rooms = []
        self.question = ""
        self.answer = ""

    def set(self, room, port_name):
        self.rooms.append({"room": room, "port_name": port_name})
        self.validate()
        return self

    def remove(self, port_name):
        for i, room in self.rooms:
            if port_name in room:
                self.rooms.pop(i)
        self.validate()

    def validate(self):
        if len(self.rooms) == 2:
            self.exist = True
        else:
            self.exist = False

    def get_across_room(self, port_name):
        if self.exist:
            for room_port in self.rooms:
                if room_port["port_name"] != port_name:
                    return room_port["room"]
