from unittest import TestCase
from app.Core import Config
from app.Repositories.DomainRepository import DomainRepository
from app.Services.HubSpotService import HubSpotService
from app.Entities.Domain import Domain
from app.Entities.Deal import Deal


class ServiceHubSpotTest(TestCase):

    _conn = None

    def setUp(self):
        self._conn = Config.get('db.conn')

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

        self.assertTrue(DomainRepository(self._conn).insert(domain))
        Config.set('domain2.id', domain.id)

    def test_error_inserting_company(self):
        domain = Domain()
        domain.domain = 'kanui.com.br'
        domain.metadata = {
            'non-defined-field': False
        }
        self.assertFalse(HubSpotService(Config.get('hubspot.hapikey')).insert_company(domain))

    def test_insert_deal(self):
        
        domain = DomainRepository(self._conn).find_by_id(Config.get('domain2.id'))

        dealName = ''
        if 'name' in domain.metadata:
            dealName = domain.metadata['name']

        deal = Deal()
        deal.company = domain
        deal.metadata = {
            'dealname': "Novo negócio com à %s" % dealName,
            'dealtype': 'newbusiness',
            'pipeline': 'default',
            'dealstage': 'appointmentscheduled'
        }
        self.assertTrue(HubSpotService(Config.get('hubspot.hapikey')).insert_deal(deal))

    def test_error_inserting_deal(self):
        domain = DomainRepository(self._conn).find_by_id(Config.get('domain.id'))

        deal = Deal()
        deal.company = domain
        deal.metadata = {
            'should_bring_what': 'some_error'
        }
        self.assertFalse(HubSpotService(Config.get('hubspot.hapikey')).insert_deal(deal))