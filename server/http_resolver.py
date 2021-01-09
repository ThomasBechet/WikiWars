import http.server
import mimetypes
import pprint
import requests
import socketserver
from urllib.parse import parse_qs
from urllib.parse import urlparse

WIKI_FR_URL = 'https://fr.wikipedia.org'

class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args):
        self._resources = {}
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
            page = url.path.split('/', 2)[2]
            r = requests.get('{}/w/api.php?action=parse&format=json&page={}&prop=pageimages|text|headhtml|images'.format(WIKI_FR_URL, page))

            self._setup_header(r.status_code, 'text/html; charset=utf-8')
            
            if r.status_code == 200:
                body = r.json()['parse']['text']['*']

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

            cookie = http.cookies.SimpleCookie()
            cookie['gid'] = gid
            cookie['uid'] = uid

            print(gid, uid)
            # 

            self.send_response(301)
            self.send_header('Location', '/wiki/France')
            for v in cookie.values():
                self.send_header('Set-Cookie', v.OutputString())
            self.end_headers()

        # Other resources requested (probably wikipedia)
        else:
            r = requests.get('{}/{}'.format(WIKI_FR_URL, url.path))
            self._setup_header(r.status_code, mimetype)
            if r.status_code == 200:
                self.wfile.write(bytes(r.content))

class HttpResolver():
    def __init__(self, game_manager):
        self._game_manager = game_manager

    def run(self):
        with socketserver.TCPServer(('', 5000), Handler) as httpd:
            httpd._gm = self._game_manager
            httpd.serve_forever()
