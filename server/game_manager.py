from player_status import PlayerStatus, PlayerStatusCode

class GameManager():
    def __init__(self):
        self._games = {}

    def add_game(self, gid, game):
        self._games[gid] = game
        self._games[gid].start('France', 'Espagne')

    def get_start_page_from_game(self, gid):
        return self._games[gid].start_page

    def move_player_and_get_status(self, gid, uid, page):
        try:
            return self._games[gid].move_player_and_get_status(uid, page)
        except KeyError:
            status         = PlayerStatus()
            status.code    = PlayerStatusCode.UNAUTHORIZED
            status.message = "Invalid GID : " + gid 
            return status