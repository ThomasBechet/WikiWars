from collections import defaultdict
import http.server
import mimetypes
import requests
import socketserver
from urllib.parse import parse_qs
from urllib.parse import urlparse
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from functools import partial
from wikipedia_api import request_page_body_and_links

class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, game_manager, links, resources, *args, **kwargs):
        self._resources = {}
        self._game_manager = game_manager
        self._links = links
        self._resources = resources

        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def _setup_header(self, code, mimetype):
        self.send_response(code)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def _setup_page_and_links(self, wikipedia_body, wikipedia_links, gid, uid, status):
        # OK header
        self._setup_header(200, 'text/html; charset=utf-8')

        # Unquote HTML body (remove %xxx characters)
        body = unquote_plus(wikipedia_body, encoding='utf-8')

        # Remove all current uid links reference
        self._links[gid][uid].clear()

        # Replace HTML body href
        for i, link in enumerate(wikipedia_links):
            title = link['*'].replace(' ', '_')
            body = body.replace('href="/wiki/{}"'.format(title), 'href="/wiki/{}?gid={}&uid={}"'.format(str(i), gid, uid))
            self._links[gid][uid][str(i)] = title

        content = '''
        <head>
            <title>WikiWars:{}</title>
            <link rel="stylesheet" type="text/css" href="/styles/load.css"/>
            <link rel="stylesheet" type="text/css" href="/styles/load_002.css"/>
        </head>
        <body>
            <div id="container" style="display: flex; justify-content: center; margin-top: 2%; text-decoration: none">
                <table>
                    <thead>
                        <tr>
                            <th colspan="5"><h1>Page : {}</h1></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><h1>Target page : {}</h1></td>
                            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></td>
                            <td><h1>Move count : {}</h1></td>
                            <td><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></td>
                            <td><h1>Username : {}</h1></td>
                        </tr>
                    </tbody>
                </table>
            </div>            
            <div style="margin: 2%;">
            {}
            </div>
        </body>
        '''.format(status.username, status.page, status.target_page, status.move_count, status.username,body).encode('utf-8')
        
        self.wfile.write(content)

    def log_message(self, format, *args):
        return

    def do_GET(self):
        url = urlparse(self.path)
        mimetype, _ = mimetypes.guess_type(url.path)
                
        # Page requested
        if url.path.startswith('/wiki'):
            # Get gid and uid
            params = parse_qs(url.query)
            gid = params['gid'][0]
            uid = params['uid'][0]
            
            # Get link code and get real page
            link_code = url.path.split('/', 2)[2]
            page = self._links[gid][uid][link_code]

            # Recover page and links from wikipedia API
            body, links = request_page_body_and_links(page)

            # Successfuly retrieve page
            if body:

                # Move player
                status = self._game_manager.move_player_and_get_status(gid, uid, page)

                # Render page
                self._setup_page_and_links(body, links, gid, uid, status)
            
            # Failed to retrieve pas
            else:
                pass

        # Local server resource requested
        elif url.path in self._resources.keys():
            self._setup_header(200, mimetype)
            self.wfile.write(self._resources[url.path])

        # Authentification requested
        elif url.path == '/authentification':
            params = parse_qs(url.query)
            gid = params['gid'][0]
            uid = params['uid'][0]

            # Get start page
            start_page = self._game_manager.get_start_page_from_game(gid)

            # Initialize the default link to start page
            self._links[gid][uid]['0'] = start_page

            # Send response
            self.send_response(301)
            self.send_header('Location', '/wiki/{}?gid={}&uid={}'.format(0, gid, uid)) # Redirect to first page
            self.end_headers()

        # Other resources requested (probably wikipedia)
        else:
            r = requests.get('{}/{}'.format('https://fr.wikipedia.org', url.path))
            self._setup_header(r.status_code, mimetype)
            if r.status_code == 200:
                self.wfile.write(bytes(r.content))

    def _nested_dict(self, n, type):
        if n == 1:
            return defaultdict(type)
        else:
            return defaultdict(lambda: self._nested_dict(n - 1, type))

class HttpResolver():
    def __init__(self, game_manager):
        self._game_manager = game_manager
        self._links = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        self._resources = {}

        resources = ['/styles/load_002.css', '/styles/load.css']
        for resource in resources:
            f = open('server' + resource, 'rb')
            self._resources[resource] = f.read()

    def run(self):
        handler = partial(Handler, self._game_manager, self._links, self._resources)
        with socketserver.TCPServer(('', 5000), handler) as httpd:
            httpd.gm = self._game_manager
            httpd.serve_forever()
