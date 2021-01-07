import socket
import json
import webbrowser

SERVER_ADDR            = '127.0.0.1'
SERVER_CONNECTION_PORT = 12345
SERVER_HTTP_PORT       = 5000
USERNAME               = "Thomas"
PLAYER_COUNT           = 2

if __name__ == "__main__":
    # Create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_ADDR, SERVER_CONNECTION_PORT))
    
    # Ask for a party
    information = {}
    information['username']     = USERNAME
    information['player_count'] = PLAYER_COUNT
    s.send(json.dumps(information).encode())

    # Wait for identifiers
    identifiers = json.loads(s.recv(512).decode())
    uid = str(identifiers['uid'])
    gid = str(identifiers['gid'])

    # Setup token
    print(uid)
    print(gid)

    # Open first page
    webbrowser.open('http://' + SERVER_ADDR + ':' + str(SERVER_HTTP_PORT) + '/goto/', new=2)

    # Terminate communication
    s.close()
