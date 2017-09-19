from unittest import TestCase
from app.Core import Config
from app.Services.HubSpotService import HubSpotService
from app.Entities.Domain import Domain


class ServiceHubSpotTest(TestCase):

    def test_insert_company(self):
        domain = Domain()
        domain.domain = 'kanui.com.br'
        domain.metadata = {
            'name': 'Kanui comercio de calçados, roupas e acessórios',
            'cnpj': '04.055/0001-32',
            
            'street': 'Rua Santa Justina, 352',
            'district': 'Itaim Bibi',
            'zipcode': '04545-041',
            'city': 'São Paulo',
            'state': 'SP'
        }
        self.assertTrue(HubSpotService(Config.get('hubspot.hapikey')).insert_company(domain))

    def test_error_inserting_company(self):
        domain = Domain()
        domain.domain = 'kanui.com.br'
        domain.metadata = {
            'non-defined-field': False
        }
        self.assertFalse(HubSpotService(Config.get('hubspot.hapikey')).insert_company(domain))