from calculate.id_generator import generate_id
from entities.player import Player
from websocket import ws
from websocket.ws import *


class Client:
    def __init__(self, id, app, socketio, request):
        self.id = id
        self.nick = "Misafir_"+str(generate_id())
        self.skin = "tospik"
        self.player = None
        self.app = app
        self.socketio = socketio
        self.request = request

    def is_in_game(self):
        if self.player is not None:
            if self.player.room is not None:
                return True
        return False

    def join_dungeon(self, dungeon_number):
        self.player = Player(self)
        ws.dungeons[dungeon_number].join_player(self.player)

    def load_room_data(self):
        if self.is_in_game():
            data = {"ports": list(self.player.room.ports.keys()),
                    "room_objects": self.player.room.room_content.get_room_objects_data(),
                    "thema": self.player.room.room_thema}
            self.socketio.emit('load_room_data', data, room=self.id)

    def get_user_info(self):
        self.socketio.emit('get_user_info', self.player.get_dict())

    def get_characters(self):
        if self.is_in_game():
            characters_data = []
            for character in list(self.player.room.get_characters().values()):
                characters_data.append(character.get_dict())
            self.socketio.emit('characters', characters_data, room=self.id)

    def speech(self, id_message):
        if self.is_in_game():
            self.socketio.emit('speech', id_message, room=self.id)

    def move(self, id, x, y, time):
        if self.is_in_game():
            self.socketio.emit('move', {"id": id, "x": x, "y": y, "t": time}, room=self.id)

    def spawn(self, characther):
        self.socketio.emit('spawn', characther.get_dict(), room=self.id)

    def despawn(self, characther):
        if self.is_in_game():
            self.socketio.emit('despawn', characther.id, room=self.id)

    def ask(self, question, answers=None):
        if self.is_in_game():
            has_answer = False
            if answers:
                has_answer = True
            self.socketio.emit("ask", {"question": question, "has_answer": has_answer, "answers": answers}, room=self.id)

    def answer(self, data):
        if self.is_in_game():
            if self.player.last_door_event is not None:
                self.player.last_door_event.answer(self.player, data)

    def answer_result(self, time):
        self.socketio.emit('answer_result', time, room=self.id)

    def in_boos_room(self):
        self.socketio.emit('in_boos_room', room=self.id)

    def click(self, id, type):
        if self.is_in_game():
            if type == "character":
                character = self.player.room.get_character(id)
                if character:
                    character.on_click(self.player)
            elif type == "room_object":
                room_object = self.player.room.room_content.get_room_object(id)
                if room_object:
                    room_object.on_click(self.player)
