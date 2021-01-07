class Player:
    def __init__(self, username):
        self.username = username
        self.score = 0
        self.page = None

class Game:
    def __init__(self, player_count):
        self.players = {}
        self.player_count = player_count
        self._start_page = None
        self._target_page = None
        self._winner = None

    def start(self, start_page, target_page):
        self._start_page = start_page
        self._target_page = target_page
        for player in self.players.values():
            player.score = 0
            player.page = self._start_page

    def nextPage(self, uid, page):
        # Update player page
        try:
            self.players[uid].page = page
        except KeyError:
            raise RuntimeError('Invalid UID')

        # Check if the game is finished
        if self._winner:
            return self.players[self._winner].username

        # Check victory
        if page == self.target_page:
            self._winner = uid
            
