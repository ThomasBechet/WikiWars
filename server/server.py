from connection_resolver import ConnectionResolver
from http_resolver import HttpResolver
from game_factory import GameFactory
from game_manager import GameManager
import threading
import sys

class ConnectionResolverThread(threading.Thread):
    def __init__(self, connection_resolver):
        threading.Thread.__init__(self)
        self._connection_resolver = connection_resolver

    def run(self):
        self._connection_resolver.run()

    def terminate(self):
        self._connection_resolver.stop()

if __name__ == '__main__':
    # Detect debug command
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            debug = True

    game_factorty       = GameFactory()
    game_manager        = GameManager(debug)
    connection_resolver = ConnectionResolver(game_factorty, game_manager)
    http_resolver       = HttpResolver(game_manager)
    
    # Create the connection resolver thread
    connection_resolver_thread = ConnectionResolverThread(connection_resolver)

    # Start the http resolver on the main thread
    # Start the connection resolver on another thread
    try:
        connection_resolver_thread.start()
        http_resolver.run()
    except KeyboardInterrupt:
        connection_resolver_thread.terminate()