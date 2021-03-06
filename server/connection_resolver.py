import socket
import select
import json
import uuid
import os

SERVER_PORT = 12345
MAX_BUFFER  = 512

class ConnectionResolver:
    def __init__(self, gf, gm):
        self._gf = gf
        self._gm = gm
        self._sockets = {}
        self._continue = True # Thread termination purpose

    def _start_game(self, gid, game):
        for uid in game.players.keys():
            # Send identifiers
            identifiers = {}
            identifiers['uid'] = uid
            identifiers['gid'] = gid
            self._sockets[uid].send(json.dumps(identifiers).encode())

            # Close socket
            self._sockets[uid].close()

            # Remove from active sockets
            del self._sockets[uid]

        # Start the game
        self._gm.add_game(gid, game)

    def stop(self):
        self._continue = False

    def run(self):
        # Create server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', SERVER_PORT))
        s.listen(1)

        # Routine
        while self._continue:
            ready, _, _ = select.select([s], [], [], 1)
            if ready:
                # Get new connection
                conn, _ = s.accept()

                # Recover information
                information = json.loads(conn.recv(MAX_BUFFER).decode())

                # Send identifiers
                uid, gid, game = self._gf.add_player(information)
                self._sockets[uid] = conn

                # Check if a game is ready to start
                if gid:
                    self._start_game(gid, game)