from enum import Enum

class PlayerStatusCode(Enum):
    GAME_RUNNING = 1
    GAME_WON     = 2
    GAME_LOST    = 3
    UNAUTHORIZED = 4

class PlayerStatus():
    def __init__(self):
        self.code = None
        self.winner_username = None
        self.winner_move_count = None
        self.username = None
        self.move_count = None
        self.message = None
        self.start_page = None
        self.target_page = None
        self.page = None