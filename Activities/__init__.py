from bs4 import BeautifulSoup
import datetime
import json
import os.path
import requests
from urllib.parse import urlparse


def domains_already_proccessed():
    if not os.path.isfile("data/already_proccessed.json"):
        return []

    fp = open("data/already_proccessed.json", 'r')
    data = json.load(fp)
    return data['data']


def extract_domain_from_url(url): 
    domain = '{uri.netloc}'.format(uri=urlparse(url))
    if domain != "":
        return domain

    return url.replace('/', '')


def search_in_google(parameters):

    google_url = parameters[0]

    request = requests.get("https://www.google.com.br/search?num=100&q=%s" % google_url)
    crawler = BeautifulSoup(request.text, 'html.parser')

    found_itens = []
    for item in crawler.find_all('div', { "class": "g" }):
        cite = item.find('cite')
        if cite is None:
            continue
        
        found_itens.append({
            'title': item.find('h3').find('a').text,
            'url': extract_domain_from_url(cite.text),
            'description': item.find('span', { "class": "st" }).text
        })

    file_name = "data/to_be_processed/%s.json" % datetime.datetime.now().time()
    fp = open(file_name, 'w')
    json.dump(found_itens, fp)