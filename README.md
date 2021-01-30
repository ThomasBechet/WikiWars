# WikiWars

The Wikiwars game is based on [Wikipedia](https://www.wikipedia.org/) encyclopedia. Players move from page to page following internal website links. The game goal is to reach a target page from a starting page in a minimum of moves.

Our game implement the following feature:
- Lobby management (using TCP & routing page for authentication)
- Score count
- Retrieve Wikipedia pages (using HTTP)
- Anticheat system (indirect page id for security)
- Random page generator (using Wikipedia API)
- Custom game display (game info and Wikipedia template)

## How to use our project ?

First of all you will need to retrive our code using
```git
$ git clone https://github.com/ThomasBechet/WikiWars.git
```

Our application is divide in two distinct part. One server side and an other client side.
At the root of the project, open three Command Prompt and run these command.

### Server side
Start the server side (First terminal):
```sh
$ python server/server.py
```
or

Start the server side with predeterminate start and target page ("France" and "Espagne"):
```sh
$ python server/server.py --debug
```


### Client side
Then the first client and the second client (Second and third terminal):
```sh
$ python client/client.py
```

For clients, fill in your **name**, **number of players** in the room and **press ENTER**.
Two players must set the same number of players to be in the same room. When the room is full, the game starts.

## Well played your game is launched 
