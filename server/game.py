from player_status import PlayerStatus, PlayerStatusCode

class Player:
    def __init__(self, username):
        self.username = username
        self.move_count = 0
        self.page = None

class Game:
    def __init__(self, player_count):
        self.players = {}
        self.player_count = player_count
        self.start_page = None
        self.target_page = None
        self.winner = None

    def start(self, start_page, target_page):
        self.start_page = start_page
        self.target_page = target_page
        for player in self.players.values():
            player.move_count = 0
            player.page = self.start_page

    def move_player_and_get_status(self, uid, page):
        # Create status
        status = PlayerStatus()

        # Update player page
        try:
            # Only if the game still running
            if not self._winner:
                self.players[uid].page = page
                self.players[uid].move_count += 1

                # Set winner if the page is reached
                if page == self.target_page:
                    self.winner = uid

        except KeyError:
            status.code    = PlayerStatusCode.UNAUTHORIZED
            status.message = "Invalid UID : " + uid
            return status

        # Setup player status
        status.username    = self.players[uid].username
        status.move_count  = self.players[uid].move_count
        status.start_page  = self.start_page
        status.target_page = self.target_page
        status.page        = self.players[uid].page

        # Check if the game is finished
        if self._winner:
            # Detect if this player won or lost the game
            status.code = PlayerStatusCode.GAME_WON if self.winner == uid else PlayerStatusCode.GAME_LOST 
            
            # Set winner information
            status.winner_username   = self.players[self.winner].username
            status.winner_move_count = self.players[self.winner].move_count

        # Game still running
        else:
            status.code = PlayerStatusCode.GAME_RUNNING

        # Return status
        return status
            
