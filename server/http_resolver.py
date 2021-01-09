from collections import defaultdict
import http.server
import mimetypes
import pprint
import requests
import socketserver
from urllib.parse import parse_qs
from urllib.parse import urlparse
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from functools import partial

WIKI_FR_URL = 'https://fr.wikipedia.org'

class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, game_manager, *args, **kwargs):
        self._links = self._nested_dict(3, str)
        self._resources = {}
        self._game_manager = game_manager
        resources = ['/styles/load_002.css', '/styles/load.css']
        for resource in resources:
            f = open('server' + resource, 'rb')
            self._resources[resource] = f.read()

        http.server.BaseHTTPRequestHandler.__init__(self, *args)

    def _setup_header(self, code, mimetype):
        self.send_response(code)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        mimetype, _ = mimetypes.guess_type(url.path)
                
        
        # Page requested
        if url.path.startswith('/wiki'):
            # Get user's cookies
            cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
            print(cookies)

            # Get cookies informations
            gid = cookies['gid'].value
            uid = cookies['uid'].value
            print('GID: {}, UID: {}'.format(gid, uid))
            
            link_code = url.path.split('/', 2)[2]
            page_name = self._links[gid][uid][link_code]
            print('Links: {}'.format(self._links[gid][uid]))
            print('Page name: {}'.format(page_name))


            r = requests.get('{}/w/api.php?action=parse&format=json&page={}&prop=pageimages|text|headhtml|images|links'.format(WIKI_FR_URL, page_name))

            self._setup_header(r.status_code, 'text/html; charset=utf-8')
            
            if r.status_code == 200:
                # Get HTML body
                body = r.json()['parse']['text']['*']

                # Unquote HTML body (remove %xxx characters)
                body = unquote_plus(body, encoding='utf-8')

                # Remove all current uid links reference
                self._links[gid][uid].clear()

                # Replace HTML body href
                cpt = 0
                for link in r.json()['parse']['links']:
                    title = link['*'].replace(' ', '_')
                    body = body.replace('href="/wiki/{}"'.format(title), 'href="/wiki/{}"'.format(str(cpt)))
                    self._links[gid][uid][str(cpt)] = title
                    cpt += 1

                content = '''
                <head>
                    <link rel="stylesheet" type="text/css" href="/styles/load.css"/>
                    <link rel="stylesheet" type="text/css" href="/styles/load_002.css"/>
                </head>
                <body style="margin: 5%;">
                    {}
                </body>
                '''.format(body).encode('utf-8')
                
                self.wfile.write(content)

        # Local server resource requested
        elif url.path in self._resources.keys():
            self._setup_header(200, mimetype)
            self.wfile.write(self._resources[url.path])

        # Authentification requested
        elif url.path == '/authentification':
            params = parse_qs(url.query)
            gid = params['gid'][0]
            uid = params['uid'][0]

            # Create cookie
            cookie = http.cookies.SimpleCookie()
            cookie['gid'] = gid
            cookie['uid'] = uid

            # Get start page
            start_page = self._game_manager.get_start_page_from_game(gid)

            # Initialize the default link to start page
            self._links[gid][uid]['0'] = 'France'

            # Send response
            self.send_response(301)
            self.send_header('Location', '/wiki/0') # Redirect to first page
            for v in cookie.values():
                self.send_header('Set-Cookie', v.OutputString())
            self.end_headers()

        # Other resources requested (probably wikipedia)
        else:
            r = requests.get('{}/{}'.format(WIKI_FR_URL, url.path))
            self._setup_header(r.status_code, mimetype)
            if r.status_code == 200:
                self.wfile.write(bytes(r.content))

    def _nested_dict(self, n, type):
        if n == 1:
            return defaultdict(type)
        else:
            return defaultdict(lambda: self._nested_dict(n-1, type))

         


class HttpResolver():
    def __init__(self, game_manager):
        self._game_manager = game_manager

    def run(self):
        handler = partial(Handler, self._game_manager)
        with socketserver.TCPServer(('', 5000), handler) as httpd:
            httpd.gm = self._game_manager
            httpd.serve_forever()
