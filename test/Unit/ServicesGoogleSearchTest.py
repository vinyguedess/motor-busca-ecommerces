import unittest
from app.Services.DomainSearchService import GoogleSearch


class ServicesGoogleSearchTest(unittest.TestCase):

    def test_search_for(self):
        results = GoogleSearch().set_limit(3).search_for('roupas,loja')
        
        self.assertGreaterEqual(1, len(results))
