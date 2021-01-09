import socket
import json
import webbrowser

SERVER_ADDR            = '127.0.0.1'
SERVER_CONNECTION_PORT = 12345
SERVER_HTTP_PORT       = 5000

if __name__ == "__main__":
    # Create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_ADDR, SERVER_CONNECTION_PORT))

    # Get user information
    username = input('Enter your username: ')
    player_count = int(input('Player count: '))
    
    # Ask for a party
    information = {}
    information['username']     = username
    information['player_count'] = player_count
    s.send(json.dumps(information).encode())

    # Wait for identifiers
    print('Waiting for players...')
    identifiers = json.loads(s.recv(512).decode())
    uid = str(identifiers['uid'])
    gid = str(identifiers['gid'])

    # Open authentication page
    print('Launching game...')
    webbrowser.open('http://' + SERVER_ADDR + ':' + str(SERVER_HTTP_PORT) + '/authentification?gid=' + gid + '&uid=' + uid, new=2)

    # Terminate connection communication
    s.close()
