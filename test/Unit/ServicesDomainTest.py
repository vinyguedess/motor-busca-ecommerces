from unittest import TestCase
from app.Core import Config, Connection
from app.Services.DomainService import DomainService
from app.Entities.Domain import Domain


class ServicesDomainTest(TestCase):

    _conn = None
    def setUp(self):
        self._conn = Connection(Config.get('db.host'), Config.get('db.name'), Config.get('db.user'), Config.get('db.pass'))

    def test_if_db_authentication_data_is_loaded(self):
        self.assertEqual(Config.get('db.port'), '5432')
        self.assertEqual(Config.get('DB_PORT'), '5432')

    def test_insert_and_update_domain(self):
        domain = Domain()
        domain.domain = 'kanui.com.br'
        domain.metadata = {
            'street': 'Rua Fidencio',
            'district': 'Vila Olimpia'
        }

        self.assertTrue(DomainService(self._conn).insert_domain(domain))

        domain.metadata['seo'] = { 'description': 'Hey boys, 50% discount' }
        self.assertTrue(DomainService(self._conn).update_domain(domain))
                
    def test_check_domain_already_exists(self):
        self.assertTrue(DomainService(self._conn).check_if_domain_exists('kanui.com.br'))