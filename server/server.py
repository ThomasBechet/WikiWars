from connection_resolver import ConnectionResolver
from http_resolver import HttpResolver
from game_factory import GameFactory

if __name__ == '__main__':
    def new_game(gid, game):
        print('Starting', gid, 'with', str(len(game.players)), 'players')
        pass

    http_resolver       = HttpResolver()
    game_factorty       = GameFactory()
    connection_resolver = ConnectionResolver(game_factorty, new_game)
    http_resolver       = HttpResolver()
    http_resolver.run()
    #connection_resolver.run()