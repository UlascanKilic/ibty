import threading
import logging
import socket

from colorama import Fore
from flask import Flask, send_from_directory, request

host = 'https://romantic-ptolemy-17ec44.netlify.app/'
port = 8080
app = Flask(__name__)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def hello_world():
   if 'nick' not in request.cookies:
       return send_from_directory('web_page', "login_page.html")
   return send_from_directory('web_page', "index.html")


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('web_page', path)


def http_thread():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host=host, port=port)


def http_start():
    global host, port

    thr_http = threading.Thread(target=http_thread, args=(), kwargs={})
    thr_http.start()

    print(("HTTP server started on" + Fore.BLUE + " %s:%d" + Fore.RESET) % (host, port))
