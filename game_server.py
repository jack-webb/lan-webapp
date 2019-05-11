import json
import time
import subprocess
import sys

class GameServer(object):
    """docstring for GameServer"""

    def __init__(self, server_conf):
        super(GameServer, self).__init__()
        self.gamedig_id = server_conf['gamedig_id']
        self.addr = server_conf['addr']
        self.join_uri = server_conf['join_uri']
        self.ttl = server_conf['ttl']
        self.max_retries = str(server_conf['max_retries'])
        self.game = server_conf['game']
        self.info = {}

        with open('conf.json') as json_data_file:
            conf = json.load(json_data_file)
            self.gamedig_exec = conf['gamedig_exec']

    def perform_gamedig(self):
        """
        Returns a dictionary of server information
        """
        dig = subprocess.check_output(
            [self.gamedig_exec,
             '--maxAttempts', str(self.max_retries),
             '--type', self.gamedig_id,
             self.addr]
        ).decode(sys.stdout.encoding)
        return json.loads(dig)

    def work(self):
        while (True):
            start = time.clock()
            self.info = self.perform_gamedig() # Our network task
            end = time.clock()
            sleep_time = self.ttl - (end - start)  # TTL minus processing time
            time.sleep(sleep_time)