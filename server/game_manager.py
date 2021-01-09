class GameManager():
    def __init__(self):
        self._games = {}

    def add_game(self, gid, game):
        self._games[gid] = game
        print('Starting', gid, 'with', str(len(game.players)), 'players')

    def move_player_and_get_status(self, gid, uid, page):
        pass