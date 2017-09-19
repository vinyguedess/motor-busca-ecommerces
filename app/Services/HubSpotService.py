import requests
from json import dumps


class HubSpotService:

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
            domain.hubspot_id = result['portalId']

            return True
        except Exception as ex:
            print(ex)
            return False

    def execute_request(self, method, url, params={}):

        url = self._hubSpotApi % (url, self._hapiKey)
        headers = {
            'content-type': 'application/json',
            'user-agent': 'motor-search-ecommerces/0.0,1'
        }

        if method == 'POST':
            return requests.post(url, headers=headers, data=dumps(params))
        if method == 'PUT':
            return requests.put(url, headers=headers, data=dumps(params))

        return request.get(url, headers=headers)

    def translate_field(self, field):
        if field == 'zipcode':
            return 'zip'

        if field == 'street':
            return 'address'

        if field == 'district':
            return 'address2'

        return field