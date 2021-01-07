import socket
import select
import json
import uuid
import os

SERVER_PORT = 12345
MAX_BUFFER  = 512

class ConnectionResolver:
    def __init__(self, gf, callback):
        self._gf = gf
        self._callback = callback
        self._sockets = {}

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
        self._callback(gid, game)

    def run(self):
        # Create server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', SERVER_PORT))
        s.listen(1)

        # Routine
        while True:
            ready, _, _ = select.select([s], [], [], 1)
            if ready:
                # Get socket
                conn, _ = s.accept()

                # Recover information
                information = json.loads(conn.recv(MAX_BUFFER).decode())

                # Send identifiers
                uid, gid, game = self._gf.add_player(information)
                self._sockets[uid] = conn

                # Check if a game is ready to start
                if gid:
                    self._start_game(gid, game)