from player_status import PlayerStatus, PlayerStatusCode
from wikipedia_api import generate_two_pages

# Game container (association between the game identifier (gid) and the game)
class GameManager():
    def __init__(self, debug=False):
        self._games = {}
        self._debug = debug

    def add_game(self, gid, game):
        # Register the game
        self._games[gid] = game
        # Generate two random pages
        start_page, target_page = generate_two_pages(self._debug)
        # Start the game
        self._games[gid].start(start_page, target_page)

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