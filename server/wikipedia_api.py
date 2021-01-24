import requests

WIKI_URL = 'https://fr.wikipedia.org'

def request_page_body_and_links(page):
    r = requests.get('{}/w/api.php?action=parse&format=json&page={}&prop=text|links'.format(WIKI_URL, page))
    if r.status_code == 200:
        j = r.json()
        return j['parse']['text']['*'], j['parse']['links']
    else:
        return None, None

def generate_two_pages():
    # Uncomment to have a simple test case
    #return 'France', 'Allemand'

    r = requests.get("{}/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=2&format=json".format(WIKI_URL))
    if r.status_code == 200:
        j = r.json()
        start_page  = j['query']['random'][0]['title'].replace(' ', '_')
        target_page = j['query']['random'][1]['title'].replace(' ', '_')
        return start_page, target_page
    else:
        return None, None