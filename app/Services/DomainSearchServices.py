from bs4 import BeautifulSoup
import datetime
import os.path
import requests
from urllib.parse import urlparse
import re


class GoogleSearch():

    _search_url = "https://www.google.com.br/search?num=3&q=%s"
    _netim_url = "https://www.netim.com/ajax/domaine.php"
    _receitaws_url = "https://www.receitaws.com.br/v1/cnpj/%s"

    def search_for(self, term):

        def find_domain_owner(item):
            item['company'] = {
                'cnpj': self.ownerid_research(item['seo']['url'])
            }
            return item

        def find_company_info(item):
            info = self.information_research(item['company']['cnpj'])

            item['address'] = {
                'street': "%s, %s" % (info['logradouro'], info['numero']),
                'district': info['bairro'],
                'info': info['complemento'],
                'zipcode': info['cep'],
                'city': info['municipio'],
                'state': info['uf']
            }
            item['company']['name'] = info['nome']
            item['company']['joint_stock'] = float(info['capital_social'])
            item['company']['contacts'] = { 'email': info['email'], 'phone': info['telefone'] }

            return item

        found_items = self.google_research(term)
        found_items = filter(
            lambda item: item['company']['cnpj'] != "", map(find_domain_owner, found_items)
        )
        found_items = map(find_company_info, found_items)

        return list(found_items)

    def google_research(self, term):
        request = requests.get(self._search_url % term)
        crawler = BeautifulSoup(request.text, 'html.parser')

        found_itens = []
        for item in crawler.find_all('div', { "class": "g" }):
            cite = item.find('cite')
            if cite is None:
                continue
            
            found_itens.append({
                'seo': {
                    'title': item.find('h3').find('a').text,
                    'url': self.extract_domain_from_url(cite.text),
                    'description': item.find('span', { "class": "st" }).text
                }
            })

        return found_itens

    def ownerid_research(self, url):
        request = requests.post(self._netim_url, data={ 'whois': 1, 'DOMAINE': url })
        extraction = re.search('ownerid\:\s+[\d\.\/\-]+', request.text)
        if not extraction:
            return ""

        return re.sub(r'ownerid\:\s+', '', extraction.group(0))

    def information_research(self, cnpj):
        cnpj = cnpj.replace('/', '').replace('.', '').replace('-', '')
        request = requests.get(self._receitaws_url % cnpj)

        return request.json()

    def extract_domain_from_url(self, url):
        domain = '{uri.netloc}'.format(uri=urlparse(url))
        if domain != "":
            return domain

        return url.replace('/', '')