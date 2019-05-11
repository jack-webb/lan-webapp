from flask import Flask, jsonify, send_from_directory, request, redirect
from flask_socketio import SocketIO, emit
import subprocess
import sys
import json
import asyncio
from cachetools import cached, TTLCache
import threading
import time
from copy import deepcopy
import os

from game_server import GameServer

game_cache = []
messages_cache = None

app = Flask(__name__)
socketio = SocketIO(app)
messages_filename = os.path.join(os.path.dirname(__file__), "messages.json")

server_workers = []

with open('conf.json') as json_data_file:
    conf = json.load(json_data_file)


@app.route('/')
def main():
    return send_from_directory('fe', filename='index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('fe/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('fe/css', path)

@app.route('/status/post', methods=['POST'])
def post_status_message():
    try:
        passw = request.form['password']
        title = request.form['title']
        subtitle = request.form['subtitle']
        css = request.form['css']
    except:     # InvalidKeyError when an input is missing
        print("Bad request")
        return redirect("/")

    css_whitelist = ["is-info", "is-success", "is-warning", "is-danger", "is-light"]
    if css not in css_whitelist:
        print("Bad request")
        return redirect("/")

    if passw != conf["password"]:
        print("Bad password")
        return redirect("/")

    perform_add_message({
        "title": title,
        "subtitle": subtitle,
        "css": css,
    })
    return redirect("/")

@app.route('/status/clear', methods=['POST'])
def clear_status_messages():
    try:
        passw = request.form['password']
    except:     # InvalidKeyError when an input is missing
        print("Bad request")
        return redirect("/")

    if passw != conf["password"]:
        print("Bad password")
        return redirect("/")

    perform_clear_messages()
    return redirect("/")

@socketio.on('connect')
def ws_connected():
    print('Client connected')
    while(True):
        emit('server_info', get_servers_info())
        emit('messages', perform_read_messages())
        socketio.sleep(3)


@socketio.on('disconnect')
def ws_disconnected():
    print('Client disconnected')


def get_servers_info():
    server_infos = [build_payload(server) for server in conf['servers']]
    return server_infos

def build_payload(game_server):
    """
    Takes a game_server config dict, retrieves the server and game info
    Combines and returns an API payload as a dict 
    """
    info = {}
    info['server'] = server_workers[game_server['addr']].info
    info['game'] = next((game for game in conf['games'] if game['slug_name'] == game_server['game']), None)
    return info

def perform_gamedig(server):
    gamedig_id = server['gamedig_id']
    gamedig_exec = conf['gamedig_exec']
    ip = server['ip']
    dig = subprocess.check_output(
        [gamedig_exec, '--maxAttempts', str(conf['maxAttempts']), '--type', gamedig_id, ip]).decode(sys.stdout.encoding)
    return json.loads(dig)

def perform_read_messages():
    global messages_cache
    if messages_cache is None:
        try:
            with open(messages_filename) as f:
                messages_cache = json.load(f)
        except:
            messages_cache = []

    return deepcopy(messages_cache)

def perform_write_messages(messages):
    global messages_cache
    messages_cache = deepcopy(messages)
    with open(messages_filename, 'w') as f:
        json.dump(messages_cache, f)   
    socketio.emit('messages', messages_cache) 

def perform_add_message(msg):

    # add message to the existing messages
    messages = perform_read_messages()
    messages.append(msg)
    perform_write_messages(messages)
    socketio.emit('message-notify', msg) 

def perform_clear_messages():
    perform_write_messages([])

if __name__ == '__main__':
    server_workers = {server['addr']:GameServer(server) for server in conf['servers']}
    for server_addr, worker_object in server_workers.items():
        server_worker_thread = socketio.start_background_task(target=worker_object.work)
    # bg_info_thread = socketio.start_background_task(target=get_server_info)

    socketio.run(app, debug=True)