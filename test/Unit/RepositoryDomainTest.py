from unittest import TestCase
from app.Core import Config, Connection
from app.Repositories.DomainRepository import DomainRepository
from app.Entities.Domain import Domain


class RepositoryDomainTest(TestCase):

    _conn = None

    def setUp(self):
        self._conn = Connection(Config.get('DB_HOST'), Config.get('DB_NAME'), Config.get('DB_USER'), Config.get('DB_PASS'))
        Config.set('db.conn', self._conn)

    def test_if_db_authentication_data_is_loaded(self):
        self.assertEqual(Config.get('db.port'), '5432')
        self.assertEqual(Config.get('DB_PORT'), '5432')

    def test_insert(self):
        domain = Domain()
        domain.domain = 'kanui.com.br'
        domain.metadata = {
            'street': 'Rua Fidencio',
            'district': 'Vila Olimpia'
        }

        self.assertTrue(DomainRepository(self._conn).insert(domain))
        Config.set('domain.id', domain.id)

    def test_error_inserting_entity(self):
        domainRepository = DomainRepository(self._conn)
        
        domain = Domain()
        domain.metadata = { 'street': 'Rua Fidencio Ramos' }

        self.assertFalse(domainRepository.insert(domain))
        self.assertTrue(domainRepository.hasErrors())
        print(domainRepository.getErrors())

    def test_error_finding_non_existent_entity(self):

        self.assertIsNone(DomainRepository(self._conn).find_by_id(-10))

    def test_update(self):
        domain = DomainRepository(self._conn).find_by_id(Config.get('domain.id'))
        self.assertIsInstance(domain, Domain)

        domain.metadata['seo'] = { 'description': 'Hey boys, 50% discount' }

        self.assertTrue(DomainRepository(self._conn).update(domain))

    def test_error_updating_non_existent_entity(self):
        self.assertFalse(DomainRepository(self._conn).update(Domain()))
                
    def test_check_domain_already_exists(self):
        self.assertTrue(DomainRepository(self._conn).check_if_domain_exists('kanui.com.br'))