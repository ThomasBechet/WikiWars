import uuid

from game import Game, Player

class GameFactory:
    def __init__(self):
        self._waiting_games = {}

    def add_player(self, info):
        # Create player info
        player = Player(info['username'])

        # Create new user id
        uid = str(uuid.uuid4())

        # Find waiting game
        gid, wg = next(((k, v) for (k, v) in self._waiting_games.items() if info['player_count'] == v.player_count), (None, None))
        if gid:
            # Add the player to the game
            wg.players[uid] = player

            # Check game ready
            if len(wg.players) == wg.player_count:
                del self._waiting_games[gid]
                return uid, gid, wg

        else:
            # Create new game id
            gid = str(uuid.uuid4())

            # Create new waiting games with initial player
            wg = Game(info['player_count'])
            wg.players[uid] = player

            # Save new waiting game
            self._waiting_games[gid] = wg

        return uid, None, None
        