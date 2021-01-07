from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import webbrowser
import pprint

PORT = 12345

r = requests.get('http://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Athletic_Club_de_Boulogne-Billancourt')

#print(r.json()['parse'].keys())
pprint.pprint(r.json()['parse']['links'])
html = r.json()['parse']['text']['*']

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

httpd = HTTPServer(('localhost', 12345), SimpleHTTPRequestHandler)
httpd.serve_forever()