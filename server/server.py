from connection_resolver import ConnectionResolver
from game_factory import GameFactory

def new_game(gid, game):
    print('Starting', gid, 'with', str(len(game.players)), 'players')
    pass

gf = GameFactory()
sc = ConnectionResolver(gf, new_game)
sc.run()