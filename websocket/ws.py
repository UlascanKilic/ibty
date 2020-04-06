from colorama import Fore
from flask import Flask, request
from flask_socketio import SocketIO, emit
import threading
import socket

from websocket.client import Client


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = socketio = SocketIO(app, cors_allowed_origins="*")
clients = {}

host = None
port = 8888

dungeons = []


@socketio.on('connect')
def connected():
    client = Client(request.sid, app, socketio, request)
    clients[request.sid] = client


@socketio.on('disconnect')
def disconnect():
    player = clients[request.sid].player
    if player is not None:
        player.despawn()
        player.room.dungeon.left_player(player)
    clients.pop(request.sid, None)


@socketio.on('speech')
def speech(message):
    player = clients[request.sid].player
    if player is not None:
        player.speech(message)


@socketio.on('dungeons')
def send_dungeon_list():
    dungeons_data = {}
    for i, dungeon in enumerate(dungeons):
        dungeons_data[i] = {"label":dungeon.label, "subject":dungeon.subject}
    emit('dungeons', dungeons_data, room=request.sid)


@socketio.on('set_user_info')
def set_user_info(user_info):
    if "nick" in user_info and "skin" in user_info:
        clients[request.sid].nick = user_info["nick"]
        clients[request.sid].skin = user_info["skin"]

@socketio.on('get_user_info')
def get_user_info():
    pass


@socketio.on('join_dungeon')
def join_dungeon(dungeon_number):
    if 0 <= dungeon_number < len(dungeons):
        clients[request.sid].join_dungeon(dungeon_number)


@socketio.on('get_room_data')
def load_room_data():
    clients[request.sid].load_room_data()


@socketio.on('get_characters')
def get_characters():
    clients[request.sid].get_characters()


@socketio.on('click')
def click(data):
    if "id" in data and "type" in data:
        clients[request.sid].click(data["id"], data["type"])


@socketio.on('answer')
def answer(data):
    clients[request.sid].answer(data)


def websocket_thread():
    socketio.run(app, host=host, port=port)


def websocket_start(_dungeons):
    global dungeons, host, port
    dungeons = _dungeons

    if host is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host = s.getsockname()[0]
        s.close()

    thr_ws = threading.Thread(target=websocket_thread, args=(), kwargs={})
    thr_ws.start()

    print(("WebSocket server started on" + Fore.BLUE + " %s:%d" + Fore.RESET) % (host, port))

    thr_ws.join()
