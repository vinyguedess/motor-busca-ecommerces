from bs4 import BeautifulSoup
import datetime
import json
import requests


def search_in_google(parameters):

    google_url = parameters[0]

    request = requests.get("https://www.google.com.br/search?q=%s" % google_url)
    crawler = BeautifulSoup(request.text, 'html.parser')

    found_itens = []
    for item in crawler.find_all('div', { "class": "g" }):
        cite = item.find('cite')
        if cite is None:
            continue

        found_itens.append({
            'title': item.find('h3').find('a').text,
            'url': cite.text,
            'description': item.find('span', { "class": "st" }).text
        })

    file_name = "data/to_be_processed/%s.json" % datetime.datetime.now().time()
    fp = open(file_name, 'w')
    json.dump(found_itens, fp)