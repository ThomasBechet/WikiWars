from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import webbrowser

PORT = 12345

r = requests.get('http://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Athletic_Club_de_Boulogne-Billancourt')

html = r.json()['parse']['text']['*']

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(html))

httpd = HTTPServer(('localhost', 12345), SimpleHTTPRequestHandler)
httpd.serve_forever()