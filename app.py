from flask import Flask, jsonify, send_from_directory
import subprocess
import sys
import json
import asyncio
from cachetools import cached, TTLCache
import threading
import time

game_cache = []

app = Flask(__name__)
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

@app.route('/status', methods=['GET'])
def get_status_messages():
    return jsonify({'status': conf['statusMessages']})

@app.route('/game', methods=['GET'])
def get_game_status():
    return jsonify({'games': game_cache})


def get_server_info():
    while (True):
        global game_cache
        game_cache = [build_info_object(game_server) for game_server in conf['game_servers']]
        print('hello', file=sys.stdout)
        time.sleep(3)

def build_info_object(game_server):
    server_info = perform_gamedig(game_server['server_instance'])
    server_info['game'] = game_server['game']
    # server_info['join_uri'] = game_server['server_instance']['join_uri']
    return server_info

def perform_gamedig(server):
    gamedig_id = server['gamedig_id']
    gamedig_exec = conf['gamedig_exec']
    ip = server['ip']
    dig = subprocess.check_output(
        [gamedig_exec, '--maxAttempts', str(conf['maxAttempts']), '--type', gamedig_id, ip]).decode(sys.stdout.encoding)
    return json.loads(dig)


if __name__ == '__main__':
    bg_info_thread = threading.Thread(target=get_server_info)
    bg_info_thread.start()

    app.run(debug=True)
