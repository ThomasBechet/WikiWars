from flask import Flask, render_template, send_file
import uuid
from api_call.api_call import searchHTMLPage, searchRawData

app = Flask(__name__)

@app.route('/game')
def hello_world():    
    return searchHTMLPage('Francky_Vincent')

@app.route('/<path:path>')
def redirectOhterURL(path):
    return send_file(searchRawData(path))



if __name__ == "__main__":
    app.run(debug=True)
