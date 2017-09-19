import requests
from json import dumps
from app.Core import ErrorsManager
from app.Entities.Deal import Deal


class HubSpotService(ErrorsManager):

    _hapiKey = None
    _hubSpotApi = "https://api.hubapi.com%s?hapikey=%s"

    def __init__(self, hapiKey):
        self._hapiKey = hapiKey

    def insert_company(self, domain):
        domain_to_be_inserted = {
            "properties": [
                { 'name': 'domain', 'value': domain.domain }
            ]
        }

        for field, value in domain.metadata.items():
            domain_to_be_inserted['properties'].append({
                'name': self.translate_field(field),
                'value': value
            })

        try:
            response = self.execute_request('POST', '/companies/v2/companies', domain_to_be_inserted)
            
            result = response.json()
            if 'status' in result and result['status'] == 'error':
                raise Exception(result['message'])

            domain.hubspot_id = result['companyId']

            return True
        except Exception as ex:
            self.addError(ex.args)
            return False

    def insert_deal(self, deal):
        deal_to_be_inserted = {
            'associations': {
                'associatedCompanyIds': [ deal.company.hubspot_id ]
            },
            'properties': []
        }

        for field, value in deal.metadata.items():
            deal_to_be_inserted['properties'].append({
                'name': field, 'value': value
            })

        try:
            response = self.execute_request('POST', '/deals/v1/deal', deal_to_be_inserted)

            result = response.json()
            if 'status' in result and result['status'] == 'error':
                raise Exception(result['message'])

            deal.id = result['dealId']

            return True
        except Exception as ex:
            print(ex)
            self.addError(ex.args)
            return False

    def execute_request(self, method, url, params={}):

        url = self._hubSpotApi % (url, self._hapiKey)
        headers = {
            'content-type': 'application/json',
            'user-agent': 'motor-search-ecommerces/0.0,1'
        }

        if method == 'POST':
            return requests.post(url, headers=headers, data=dumps(params))

    def translate_field(self, field):
        if field == 'zipcode':
            return 'zip'

        if field == 'street':
            return 'address'

        if field == 'district':
            return 'address2'

        return field