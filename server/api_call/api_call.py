import pprint
import wikipediaapi
import requests

WIKI_FR_URL = 'https://fr.wikipedia.org'



#Set language and extraction format
wiki = wikipediaapi.Wikipedia(
        language='fr',
        extract_format=wikipediaapi.ExtractFormat.HTML
)

#Search a specific HTML page
def searchHTMLPage(p_page_name):
        html_response = requests.get('{}/w/api.php?action=parse&format=json&page={}&prop=text|headhtml'.format(WIKI_FR_URL, p_page_name))
        html_response = html_response.json()
        return '{}{}'.format(html_response['parse']['headhtml']['*'],html_response['parse']['text']['*'])

def searchRawData(p_link):
        print('p_link: {}'.format(p_link))
        print('html_url: {}/{}'.format(WIKI_FR_URL, p_link))
        html_response = requests.get('{}/{}'.format(WIKI_FR_URL, p_link))
        print('Encoding: {}'.format(html_response.encoding))
        print('Type of content: {}'.format(type(html_response.content)))
        print('Content-type: {}'.format(html_response.headers['content-type']))
        return html_response.content